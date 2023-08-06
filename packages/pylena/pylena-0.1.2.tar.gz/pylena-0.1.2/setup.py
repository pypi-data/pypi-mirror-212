# pylint: skip-file
# Setuptools
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.errors import OptionError, SetupError

# Conan
from conan.api.conan_api import ConanAPI
from conan.api.model import Remote
from conan.tools.env.environment import ProfileEnvironment
from conans.client.cache.cache import ClientCache

# Other
from tempfile import TemporaryDirectory
import pathlib
import subprocess
import pybind11
import os

from typing import Tuple

#-------------------------------------------------------------
# CMake Wrapper
#-------------------------------------------------------------

def _from_subprocess_output(subprocess_result : subprocess.Popen) -> Tuple[str, str]:
    return subprocess_result.stdout.decode("utf-8"), subprocess_result.stderr.decode("utf-8")

class CMake:
    def __init__(self, path=os.path.abspath(os.path.dirname(__file__)), variables={}, verbose=False):
        self.path = path
        self.variables = variables
        self.verbose = verbose

    def add_variable(self, name, value):
        if self.variables.get(name) is not None:
            raise ValueError(f"CMake variable {name} already set to {self.variable[name]}")
        self.variables[name] = value

    def configure(self):
        print("-- Configuring CMake")
        out = subprocess.run(["cmake", self.path] + [f"-D{variable}={value}" for (variable, value) in self.variables.items()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if out.returncode != 0:
            stdout, stderr = _from_subprocess_output(out)
            raise SetupError(f"[ERROR]: No able to configure CMake\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        print("-- CMake configured")

    def build(self, target=None):
        target_log = f" for target {target}" if target is not None else ""
        target_invoke = ["--target", target] if target is not None else []
        print(f"-- Building project{target_log}")
        out = subprocess.run(["cmake", "--build", "."] + target_invoke, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if out.returncode != 0:
            stdout, stderr = _from_subprocess_output(out)
            raise SetupError(f"[ERROR]: No able to build{target_log}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        print(f"-- Project built{target_log}")


#-------------------------------------------------------------
# Extension class
#-------------------------------------------------------------

class ConanCMakeExtension(Extension):
    def __init__(self, name, build_type="Release"):
        super().__init__(name, sources=[])
        if build_type not in ["Debug", "Release"]:
            raise OptionError(f"Extension build_type should be Debug or Release (Got {build_type}")
        self.build_type = build_type

class ConanCMakeBuildExtension(build_ext):
    def run(self):
        for ext in self.extensions:
            if not isinstance(ext, ConanCMakeExtension):
                raise SetupError("Extension is not ConanCMakeExtension")
            self._build(ext)

    def _configure_conan_profile(self, conan : ConanAPI, cache: ClientCache, ext):
        profile = conan.profiles.detect()
        if profile.settings["compiler"] == "Visual Studio":
            self.is_msvc = True
        profile.settings["compiler.cppstd"] = 20
        profile.settings["compiler.libcxx"] = "libstdc++11"
        profile.settings["build_type"] = f"{ext.build_type}"
        profile.process_settings(cache)
        print(profile.dumps())
        return profile

    def _conan_install(self, conan : ConanAPI, root, profile):
        LRDE_PUBLIC_URL = 'https://artifactory.lrde.epita.fr/artifactory/api/conan/lrde-public'
        remotes = conan.remotes.list(only_enabled=True)
        if not LRDE_PUBLIC_URL in (e.url for e in remotes):
            remotes.append(Remote("lrde-public", LRDE_PUBLIC_URL))
        path = conan.local.get_conanfile_path(root, str(self.absolute_build_temp), False)
        deps = conan.graph.load_graph_consumer(path, None, None, None, None, profile, profile, None, remotes, True)
        conan.graph.analyze_binaries(deps, ["missing", "onetbb/*", "fmt/*"], remotes=remotes)
        conan.install.install_binaries(deps, remotes)
        conan.install.install_consumer(deps, output_folder=str(self.absolute_build_temp))

    # Some code here come from https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py
    def _build(self, ext : ConanCMakeExtension):
        cwd = pathlib.Path().absolute()
        cache_folder = TemporaryDirectory()

        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        self.absolute_build_temp = build_temp.absolute()
        self.extdir = os.path.dirname(str(pathlib.Path(self.get_ext_fullpath(ext.name)).absolute()))

        os.chdir(self.build_temp)

        # Conan install
        conan = ConanAPI()
        cache = ClientCache(cache_folder.name)
        profile = self._configure_conan_profile(conan, cache, ext)
        self._conan_install(conan, str(cwd), profile)

        # CMake
        cmake_variables = self._make_cmake_variable(ext)
        cmake = CMake(cwd, cmake_variables)
        cmake.configure()
        if not self.dry_run:
            cmake.build()

        os.chdir(cwd)

    def _make_cmake_variable(self, ext : ConanCMakeExtension):
        cmake_variables = {
            "CMAKE_BUILD_TYPE": ext.build_type,
            "CMAKE_TOOLCHAIN_FILE": os.path.join(self.absolute_build_temp, "build", "conan_toolchain.cmake"),
            "pybind11_DIR": pybind11.get_cmake_dir(),
            "CMAKE_LIBRARY_OUTPUT_DIRECTORY": self.extdir,
            "CMAKE_BUILD_PARALLEL_LEVEL": 8
        }
        if "PYTHON_EXECUTABLE" in os.environ:
            cmake_variables["PYTHON_EXECUTABLE"] = os.environ["PYTHON_EXECUTABLE"]
        cmake_variables["CMAKE_POLICY_DEFAULT_CMP0091"] = "NEW"
        return cmake_variables

#-------------------------------------------------------------
# Setup
#-------------------------------------------------------------

setup(
    cmdclass={"build_ext": ConanCMakeBuildExtension},
    ext_modules=[ConanCMakeExtension("pylena/pylena_cxx")],
    platforms=["linux"],
    packages=find_packages(exclude=["tests", "doc"])
)
