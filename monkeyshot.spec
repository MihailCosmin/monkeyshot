# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['monkeyshot\\monkeyshot.pyw'],
             pathex=['monkeyShot_venv\\\\Lib\\site-packages', 'monkeyShot_venv\\\\Lib\\site-packages\\\\cv2\\', 'D:\\monkeyshot'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('img\\monkey.ico','monkeyshot\\img\\monkey.ico', "DATA"),
	('img\\close_button_24px_#AA0000.png','monkeyshot\\img\\close_button_24px_#AA0000.png', "DATA"),
	('img\\dynamic_screenshot_button_48px_#AA0000.png','monkeyshot\\img\\dynamic_screenshot_button_48px_#AA0000.png', "DATA"),
	('img\\record_button_48px_#AA0000.png','monkeyshot\\img\\record_button_48px_#AA0000.png', "DATA"),
	('img\\region_record_button_48px_#AA0000.png','monkeyshot\\img\\region_record_button_48px_#AA0000.png', "DATA"),
	('img\\settings_button_48px_#AA0000.png','monkeyshot\\img\\settings_button_48px_#AA0000.png', "DATA"),
	('img\\static_screenshot_button_48px_#AA0000.png','monkeyshot\\img\\static_screenshot_button_48px_#AA0000.png', "DATA")
]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='monkeyshot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=True,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='monkeyshot')
