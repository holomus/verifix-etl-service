@echo off
for /f "tokens=1,2 delims==" %%i in (../dev.env) do (
    set %%i=%%j
)

set DATABASE_URL=postgresql+asyncpg://%VERIFIX_DB_USER%:%VERIFIX_DB_PASSWORD%@localhost:5432/%VERIFIX_DB%

python app.py