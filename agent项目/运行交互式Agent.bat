@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   我的交互式 Agent
echo ========================================
echo.

call agent_env\Scripts\activate.bat
python apps\my_agent.py

echo.
pause
