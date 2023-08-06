# pylint: skip-file
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake

class PyleneNumpyConan(ConanFile):
    name = "pylene-numpy"
    version = "head"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True, "pylene/*:fPIC": True}
    exports_sources = "CMakeLists.txt", "pylene-numpy/*", "LICENCE"

    def requirements(self):
        self.requires("pylene/head@lrde/unstable", transitive_libs=True, transitive_headers=True)
        self.requires("pybind11/2.9.2", transitive_headers=True)

    def validate(self):
        check_min_cppstd(self, 20)

    def configure(self):
        if self.options.shared:
            self.options.fPIC = True
        if self.settings.os != "Windows" and not self.options.fPIC:
            self.output.error("pylene-numpy is intended to be linked to python module and should be compiled with fPIC")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def layout(self):
        self.folders.source = "."
        self.folders.build = "build"
        self.folders.generators = "build"

        self.cpp.source.includedirs = ["pylene-numpy/include"]
        self.cpp.build.libdirs = ["pylene-numpy"]
        self.cpp.package.libs = ["lib"]
        self.cpp.package.includedirs = ["include"]

    def build(self):
        variables = {"BUILD_PYLENA": "OFF"}
        cmake = CMake(self)
        cmake.configure(variables)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "pylene-numpy::pylene-numpy")

        # Core pylene numpy
        self.cpp_info.requires = ["pylene::core", "pybind11::pybind11"]
        self.cpp_info.libs = ["pylene-numpy"]