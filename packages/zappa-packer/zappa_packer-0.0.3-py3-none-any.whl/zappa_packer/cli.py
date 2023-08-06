#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Zappa CLI

Deploy arbitrary Python programs as serverless Zappa applications.

"""
import argparse
import click
import os
import re
import sys
import subprocess
import inspect
import hjson as json
import tempfile
import zipfile
from past.builtins import basestring
import slugify
from .zappa import Zappa

from click import Context, BaseCommand
from click.exceptions import ClickException
from click.globals import push_context

class InvalidAwsLambdaName(Exception):
    """Exception: proposed AWS Lambda name is invalid"""
    pass

def human_size(num, suffix="B"):
    """
    Convert bytes length to a human-readable version
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return "{0:3.1f}{1!s}{2!s}".format(num, unit, suffix)
        num /= 1024.0
    return "{0:.1f}{1!s}{2!s}".format(num, "Yi", suffix)

class ZappaPackager:
    """
    ZappaPackager object is responsible for loading the settings,
    handling the input arguments and executing the calls to the core library.

    """

    # CLI
    vargs = None
    command = None
    stage_env = None

    # Zappa settings
    zappa = None
    zappa_settings = None
    load_credentials = True
    disable_progress = False

    # Specific settings
    api_stage = None
    app_function = None
    aws_region = None
    debug = None
    prebuild_script = None
    project_name = None
    profile_name = None
    lambda_arn = None
    lambda_name = None
    lambda_description = None
    lambda_concurrency = None
    s3_bucket_name = None
    settings_file = None
    zip_path = None
    handler_path = None
    vpc_config = None
    memory_size = None
    use_apigateway = None
    lambda_handler = None
    django_settings = None
    manage_roles = True
    exception_handler = None
    environment_variables = None
    authorizer = None
    xray_tracing = False
    aws_kms_key_arn = ''
    context_header_mappings = None
    tags = []
    layers = None

    stage_name_env_pattern = re.compile('^[a-zA-Z0-9_]+$')

    def __init__(self):
        self._stage_config_overrides = {}  # change using self.override_stage_config_setting(key, val)

    @property
    def stage_config_overrides(self):
        """
        Returns zappa_settings we forcefully override for the current stage
        set by `self.override_stage_config_setting(key, value)`
        """
        return getattr(self, "_stage_config_overrides", {}).get(self.api_stage, {})

    @property
    def stage_config(self):
        """
        A shortcut property for settings of a stage.
        """

        def get_stage_setting(stage, extended_stages=None):
            if extended_stages is None:
                extended_stages = []

            if stage in extended_stages:
                raise RuntimeError(stage + " has already been extended to these settings. "
                                           "There is a circular extends within the settings file.")
            extended_stages.append(stage)

            try:
                stage_settings = dict(self.zappa_settings[stage].copy())
            except KeyError:
                raise ClickException("Cannot extend settings for undefined stage '" + stage + "'.")

            extends_stage = self.zappa_settings[stage].get('extends', None)
            if not extends_stage:
                return stage_settings
            extended_settings = get_stage_setting(stage=extends_stage, extended_stages=extended_stages)
            extended_settings.update(stage_settings)
            return extended_settings

        settings = get_stage_setting(stage=self.api_stage)

        # Backwards compatible for delete_zip setting that was more explicitly named delete_local_zip
        if 'delete_zip' in settings:
            settings['delete_local_zip'] = settings.get('delete_zip')

        settings.update(self.stage_config_overrides)

        return settings

    def handle(self, argv=None):
        """
        Main function.

        Parses command, load settings and dispatches accordingly.

        """

        desc = ('Zappa - Deploy Python applications to AWS Lambda'
                ' and API Gateway.\n')
        parser = argparse.ArgumentParser(description=desc)
        env_parser = argparse.ArgumentParser(add_help=False)
        subparsers = parser.add_subparsers(title='subcommands', dest='command')
        self.load_settings_file()

        args = parser.parse_args(argv)
        self.vargs = vars(args)

        # Parse the input
        # NOTE(rmoe): Special case for manage command
        # The manage command can't have both stage_env and command_rest
        # arguments. Since they are both positional arguments argparse can't
        # differentiate the two. This causes problems when used with --all.
        # (e.g. "manage --all showmigrations admin" argparse thinks --all has
        # been specified AND that stage_env='showmigrations')
        # By having command_rest collect everything but --all we can split it
        # apart here instead of relying on argparse.
        self.load_credentials = False

        # Load and Validate Settings File
        self.load_settings_file(self.vargs.get("settings_file"))

        # Should we execute this for all stages, or just one?
        all_stages = self.vargs.get("all")
        stages = []

        if all_stages:  # All stages!
            stages = self.zappa_settings.keys()
        else:  # Just one env.
            if not self.stage_env:
                # If there's only one stage defined in the settings,
                # use that as the default.
                if len(self.zappa_settings.keys()) == 1:
                    stages.append(list(self.zappa_settings.keys())[0])
                else:
                    parser.error("Please supply a stage to interact with.")
            else:
                stages.append(self.stage_env)

        for stage in stages:
            try:
                self.dispatch_command(self.command, stage)
            except ClickException as e:
                # Discussion on exit codes: https://github.com/Miserlou/Zappa/issues/407
                e.show()
                sys.exit(e.exit_code)

    def dispatch_command(self, command, stage):
        """
        Given a command to execute and stage,
        execute that command.
        """
        self.check_stage_name(stage)
        self.api_stage = stage

        # Explicitly define the app function.
        # Related: https://github.com/Miserlou/Zappa/issues/832
        if self.vargs.get("app_function", None):
            self.app_function = self.vargs["app_function"]

        # Load our settings, based on api_stage.
        try:
            self.load_settings(self.vargs.get("settings_file"))
        except ValueError as e:
            if hasattr(e, "message"):
                print("Error: {}".format(e.message))
            else:
                print(str(e))
            sys.exit(-1)

        self.create_package("deployment.zip")

    def validate_name(self, name, maxlen=80):
        """Validate name for AWS Lambda function.
        name: actual name (without `arn:aws:lambda:...:` prefix and without
            `:$LATEST`, alias or version suffix.
        maxlen: max allowed length for name without prefix and suffix.
        The value 80 was calculated from prefix with longest known region name
        and assuming that no alias or version would be longer than `$LATEST`.
        Based on AWS Lambda spec
        http://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html
        Return: the name
        Raise: InvalidAwsLambdaName, if the name is invalid.
        """
        if not isinstance(name, basestring):
            msg = "Name must be of type string"
            raise InvalidAwsLambdaName(msg)
        if len(name) > maxlen:
            msg = "Name is longer than {maxlen} characters."
            raise InvalidAwsLambdaName(msg.format(maxlen=maxlen))
        if len(name) == 0:
            msg = "Name must not be empty string."
            raise InvalidAwsLambdaName(msg)
        if not re.match("^[a-zA-Z0-9-_]+$", name):
            msg = "Name can only contain characters from a-z, A-Z, 0-9, _ and -"
            raise InvalidAwsLambdaName(msg)
        return name

    def get_runtime_from_python_version(self):
        """ """
        if sys.version_info[0] < 3:
            raise ValueError("Python 2.x is no longer supported.")
        else:
            if sys.version_info[1] <= 7:
                return "python3.7"
            elif sys.version_info[1] <= 8:
                return "python3.8"
            elif sys.version_info[1] <= 9:
                return "python3.9"
            else:
                return "python3.10"

    def get_current_venv():
        """
        Returns the path to the current virtualenv
        """
        if "VIRTUAL_ENV" in os.environ:
            venv = os.environ["VIRTUAL_ENV"]
            return venv

        # pyenv available check
        try:  # progma: no cover
            subprocess.check_output(["pyenv", "help"], stderr=subprocess.STDOUT)
            pyenv_available = True
        except OSError:
            pyenv_available = False

        if pyenv_available:  # progma: no cover
            # Each Python version is installed into its own directory under $(pyenv root)/versions
            # https://github.com/pyenv/pyenv#locating-pyenv-provided-python-installations
            # Related: https://github.com/zappa/Zappa/issues/1132
            pyenv_root = subprocess.check_output(["pyenv", "root"]).decode("utf-8").strip()
            pyenv_version = subprocess.check_output(["pyenv", "version-name"]).decode("utf-8").strip()
            venv = os.path.join(pyenv_root, "versions", pyenv_version)
            return venv

        return None

    def create_package(self, output=None):
        """
        Ensure that the package can be properly configured,
        and then create it.

        """

        # Create the Lambda zip package (includes project and virtualenvironment)
        # Also define the path the handler file so it can be copied to the zip
        # root for Lambda.
        current_file = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        handler_file = os.sep.join(current_file.split(os.sep)[0:]) + os.sep + 'handler.py'

        # Create the zip file(s)
        # This could be python3.6 optimized.
        exclude = self.stage_config.get(
                'exclude', [
                                "boto3",
                                "dateutil",
                                "botocore",
                                "s3transfer",
                                "concurrent"
                            ])

        # Create a single zip that has the handler and application
        self.zip_path = self.zappa.create_lambda_zip(
            prefix=self.lambda_name,
            handler_file=handler_file,
            use_precompiled_packages=self.stage_config.get('use_precompiled_packages', True),
            exclude=exclude,
            exclude_glob=self.stage_config.get('exclude_glob', []),
            output=output,
            disable_progress=self.disable_progress
        )

        # Warn if this is too large for Lambda.
        file_stats = os.stat(self.zip_path)
        if file_stats.st_size > 52428800:  # pragma: no cover
                print('\n\nWarning: Application zip package is likely to be too large for AWS Lambda. '
                      'Try setting "slim_handler" to true in your Zappa settings file.\n\n')

        # Throw custom settings into the zip that handles requests
        if self.stage_config.get('slim_handler', False):
            handler_zip = self.handler_path
        else:
            handler_zip = self.zip_path

        with zipfile.ZipFile(handler_zip, 'a') as lambda_zip:

            settings_s = "# Generated by Zappa\n"

            if self.app_function:
                if '.' not in self.app_function: # pragma: no cover
                    raise ClickException("Your " + click.style("app_function", fg='red', bold=True) + " value is not a modular path." +
                        " It needs to be in the format `" + click.style("your_module.your_app_object", bold=True) + "`.")
                app_module, app_function = self.app_function.rsplit('.', 1)
                settings_s = settings_s + "APP_MODULE='{0!s}'\nAPP_FUNCTION='{1!s}'\n".format(app_module, app_function)

            if self.exception_handler:
                settings_s += "EXCEPTION_HANDLER='{0!s}'\n".format(self.exception_handler)
            else:
                settings_s += "EXCEPTION_HANDLER=None\n"

            if self.debug:
                settings_s = settings_s + "DEBUG=True\n"
            else:
                settings_s = settings_s + "DEBUG=False\n"

            settings_s = settings_s + "LOG_LEVEL='{0!s}'\n".format((self.log_level))

            if self.binary_support:
                settings_s = settings_s + "BINARY_SUPPORT=True\n"
            else:
                settings_s = settings_s + "BINARY_SUPPORT=False\n"

            head_map_dict = {}
            head_map_dict.update(dict(self.context_header_mappings))
            settings_s = settings_s + "CONTEXT_HEADER_MAPPINGS={0}\n".format(
                head_map_dict
            )

            # If we're on a domain, we don't need to define the /<<env>> in
            # the WSGI PATH
            if self.domain:
                settings_s = settings_s + "DOMAIN='{0!s}'\n".format((self.domain))
            else:
                settings_s = settings_s + "DOMAIN=None\n"

            if self.base_path:
                settings_s = settings_s + "BASE_PATH='{0!s}'\n".format((self.base_path))
            else:
                settings_s = settings_s + "BASE_PATH=None\n"

            # Pass through remote config bucket and path
            if self.remote_env:
                settings_s = settings_s + "REMOTE_ENV='{0!s}'\n".format(
                    self.remote_env
                )
            # DEPRECATED. use remove_env instead
            elif self.remote_env_bucket and self.remote_env_file:
                settings_s = settings_s + "REMOTE_ENV='s3://{0!s}/{1!s}'\n".format(
                    self.remote_env_bucket, self.remote_env_file
                )

            # Local envs
            env_dict = {}
            if self.aws_region:
                env_dict['AWS_REGION'] = self.aws_region
            env_dict.update(dict(self.environment_variables))

            # Environment variable keys must be ascii
            # https://github.com/Miserlou/Zappa/issues/604
            # https://github.com/Miserlou/Zappa/issues/998
            try:
                env_dict = dict((k.encode('ascii').decode('ascii'), v) for (k, v) in env_dict.items())
            except Exception:
                raise ValueError("Environment variable keys must be ascii.")

            settings_s = settings_s + "ENVIRONMENT_VARIABLES={0}\n".format(
                    env_dict
                )

            # We can be environment-aware
            settings_s = settings_s + "API_STAGE='{0!s}'\n".format((self.api_stage))
            settings_s = settings_s + "PROJECT_NAME='{0!s}'\n".format((self.project_name))

            if self.settings_file:
                settings_s = settings_s + "SETTINGS_FILE='{0!s}'\n".format((self.settings_file))
            else:
                settings_s = settings_s + "SETTINGS_FILE=None\n"

            if self.django_settings:
                settings_s = settings_s + "DJANGO_SETTINGS='{0!s}'\n".format((self.django_settings))
            else:
                settings_s = settings_s + "DJANGO_SETTINGS=None\n"

            # If slim handler, path to project zip
            if self.stage_config.get('slim_handler', False):
                settings_s += "ARCHIVE_PATH='s3://{0!s}/{1!s}_{2!s}_current_project.tar.gz'\n".format(
                    self.s3_bucket_name, self.api_stage, self.project_name)

                # since includes are for slim handler add the setting here by joining arbitrary list from zappa_settings file
                # and tell the handler we are the slim_handler
                # https://github.com/Miserlou/Zappa/issues/776
                settings_s += "SLIM_HANDLER=True\n"

                include = self.stage_config.get('include', [])
                if len(include) >= 1:
                    settings_s += "INCLUDE=" + str(include) + '\n'

            # AWS Events function mapping
            event_mapping = {}
            events = self.stage_config.get('events', [])
            for event in events:
                arn = event.get('event_source', {}).get('arn')
                function = event.get('function')
                if arn and function:
                    event_mapping[arn] = function
            settings_s = settings_s + "AWS_EVENT_MAPPING={0!s}\n".format(event_mapping)

            # Map Lext bot events
            bot_events = self.stage_config.get('bot_events', [])
            bot_events_mapping = {}
            for bot_event in bot_events:
                event_source = bot_event.get('event_source', {})
                intent = event_source.get('intent')
                invocation_source = event_source.get('invocation_source')
                function = bot_event.get('function')
                if intent and invocation_source and function:
                    bot_events_mapping[str(intent) + ':' + str(invocation_source)] = function

            settings_s = settings_s + "AWS_BOT_EVENT_MAPPING={0!s}\n".format(bot_events_mapping)

            # Map cognito triggers
            cognito_trigger_mapping = {}
            cognito_config = self.stage_config.get('cognito', {})
            triggers = cognito_config.get('triggers', [])
            for trigger in triggers:
                source = trigger.get('source')
                function = trigger.get('function')
                if source and function:
                    cognito_trigger_mapping[source] = function
            settings_s = settings_s + "COGNITO_TRIGGER_MAPPING={0!s}\n".format(cognito_trigger_mapping)

            # Authorizer config
            authorizer_function = self.authorizer.get('function', None)
            if authorizer_function:
                settings_s += "AUTHORIZER_FUNCTION='{0!s}'\n".format(authorizer_function)

            # Copy our Django app into root of our package.
            # It doesn't work otherwise.
            if self.django_settings:
                base = __file__.rsplit(os.sep, 1)[0]
                django_py = ''.join(os.path.join(base, 'ext', 'django_zappa.py'))
                lambda_zip.write(django_py, 'django_zappa_app.py')

            # async response
            async_response_table = self.stage_config.get('async_response_table', '')
            settings_s += "ASYNC_RESPONSE_TABLE='{0!s}'\n".format(async_response_table)

            # Lambda requires a specific chmod
            temp_settings = tempfile.NamedTemporaryFile(delete=False)
            os.chmod(temp_settings.name, 0o644)
            temp_settings.write(bytes(settings_s, "utf-8"))
            temp_settings.close()
            lambda_zip.write(temp_settings.name, 'zappa_settings.py')
            os.unlink(temp_settings.name)

    def get_json_settings(self, settings_name="zappa_settings"):
        """
        Return zappa_settings path as JSON
        """
        zs_json = settings_name + ".json"

        # Must have at least one
        if not os.path.isfile(zs_json):
            raise ClickException("Please configure a zappa_settings file or call `zappa init`.")

        # Prefer JSON
        if os.path.isfile(zs_json):
            settings_file = zs_json
        else:
            raise ClickException("Please configure a zappa_settings file or call `zappa init`. JSON file could not be found.")

        return settings_file

    def load_settings_file(self, settings_file=None):
        """
        Load our settings file.
        """

        if not settings_file:
            settings_file = self.get_json_settings()
        if not os.path.isfile(settings_file):
            raise ClickException("Please configure your zappa_settings file or call `zappa init`.")

        path, ext = os.path.splitext(settings_file)
        if ext == '.json':
            with open(settings_file) as json_file:
                try:
                    self.zappa_settings = json.load(json_file)
                except ValueError: # pragma: no cover
                    raise ValueError("Unable to load the Zappa settings JSON. It may be malformed.")
        else:
            raise ValueError("File needs to be in JSON format. It may be malformed.")

    def check_stage_name(self, stage_name):
        """
        Make sure the stage name matches the AWS-allowed pattern
        (calls to apigateway_client.create_deployment, will fail with error
        message "ClientError: An error occurred (BadRequestException) when
        calling the CreateDeployment operation: Stage name only allows
        a-zA-Z0-9_" if the pattern does not match)
        """
        if self.stage_name_env_pattern.match(stage_name):
            return True
        raise ValueError("AWS requires stage name to match a-zA-Z0-9_")

    def get_project_name(self):
        return slugify.slugify(os.getcwd().split(os.sep)[-1])[:15]

    def check_environment(self, environment):
        """
        Make sure the environment contains only strings
        (since putenv needs a string)
        """

        non_strings = []
        for k, v in environment.items():
            if not isinstance(v, str):
                non_strings.append(k)
        if non_strings:
            raise ValueError("The following environment variables are not strings: {}".format(", ".join(non_strings)))
        else:
            return True

    def collision_warning(self, item):
        """
        Given a string, print a warning if this could
        collide with a Zappa core package module.
        Use for app functions and events.
        """

        namespace_collisions = [
            "zappa.",
            "wsgi.",
            "middleware.",
            "handler.",
            "util.",
            "letsencrypt.",
            "cli.",
        ]
        for namespace_collision in namespace_collisions:
            if item.startswith(namespace_collision):
                click.echo(
                    click.style("Warning!", fg="red", bold=True)
                    + " You may have a namespace collision between "
                    + click.style(item, bold=True)
                    + " and "
                    + click.style(namespace_collision, bold=True)
                    + "! You may want to rename that file."
                )

    def load_settings(self, settings_file=None, session=None):
        """
        Load the local zappa_settings file.
        Returns the loaded Zappa object.
        """

        # Ensure we're passed a valid settings file.
        if not settings_file:
            settings_file = self.get_json_settings()
        if not os.path.isfile(settings_file):
            raise ClickException("Please configure your zappa_settings file.")

        # Load up file
        self.load_settings_file(settings_file)

        # Make sure that the stages are valid names:
        for stage_name in self.zappa_settings.keys():
            try:
                self.check_stage_name(stage_name)
            except ValueError:
                raise ValueError("API stage names must match a-zA-Z0-9_ ; '{0!s}' does not.".format(stage_name))

        # Make sure that this stage is our settings
        if self.api_stage not in self.zappa_settings.keys():
            raise ClickException("Please define stage '{0!s}' in your Zappa settings.".format(self.api_stage))

        # We need a working title for this project. Use one if supplied, else cwd dirname.
        if 'project_name' in self.stage_config: # pragma: no cover
            # If the name is invalid, this will throw an exception with message up stack
            self.project_name = self.validate_name(self.stage_config['project_name'])
        else:
            self.project_name = self.get_project_name()

        # The name of the actual AWS Lambda function, ex, 'helloworld-dev'
        # Assume that we already have have validated the name beforehand.
        # Related:  https://github.com/Miserlou/Zappa/pull/664
        #           https://github.com/Miserlou/Zappa/issues/678
        #           And various others from Slack.
        self.lambda_name = slugify.slugify(self.project_name + '-' + self.api_stage)

        # Load stage-specific settings
        self.vpc_config = self.stage_config.get('vpc_config', {})
        self.memory_size = self.stage_config.get('memory_size', 512)
        self.app_function = self.stage_config.get('app_function', None)
        self.exception_handler = self.stage_config.get('exception_handler', None)
        self.aws_region = self.stage_config.get('aws_region', None)
        self.debug = self.stage_config.get('debug', True)
        self.prebuild_script = self.stage_config.get('prebuild_script', None)
        self.profile_name = self.stage_config.get('profile_name', None)
        self.log_level = self.stage_config.get('log_level', "DEBUG")
        self.domain = self.stage_config.get('domain', None)
        self.base_path = self.stage_config.get('base_path', None)
        self.timeout_seconds = self.stage_config.get('timeout_seconds', 30)
        dead_letter_arn = self.stage_config.get('dead_letter_arn', '')
        self.dead_letter_config = {'TargetArn': dead_letter_arn} if dead_letter_arn else {}
        self.cognito = self.stage_config.get('cognito', None)
        self.num_retained_versions = self.stage_config.get('num_retained_versions',None)

        # Check for valid values of num_retained_versions
        if self.num_retained_versions is not None and type(self.num_retained_versions) is not int:
            raise ClickException("Please supply either an integer or null for num_retained_versions in the zappa_settings.json. Found %s" % type(self.num_retained_versions))
        elif type(self.num_retained_versions) is int and self.num_retained_versions<1:
            raise ClickException("The value for num_retained_versions in the zappa_settings.json should be greater than 0.")

        # Provide legacy support for `use_apigateway`, now `apigateway_enabled`.
        # https://github.com/Miserlou/Zappa/issues/490
        # https://github.com/Miserlou/Zappa/issues/493
        self.use_apigateway = self.stage_config.get('use_apigateway', True)
        if self.use_apigateway:
            self.use_apigateway = self.stage_config.get('apigateway_enabled', True)
        self.apigateway_description = self.stage_config.get('apigateway_description', None)

        self.lambda_handler = self.stage_config.get('lambda_handler', 'handler.lambda_handler')
        # DEPRECATED. https://github.com/Miserlou/Zappa/issues/456
        self.remote_env_bucket = self.stage_config.get('remote_env_bucket', None)
        self.remote_env_file = self.stage_config.get('remote_env_file', None)
        self.remote_env = self.stage_config.get('remote_env', None)
        self.settings_file = self.stage_config.get('settings_file', None)
        self.django_settings = self.stage_config.get('django_settings', None)
        self.manage_roles = self.stage_config.get('manage_roles', True)
        self.binary_support = self.stage_config.get('binary_support', True)
        self.api_key_required = self.stage_config.get('api_key_required', False)
        self.api_key = self.stage_config.get('api_key')
        self.endpoint_configuration = self.stage_config.get('endpoint_configuration', None)
        self.iam_authorization = self.stage_config.get('iam_authorization', False)
        self.cors = self.stage_config.get("cors", False)
        self.lambda_description = self.stage_config.get('lambda_description', "Zappa Deployment")
        self.lambda_concurrency = self.stage_config.get('lambda_concurrency', None)
        self.environment_variables = self.stage_config.get('environment_variables', {})
        self.aws_environment_variables = self.stage_config.get('aws_environment_variables', {})
        self.check_environment(self.environment_variables)
        self.authorizer = self.stage_config.get('authorizer', {})
        self.runtime = self.stage_config.get('runtime', self.get_runtime_from_python_version())
        self.aws_kms_key_arn = self.stage_config.get('aws_kms_key_arn', '')
        self.context_header_mappings = self.stage_config.get('context_header_mappings', {})
        self.xray_tracing = self.stage_config.get('xray_tracing', False)
        self.desired_role_arn = self.stage_config.get('role_arn')
        self.layers = self.stage_config.get('layers', None)

        # Load ALB-related settings
        self.use_alb = self.stage_config.get('alb_enabled', False)
        self.alb_vpc_config = self.stage_config.get('alb_vpc_config', {})

        # Additional tags
        self.tags = self.stage_config.get('tags', {})

        self.zappa = Zappa(runtime=self.runtime)

        if self.app_function:
            self.collision_warning(self.app_function)
            if self.app_function[-3:] == '.py':
                click.echo(click.style("Warning!", fg="red", bold=True) +
                           " Your app_function is pointing to a " + click.style("file and not a function", bold=True) +
                           "! It should probably be something like 'my_file.app', not 'my_file.py'!")

        return self.zappa

    def package(self, output=None):
        """
        Only build the package
        """
        # Make sure we're in a venv.
        self.get_current_venv()

        # Create the Lambda Zip
        self.create_package(output)
        self.callback('zip')
        size = human_size(os.path.getsize(self.zip_path))
        click.echo(click.style("Package created", fg="green", bold=True) + ": " + click.style(self.zip_path, bold=True) + " (" + size + ")")

