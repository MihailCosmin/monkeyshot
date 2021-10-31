call virtualenv monkeyShot_venv
call monkeyShot_venv\\Scripts\\activate

call monkeyShot_venv\\Scripts\\python.exe -m pip install -r requirements.txt
call pyinstaller --paths="monkeyShot_venv\\Lib\site-packages" --paths="monkeyShot_venv\\Lib\site-packages\\cv2\\" "monkeyshot\\monkeyshot.py"
rem call pyinstaller monkeyshot.spec

rem if exist "__pycache__\" @RD /S /Q "__pycache__"
rem if exist "build\" @RD /S /Q "build"
rem if exist "dist\monkeyshot.exe" copy "dist\monkeyshot.exe" "."
rem if exist "dist\" @RD /S /Q "dist"
rem del "monkeyshot.spec"
rem if exist "monkeyShot_venv\" @RD /S /Q "monkeyShot_venv"

timeout /t 100