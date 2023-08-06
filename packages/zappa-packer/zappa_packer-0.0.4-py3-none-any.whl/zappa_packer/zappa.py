"""
Zappa core library. You may also want to look at `cli.py` and `util.py`.
"""

##
# Imports
##
import getpass
import glob
import json
import logging
import os
import re
import shutil
import requests
import subprocess
import tarfile
import tempfile
import time
import uuid
import zipfile
from builtins import bytes, int
from distutils.dir_util import copy_tree
from io import open
from typing import Optional
from setuptools import find_packages
import sys
import stat
from tqdm import tqdm

##
# Logging Config
##

logging.basicConfig(format="%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# We never need to include these.
# Related: https://github.com/Miserlou/Zappa/pull/56
# Related: https://github.com/Miserlou/Zappa/pull/581
ZIP_EXCLUDES = [
    "*.exe",
    "*.DS_Store",
    "*.Python",
    "*.git",
    ".git/*",
    "*.zip",
    "*.tar.gz",
    "*.hg",
    "pip",
    "docutils*",
    "setuputils*",
    "__pycache__/*",
]

##
# Classes
##
def copytree(src, dst, metadata=True, symlinks=False, ignore=None):
    """
    This is a contributed re-implementation of 'copytree' that
    should work with the exact same behavior on multiple platforms.
    When `metadata` is False, file metadata such as permissions and modification
    times are not copied.
    """

    def copy_file(src, dst, item):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if symlinks and os.path.islink(s):  # pragma: no cover
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            if metadata:
                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    os.lchmod(d, mode)
                except Exception:
                    pass  # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, metadata, symlinks, ignore)
        else:
            shutil.copy2(s, d) if metadata else shutil.copy(s, d)

    try:
        lst = os.listdir(src)
        if not os.path.exists(dst):
            os.makedirs(dst)
            if metadata:
                shutil.copystat(src, dst)
    except NotADirectoryError:  # egg-link files
        copy_file(os.path.dirname(src), os.path.dirname(dst), os.path.basename(src))
        return

    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]

    for item in lst:
        copy_file(src, dst, item)

def contains_python_files_or_subdirs(folder):
    """
    Checks (recursively) if the directory contains .py or .pyc files
    """
    for root, dirs, files in os.walk(folder):
        if [filename for filename in files if filename.endswith(".py") or filename.endswith(".pyc")]:
            return True

        for d in dirs:
            for _, subdirs, subfiles in os.walk(d):
                if [filename for filename in subfiles if filename.endswith(".py") or filename.endswith(".pyc")]:
                    return True

    return False

def conflicts_with_a_neighbouring_module(directory_path):
    """
    Checks if a directory lies in the same directory as a .py file with the same name.
    """
    parent_dir_path, current_dir_name = os.path.split(os.path.normpath(directory_path))
    neighbours = os.listdir(parent_dir_path)
    conflicting_neighbour_filename = current_dir_name + ".py"
    return conflicting_neighbour_filename in neighbours

