import datetime
import logging
from typing import Any, Callable

LOG = logging.getLogger(__name__)

##
# Settings / Packaging
##

# mimetypes starting with entries defined here are considered as TEXT when BINARTY_SUPPORT is True.
# - Additional TEXT mimetypes may be defined with the 'ADDITIONAL_TEXT_MIMETYPES' setting.
DEFAULT_TEXT_MIMETYPES = (
    "text/",
    "application/json",  # RFC 4627
    "application/javascript",  # RFC 4329
    "application/ecmascript",  # RFC 4329
    "application/xml",  # RFC 3023
    "application/xml-external-parsed-entity",  # RFC 3023
    "application/xml-dtd",  # RFC 3023
    "image/svg+xml",  # RFC 3023
)

def merge_headers(event):
    """
    Merge the values of headers and multiValueHeaders into a single dict.
    Opens up support for multivalue headers via API Gateway and ALB.
    See: https://github.com/Miserlou/Zappa/pull/1756
    """
    headers = event.get("headers") or {}
    multi_headers = (event.get("multiValueHeaders") or {}).copy()
    for h in set(headers.keys()):
        if h not in multi_headers:
            multi_headers[h] = [headers[h]]
    for h in multi_headers.keys():
        multi_headers[h] = ", ".join(multi_headers[h])
    return multi_headers

# https://github.com/Miserlou/Zappa/issues/1188
def titlecase_keys(d):
    """
    Takes a dict with keys of type str and returns a new dict with all keys titlecased.
    """
    return {k.title(): v for k, v in d.items()}

class ApacheNCSAFormatters:
    """
    NCSA extended/combined Log Format:
    "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
    %h: Remote hostname.
    %l: Remote logname
    %u: Remote user if the request was authenticated. May be bogus if return status (%s) is 401 (unauthorized).
    %t: Time the request was received, in the format [18/Sep/2011:19:18:28 -0400].
        The last number indicates the timezone offset from GMT
    %r: First line of request.
    %>s: Final Status
    %b: Size of response in bytes, excluding HTTP headers.
        In CLF format, i.e. a '-' rather than a 0 when no bytes are sent.
    %{Referer}i:The contents of Referer: header line(s) in the request sent to the server.
    %{User-agent}i: The contents of User-agent: header line(s) in the request sent to the server.

    Refer to:
    https://httpd.apache.org/docs/current/en/mod/mod_log_config.html
    """

    @staticmethod
    def format_log(status_code: int, environ: dict, content_length: int, **kwargs) -> str:
        ip_header = kwargs.get("ip_header", None)
        if ip_header:
            host = environ.get(ip_header, "")
        else:
            host = environ.get("REMOTE_ADDR", "")

        logname = "-"
        user = "-"
        now = datetime.datetime.now(datetime.timezone.utc)
        display_datetime = now.strftime("%d/%b/%Y:%H:%M:%S %z")
        method = environ.get("REQUEST_METHOD", "")
        path_info = environ.get("PATH_INFO", "")
        query_string = ""
        raw_query_string = environ.get("QUERY_STRING", "")
        if raw_query_string:
            query_string = f"?{raw_query_string}"
        server_protocol = environ.get("SERVER_PROTOCOL", "")
        request = f"{method} {path_info}{query_string} {server_protocol}"
        referer = environ.get("HTTP_REFERER", "")
        agent = environ.get("HTTP_USER_AGENT", "")
        log_entry = (
            f'{host} {logname} {user} [{display_datetime}] "{request}" {status_code} {content_length} "{referer}" "{agent}"'
        )
        return log_entry

    @staticmethod
    def format_log_with_response_time(*args, **kwargs) -> str:
        """
        Expect that kwargs includes response time in microseconds, 'rt_us'.
        Mimics Apache-like access HTTP log where the response time data is enabled

        NCSA extended/combined Log Format:
            "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\" %T/%D"

        %T: The time taken to serve the request, in seconds.
        %D: The time taken to serve the request, in microseconds.
        """
        response_time_microseconds = kwargs.get("rt_us", None)
        log_entry = ApacheNCSAFormatters.format_log(*args, **kwargs)
        if response_time_microseconds:
            response_time_seconds = int(response_time_microseconds / 1_000_000)
            log_entry = f"{log_entry} {response_time_seconds}/{response_time_microseconds}"
        return log_entry

def ApacheNCSAFormatter(with_response_time: bool = True) -> Callable:
    """A factory that returns the wanted formatter"""
    if with_response_time:
        return ApacheNCSAFormatters.format_log_with_response_time
    else:
        return ApacheNCSAFormatters.format_log
