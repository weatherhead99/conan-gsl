from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

GSL_2_4_SHA256 = "4d46d07b946e7b31c19bbf33dda6204d7bedc2f5462a1bae1d4013426cd1ce9b"

class GslConan(ConanFile):
    name = "gsl"
    version = "2.4"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gsl here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    

    def source(self):
        tools.ftp_download("ftp.gnu.org","/gnu/gsl/gsl-%s.tar.gz" % self.version)
        tools.check_sha256("gsl-%s.tar.gz" % self.version,GSL_2_4_SHA256)        
        tools.untargz("gsl-%s.tar.gz" % self.version)
        

    def build(self):
        if self.settings.os == "Windows":
            abe = AutoToolsBuildEnvironment(self,win_bash=True)
        else:
            abe = AutoToolsBuildEnvironment(self)
        
        abe.configure(configure_dir=os.path.join(self.source_folder,
                                                 "gsl-%s" % self.version))
        abe.make()


    def package(self):
        self.copy("*.h", dst="include", src=self.build_folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        
        if self.options["shared"] == True:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.so.*",dst="lib",keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.copy("libgsl.a", dst="lib", keep_path=False)
            self.copy("libgslcblas.a",dst="lib",keep_path=False)

    def package_info(self):
        if not self.settings.os == "Windows":
            if self.options["shared"] == True:
                self.cpp_info.libs = ["libgsl.so", "libgslcblas.so"]
            else:
                self.cpp_info.libs = ["libgsl.a"]
                
        else:
            pass
            #TODO: windows config!
