@echo off
chcp 65001 >nul
REM ============================================================================
REM  桌面宠物 一键打包脚本
REM  产物：dist\DesktopPet.exe  —— 单个文件，素材已内嵌，别人双击即可运行
REM ============================================================================
cd /d "%~dp0"

echo [1/4] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [错误] 没找到 python，请先安装 Python 3 并勾选 "Add to PATH"
    pause & exit /b 1
)

echo [2/4] 安装依赖 pygame / numpy / pyinstaller...
python -m pip install --quiet --upgrade pygame numpy pyinstaller
if errorlevel 1 (
    echo   [错误] 依赖安装失败，检查网络
    pause & exit /b 1
)

echo [3/4] 清理旧产物...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist DesktopPet.spec del /q DesktopPet.spec

echo [4/4] 打包中（首次约 1-3 分钟）...
pyinstaller --onefile --noconsole --name DesktopPet ^
            --add-data "pet.png;." ^
            --exclude-module tkinter ^
            --exclude-module unittest ^
            desktop_pet.py
if errorlevel 1 (
    echo   [错误] 打包失败
    pause & exit /b 1
)

echo.
echo ============================================================
echo  完成！产物： %cd%\dist\DesktopPet.exe
echo  素材已内嵌，直接把这一个 exe 发给别人，双击就能跑。
echo ============================================================
echo.
pause
