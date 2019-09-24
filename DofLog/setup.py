from DofLog import df_version

import sys
import pkg_resources
from os.path import join, basename

from os import environ
from cx_Freeze import setup, Executable

environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\tcl\tcl8.6'
environ['TK_LIBRARY'] = r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\tcl\tk8.6'

def collect_dist_info(packages):
    """
    Recursively collects the path to the packages' dist-info.
    """
    if not isinstance(packages, list):
        packages = [packages]
    dirs = ["res/icon.ico","res/organiser.ico","res/add.png","res/rem.png","res/login.png","res/up.png","res/down.png","res/bg_2.jpg","res/checkbox_uc.jpg","res/checkbox_c.jpg"]
    for pkg in packages:
        distrib = pkg_resources.get_distribution(pkg)
        for req in distrib.requires():
            dirs.extend(collect_dist_info(req.key))
        dirs.append((distrib.egg_info, join('Lib', basename(distrib.egg_info))))
    return dirs

executable = [Executable(script="DofLog_UI.py",
                         base = "Win32GUI", 
                         targetName="DofLog.exe", 
                         icon="res/icon.ico")
               ]

setup(name='DofLog',
      version=df_version,
      description="DofLog",
      options={
        "build_exe": {
            "packages": ["pkg_resources", "asyncio"],
            "include_files": collect_dist_info("win10toast"),
        },
    },
      executables = executable
     )

# Python Envs > Open in PowerShell
# cd "C:\Users\Tom SUBLET\Documents\#DOC PERSO\Python\DofLog\DofLog"
# python setup.py build
# python setup.py bdist_msi
