@echo off
chcp 65001 >nul
echo ========================================
echo    社区志愿服务系统启动脚本
echo ========================================
echo.

echo [INFO] 正在启动后端服务...
start "后端服务" cmd /k "cd /d backend & python run.py"

echo [INFO] 等待后端服务启动...
timeout /t 3 /nobreak >nul

echo [INFO] 正在启动前端服务...
start "前端服务" cmd /k "cd /d frontend & npm run serve"

echo.
echo [SUCCESS] 前后端服务启动完成！
echo.
echo 服务地址：
echo   后端API: http://localhost:5000
echo   前端应用: http://localhost:8081
echo.
echo 按任意键退出...
pause >nul