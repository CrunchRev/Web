@echo off

:x
git fetch

for /f "tokens=*" %%a in ('git rev-list HEAD...origin/main --count') do set COUNT=%%a

if not "%COUNT%"=="0" (
    echo Updates available. Stashing local changes and pulling latest updates...
    git stash
    git pull
) else (
    echo No updates found.
)

python main.py
goto x