class Zappa:
    """
    Zappa!
    Makes it easy to run Python web applications on AWS Lambda/API Gateway.
    """

    ##
    # Configurables
    ##

    http_methods = ["ANY"]
    role_name = "ZappaLambdaExecution"
    extra_permissions = None
    apigateway_policy = None
    cloudwatch_log_levels = ["OFF", "ERROR", "INFO"]
    xray_tracing = False

    def __init__(
        self,
        runtime="python3.7"  # Detected at runtime in CLI
    ):
        """
        Instantiate this new Zappa instance, loading any custom credentials if necessary.
        """

        self.runtime = runtime

        if self.runtime == "python3.7":
            self.manylinux_suffix_start = "cp37m"
        elif self.runtime == "python3.8":
            # The 'm' has been dropped in python 3.8+ since builds with and without pymalloc are ABI compatible
            # See https://github.com/pypa/manylinux for a more detailed explanation
            self.manylinux_suffix_start = "cp38"
        elif self.runtime == "python3.9":
            self.manylinux_suffix_start = "cp39"
        else:
            self.manylinux_suffix_start = "cp310"

        # AWS Lambda supports manylinux1/2010, manylinux2014, and manylinux_2_24
        manylinux_suffixes = ("_2_24", "2014", "2010", "1")
        self.manylinux_wheel_file_match = re.compile(
            rf'^.*{self.manylinux_suffix_start}-(manylinux_\d+_\d+_x86_64[.])?manylinux({"|".join(manylinux_suffixes)})_x86_64[.]whl$'  # noqa: E501
        )
        self.manylinux_wheel_abi3_file_match = re.compile(
            rf'^.*cp3.-abi3-manylinux({"|".join(manylinux_suffixes)})_x86_64.whl$'
        )
    ##
    # Packaging
    ##

    def copy_editable_packages(self, egg_links, temp_package_path):
        """ """
        for egg_link in egg_links:
            with open(egg_link, "rb") as df:
                egg_path = df.read().decode("utf-8").splitlines()[0].strip()
                pkgs = set([x.split(".")[0] for x in find_packages(egg_path, exclude=["test", "tests"])])
                for pkg in pkgs:
                    copytree(
                        os.path.join(egg_path, pkg),
                        os.path.join(temp_package_path, pkg),
                        metadata=False,
                        symlinks=False,
                    )

        if temp_package_path:
            # now remove any egg-links as they will cause issues if they still exist
            for link in glob.glob(os.path.join(temp_package_path, "*.egg-link")):
                os.remove(link)

    def get_deps_list(self, pkg_name, installed_distros=None):
        """
        For a given package, returns a list of required packages. Recursive.
        """
        # https://github.com/Miserlou/Zappa/issues/1478.  Using `pkg_resources`
        # instead of `pip` is the recommended approach.  The usage is nearly
        # identical.
        import pkg_resources

        deps = []
        if not installed_distros:
            installed_distros = pkg_resources.WorkingSet()
        for package in installed_distros:
            if package.project_name.lower() == pkg_name.lower():
                deps = [(package.project_name, package.version)]
                for req in package.requires():
                    deps += self.get_deps_list(pkg_name=req.project_name, installed_distros=installed_distros)
        return list(set(deps))  # de-dupe before returning

    def create_handler_venv(self, use_zappa_release: Optional[str] = None):
        """
        Takes the installed zappa and brings it into a fresh virtualenv-like folder. All dependencies are then downloaded.
        """
        import subprocess

        # We will need the currenv venv to pull Zappa from
        current_venv = self.get_current_venv()

        # Make a new folder for the handler packages
        ve_path = os.path.join(os.getcwd(), "handler_venv")

        if os.sys.platform == "win32":
            current_site_packages_dir = os.path.join(current_venv, "Lib", "site-packages")
            venv_site_packages_dir = os.path.join(ve_path, "Lib", "site-packages")
        else:
            current_site_packages_dir = os.path.join(current_venv, "lib", self.get_venv_from_python_version(), "site-packages")
            venv_site_packages_dir = os.path.join(ve_path, "lib", self.get_venv_from_python_version(), "site-packages")

        if not os.path.isdir(venv_site_packages_dir):
            os.makedirs(venv_site_packages_dir)

        # Copy zappa* to the new virtualenv
        zappa_things = [z for z in os.listdir(current_site_packages_dir) if z.lower()[:5] == "zappa"]
        for z in zappa_things:
            copytree(
                os.path.join(current_site_packages_dir, z),
                os.path.join(venv_site_packages_dir, z),
            )

        # Use pip to download zappa's dependencies.
        # Copying from current venv causes issues with things like PyYAML that installs as yaml
        zappa_deps = self.get_deps_list("zappa")
        pkg_list = []
        for dep, version in zappa_deps:
            # allow specified zappa version for slim_handler_test
            if dep == "zappa" and use_zappa_release:
                pkg_version_str = f"{dep}=={use_zappa_release}"
            else:
                pkg_version_str = f"{dep}=={version}"
            pkg_list.append(pkg_version_str)

        # Need to manually add setuptools
        pkg_list.append("setuptools")
        command = [
            "pip",
            "install",
            "--quiet",
            "--target",
            venv_site_packages_dir,
        ] + pkg_list

        # This is the recommended method for installing packages if you don't
        # to depend on `setuptools`
        # https://github.com/pypa/pip/issues/5240#issuecomment-381662679
        pip_process = subprocess.Popen(command, stdout=subprocess.PIPE)
        # Using communicate() to avoid deadlocks
        pip_process.communicate()
        pip_return_code = pip_process.returncode

        if pip_return_code:
            raise EnvironmentError("Pypi lookup failed")

        return ve_path

    # staticmethod as per https://github.com/Miserlou/Zappa/issues/780
    @staticmethod
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

    def get_venv_from_python_version(self):
        return "python{}.{}".format(*sys.version_info)

    def create_lambda_zip(
        self,
        prefix="lambda_package",
        handler_file=None,
        slim_handler=False,
        minify=True,
        exclude=None,
        exclude_glob=None,
        use_precompiled_packages=True,
        include=None,
        venv=None,
        output=None,
        disable_progress=False,
        archive_format="zip",
    ):
        """
        Create a Lambda-ready zip file of the current virtualenvironment and working directory.
        Returns path to that file.
        """
        # Validate archive_format
        if archive_format not in ["zip", "tarball"]:
            raise KeyError("The archive format to create a lambda package must be zip or tarball")

        # Pip is a weird package.
        # Calling this function in some environments without this can cause.. funkiness.
        import pip  # noqa: 547

        if not venv:
            venv = self.get_current_venv()

        build_time = str(int(time.time()))
        cwd = os.getcwd()
        if not output:
            if archive_format == "zip":
                archive_fname = prefix + "-" + build_time + ".zip"
            elif archive_format == "tarball":
                archive_fname = prefix + "-" + build_time + ".tar.gz"
        else:
            archive_fname = output
        archive_path = os.path.join(cwd, archive_fname)

        # Files that should be excluded from the zip
        if exclude is None:
            exclude = list()

        if exclude_glob is None:
            exclude_glob = list()

        # Exclude the zip itself
        exclude.append(archive_path)

        # Make sure that 'concurrent' is always forbidden.
        # https://github.com/Miserlou/Zappa/issues/827
        if "concurrent" not in exclude:
            exclude.append("concurrent")

        def splitpath(path):
            parts = []
            (path, tail) = os.path.split(path)
            while path and tail:
                parts.append(tail)
                (path, tail) = os.path.split(path)
            parts.append(os.path.join(path, tail))
            return list(map(os.path.normpath, parts))[::-1]

        split_venv = splitpath(venv)
        split_cwd = splitpath(cwd)

        # Ideally this should be avoided automatically,
        # but this serves as an okay stop-gap measure.
        if split_venv[-1] == split_cwd[-1]:  # pragma: no cover
            print(
                "Warning! Your project and virtualenv have the same name! You may want "
                "to re-create your venv with a new name, or explicitly define a "
                "'project_name', as this may cause errors."
            )

        # First, do the project..
        temp_project_path = tempfile.mkdtemp(prefix="zappa-project")

        if not slim_handler:
            # Slim handler does not take the project files.
            if minify:
                # Related: https://github.com/Miserlou/Zappa/issues/744
                excludes = ZIP_EXCLUDES + exclude + [split_venv[-1]]
                copytree(
                    cwd,
                    temp_project_path,
                    metadata=False,
                    symlinks=False,
                    ignore=shutil.ignore_patterns(*excludes),
                )
            else:
                copytree(cwd, temp_project_path, metadata=False, symlinks=False)
            for glob_path in exclude_glob:
                for path in glob.glob(os.path.join(temp_project_path, glob_path)):
                    try:
                        os.remove(path)
                    except OSError:  # is a directory
                        shutil.rmtree(path)

        # If a handler_file is supplied, copy that to the root of the package,
        # because that's where AWS Lambda looks for it. It can't be inside a package.
        if handler_file:
            filename = handler_file.split(os.sep)[-1]
            shutil.copy(handler_file, os.path.join(temp_project_path, filename))

        # Create and populate package ID file and write to temp project path
        package_info = {}
        package_info["uuid"] = str(uuid.uuid4())
        package_info["build_time"] = build_time
        package_info["build_platform"] = os.sys.platform
        package_info["build_user"] = getpass.getuser()
        # TODO: Add git head and info?

        # Ex, from @scoates:
        # def _get_git_branch():
        #     chdir(DIR)
        #     out = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
        #     lambci_branch = environ.get('LAMBCI_BRANCH', None)
        #     if out == "HEAD" and lambci_branch:
        #         out += " lambci:{}".format(lambci_branch)
        #     return out

        # def _get_git_hash():
        #     chdir(DIR)
        #     return check_output(['git', 'rev-parse', 'HEAD']).strip()

        # def _get_uname():
        #     return check_output(['uname', '-a']).strip()

        # def _get_user():
        #     return check_output(['whoami']).strip()

        # def set_id_info(zappa_cli):
        #     build_info = {
        #         'branch': _get_git_branch(),
        #         'hash': _get_git_hash(),
        #         'build_uname': _get_uname(),
        #         'build_user': _get_user(),
        #         'build_time': datetime.datetime.utcnow().isoformat(),
        #     }
        #     with open(path.join(DIR, 'id_info.json'), 'w') as f:
        #         json.dump(build_info, f)
        #     return True

        package_id_file = open(os.path.join(temp_project_path, "package_info.json"), "w")
        dumped = json.dumps(package_info, indent=4)
        try:
            package_id_file.write(dumped)
        except TypeError:  # This is a Python 2/3 issue. TODO: Make pretty!
            package_id_file.write(str(dumped))
        package_id_file.close()

        # Then, do site site-packages..
        egg_links = []
        temp_package_path = tempfile.mkdtemp(prefix="zappa-packages")
        if os.sys.platform == "win32":
            site_packages = os.path.join(venv, "Lib", "site-packages")
        else:
            site_packages = os.path.join(venv, "lib", self.get_venv_from_python_version(), "site-packages")
        egg_links.extend(glob.glob(os.path.join(site_packages, "*.egg-link")))

        if minify:
            excludes = ZIP_EXCLUDES + exclude
            copytree(
                site_packages,
                temp_package_path,
                metadata=False,
                symlinks=False,
                ignore=shutil.ignore_patterns(*excludes),
            )
        else:
            copytree(site_packages, temp_package_path, metadata=False, symlinks=False)

        # We may have 64-bin specific packages too.
        site_packages_64 = os.path.join(venv, "lib64", self.get_venv_from_python_version(), "site-packages")
        if os.path.exists(site_packages_64):
            egg_links.extend(glob.glob(os.path.join(site_packages_64, "*.egg-link")))
            if minify:
                excludes = ZIP_EXCLUDES + exclude
                copytree(
                    site_packages_64,
                    temp_package_path,
                    metadata=False,
                    symlinks=False,
                    ignore=shutil.ignore_patterns(*excludes),
                )
            else:
                copytree(site_packages_64, temp_package_path, metadata=False, symlinks=False)

        if egg_links:
            self.copy_editable_packages(egg_links, temp_package_path)

        copy_tree(temp_package_path, temp_project_path, update=True)

        # Then the pre-compiled packages..
        if use_precompiled_packages:
            print("Downloading and installing dependencies..")
            installed_packages = self.get_installed_packages(site_packages, site_packages_64)

            try:
                for (
                    installed_package_name,
                    installed_package_version,
                ) in installed_packages.items():
                    cached_wheel_path = self.get_cached_manylinux_wheel(
                        installed_package_name,
                        installed_package_version,
                        disable_progress,
                    )
                    if cached_wheel_path:
                        # Otherwise try to use manylinux packages from PyPi..
                        # Related: https://github.com/Miserlou/Zappa/issues/398
                        shutil.rmtree(
                            os.path.join(temp_project_path, installed_package_name),
                            ignore_errors=True,
                        )
                        with zipfile.ZipFile(cached_wheel_path) as zfile:
                            zfile.extractall(temp_project_path)

            except Exception as e:
                print(e)
                # XXX - What should we do here?

        # Cleanup
        for glob_path in exclude_glob:
            for path in glob.glob(os.path.join(temp_project_path, glob_path)):
                try:
                    os.remove(path)
                except OSError:  # is a directory
                    shutil.rmtree(path)

        # Then archive it all up..
        if archive_format == "zip":
            print("Packaging project as zip.")

            try:
                compression_method = zipfile.ZIP_DEFLATED
            except ImportError:  # pragma: no cover
                compression_method = zipfile.ZIP_STORED
            archivef = zipfile.ZipFile(archive_path, "w", compression_method)

        elif archive_format == "tarball":
            print("Packaging project as gzipped tarball.")
            archivef = tarfile.open(archive_path, "w|gz")

        for root, dirs, files in os.walk(temp_project_path):
            for filename in files:
                # Skip .pyc files for Django migrations
                # https://github.com/Miserlou/Zappa/issues/436
                # https://github.com/Miserlou/Zappa/issues/464
                if filename[-4:] == ".pyc" and root[-10:] == "migrations":
                    continue

                # If there is a .pyc file in this package,
                # we can skip the python source code as we'll just
                # use the compiled bytecode anyway..
                if filename[-3:] == ".py" and root[-10:] != "migrations":
                    abs_filname = os.path.join(root, filename)
                    abs_pyc_filename = abs_filname + "c"
                    if os.path.isfile(abs_pyc_filename):
                        # but only if the pyc is older than the py,
                        # otherwise we'll deploy outdated code!
                        py_time = os.stat(abs_filname).st_mtime
                        pyc_time = os.stat(abs_pyc_filename).st_mtime

                        if pyc_time > py_time:
                            continue

                # Make sure that the files are all correctly chmodded
                # Related: https://github.com/Miserlou/Zappa/issues/484
                # Related: https://github.com/Miserlou/Zappa/issues/682
                os.chmod(os.path.join(root, filename), 0o755)

                if archive_format == "zip":
                    # Actually put the file into the proper place in the zip
                    # Related: https://github.com/Miserlou/Zappa/pull/716
                    zipi = zipfile.ZipInfo(os.path.join(root.replace(temp_project_path, "").lstrip(os.sep), filename))
                    zipi.create_system = 3
                    zipi.external_attr = 0o755 << int(16)  # Is this P2/P3 functional?
                    with open(os.path.join(root, filename), "rb") as f:
                        archivef.writestr(zipi, f.read(), compression_method)
                elif archive_format == "tarball":
                    tarinfo = tarfile.TarInfo(os.path.join(root.replace(temp_project_path, "").lstrip(os.sep), filename))
                    tarinfo.mode = 0o755

                    stat = os.stat(os.path.join(root, filename))
                    tarinfo.mtime = stat.st_mtime
                    tarinfo.size = stat.st_size
                    with open(os.path.join(root, filename), "rb") as f:
                        archivef.addfile(tarinfo, f)

            # Create python init file if it does not exist
            # Only do that if there are sub folders or python files and does not conflict with a neighbouring module
            # Related: https://github.com/Miserlou/Zappa/issues/766
            if not contains_python_files_or_subdirs(root):
                # if the directory does not contain any .py file at any level, we can skip the rest
                dirs[:] = [d for d in dirs if d != root]
            else:
                if "__init__.py" not in files and not conflicts_with_a_neighbouring_module(root):
                    tmp_init = os.path.join(temp_project_path, "__init__.py")
                    open(tmp_init, "a").close()
                    os.chmod(tmp_init, 0o755)

                    arcname = os.path.join(
                        root.replace(temp_project_path, ""),
                        os.path.join(root.replace(temp_project_path, ""), "__init__.py"),
                    )
                    if archive_format == "zip":
                        archivef.write(tmp_init, arcname)
                    elif archive_format == "tarball":
                        archivef.add(tmp_init, arcname)

        # And, we're done!
        archivef.close()

        # Trash the temp directory
        shutil.rmtree(temp_project_path)
        shutil.rmtree(temp_package_path)
        if os.path.isdir(venv) and slim_handler:
            # Remove the temporary handler venv folder
            shutil.rmtree(venv)

        return archive_fname

    @staticmethod
    def get_installed_packages(site_packages, site_packages_64):
        """
        Returns a dict of installed packages that Zappa cares about.
        """
        import pkg_resources

        package_to_keep = []
        if os.path.isdir(site_packages):
            package_to_keep += os.listdir(site_packages)
        if os.path.isdir(site_packages_64):
            package_to_keep += os.listdir(site_packages_64)

        package_to_keep = [x.lower() for x in package_to_keep]

        installed_packages = {
            package.project_name.lower(): package.version
            for package in pkg_resources.WorkingSet()
            if package.project_name.lower() in package_to_keep
            or package.location.lower() in [site_packages.lower(), site_packages_64.lower()]
        }

        return installed_packages

    @staticmethod
    def download_url_with_progress(url, stream, disable_progress):
        """
        Downloads a given url in chunks and writes to the provided stream (can be any io stream).
        Displays the progress bar for the download.
        """
        resp = requests.get(url, timeout=float(os.environ.get("PIP_TIMEOUT", 2)), stream=True)
        resp.raw.decode_content = True

        progress = tqdm(
            unit="B",
            unit_scale=True,
            total=int(resp.headers.get("Content-Length", 0)),
            disable=disable_progress,
        )
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                progress.update(len(chunk))
                stream.write(chunk)

        progress.close()

    def get_cached_manylinux_wheel(self, package_name, package_version, disable_progress=False):
        """
        Gets the locally stored version of a manylinux wheel. If one does not exist, the function downloads it.
        """
        cached_wheels_dir = os.path.join(tempfile.gettempdir(), "cached_wheels")

        if not os.path.isdir(cached_wheels_dir):
            os.makedirs(cached_wheels_dir)
        else:
            # Check if we already have a cached copy
            wheel_name = re.sub(r"[^\w\d.]+", "_", package_name, re.UNICODE)
            wheel_file = f"{wheel_name}-{package_version}-*_x86_64.whl"
            wheel_path = os.path.join(cached_wheels_dir, wheel_file)

            for pathname in glob.iglob(wheel_path):
                if re.match(self.manylinux_wheel_file_match, pathname) or re.match(
                    self.manylinux_wheel_abi3_file_match, pathname
                ):
                    print(f" - {package_name}=={package_version}: Using locally cached manylinux wheel")
                    return pathname

        # The file is not cached, download it.
        wheel_url, filename = self.get_manylinux_wheel_url(package_name, package_version)
        if not wheel_url:
            return None

        wheel_path = os.path.join(cached_wheels_dir, filename)
        print(f" - {package_name}=={package_version}: Downloading")
        with open(wheel_path, "wb") as f:
            self.download_url_with_progress(wheel_url, f, disable_progress)

        if not zipfile.is_zipfile(wheel_path):
            return None

        return wheel_path

    def get_manylinux_wheel_url(self, package_name, package_version):
        """
        For a given package name, returns a link to the download URL,
        else returns None.
        Related: https://github.com/Miserlou/Zappa/issues/398
        Examples here: https://gist.github.com/perrygeo/9545f94eaddec18a65fd7b56880adbae
        This function downloads metadata JSON of `package_name` from Pypi
        and examines if the package has a manylinux wheel. This function
        also caches the JSON file so that we don't have to poll Pypi
        every time.
        """
        cached_pypi_info_dir = os.path.join(tempfile.gettempdir(), "cached_pypi_info")
        if not os.path.isdir(cached_pypi_info_dir):
            os.makedirs(cached_pypi_info_dir)
        # Even though the metadata is for the package, we save it in a
        # filename that includes the package's version. This helps in
        # invalidating the cached file if the user moves to a different
        # version of the package.
        # Related: https://github.com/Miserlou/Zappa/issues/899
        json_file = "{0!s}-{1!s}.json".format(package_name, package_version)
        json_file_path = os.path.join(cached_pypi_info_dir, json_file)
        if os.path.exists(json_file_path):
            with open(json_file_path, "rb") as metafile:
                data = json.load(metafile)
        else:
            url = "https://pypi.python.org/pypi/{}/json".format(package_name)
            try:
                res = requests.get(url, timeout=float(os.environ.get("PIP_TIMEOUT", 1.5)))
                data = res.json()
            except Exception:  # pragma: no cover
                return None, None
            with open(json_file_path, "wb") as metafile:
                jsondata = json.dumps(data)
                metafile.write(bytes(jsondata, "utf-8"))

        if package_version not in data.get("releases", []):
            logger.warning(f"package_version({package_version}) not found in {package_name} metafile={json_file_path}")
            return None, None

        for f in data["releases"][package_version]:
            if re.match(self.manylinux_wheel_file_match, f["filename"]):
                return f["url"], f["filename"]
            elif re.match(self.manylinux_wheel_abi3_file_match, f["filename"]):
                return f["url"], f["filename"]
        return None, None

