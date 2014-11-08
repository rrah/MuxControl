from distutils.core import setup
import sys
import py2exe

sys.path.append('C:\\Windows\\winsxs\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.6161_none_50934f2ebcb7eb57')

setup(
    windows = ['__main__.py'],
    options = {'py2exe':{'bundle_files': 3}},
    zipfile = None,
)