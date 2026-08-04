@echo off
setlocal

net session >nul 2>&1
if not "%errorlevel%"=="0" (
  powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

netsh advfirewall firewall show rule name="IPC Yonetim Sistemi (Ozel Ag)" >nul 2>&1
if not "%errorlevel%"=="0" (
  netsh advfirewall firewall add rule name="IPC Yonetim Sistemi (Ozel Ag)" dir=in action=allow protocol=TCP localport=5000 profile=private
) else (
  netsh advfirewall firewall set rule name="IPC Yonetim Sistemi (Ozel Ag)" new enable=yes profile=private
)

echo.
echo IPC Yonetim Sistemi icin TCP 5000 yalnizca Ozel aglarda acildi.
echo Bu pencereyi kapatabilirsiniz.
pause
