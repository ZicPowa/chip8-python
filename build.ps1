# Builds a standalone Windows exe with PyInstaller.
# ROMs are NOT bundled - users place their own `roms/` folder next to chip8.exe.
# Usage: .\build.ps1

python -m pip install --upgrade pyinstaller
pyinstaller --onefile --windowed --name chip8 src/main.py
