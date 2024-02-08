# -*- mode: python -*-

block_cipher = None

data_files = [
    #,('../images/*.*', 'images') no need to add images since its using QT resource file
]

a = Analysis(['../../../main.py'],
             pathex=[],
             binaries=[],
             datas = data_files,
             hiddenimports=['sqlalchemy.sql.default_comparator', 'fsspec.implementations.github'],
             copy_metadata=['importlib_metadata'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pysqlite2', 'MySQLdb', 'psycopg2', 'sip'],
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
          upx=True,
          runtime_tmpdir=None,
          console=False,
          version='version.rc',
          uac_admin=False,
          copy_metadata=['ddcutils'],
          icon='')
