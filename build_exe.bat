call virtualenv monkeyShot_venv
call monkeyShot_venv\\Scripts\\activate

call monkeyShot_venv\\Scripts\\python.exe -m pip install -r requirements.txt
rem call pyinstaller --paths="monkeyShot_venv\\Lib\site-packages" --paths="monkeyShot_venv\\Lib\site-packages\\cv2\\" "monkeyshot\\monkeyshot.py"
call pyinstaller monkeyshot.spec

if exist "__pycache__\" @RD /S /Q "__pycache__"
if exist "build\" @RD /S /Q "build"
rem if exist "dist\monkeyshot\" copy "dist\monkeyshot" "."
rem if exist "dist\" @RD /S /Q "dist"
rem del "monkeyshot.spec"
if exist "monkeyShot_venv\" @RD /S /Q "monkeyShot_venv"

timeout /t 100