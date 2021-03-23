# -*- mode: python -*-

block_cipher = None

add_media = [ ('src/media/*.*', 'media') ]

a = Analysis(['main.py'],
             pathex=['*path*'],
             binaries=[],
             datas=add_media,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure,
		  a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ReshadeUtils',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False,
          version='resources.rc',
          uac_admin=True,
          icon='')

#coll = COLLECT(exe,
#               strip=False,
#               upx=False,
#               name='ReshadeUtils')
