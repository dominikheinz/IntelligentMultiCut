cd %~dp0
cd..
IF EXIST venv rmdir /s /q venv
IF EXIST Intelligent_Multicut.bat del Intelligent_Multicut.bat

echo cd %%~dp0% > "Intelligent_Multicut.bat"
echo cd venv >> "Intelligent_Multicut.bat"
echo cd Scripts >> "Intelligent_Multicut.bat"
echo activate ^&^& cd %%~dp0% ^&^& cd src ^&^& python main.py  >> "Intelligent_Multicut.bat"

GOTO open_python_install
IF %ERRORLEVEL% NEQ 0 GOTO open_py_install


:open_python_install
cd %~dp0
python data\virtualenv-15.1.0\virtualenv.py ../venv
cd ..
cd venv\Scripts
activate && cd.. && cd.. && cd installer && python installer.py
deactivate

:open_py_install
cd %~dp0
py data\virtualenv-15.1.0\virtualenv.py ../venv
cd ..
cd venv\Scripts
activate && cd.. && cd.. && cd installer && python installer.py
deactivate