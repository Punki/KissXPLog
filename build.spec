# -*- mode: python ; coding: utf-8 -*-
import sys


block_cipher = None


a = Analysis(['KissXPLog/__init__.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if sys.platform == 'win32' or sys.platform == 'win64':
	exe = EXE(pyz,
		  a.scripts,
		  [],
		  exclude_binaries=True,
		  name='KissXPLog.exe',
		  debug=False,
		  bootloader_ignore_signals=False,
		  strip=False,
		  upx=True,
		  upx_exclude=[],
		  runtime_tmpdir=None,
		  console=False,
		  disable_windowed_traceback=False,
		  target_arch=None,
		  codesign_identity=None,
		  entitlements_file=None )


if sys.platform == 'linux':
	exe = EXE(pyz,
		  a.scripts,
		  a.binaries,
		  a.zipfiles,
		  a.datas,  
		  [],
		  name='KissXPLog',
		  debug=False,
		  bootloader_ignore_signals=False,
		  strip=False,
		  upx=True,
		  upx_exclude=[],
		  runtime_tmpdir=None,
		  console=False,
		  disable_windowed_traceback=False,
		  target_arch=None,
		  codesign_identity=None,
		  entitlements_file=None )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KissXPLog.exe',
)
