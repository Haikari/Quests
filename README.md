# Quests - Quest Manager App

A gamified task management application built with Python and Tkinter. Organize your tasks as quests and track your progress through an RPG-like experience system.

## Features

- 🎮 **Quest-Based Task Management**: Organize tasks as quests with difficulty levels
- ⭐ **Experience System**: Gain EXP and coins by completing quests
- 📊 **Level Progression**: Watch your character level up as you progress
- 🌙 **Dark Theme Support**: Switch between light and dark themes
- 💾 **Auto-Save**: Your data is automatically saved
- 📝 **Quest Descriptions**: Add detailed descriptions to your quests
- 📋 **Quest History**: Track completed quests in a separate history tab
- 🎨 **Customizable UI**: Adjust font size and theme to your preference

## Installation

### Linux

1. Download the latest release from [GitHub Releases](https://github.com/Haikari/Quests/releases)
2. Extract the archive
3. Run the executable:
   ```bash
   ./quests-linux
   ```

Alternatively, install as a system application:
```bash
chmod +x quests-linux
sudo cp -r dist/Quests /opt/
cp quests.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

The app will be available in your applications menu under "Quests".

### Windows

To run on Windows, you have two options:

**Option 1: Build from source (recommended)**
1. Install Python 3.10+
2. Clone the repository
3. Run `python -m pip install -r requirements.txt`
4. Run `pyinstaller build_windows.spec --distpath dist`
5. Execute `dist/Quests/Quests.exe`

**Option 2: Use WSL2**
- Install WSL2 with Python and follow Linux instructions above

**Note:** Pre-built Windows executables are not currently distributed. The build process requires running PyInstaller on Windows or WSL2.

## Building from Source

### Prerequisites

- Python 3.10 or higher
- pip or poetry

### Linux/macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/Haikari/Quests.git
   cd Quests/versão\ estavel
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python main.py
   ```

5. Build executable:
   ```bash
   pip install pyinstaller
   pyinstaller --onedir --windowed --name Quests main.py
   ```

### Windows

1. Clone the repository
2. Create virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

4. Run the app:
   ```cmd
   python main.py
   ```

5. Build executable:
   ```cmd
   pip install pyinstaller
   pyinstaller build_windows.spec --distpath dist
   ```

## Usage

### Creating a Quest

1. Enter the quest name
2. Set difficulty level (0-10)
3. Set EXP reward
4. Set coin reward
5. (Optional) Add a description
6. Click "Criar Quest"

### Managing Quests

- **Complete Quest**: Select a quest from "Quests Ativas" and click "Completar Quest Selecionada"
- **Delete Quest**: Select a quest and click "Excluir Quest Selecionada"
- **View History**: Switch to "Histórico" tab to see completed quests

### Settings

- Click "Configurações" to:
  - Enable/disable dark theme
  - Adjust font size
  
- Click "Anotações" to add notes/annotations

## Data Storage

All your data (quests, progress, settings) is automatically saved in:
- **Linux**: `~/.local/share/Quests/quests.json`
- **Windows**: `%APPDATA%\Local\Quests\quests.json`

## Development

### Project Structure

```
versão estavel/
├── main.py              # Main application code
├── icon.png            # App icon
├── quests.json         # Data file (auto-generated)
├── build_windows.spec  # PyInstaller config for Windows
├── build_windows.sh    # Windows build script for WSL2
└── README.md           # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Known Issues

- Tcl/Tk warning during build (harmless)
- Icons not fully supported on Linux (app still works)

## Future Features

- Cloud sync
- Mobile app companion
- Quest templates
- Achievements/badges
- Leaderboard
- Quest scheduling

## License

This project is open source and available under the MIT License.

## Support

For issues, feature requests, or questions, please open an issue on [GitHub Issues](https://github.com/Haikari/Quests/issues).

---

**Made with ❤️ by Haikari**
