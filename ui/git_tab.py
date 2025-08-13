"""
Professional Git Operations Tab with Clean Layout
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QComboBox, QFileDialog, QMessageBox,
    QGroupBox, QGridLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

from core.git_operations import GitOperations
from core.command_runner import CommandRunner

class GitTab(QWidget):
    """Professional Git operations tab with clean, organized layout"""
    
    def __init__(self, log_panel=None):
        super().__init__()
        self.log_panel = log_panel
        self.git_ops = GitOperations()
        self.command_runner = CommandRunner()
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the professional UI layout"""
        # Main layout with proper spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # Create sections
        self.create_clone_section(main_layout)
        self.create_commit_section(main_layout)
        self.create_branch_section(main_layout)
        
        # Add stretch to push content to top
        main_layout.addStretch()
        
    def create_clone_section(self, parent_layout):
        """Create the repository cloning section"""
        clone_group = QGroupBox("🔄 Clone Repository")
        clone_group.setObjectName("cloneGroup")
        
        # Use grid layout for better organization
        grid_layout = QGridLayout(clone_group)
        grid_layout.setContentsMargins(25, 30, 25, 25)
        grid_layout.setVerticalSpacing(15)
        grid_layout.setHorizontalSpacing(15)
        
        # Repository URL
        url_label = QLabel("Repository URL:")
        url_label.setObjectName("fieldLabel")
        grid_layout.addWidget(url_label, 0, 0, 1, 3)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://github.com/username/repository.git")
        self.url_input.setObjectName("urlInput")
        grid_layout.addWidget(self.url_input, 1, 0, 1, 3)
        
        # Destination folder
        dest_label = QLabel("Destination Folder:")
        dest_label.setObjectName("fieldLabel")
        grid_layout.addWidget(dest_label, 2, 0, 1, 3)
        
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Choose where to save the repository...")
        self.folder_input.setObjectName("folderInput")
        grid_layout.addWidget(self.folder_input, 3, 0, 1, 2)
        
        self.browse_button = QPushButton("📁 Browse")
        self.browse_button.setObjectName("secondaryButton")
        self.browse_button.setFixedWidth(120)
        self.browse_button.clicked.connect(self.browse_folder)
        grid_layout.addWidget(self.browse_button, 3, 2)
        
        # Clone button
        self.clone_button = QPushButton("🚀 Clone Repository")
        self.clone_button.setObjectName("primaryButton")
        self.clone_button.setMinimumHeight(45)
        self.clone_button.clicked.connect(self.clone_repository)
        grid_layout.addWidget(self.clone_button, 4, 0, 1, 3)
        
        parent_layout.addWidget(clone_group)
        
    def create_commit_section(self, parent_layout):
        """Create the commit and push section"""
        commit_group = QGroupBox("💾 Commit & Push Changes")
        commit_group.setObjectName("commitGroup")
        
        # Use grid layout
        grid_layout = QGridLayout(commit_group)
        grid_layout.setContentsMargins(25, 30, 25, 25)
        grid_layout.setVerticalSpacing(15)
        grid_layout.setHorizontalSpacing(15)
        
        # Repository path
        workdir_label = QLabel("Repository Path:")
        workdir_label.setObjectName("fieldLabel")
        grid_layout.addWidget(workdir_label, 0, 0, 1, 3)
        
        self.workdir_input = QLineEdit()
        self.workdir_input.setPlaceholderText("Select your git repository folder...")
        self.workdir_input.setObjectName("workdirInput")
        grid_layout.addWidget(self.workdir_input, 1, 0, 1, 2)
        
        self.browse_workdir_button = QPushButton("📁 Browse")
        self.browse_workdir_button.setObjectName("secondaryButton")
        self.browse_workdir_button.setFixedWidth(120)
        self.browse_workdir_button.clicked.connect(self.browse_workdir)
        grid_layout.addWidget(self.browse_workdir_button, 1, 2)
        
        # Commit message
        msg_label = QLabel("Commit Message:")
        msg_label.setObjectName("fieldLabel")
        grid_layout.addWidget(msg_label, 2, 0, 1, 3)
        
        self.commit_msg_input = QLineEdit()
        self.commit_msg_input.setPlaceholderText("Describe what you changed...")
        self.commit_msg_input.setObjectName("commitMsgInput")
        grid_layout.addWidget(self.commit_msg_input, 3, 0, 1, 3)
        
        # Action buttons in horizontal layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Status button
        self.status_button = QPushButton("📊 Check Status")
        self.status_button.setObjectName("secondaryButton")
        self.status_button.clicked.connect(self.check_status)
        button_layout.addWidget(self.status_button)
        
        # Commit & Push button
        self.commit_push_button = QPushButton("📤 Commit & Push")
        self.commit_push_button.setObjectName("primaryButton")
        self.commit_push_button.setMinimumHeight(45)
        self.commit_push_button.clicked.connect(self.commit_and_push)
        button_layout.addWidget(self.commit_push_button)
        
        grid_layout.addLayout(button_layout, 4, 0, 1, 3)
        
        parent_layout.addWidget(commit_group)
        
    def create_branch_section(self, parent_layout):
        """Create the branch management section"""
        branch_group = QGroupBox("🌿 Branch Management")
        branch_group.setObjectName("branchGroup")
        
        # Use grid layout
        grid_layout = QGridLayout(branch_group)
        grid_layout.setContentsMargins(25, 30, 25, 25)
        grid_layout.setVerticalSpacing(15)
        grid_layout.setHorizontalSpacing(15)
        
        # Current branch info
        current_branch_label = QLabel("Current Branch:")
        current_branch_label.setObjectName("fieldLabel")
        grid_layout.addWidget(current_branch_label, 0, 0, 1, 3)
        
        self.current_branch_display = QLabel("Not in a git repository")
        self.current_branch_display.setObjectName("currentBranchDisplay")
        grid_layout.addWidget(self.current_branch_display, 1, 0, 1, 3)
        
        # Branch selection
        branch_label = QLabel("Switch to Branch:")
        branch_label.setObjectName("fieldLabel")
        grid_layout.addWidget(branch_label, 2, 0, 1, 3)
        
        self.branch_combo = QComboBox()
        self.branch_combo.setEditable(True)
        self.branch_combo.lineEdit().setPlaceholderText("Choose or type branch name...")
        self.branch_combo.setObjectName("branchCombo")
        grid_layout.addWidget(self.branch_combo, 3, 0, 1, 2)
        
        self.refresh_branches_button = QPushButton("🔄 Refresh")
        self.refresh_branches_button.setObjectName("secondaryButton")
        self.refresh_branches_button.setFixedWidth(120)
        self.refresh_branches_button.clicked.connect(self.refresh_branches)
        grid_layout.addWidget(self.refresh_branches_button, 3, 2)
        
        # Branch action buttons
        branch_button_layout = QHBoxLayout()
        branch_button_layout.setSpacing(15)
        
        self.create_branch_button = QPushButton("➕ Create Branch")
        self.create_branch_button.setObjectName("secondaryButton")
        self.create_branch_button.clicked.connect(self.create_branch)
        branch_button_layout.addWidget(self.create_branch_button)
        
        self.switch_branch_button = QPushButton("🔀 Switch Branch")
        self.switch_branch_button.setObjectName("primaryButton")
        self.switch_branch_button.setMinimumHeight(45)
        self.switch_branch_button.clicked.connect(self.switch_branch)
        branch_button_layout.addWidget(self.switch_branch_button)
        
        grid_layout.addLayout(branch_button_layout, 4, 0, 1, 3)
        
        parent_layout.addWidget(branch_group)
        
        # Apply section-specific styling
        self.apply_section_styling()
        
    def apply_section_styling(self):
        """Apply specific styling to sections"""
        self.setStyleSheet("""
            #fieldLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 5px;
            }
            
            #currentBranchDisplay {
                background-color: #e9ecef;
                color: #495057;
                padding: 12px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                border: 2px solid #dee2e6;
            }
            
            #primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                font-size: 15px;
                font-weight: 700;
            }
            
            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1e7e34);
            }
            
            #secondaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #5a6268);
                color: white;
                font-size: 13px;
                font-weight: 600;
                min-height: 35px;
            }
            
            #secondaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #495057);
            }
        """)
        
    def browse_folder(self):
        """Browse for destination folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Destination Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.folder_input.setText(folder)
            self.log_message(f"📁 Selected destination: {folder}", "#17a2b8")
            
    def browse_workdir(self):
        """Browse for working directory"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Git Repository",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.workdir_input.setText(folder)
            self.log_message(f"📁 Selected repository: {folder}", "#17a2b8")
            self.update_current_branch()
            
    def update_current_branch(self):
        """Update the current branch display"""
        workdir = self.workdir_input.text().strip()
        if not workdir:
            self.current_branch_display.setText("No repository selected")
            return
            
        success, output, error = self.command_runner.run_command(
            ["git", "branch", "--show-current"], 
            cwd=workdir
        )
        
        if success and output.strip():
            branch_name = output.strip()
            self.current_branch_display.setText(f"🌿 {branch_name}")
            self.current_branch_display.setStyleSheet("""
                background-color: #d4edda;
                color: #155724;
                padding: 12px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                border: 2px solid #c3e6cb;
            """)
        else:
            self.current_branch_display.setText("❌ Not a git repository")
            self.current_branch_display.setStyleSheet("""
                background-color: #f8d7da;
                color: #721c24;
                padding: 12px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                border: 2px solid #f5c6cb;
            """)
            
    def check_status(self):
        """Check git status"""
        workdir = self.workdir_input.text().strip()
        if not workdir:
            QMessageBox.warning(self, "Warning", "Please select a working directory")
            return
            
        self.log_message("📊 Checking repository status...", "#17a2b8")
        
        success, output, error = self.command_runner.run_command(
            ["git", "status", "--porcelain"], 
            cwd=workdir
        )
        
        if success:
            if output.strip():
                changes = output.strip().split('\n')
                self.log_message(f"📝 Found {len(changes)} changes:", "#ffc107")
                for change in changes[:10]:  # Show first 10 changes
                    self.log_message(f"  {change}", "#6c757d")
                if len(changes) > 10:
                    self.log_message(f"  ... and {len(changes) - 10} more", "#6c757d")
            else:
                self.log_message("✨ Working directory is clean", "#28a745")
        else:
            self.log_message(f"❌ Status check failed: {error}", "#dc3545")
            
    def create_branch(self):
        """Create a new branch"""
        workdir = self.workdir_input.text().strip()
        branch_name = self.branch_combo.currentText().strip()
        
        if not workdir:
            QMessageBox.warning(self, "Warning", "Please select a working directory")
            return
            
        if not branch_name:
            QMessageBox.warning(self, "Warning", "Please enter a branch name")
            return
            
        self.log_message(f"➕ Creating branch: {branch_name}", "#17a2b8")
        
        success, output, error = self.command_runner.run_command(
            ["git", "checkout", "-b", branch_name], 
            cwd=workdir
        )
        
        if success:
            self.log_message(f"✅ Branch '{branch_name}' created and switched to", "#28a745")
            self.update_current_branch()
            self.refresh_branches()
        else:
            self.log_message(f"❌ Failed to create branch: {error}", "#dc3545")
            
    def clone_repository(self):
        """Clone a git repository with progress feedback"""
        url = self.url_input.text().strip()
        destination = self.folder_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Input Required", "Please enter a Git repository URL")
            return
            
        if not destination:
            QMessageBox.warning(self, "Input Required", "Please select a destination folder")
            return
            
        # Update UI state
        self.clone_button.setEnabled(False)
        self.clone_button.setText("🔄 Cloning...")
        
        self.log_message(f"🚀 Starting clone from: {url}", "#17a2b8")
        self.log_message(f"📁 Destination: {destination}", "#6c757d")
        
        # Run clone command
        success, output, error = self.command_runner.run_command(
            ["git", "clone", url], 
            cwd=destination
        )
        
        # Reset UI state
        self.clone_button.setEnabled(True)
        self.clone_button.setText("🚀 Clone Repository")
        
        if success:
            self.log_message("✅ Repository cloned successfully!", "#28a745")
            if output:
                self.log_message(f"Details: {output}", "#6c757d")
        else:
            self.log_message(f"❌ Clone failed: {error}", "#dc3545")
            
    def commit_and_push(self):
        """Commit changes and push to remote with detailed feedback"""
        workdir = self.workdir_input.text().strip()
        message = self.commit_msg_input.text().strip()
        
        if not workdir:
            QMessageBox.warning(self, "Input Required", "Please select a working directory")
            return
            
        if not message:
            QMessageBox.warning(self, "Input Required", "Please enter a commit message")
            return
            
        # Update UI state
        self.commit_push_button.setEnabled(False)
        self.commit_push_button.setText("📤 Working...")
        
        self.log_message("📤 Starting commit and push process...", "#17a2b8")
        
        # Step 1: Add all files
        self.log_message("1️⃣ Adding files to staging area...", "#6c757d")
        success, output, error = self.command_runner.run_command(
            ["git", "add", "."], 
            cwd=workdir
        )
        
        if not success:
            self.log_message(f"❌ Failed to add files: {error}", "#dc3545")
            self.reset_commit_button()
            return
            
        # Step 2: Commit
        self.log_message("2️⃣ Creating commit...", "#6c757d")
        success, output, error = self.command_runner.run_command(
            ["git", "commit", "-m", message], 
            cwd=workdir
        )
        
        if not success:
            if "nothing to commit" in error.lower():
                self.log_message("ℹ️ No changes to commit", "#ffc107")
            else:
                self.log_message(f"❌ Commit failed: {error}", "#dc3545")
            self.reset_commit_button()
            return
            
        # Step 3: Push
        self.log_message("3️⃣ Pushing to remote...", "#6c757d")
        success, output, error = self.command_runner.run_command(
            ["git", "push"], 
            cwd=workdir
        )
        
        if success:
            self.log_message("✅ Commit and push completed successfully!", "#28a745")
            self.commit_msg_input.clear()
        else:
            self.log_message(f"❌ Push failed: {error}", "#dc3545")
            
        self.reset_commit_button()
        
    def reset_commit_button(self):
        """Reset commit button to original state"""
        self.commit_push_button.setEnabled(True)
        self.commit_push_button.setText("📤 Commit & Push")
        
    def refresh_branches(self):
        """Refresh the list of available branches"""
        workdir = self.workdir_input.text().strip()
        
        if not workdir:
            QMessageBox.warning(self, "Warning", "Please select a working directory")
            return
            
        self.log_message("🔄 Refreshing branch list...", "#17a2b8")
        
        # Get local and remote branches
        success, output, error = self.command_runner.run_command(
            ["git", "branch", "-a"], 
            cwd=workdir
        )
        
        if success:
            branches = set()
            current_branch = ""
            
            for line in output.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith('*'):
                    current_branch = line[2:].strip()
                    branches.add(current_branch)
                elif line.startswith('remotes/origin/'):
                    branch = line.replace('remotes/origin/', '').strip()
                    if branch != 'HEAD':
                        branches.add(branch)
                elif not line.startswith('remotes/'):
                    branches.add(line)
                    
            # Update combo box
            self.branch_combo.clear()
            sorted_branches = sorted(branches)
            self.branch_combo.addItems(sorted_branches)
            
            self.log_message(f"✅ Found {len(sorted_branches)} branches", "#28a745")
            
            # Update current branch display
            self.update_current_branch()
            
        else:
            self.log_message(f"❌ Failed to get branches: {error}", "#dc3545")
            
    def switch_branch(self):
        """Switch to selected branch"""
        workdir = self.workdir_input.text().strip()
        branch = self.branch_combo.currentText().strip()
        
        if not workdir:
            QMessageBox.warning(self, "Warning", "Please select a working directory")
            return
            
        if not branch:
            QMessageBox.warning(self, "Warning", "Please select or enter a branch name")
            return
            
        # Update UI state
        self.switch_branch_button.setEnabled(False)
        self.switch_branch_button.setText("🔀 Switching...")
        
        self.log_message(f"🔀 Switching to branch: {branch}", "#17a2b8")
        
        # Switch branch
        success, output, error = self.command_runner.run_command(
            ["git", "checkout", branch], 
            cwd=workdir
        )
        
        # Reset UI state
        self.switch_branch_button.setEnabled(True)
        self.switch_branch_button.setText("🔀 Switch Branch")
        
        if success:
            self.log_message(f"✅ Switched to branch: {branch}", "#28a745")
            self.update_current_branch()
        else:
            self.log_message(f"❌ Branch switch failed: {error}", "#dc3545")
            
    def log_message(self, message, color="#6c757d"):
        """Log message to console if available"""
        if self.log_panel:
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.log_panel.append(f'<span style="color: #6c757d;">[{timestamp}]</span> <span style="color: {color};">{message}</span>')