"""
DevTerm - Professional Main Window with Modern UI Design
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QTextEdit, QLabel, QSplitter, QFrame, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor

from .git_tab import GitTab
from .docker_tab import DockerTab

class MainWindow(QMainWindow):
    """Professional main window with clean, modern design"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevTerm - Git & Docker Automation")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)
        
        # Apply global theme first
        self.apply_global_theme()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        self.create_header(main_layout)
        
        # Create main content area
        self.create_content_area(main_layout)
        
    def create_header(self, parent_layout):
        """Create professional header with gradient background"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setObjectName("headerFrame")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        # Title section
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        
        # Main title
        title_label = QLabel("DevTerm")
        title_label.setObjectName("mainTitle")
        title_container.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Professional Git & Docker Automation")
        subtitle_label.setObjectName("subtitle")
        title_container.addWidget(subtitle_label)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("version")
        header_layout.addWidget(version_label)
        
        parent_layout.addWidget(header_frame)
        
    def create_content_area(self, parent_layout):
        """Create main content area with tabs and console"""
        # Content container
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Create splitter for main content and console
        splitter = QSplitter(Qt.Vertical)
        splitter.setObjectName("mainSplitter")
        
        # Create tab widget
        self.create_tab_widget(splitter)
        
        # Create console
        self.create_console(splitter)
        
        # Set splitter proportions (70% for tabs, 30% for console)
        splitter.setSizes([500, 200])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        content_layout.addWidget(splitter)
        parent_layout.addWidget(content_frame)
        
    def create_tab_widget(self, parent_splitter):
        """Create professional tab widget with Git and Docker tabs"""
        # Tab container
        tab_container = QFrame()
        tab_container.setObjectName("tabContainer")
        
        tab_layout = QVBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabWidget")
        
        # Create scrollable areas for tabs
        git_scroll = QScrollArea()
        git_scroll.setWidgetResizable(True)
        git_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        git_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        git_scroll.setObjectName("gitScrollArea")
        
        docker_scroll = QScrollArea()
        docker_scroll.setWidgetResizable(True)
        docker_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        docker_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        docker_scroll.setObjectName("dockerScrollArea")
        
        # Create tabs
        self.git_tab = GitTab(self.log_panel if hasattr(self, 'log_panel') else None)
        self.docker_tab = DockerTab(self.log_panel if hasattr(self, 'log_panel') else None)
        
        # Add tabs to scroll areas
        git_scroll.setWidget(self.git_tab)
        docker_scroll.setWidget(self.docker_tab)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(git_scroll, "🔧 Git Operations")
        self.tab_widget.addTab(docker_scroll, "🐳 Docker Management")
        
        tab_layout.addWidget(self.tab_widget)
        parent_splitter.addWidget(tab_container)
        
    def create_console(self, parent_splitter):
        """Create professional console output area"""
        console_container = QFrame()
        console_container.setObjectName("consoleContainer")
        
        console_layout = QVBoxLayout(console_container)
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(0)
        
        # Console header
        console_header = QFrame()
        console_header.setFixedHeight(40)
        console_header.setObjectName("consoleHeader")
        
        header_layout = QHBoxLayout(console_header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        console_title = QLabel("📋 Output Console")
        console_title.setObjectName("consoleTitle")
        header_layout.addWidget(console_title)
        
        header_layout.addStretch()
        
        # Clear button
        clear_button = QPushButton("🗑️ Clear")
        clear_button.setObjectName("clearButton")
        clear_button.clicked.connect(self.clear_console)
        header_layout.addWidget(clear_button)
        
        console_layout.addWidget(console_header)
        
        # Console output
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setObjectName("consoleOutput")
        self.log_panel.setPlaceholderText("Ready to execute commands... 🚀")
        
        console_layout.addWidget(self.log_panel)
        
        # Update tab references
        if hasattr(self, 'git_tab'):
            self.git_tab.log_panel = self.log_panel
        if hasattr(self, 'docker_tab'):
            self.docker_tab.log_panel = self.log_panel
        
        parent_splitter.addWidget(console_container)
        
    def clear_console(self):
        """Clear the console output"""
        self.log_panel.clear()
        self.log_panel.append('<span style="color: #74c0fc;">Console cleared 🧹</span>')
        
    def apply_global_theme(self):
        """Apply professional theme to the entire application"""
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
            }
            
            /* Header */
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
                border-bottom: 3px solid #5a67d8;
            }
            
            #mainTitle {
                color: white;
                font-size: 28px;
                font-weight: 700;
                margin: 0;
                padding: 0;
            }
            
            #subtitle {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 400;
                margin: 0;
                padding: 0;
            }
            
            #version {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                font-weight: 500;
                background-color: rgba(255, 255, 255, 0.2);
                padding: 4px 12px;
                border-radius: 12px;
                margin-top: 20px;
            }
            
            /* Content Frame */
            #contentFrame {
                background-color: #f8f9fa;
                border: none;
            }
            
            /* Tab Widget */
            #mainTabWidget {
                background-color: transparent;
                border: none;
            }
            
            #mainTabWidget::pane {
                border: 2px solid #e9ecef;
                border-radius: 12px;
                background-color: white;
                margin-top: -2px;
            }
            
            #mainTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #e9ecef;
                border-bottom: none;
                padding: 12px 24px;
                margin-right: 4px;
                border-radius: 8px 8px 0 0;
                font-weight: 600;
                font-size: 14px;
                color: #495057;
                min-width: 150px;
            }
            
            QTabBar::tab:selected {
                background: white;
                border-color: #e9ecef;
                border-bottom: 2px solid white;
                color: #667eea;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #495057;
            }
            
            /* Scroll Areas */
            #gitScrollArea, #dockerScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background-color: #ced4da;
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            
            /* Console */
            #consoleContainer {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
            }
            
            #consoleHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-bottom: 1px solid #dee2e6;
                border-radius: 10px 10px 0 0;
            }
            
            #consoleTitle {
                color: #495057;
                font-size: 14px;
                font-weight: 600;
            }
            
            #clearButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            
            #clearButton:hover {
                background-color: #c82333;
            }
            
            #clearButton:pressed {
                background-color: #bd2130;
            }
            
            #consoleOutput {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                border: none;
                border-radius: 0 0 10px 10px;
                padding: 15px;
                line-height: 1.5;
            }
            
            #consoleOutput::placeholder {
                color: #6c757d;
                font-style: italic;
            }
            
            /* Splitter */
            #mainSplitter::handle {
                background-color: #dee2e6;
                height: 4px;
                border-radius: 2px;
                margin: 2px 0;
            }
            
            #mainSplitter::handle:hover {
                background-color: #667eea;
            }
            
            /* Group Boxes - Global Style */
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                color: #495057;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                margin-top: 16px;
                padding-top: 16px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 4px 12px;
                background-color: white;
                color: #495057;
                font-weight: 600;
                border-radius: 6px;
            }
            
            /* Buttons - Global Style */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
            
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
            
            /* Input Fields - Global Style */
            QLineEdit {
                padding: 14px 16px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #495057;
                font-weight: 500;
                selection-background-color: #667eea;
                selection-color: white;
            }
            
            QLineEdit:focus {
                border-color: #667eea;
                background-color: #ffffff;
                outline: none;
            }
            
            QLineEdit::placeholder {
                color: #adb5bd;
                font-style: italic;
                font-weight: 400;
            }
            
            /* ComboBox - Global Style */
            QComboBox {
                padding: 14px 16px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #495057;
                font-weight: 500;
                min-width: 200px;
            }
            
            QComboBox:focus {
                border-color: #667eea;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #495057;
                margin-right: 12px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                color: #495057;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                selection-background-color: #667eea;
                selection-color: white;
                font-size: 14px;
                padding: 4px;
            }
            
            /* Labels - Global Style */
            QLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 500;
                padding: 2px 0;
            }
            
            /* List Widget - Global Style */
            QListWidget {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
                color: #495057;
                padding: 8px;
                font-size: 13px;
                font-weight: 500;
            }
            
            QListWidget::item {
                padding: 12px;
                border-radius: 6px;
                margin: 2px 0;
                border: 1px solid transparent;
            }
            
            QListWidget::item:selected {
                background-color: #667eea;
                color: white;
                border: 1px solid #5a67d8;
            }
            
            QListWidget::item:hover {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
            }
            
            /* Spin Box - Global Style */
            QSpinBox {
                padding: 14px 16px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #495057;
                font-weight: 500;
                min-width: 100px;
            }
            
            QSpinBox:focus {
                border-color: #667eea;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                width: 24px;
                border-radius: 4px;
            }
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e9ecef;
            }
        """)
    
    def log_message(self, message, color="#d4d4d4"):
        """Add message to log panel with timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_panel.append(f'<span style="color: #6c757d;">[{timestamp}]</span> <span style="color: {color};">{message}</span>')
        
    def log_error(self, message):
        """Add error message to log panel"""
        self.log_message(f"❌ {message}", "#dc3545")
        
    def log_success(self, message):
        """Add success message to log panel"""
        self.log_message(f"✅ {message}", "#28a745")
        
    def log_info(self, message):
        """Add info message to log panel"""
        self.log_message(f"ℹ️ {message}", "#17a2b8")
        
    def log_warning(self, message):
        """Add warning message to log panel"""
        self.log_message(f"⚠️ {message}", "#ffc107")