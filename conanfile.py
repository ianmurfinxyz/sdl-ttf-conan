from conans import ConanFile, CMake, tools
import os, shutil

class SDLTTFConan(ConanFile):
	name = "sdl-ttf"
	version = "2.0.18"
	description = "Library which allows you to use TrueType fonts in your SDL applications"
	homepage = "https://github.com/libsdl-org/SDL_ttf"
	license = "Zlib https://www.libsdl.org/license.php"
	url="https://github.com/ianmurfinxyz/sdl-ttf-conan"
	settings = "os", "compiler", "arch", "build_type"
	options = {"shared": [True, False]}
	default_options = {"shared": False}
	generators = "cmake"
	exports_sources = ["CMakeLists.txt", "CMakeLists-sdl-ttf.txt"]
	zip_name = f"release-{version}.tar.gz"
	zip_folder_name = f"SDL_ttf-release-{version}"
	build_subfolder = "build"
	source_subfolder = "source"
	user = "ianmurfinxyz"
	channel = "stable"

	def requirements(self):
		self.requires("freetype/2.11.1")
		self.requires("sdl/2.0.20@ianmurfinxyz/stable")

	def source(self):
		tools.get(f"https://github.com/libsdl-org/SDL_ttf/archive/refs/tags/{self.zip_name}")
		os.rename(self.zip_folder_name, self.source_subfolder)
		shutil.move("CMakeLists-sdl-ttf.txt", os.path.join(self.source_subfolder, "CMakeLists.txt"))

	def build(self):
		cmake = CMake(self)
		cmake.configure(build_folder=self.build_subfolder)
		cmake.build()

	def package(self):
		self.copy("SDL_ttf.h", dst="include", src=self.source_subfolder)
		self.copy("*.lib", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)
		self.copy("*.exp", dst="lib", keep_path=False)
		self.copy("*.dll", dst="bin",keep_path=False)
		self.copy("*.so", dst="bin", keep_path=False)
		self.copy("*.pdb", dst="bin", keep_path=False)

	def package_info(self):
		self.cpp_info.includedirs = ['include']
		
		build_type = self.settings.get_safe("build_type", default="Release")
		postfix = "d" if build_type == "Debug" else ""
		
		if self.settings.os == "Windows":
			static = "-static" if not self.options.shared else ""
			self.cpp_info.libs = [
				f"SDL_ttf{static}{postfix}.lib"
			]
		elif self.settings.os == "Linux":
			extension = "so" if self.options.shared else "a"
			self.cpp_info.libs = [
				f"SDL_ttf{static}{postfix}.{extension}"
			]
		
		self.cpp_info.libdirs = ['lib']
		self.cpp_info.bindirs = ['bin']
