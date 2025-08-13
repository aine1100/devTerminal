#!/usr/bin/env python3
"""
DevTerm - GUI tool for automating Git and Docker actions
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from PySide6.QtWidgets import QApplication
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install PySide6 with: pip install PySide6")
    sys.exit(1)

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("DevTerm")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()