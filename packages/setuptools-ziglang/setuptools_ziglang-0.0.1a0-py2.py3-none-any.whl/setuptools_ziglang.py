from setuptools.command.build_ext import build_ext

import sys

class build_zig_ext(build_ext):
    def build_extensions(self):
        self.compiler.set_executable("compiler", ["zig", "cc"])
        self.compiler.set_executable("compiler_so", ["zig", "cc"])
        self.compiler.set_executable("compiler_cxx", ["zig", "cc"])
        self.compiler.set_executable("linker_so", ["zig", "cc", "-shared"])
        self.compiler.set_executable("linker_exe", ["zig", "cc"])
        self.compiler.set_executable("archiver", ["zig", "ar", "-cr"])
        
        if sys.platform[:6] == "darwin":
            self.compiler.set_executable("ranlib", ["zig", "ranlib"])
    
        build_ext.build_extensions(self)


