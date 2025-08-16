# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('background.png', '.'), ('logo_server.png', '.'), ('music.mp3', '.'), ('info.ico', '.'), ('on.png', '.'), ('off.png', '.'), ('girocarte.png', '.'), ('char1.png', '.'), ('char1_hover.png', '.'), ('char2.png', '.'), ('char2_hover.png', '.'), ('char3.png', '.'), ('char3_hover.png', '.'), ('instagram.png', '.'), ('instagram_hover.png', '.'), ('tiktok.png', '.'), ('tiktok_hover.png', '.'), ('youtube.png', '.'), ('youtube_hover.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
