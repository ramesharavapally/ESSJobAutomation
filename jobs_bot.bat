@echo off

REM Step 1: Activate py_automate venv
call %~dp0py_automate\Scripts\activate

REM Step 2: Navigate to ERPE2E\tests folder
cd /d "%~dp0tests"

REM Step 3: Run pyteest -m jobs command
pytest -m jobs

REM Step 4: Deactivate py_automate venv (optional)
deactivate