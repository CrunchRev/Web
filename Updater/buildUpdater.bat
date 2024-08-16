@echo off

cd /d %~dp0
pyinstaller --onefile WebUpdater.py --icon C:\Web\CrunchRevSite\staticContent\CrunchRevAsset1.png
pause