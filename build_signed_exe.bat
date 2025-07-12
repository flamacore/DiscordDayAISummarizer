@echo off
echo.
echo 🚀 Discord Day Summarizer - Auto-Build with Signing
echo ======================================================
echo.
echo This will create a portable, self-signed executable...
echo.
pause

python build_exe.py

echo.
echo ✨ Build process completed!
echo.
if exist "dist\DiscordDaySummarizer.exe" (
    echo ✅ Success! Your executable is ready:
    echo    📁 dist\DiscordDaySummarizer.exe
    echo.
    echo 💡 This file is fully portable and can run on any Windows machine
    echo    without requiring Python or any other dependencies.
) else (
    echo ❌ Build failed. Check the output above for errors.
)
echo.
pause
