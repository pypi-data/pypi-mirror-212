import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# pybind11 import, if it's missing then try to install it
try:
    import pybind11
except ImportError:
    print("pybind11 not found, installing...")
    # Install pybind11 using pip
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pybind11'])
    import pybind11

# Get the numpy include directory
try:
    import numpy as np
except ImportError:
    print("numpy not found, installing...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

def get_numpy_include():
    """Return numpy include directory."""
    return np.get_include()

def get_pybind_include():
    """Return pybind11 include directory."""
    return pybind11.get_include()

# Define the extension module based on the platform
if sys.platform.startswith('win'):
    ext_module = Extension(
        'pyeCam',
        sources=['Windows/PyeCam.cpp', 'Windows/HID.cpp', 'Windows/Ext.cpp','Windows/Devices.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_numpy_include(),
            'Windows/DeviceManager.hpp',
            'Windows/Devices.hpp',
            
        ],
        language='c++'
    )
else:
    ext_module = Extension(
        'pyeCam',
        sources=['Linux/pyCam.cpp', 'Linux/HID.cpp', 'Linux/Ext.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_numpy_include()
        ],
        language='c++'
    )

# Custom build_ext command to enable passing extra compiler options
class BuildExt(build_ext):
    def build_extensions(self):
        extra_compile_args = ['-std=c++11']
        if sys.platform.startswith('win'):
            extra_compile_args.extend(['/DUNICODE', '/D_UNICODE'])
            extra_link_args = [
        '/LTCG', 'ole32.lib', 'strmiids.lib', 'uuid.lib', 'oleaut32.lib',
        'user32.lib', 'gdi32.lib', 'winspool.lib', 'shell32.lib', 'comdlg32.lib',
        'advapi32.lib', 'mfplat.lib', 'mf.lib', 'mfplay.lib', 'shlwapi.lib',
        'Mfreadwrite.lib', 'mfuuid.lib', 'powrprof.lib', 'd3d11.lib', 'd3d9.lib',
        'Setupapi.lib', 'wmcodecdspuuid.lib', 'Msimg32.lib', 'wbemuuid.lib'
    ]
        else:
            extra_link_args = []
        for ext in self.extensions:
            ext.extra_compile_args = extra_compile_args
            ext.extra_link_args = extra_link_args
        build_ext.build_extensions(self)

# Setup configuration
setup(
    name='pyeCam',
    version='0.0.42',
    description='Example project using pybind11',
    author='Your Name',
    author_email='your_email@example.com',
    ext_modules=[ext_module],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False
)