####################################################################
# Main
####################################################################

def shamelessly_promote():
    """
    Shamelessly promote our little community.
    """

    click.echo("Need " + click.style("help", fg='green', bold=True) +
               "? Found a " + click.style("bug", fg='green', bold=True) +
               "? Let us " + click.style("know", fg='green', bold=True) + "! :D")
    click.echo("File bug reports on " + click.style("GitHub", bold=True) + " here: "
               + click.style("https://github.com/Miserlou/Zappa", fg='cyan', bold=True))
    click.echo("And join our " + click.style("Slack", bold=True) + " channel here: "
               + click.style("https://zappateam.slack.com", fg='cyan', bold=True))
    click.echo("Love!,")
    click.echo(" ~ Team " + click.style("Zappa", bold=True) + "!")

def disable_click_colors():
    """
    Set a Click context where colors are disabled. Creates a throwaway BaseCommand
    to play nicely with the Context constructor.
    The intended side-effect here is that click.echo() checks this context and will
    suppress colors.
    https://github.com/pallets/click/blob/e1aa43a3/click/globals.py#L39
    """

    ctx = Context(BaseCommand('AllYourBaseAreBelongToUs'))
    ctx.color = False
    push_context(ctx)

def handle(): # pragma: no cover
    """
    Main program execution handler.
    """

    try:
        cli = ZappaPackager()
        sys.exit(cli.handle())
    except SystemExit as e: # pragma: no cover

        sys.exit(e.code)

    except KeyboardInterrupt: # pragma: no cover

        sys.exit(130)
    except Exception as e:


        click.echo("Oh no! An " + click.style("error occurred", fg='red', bold=True) + "! :(")
        click.echo("\n==============\n")
        import traceback
        traceback.print_exc()
        click.echo("\n==============\n")
        shamelessly_promote()

        sys.exit(-1)

if __name__ == '__main__': # pragma: no cover
    handle()
