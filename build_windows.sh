#!/bin/bash
# Script para compilar para Windows no WSL2

echo "Compilando para Windows..."
python3 -m pip install pyinstaller -q
pyinstaller build_windows.spec --distpath dist

if [ $? -eq 0 ]; then
    echo "Executável criado em: dist/Quests/Quests.exe"
else
    echo "Erro ao compilar para Windows"
    exit 1
fi
