@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   周报自动生成器
echo ========================================
echo.

call agent_env\Scripts\activate.bat
python apps\04_weekly_report.py

echo.
echo ========================================
echo   按任意键关闭窗口...
echo ========================================
pause >nul
