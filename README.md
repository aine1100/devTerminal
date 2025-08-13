# DevTerm - Git & Docker Automation GUI

DevTerm is a cross-platform GUI application that simplifies Git and Docker operations for developers. No more command line complexity - just click buttons and get things done!

## Features

### Git Operations
- **Clone Repository**: Enter a Git URL and destination folder to clone repositories
- **Commit & Push**: Add commit messages and push changes with one click
- **Branch Management**: Switch between branches easily with a dropdown interface

### Docker Operations
- **Build Images**: Build Docker images from Dockerfiles with a simple interface
- **Run Containers**: Start containers with port mapping and environment variables
- **Container Management**: View, stop, and remove running containers
- **View Logs**: Check container logs directly from the GUI

## Installation

### Prerequisites
- Python 3.10 or higher
- Git (for Git operations)
- Docker (for Docker operations)

### Quick Start (Recommended)

#### Windows
Double-click `run.bat` or run in Command Prompt:
```cmd
run.bat
```

#### Linux/macOS
Make the script executable and run:
```bash
chmod +x run.sh
./run.sh
```

### Manual Setup

1. **Create Virtual Environment**:
```bash
python -m venv venv
```

2. **Activate Virtual Environment**:

Windows:
```cmd
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the Application**:
```bash
python main.py
```

### Development Setup
For development, you can also install in editable mode:
```bash
pip install -e .
```

### Git Tab
1. **Clone Repository**:
   - Enter the Git repository URL
   - Select destination folder
   - Click "Clone Repository"

2. **Commit & Push**:
   - Select your repository working directory
   - Enter a commit message
   - Click "Commit & Push"

3. **Switch Branch**:
   - Select your repository working directory
   - Click "Refresh" to load available branches
   - Select a branch and click "Switch Branch"

### Docker Tab
1. **Build Image**:
   - Enter image name (e.g., `my-app:latest`)
   - Select Dockerfile path or directory
   - Click "Build Image"

2. **Run Container**:
   - Enter image name
   - Configure port mapping (host port → container port)
   - Add additional options if needed
   - Click "Run Container"

3. **Manage Containers**:
   - View running containers in the list
   - Select a container and use Stop/Remove/View Logs buttons

## Project Structure

```
devterm/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── ui/                 # User interface components
│   ├── __init__.py
│   ├── main_window.py  # Main application window
│   ├── git_tab.py      # Git operations tab
│   └── docker_tab.py   # Docker operations tab
└── core/               # Core functionality
    ├── __init__.py
    ├── command_runner.py    # Shell command execution
    ├── git_operations.py    # Git command wrappers
    ├── docker_operations.py # Docker command wrappers
    └── config_manager.py    # Configuration management
```

## Configuration

DevTerm automatically saves your preferences (last used paths, port settings, etc.) in `~/.devterm/config.json`.

## Error Handling

- All commands are executed safely with proper error handling
- Command output and errors are displayed in the log panel
- Failed operations are highlighted in red, successful ones in green

## Cross-Platform Support

DevTerm works on:
- **Windows**: Uses cmd shell for command execution
- **macOS**: Uses bash shell
- **Linux**: Uses bash shell

## Future Enhancements

The modular design allows for easy addition of new features:
- Cybersecurity tools tab
- Kubernetes operations
- CI/CD pipeline management
- Custom command scripting

## Troubleshooting

### Git not found
Make sure Git is installed and available in your system PATH.

### Docker not found
Make sure Docker is installed and the Docker daemon is running.

### PySide6 installation issues
Try installing with:
```bash
pip install --upgrade pip
pip install PySide6
```

## License

This project is open source. Feel free to modify and distribute as needed.