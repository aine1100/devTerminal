"""
Command runner utility for executing shell commands
"""

import subprocess
import sys
from pathlib import Path

class CommandRunner:
    """Utility class for running shell commands safely"""
    
    def __init__(self):
        self.encoding = 'utf-8'
        
    def run_command(self, cmd, cwd=None, timeout=300):
        """
        Run a shell command and return success status, output, and error
        
        Args:
            cmd (list): Command and arguments as list
            cwd (str): Working directory for command
            timeout (int): Timeout in seconds
            
        Returns:
            tuple: (success: bool, output: str, error: str)
        """
        try:
            # Ensure cwd exists if provided
            if cwd and not Path(cwd).exists():
                return False, "", f"Directory does not exist: {cwd}"
                
            # Run the command
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding=self.encoding,
                timeout=timeout,
                shell=sys.platform.startswith('win')  # Use shell on Windows
            )
            
            # Return results
            success = result.returncode == 0
            output = result.stdout.strip() if result.stdout else ""
            error = result.stderr.strip() if result.stderr else ""
            
            return success, output, error
            
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout} seconds"
            
        except FileNotFoundError:
            cmd_name = cmd[0] if cmd else "unknown"
            return False, "", f"Command not found: {cmd_name}. Make sure it's installed and in PATH."
            
        except Exception as e:
            return False, "", f"Unexpected error: {str(e)}"
            
    def check_command_available(self, command):
        """
        Check if a command is available in the system PATH
        
        Args:
            command (str): Command to check
            
        Returns:
            bool: True if command is available
        """
        try:
            if sys.platform.startswith('win'):
                # Windows
                result = subprocess.run(
                    ['where', command],
                    capture_output=True,
                    shell=True
                )
            else:
                # Unix-like systems
                result = subprocess.run(
                    ['which', command],
                    capture_output=True
                )
                
            return result.returncode == 0
            
        except Exception:
            return False