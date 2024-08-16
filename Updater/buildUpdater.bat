@echo off

cd /d %~dp0
pyinstaller --onefile WebUpdater.py --icon D:\CrunchRev\Web\CrunchRevSite\staticContent\CrunchRevAsset1.png
pause