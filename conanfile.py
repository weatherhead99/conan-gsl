import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment

class GslConan(ConanFile):
    name = "gsl"
    version = "2.4"
    license = "GPL-3.0"
    url = "https://github.com/weatherhead99/conan-gsl"
    description = "The GNU Scientific Library (GSL), a collection of numerical routines for scientific computing"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "cpp_exceptions_compat" : [True, False]}
    default_options = "shared=False", "cpp_exceptions_compat=True"
    exports = ["LICENSE.md"]
    gsl_2_4_sha256 = "4d46d07b946e7b31c19bbf33dda6204d7bedc2f5462a1bae1d4013426cd1ce9b"

    def source(self):
        tools.ftp_download("ftp.gnu.org", "/gnu/gsl/gsl-%s.tar.gz" % self.version)
        tools.check_sha256("gsl-%s.tar.gz" % self.version, self.gsl_2_4_sha256)
        tools.untargz("gsl-%s.tar.gz" % self.version)

    def build(self):
        gsl_source = os.path.join(self.source_folder, "gsl-%s" % self.version)

        if self.settings.os == "Windows":
            abe = AutoToolsBuildEnvironment(self, win_bash=True)
        else:
            abe = AutoToolsBuildEnvironment(self)

        if self.options["cpp_exceptions_compat"]:
            abe.flags.append("-fexceptions")

        abe.configure(configure_dir=gsl_source,
                      args=["--enable-silent-rules"])
        abe.make()


    def package(self):
        self.copy("*.h", dst="include", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("COPYING", dst="licenses", src=self.source_folder,
                  keep_path=False)

        if self.options["shared"]:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.so.*", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.output.info("static build")
            libs_folder = os.path.join(self.build_folder, ".libs")
            cblas_folder = os.path.join(self.build_folder, "cblas", ".libs")
            self.copy("libgsl.a", dst="lib", src=libs_folder, keep_path=False)
            self.copy("libgslcblas.a", dst="lib", src=cblas_folder,
                      keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["gsl", "gslcblas"]
