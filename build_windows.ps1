# Script para compilar para Windows
# Use isso em um Windows ou WSL2 com Python instalado

if ($PSVersionTable.Platform -eq 'Win32NT') {
    Write-Host "Compilando para Windows..."
    python -m pip install pyinstaller -q
    pyinstaller build_windows.spec --distpath dist
    Write-Host "Executável criado em: dist/Quests/Quests.exe"
} else {
    echo "Este script deve ser executado em um Windows PowerShell"
    echo "Ou instale WSL2 com Python e execute este script"
}
