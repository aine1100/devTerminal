"""
Professional Docker Management Tab with Clean Layout
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QComboBox, QFileDialog, QMessageBox,
    QGroupBox, QListWidget, QSpinBox, QGridLayout, QFrame,
    QSizePolicy, QTextEdit
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

from core.docker_operations import DockerOperations
from core.command_runner import CommandRunner

class DockerTab(QWidget):
    """Professional Docker management tab with clean, organized layout"""
    
    def __init__(self, log_panel=None):
        super().__init__()
        self.log_panel = log_panel
        self.docker_ops = DockerOperations()
        self.command_runner = CommandRunner()
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the professional UI layout"""
        # Main layout with proper spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # Create sections
        self.create_build_section(main_layout)
        self.create_run_section(main_layout)
        self.create_management_section(main_layout)
        
        # Add stretch to push content to top
        main_layout.addStretch()
        
        # Load initial data
        self.refresh_containers()
        
    def create_build_section(self, parent_layout):
        """Create the image building section"""
        build_group = QGroupBox("🏗️ Build Docker Image")
        build_group.setObjectName("buildGroup")
        
        # Use grid layout for better organization
        grid_layout = QGridLayout(build_group)
        grid_layout.setContentsMargins(25, 30, 25, 25)
        grid_layout.setVerticalSpacing(15)
        grid_layout.setHorizontalSpacing(15)
        
        # Image name and tag
        name_label = QLabel("Image Name & Tag:")
        name_label.setObjectName("fieldLabel")
        grid_layout.addWidget(name_label, 0, 0, 1, 3)
        
        self.image_name_input = QLineEdit()
        self.image_name_input.setPlaceholderText("my-app:latest")
        self.image_name_input.setObjectName("imageNameInput")
        grid_layout.addWidget(self.image_name_input, 1, 0, 1, 3)
        
        # Dockerfile location
        dockerfile_label = QLabel("Dockerfile Location:")
        dockerfile_label.setObjectName("fieldLabel")
        grid_layout.addWidget(dockerfile_label, 2, 0, 1, 3)
        
        self.dockerfile_input = QLineEdit()
        self.dockerfile_input.setPlaceholderText("Select Dockerfile or project directory...")
        self.dockerfile_input.setObjectName("dockerfileInput")
        grid_layout.addWidget(self.dockerfile_input, 3, 0, 1, 2)
        
        self.browse_dockerfile_button = QPushButton("📁 Browse")
        self.browse_dockerfile_button.setObjectName("secondaryButton")
        self.browse_dockerfile_button.setFixedWidth(120)
        self.browse_dockerfile_button.clicked.connect(self.browse_dockerfile)
        grid_layout.addWidget(self.browse_dockerfile_button, 3, 2)
        
        # Build options
        options_label = QLabel("Build Options (Optional):")
        options_label.setObjectName("fieldLabel")
        grid_layout.addWidget(options_label, 4, 0, 1, 3)
        
        self.build_options_input = QLineEdit()
        self.build_options_input.setPlaceholderText("--no-cache --build-arg ENV=production")
        self.build_options_input.setObjectName("buildOptionsInput")
        grid_layout.addWidget(self.build_options_input, 5, 0, 1, 3)
        
        # Build button
        self.build_button = QPushButton("🔨 Build Image")
        self.build_button.setObjectName("primaryButton")
        self.build_button.setMinimumHeight(45)
        self.build_button.clicked.connect(self.build_image)
        grid_layout.addWidget(self.build_button, 6, 0, 1, 3)
        
        parent_layout.addWidget(build_group)
        
    def create_run_section(self, parent_layout):
        """Create the container running section"""
        run_group = QGroupBox("🚀 Run Container")
        run_group.setObjectName("runGroup")
        
        # Use grid layout
        grid_layout = QGridLayout(run_group)
        grid_layout.setContentsMargins(25, 30, 25, 25)
        grid_layout.setVerticalSpacing(15)
        grid_layout.setHorizontalSpacing(15)
        
        # Image selection
        image_label = QLabel("Docker Image:")
        image_label.setObjectName("fieldLabel")
        grid_layout.addWidget(image_label, 0, 0, 1, 3)
        
        image_layout = QHBoxLayout()
        image_layout.setSpacing(10)
        
        self.run_image_input = QLineEdit()
        self.run_image_input.setPlaceholderText("nginx:latest or my-app:v1.0")
        self.run_image_input.setObjectName("runImageInput")
        image_layout.addWidget(self.run_image_input)
        
        self.refresh_images_button = QPushButton("🔄 Refresh")
        self.refresh_images_button.setObjectName("secondaryButton")
        self.refresh_images_button.setFixedWidth(120)
        self.refresh_images_button.clicked.connect(self.refresh_images)
        image_layout.addWidget(self.refresh_images_button)
        
        grid_layout.addLayout(image_layout, 1, 0, 1, 3)
        
        # Port mapping section
        port_label = QLabel("Port Mapping:")
        port_label.setObjectName("fieldLabel")
        grid_layout.addWidget(port_label, 2, 0, 1, 3)
        
        # Port mapping layout
        port_frame = QFrame()
        port_frame.setObjectName("portFrame")
        port_layout = QHBoxLayout(port_frame)
        port_layout.setContentsMargins(15, 15, 15, 15)
        port_layout.setSpacing(20)
        
        # Host port
        host_port_layout = QVBoxLayout()
        host_port_label = QLabel("Host Port")
        host_port_label.setObjectName("portLabel")
        host_port_layout.addWidget(host_port_label)
        
        self.host_port_input = QSpinBox()
        self.host_port_input.setRange(1, 65535)
        self.host_port_input.setValue(8080)
        self.host_port_input.setObjectName("hostPortInput")
        host_port_layout.addWidget(self.host_port_input)
        port_layout.addLayout(host_port_layout)
        
        # Arrow
        arrow_label = QLabel("→")
        arrow_label.setObjectName("arrowLabel")
        port_layout.addWidget(arrow_label)
        
        # Container port
        container_port_layout = QVBoxLayout()
        container_port_label = QLabel("Container Port")
        container_port_label.setObjectName("portLabel")
        container_port_layout.addWidget(container_port_label)
        
        self.container_port_input = QSpinBox()
        self.container_port_input.setRange(1, 65535)
        self.container_port_input.setValue(80)
        self.container_port_input.setObjectName("containerPortInput")
        container_port_layout.addWidget(self.container_port_input)
        port_layout.addLayout(container_port_layout)
        
        port_layout.addStretch()
        grid_layout.addWidget(port_frame, 3, 0, 1, 3)
        
        # Container name
        name_label = QLabel("Container Name (Optional):")
        name_label.setObjectName("fieldLabel")
        grid_layout.addWidget(name_label, 4, 0, 1, 3)
        
        self.container_name_input = QLineEdit()
        self.container_name_input.setPlaceholderText("my-container")
        self.container_name_input.setObjectName("containerNameInput")
        grid_layout.addWidget(self.container_name_input, 5, 0, 1, 3)
        
        # Additional options
        run_options_label = QLabel("Additional Options:")
        run_options_label.setObjectName("fieldLabel")
        grid_layout.addWidget(run_options_label, 6, 0, 1, 3)
        
        self.run_options_input = QLineEdit()
        self.run_options_input.setPlaceholderText("-e ENV_VAR=value --restart unless-stopped")
        self.run_options_input.setObjectName("runOptionsInput")
        grid_layout.addWidget(self.run_options_input, 7, 0, 1, 3)
        
        # Run button
        self.run_button = QPushButton("🚀 Run Container")
        self.run_button.setObjectName("primaryButton")
        self.run_button.setMinimumHeight(45)
        self.run_button.clicked.connect(self.run_container)
        grid_layout.addWidget(self.run_button, 8, 0, 1, 3)
        
        parent_layout.addWidget(run_group)
        
    def create_management_section(self, parent_layout):
        """Create the container management section"""
        manage_group = QGroupBox("📦 Container Management")
        manage_group.setObjectName("manageGroup")
        
        # Use grid layout
        grid_layout = QGridLayout(manage_group)
        grid_layout.setContentsMargins(25, 30, 25, 25)
        grid_layout.setVerticalSpacing(15)
        grid_layout.setHorizontalSpacing(15)
        
        # Container list header
        list_header_layout = QHBoxLayout()
        
        containers_label = QLabel("Active Containers:")
        containers_label.setObjectName("fieldLabel")
        list_header_layout.addWidget(containers_label)
        
        list_header_layout.addStretch()
        
        self.refresh_containers_button = QPushButton("🔄 Refresh")
        self.refresh_containers_button.setObjectName("secondaryButton")
        self.refresh_containers_button.setFixedWidth(120)
        self.refresh_containers_button.clicked.connect(self.refresh_containers)
        list_header_layout.addWidget(self.refresh_containers_button)
        
        grid_layout.addLayout(list_header_layout, 0, 0, 1, 3)
        
        # Container list
        self.container_list = QListWidget()
        self.container_list.setObjectName("containerList")
        self.container_list.setMinimumHeight(150)
        grid_layout.addWidget(self.container_list, 1, 0, 1, 3)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.stop_button = QPushButton("⏹️ Stop")
        self.stop_button.setObjectName("warningButton")
        self.stop_button.clicked.connect(self.stop_container)
        action_layout.addWidget(self.stop_button)
        
        self.restart_button = QPushButton("🔄 Restart")
        self.restart_button.setObjectName("secondaryButton")
        self.restart_button.clicked.connect(self.restart_container)
        action_layout.addWidget(self.restart_button)
        
        self.logs_button = QPushButton("📋 View Logs")
        self.logs_button.setObjectName("infoButton")
        self.logs_button.clicked.connect(self.view_logs)
        action_layout.addWidget(self.logs_button)
        
        self.remove_button = QPushButton("🗑️ Remove")
        self.remove_button.setObjectName("dangerButton")
        self.remove_button.clicked.connect(self.remove_container)
        action_layout.addWidget(self.remove_button)
        
        grid_layout.addLayout(action_layout, 2, 0, 1, 3)
        
        parent_layout.addWidget(manage_group)
        
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
            
            #portFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 8px;
            }
            
            #portLabel {
                color: #6c757d;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
            }
            
            #arrowLabel {
                color: #667eea;
                font-size: 24px;
                font-weight: bold;
                margin: 0 15px;
            }
            
            #primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                font-size: 15px;
                font-weight: 700;
            }
            
            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004085);
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
            
            #warningButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffc107, stop:1 #e0a800);
                color: #212529;
                font-weight: 600;
            }
            
            #warningButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0a800, stop:1 #d39e00);
            }
            
            #dangerButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                font-weight: 600;
            }
            
            #dangerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
            
            #infoButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                font-weight: 600;
            }
            
            #infoButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #117a8b);
            }
            
            #containerList {
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        
    def browse_dockerfile(self):
        """Browse for Dockerfile or directory"""
        # Try to select a Dockerfile first
        dockerfile_path = QFileDialog.getOpenFileName(
            self,
            "Select Dockerfile",
            "",
            "Dockerfile (Dockerfile);;All Files (*)"
        )[0]
        
        if dockerfile_path:
            self.dockerfile_input.setText(dockerfile_path)
            self.log_message(f"📄 Selected Dockerfile: {dockerfile_path}", "#17a2b8")
        else:
            # If no file selected, try directory
            directory_path = QFileDialog.getExistingDirectory(
                self,
                "Select Directory with Dockerfile"
            )
            if directory_path:
                self.dockerfile_input.setText(directory_path)
                self.log_message(f"📁 Selected directory: {directory_path}", "#17a2b8")
                
    def build_image(self):
        """Build Docker image with detailed progress"""
        image_name = self.image_name_input.text().strip()
        dockerfile_path = self.dockerfile_input.text().strip()
        build_options = self.build_options_input.text().strip()
        
        if not image_name:
            QMessageBox.warning(self, "Input Required", "Please enter an image name")
            return
            
        if not dockerfile_path:
            QMessageBox.warning(self, "Input Required", "Please select Dockerfile path")
            return
            
        # Update UI state
        self.build_button.setEnabled(False)
        self.build_button.setText("🔨 Building...")
        
        self.log_message(f"🏗️ Starting build for image: {image_name}", "#17a2b8")
        self.log_message(f"📄 Using Dockerfile: {dockerfile_path}", "#6c757d")
        
        # Build command
        cmd = ["docker", "build", "-t", image_name]
        
        # Add build options if provided
        if build_options:
            cmd.extend(build_options.split())
            self.log_message(f"⚙️ Build options: {build_options}", "#6c757d")
            
        cmd.append(dockerfile_path)
        
        # Run build command
        success, output, error = self.command_runner.run_command(cmd, timeout=600)
        
        # Reset UI state
        self.build_button.setEnabled(True)
        self.build_button.setText("🔨 Build Image")
        
        if success:
            self.log_message("✅ Image built successfully!", "#28a745")
            if output:
                # Show last few lines of build output
                lines = output.strip().split('\n')
                for line in lines[-5:]:
                    if line.strip():
                        self.log_message(f"  {line}", "#6c757d")
        else:
            self.log_message(f"❌ Build failed: {error}", "#dc3545")
            
    def refresh_images(self):
        """Refresh available Docker images"""
        self.log_message("🔄 Refreshing Docker images...", "#17a2b8")
        
        success, output, error = self.command_runner.run_command(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"]
        )
        
        if success:
            images = [line.strip() for line in output.split('\n') if line.strip() and line.strip() != "<none>:<none>"]
            if images:
                # Update the input with first image as suggestion
                self.run_image_input.setText(images[0])
                self.log_message(f"✅ Found {len(images)} images", "#28a745")
                # Show first few images
                for img in images[:5]:
                    self.log_message(f"  📦 {img}", "#6c757d")
                if len(images) > 5:
                    self.log_message(f"  ... and {len(images) - 5} more", "#6c757d")
            else:
                self.log_message("⚠️ No images found", "#ffc107")
        else:
            self.log_message(f"❌ Failed to get images: {error}", "#dc3545")
            
    def run_container(self):
        """Run Docker container with comprehensive options"""
        image = self.run_image_input.text().strip()
        host_port = self.host_port_input.value()
        container_port = self.container_port_input.value()
        container_name = self.container_name_input.text().strip()
        options = self.run_options_input.text().strip()
        
        if not image:
            QMessageBox.warning(self, "Input Required", "Please enter an image name")
            return
            
        # Update UI state
        self.run_button.setEnabled(False)
        self.run_button.setText("🚀 Starting...")
        
        self.log_message(f"🚀 Starting container from image: {image}", "#17a2b8")
        self.log_message(f"🔌 Port mapping: {host_port} → {container_port}", "#6c757d")
        
        # Build run command
        cmd = ["docker", "run", "-d", "-p", f"{host_port}:{container_port}"]
        
        # Add container name if provided
        if container_name:
            cmd.extend(["--name", container_name])
            self.log_message(f"🏷️ Container name: {container_name}", "#6c757d")
            
        # Add additional options if provided
        if options:
            cmd.extend(options.split())
            self.log_message(f"⚙️ Additional options: {options}", "#6c757d")
            
        cmd.append(image)
        
        # Run command
        success, output, error = self.command_runner.run_command(cmd)
        
        # Reset UI state
        self.run_button.setEnabled(True)
        self.run_button.setText("🚀 Run Container")
        
        if success:
            container_id = output.strip()[:12]
            self.log_message(f"✅ Container started successfully!", "#28a745")
            self.log_message(f"🆔 Container ID: {container_id}", "#6c757d")
            self.log_message(f"🌐 Access at: http://localhost:{host_port}", "#17a2b8")
            self.refresh_containers()
        else:
            self.log_message(f"❌ Failed to run container: {error}", "#dc3545")
            
    def refresh_containers(self):
        """Refresh running containers list"""
        success, output, error = self.command_runner.run_command([
            "docker", "ps", 
            "--format", "{{.ID}} | {{.Image}} | {{.Status}} | {{.Names}} | {{.Ports}}"
        ])
        
        self.container_list.clear()
        
        if success:
            containers = [line.strip() for line in output.split('\n') if line.strip()]
            for container in containers:
                self.container_list.addItem(container)
                
            if not containers:
                self.container_list.addItem("No running containers")
                
            self.log_message(f"📦 Found {len(containers)} running containers", "#17a2b8")
        else:
            self.container_list.addItem(f"Error: {error}")
            self.log_message(f"❌ Failed to list containers: {error}", "#dc3545")
            
    def stop_container(self):
        """Stop selected container"""
        current_item = self.container_list.currentItem()
        if not current_item or current_item.text() in ["No running containers", ""] or current_item.text().startswith("Error:"):
            QMessageBox.warning(self, "Selection Required", "Please select a container to stop")
            return
            
        container_info = current_item.text()
        container_id = container_info.split(' | ')[0]
        
        self.log_message(f"⏹️ Stopping container: {container_id}", "#ffc107")
        
        success, output, error = self.command_runner.run_command(["docker", "stop", container_id])
        
        if success:
            self.log_message(f"✅ Container stopped: {container_id}", "#28a745")
            self.refresh_containers()
        else:
            self.log_message(f"❌ Failed to stop container: {error}", "#dc3545")
            
    def restart_container(self):
        """Restart selected container"""
        current_item = self.container_list.currentItem()
        if not current_item or current_item.text() in ["No running containers", ""] or current_item.text().startswith("Error:"):
            QMessageBox.warning(self, "Selection Required", "Please select a container to restart")
            return
            
        container_info = current_item.text()
        container_id = container_info.split(' | ')[0]
        
        self.log_message(f"🔄 Restarting container: {container_id}", "#17a2b8")
        
        success, output, error = self.command_runner.run_command(["docker", "restart", container_id])
        
        if success:
            self.log_message(f"✅ Container restarted: {container_id}", "#28a745")
            self.refresh_containers()
        else:
            self.log_message(f"❌ Failed to restart container: {error}", "#dc3545")
            
    def remove_container(self):
        """Remove selected container"""
        current_item = self.container_list.currentItem()
        if not current_item or current_item.text() in ["No running containers", ""] or current_item.text().startswith("Error:"):
            QMessageBox.warning(self, "Selection Required", "Please select a container to remove")
            return
            
        container_info = current_item.text()
        container_id = container_info.split(' | ')[0]
        
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove container {container_id}?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.log_message(f"🗑️ Removing container: {container_id}", "#dc3545")
            
            # Stop first, then remove
            self.command_runner.run_command(["docker", "stop", container_id])
            success, output, error = self.command_runner.run_command(["docker", "rm", container_id])
            
            if success:
                self.log_message(f"✅ Container removed: {container_id}", "#28a745")
                self.refresh_containers()
            else:
                self.log_message(f"❌ Failed to remove container: {error}", "#dc3545")
                
    def view_logs(self):
        """View logs for selected container"""
        current_item = self.container_list.currentItem()
        if not current_item or current_item.text() in ["No running containers", ""] or current_item.text().startswith("Error:"):
            QMessageBox.warning(self, "Selection Required", "Please select a container to view logs")
            return
            
        container_info = current_item.text()
        container_id = container_info.split(' | ')[0]
        
        self.log_message(f"📋 Fetching logs for container: {container_id}", "#17a2b8")
        
        success, output, error = self.command_runner.run_command([
            "docker", "logs", "--tail", "50", container_id
        ])
        
        if success:
            self.log_message("--- Container Logs (Last 50 lines) ---", "#6c757d")
            if output.strip():
                for line in output.strip().split('\n'):
                    self.log_message(f"  {line}", "#6c757d")
            else:
                self.log_message("  (No logs available)", "#6c757d")
            self.log_message("--- End of Logs ---", "#6c757d")
        else:
            self.log_message(f"❌ Failed to get logs: {error}", "#dc3545")
            
    def log_message(self, message, color="#6c757d"):
        """Log message to console if available"""
        if self.log_panel:
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.log_panel.append(f'<span style="color: #6c757d;">[{timestamp}]</span> <span style="color: {color};">{message}</span>')