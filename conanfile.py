from conans import ConanFile, CMake, tools
import shutil
import os


# From https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth/31039095
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)

    root_files = os.listdir(src)
    if ignore:
        excluded = ignore(src, root_files)
        root_files = [x for x in root_files if x not in excluded]

    for item in root_files:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class YatConan(ConanFile):
    name = "yat"
    version = "1.11.1"
    license = "GPL-2"
    author = "marius.elvert@softwareschneiderei.de"
    url = ""
    description = ""
    topics = ("utility", "control-system",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "cmake_fixes.patch"

    def source(self):
        tag = "svn://svn.code.sf.net/p/tango-cs/code/share/yat/tags/YAT-1.11.1/"
        svn = tools.SVN()
        svn.checkout(tag)

    def build(self):
        copytree(self.source_folder, self.build_folder,
                 ignore=shutil.ignore_patterns(".svn", ".kdev4", "msvc", "macosx"))

        self.output.info("Applying patch")
        tools.patch(patch_file=os.path.join(self.source_folder, "cmake_fixes.patch"))

        cmake = CMake(self)
        cmake.configure(source_folder=self.build_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["libyat"]

