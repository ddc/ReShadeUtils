# -*- mode: python -*-

block_cipher = None
#images = [('../images/*.*', 'images')] no need to add images since its using QT resource file

a = Analysis(['../../main.py'],
             pathex=['*path*'],
             binaries=[],
             datas = [],
             hiddenimports=['sqlalchemy.sql.default_comparator'],
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
          upx=False,
          runtime_tmpdir=None,
          console=False,
          version='version.rc',
          uac_admin=False,
          icon='')
