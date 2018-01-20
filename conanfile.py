from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

GSL_2_4_SHA256 = "4d46d07b946e7b31c19bbf33dda6204d7bedc2f5462a1bae1d4013426cd1ce9b"

class GslConan(ConanFile):
    name = "gsl"
    version = "2.4"
    license = "MIT"
    url = "https://github.com/weatherhead99/conan-gsl"
    description = "The GNU Scientific Library (GSL), a collection of numerical routines for scientific computing"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "cpp_exceptions_compat"}
    default_options = "shared=False","cpp_exceptions_compat=True"
    exports = ["LICENSE.md"]
    

    def source(self):
        tools.ftp_download("ftp.gnu.org","/gnu/gsl/gsl-%s.tar.gz" % self.version)
        tools.check_sha256("gsl-%s.tar.gz" % self.version,GSL_2_4_SHA256)        
        tools.untargz("gsl-%s.tar.gz" % self.version)
        

    def build(self):
        if self.settings.os == "Windows":
            abe = AutoToolsBuildEnvironment(self,win_bash=True)
        else:
            abe = AutoToolsBuildEnvironment(self)

        if self.options["cpp_exceptions_compat"]:
            abe.flags.append("-fexceptions")
            
        abe.configure(configure_dir=os.path.join(self.source_folder,
                                                 "gsl-%s" % self.version))
        abe.make()


    def package(self):
        self.copy("*.h", dst="include", src=self.build_folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        
        if self.options["shared"] == True:
            self.copy("*.dll", dst="bin", src=self.build_folder, keep_path=False)
            self.copy("*.so", dst="lib", src=self.build_folder, keep_path=False)
            self.copy("*.so.*",dst="lib", src=self.build_folder, keep_path=False)
            self.copy("*.dylib", dst="lib", src=self.build_folder, keep_path=False)
        else:
            print("static build")
            self.copy(".libs/libgsl.a", dst="lib", src=self.build_folder, keep_path=False)
            self.copy("cblas/.libs/libgslcblas.a", dst="lib", src=self.build_folder,keep_path=False)

    def package_info(self):
        if not self.settings.os == "Windows":
            if self.options["shared"] == True:
                self.cpp_info.libs = ["libgsl.so", "libgslcblas.so"]
            else:
                self.cpp_info.libs = ["libgsl.a"]
                
        else:
            self.cpp_info.libs = ["libgsl.lib", "libgslcblas.lib"]
            if self.options["shared"] == True:
                self.cpp_info.libs.extend(["libgsl.dll", "libgslcblas.dll"])
