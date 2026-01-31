# Instruções para gerar a versão Windows

## Para Linux/macOS (WSL2):
```bash
./build_windows.sh
```

## Para Windows (PowerShell):
```powershell
python -m pip install pyinstaller
pyinstaller build_windows.spec --distpath dist
```

O executável `.exe` será criado em `dist/Quests/Quests.exe`

## Alternativa: Usar GitHub Actions
Se preferir, você pode adicionar um workflow de CI/CD no GitHub para compilar para Windows automaticamente em cada release.
