#!/usr/bin/env python3
from distutils.core import setup, Extension
import platform
import os
import subprocess


def get_command_output(command):
    return subprocess.check_output(command, shell=True).decode("utf-8").strip()


def find_c_sources(path):
    sources = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".c"):
                sources.append(os.path.join(root, file))
    return sources


def find_include_headers(path):
    headers = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".h"):
                headers.append(os.path.join(root, file))
    return headers


def find_include_dirs():
    includes = [
        "/usr/local/include",
        "/usr/local/include/freerdp2",
        "/usr/local/include/winpr2",
        "/usr/include/freerdp2",
        "/usr/include/winpr2",
    ]
    if platform.system() == "Darwin":
        freerdp2_prefix = get_command_output("brew --prefix freerdp")
        includes.append(os.path.join(freerdp2_prefix, "include", "freerdp2"))
        includes.append(os.path.join(freerdp2_prefix, "include", "winpr2"))
    elif platform.system() == "Windows":
        vcpkg_path = os.environ.get("VCPKG_INSTALLATION_ROOT")
        arch_ret = platform.architecture()
        if arch_ret[0].startswith('64'):
            arch_dir = "x64-windows"
        else:
            arch_dir = "x86-windows"
        windows_include = os.path.join(vcpkg_path, "installed", arch_dir, "include")
        includes.append(windows_include)
    return includes


def find_library_dirs():
    libraries = ["/usr/local/lib", "/usr/lib", "/usr/lib64"]
    if platform.system() == "Windows":
        vcpkg_path = os.environ.get("VCPKG_INSTALLATION_ROOT")
        arch_ret = platform.architecture()
        if arch_ret[0].startswith('64'):
            arch_dir = "x64-windows"
        else:
            arch_dir = "x86-windows"
        windows_lib = os.path.join(vcpkg_path, "installed", arch_dir, "bin")
        libraries.append(windows_lib)
    return libraries


target_os = platform.system()
package_root = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(package_root, "src")
c_sources = [os.path.relpath(item, package_root) for item in find_c_sources(src)]
c_headers = [os.path.relpath(item, package_root) for item in find_include_headers(src)]
include_dirs = find_include_dirs()
library_dirs = find_library_dirs()

module = Extension("pyfreerdp",
                   sources=c_sources,
                   depends=c_headers,
                   define_macros=[("TARGET_OS_WATCH", target_os),
                                  ("TARGET_OS_IPHONE", '0'), ],
                   libraries=['freerdp2'],
                   include_dirs=include_dirs,
                   library_dirs=library_dirs, )

setup(
    name="pyfreerdp",
    author="Eric",
    url="https://github.com/LeeEirc",
    author_email="xplzv@126.com",
    version="0.0.1",
    description="Python wrapper for FreeRDP",
    ext_modules=[module, ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
)
