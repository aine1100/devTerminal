"""
Git operations wrapper
"""

from .command_runner import CommandRunner

class GitOperations:
    """Git operations handler"""
    
    def __init__(self):
        self.runner = CommandRunner()
        
    def is_git_available(self):
        """Check if git is available in system PATH"""
        return self.runner.check_command_available('git')
        
    def clone_repository(self, url, destination):
        """
        Clone a git repository
        
        Args:
            url (str): Git repository URL
            destination (str): Destination directory
            
        Returns:
            tuple: (success: bool, output: str, error: str)
        """
        return self.runner.run_command(['git', 'clone', url], cwd=destination)
        
    def add_all(self, repo_path):
        """Add all changes to staging"""
        return self.runner.run_command(['git', 'add', '.'], cwd=repo_path)
        
    def commit(self, repo_path, message):
        """Commit changes with message"""
        return self.runner.run_command(['git', 'commit', '-m', message], cwd=repo_path)
        
    def push(self, repo_path, remote='origin', branch=None):
        """Push changes to remote"""
        cmd = ['git', 'push']
        if remote:
            cmd.append(remote)
        if branch:
            cmd.append(branch)
        return self.runner.run_command(cmd, cwd=repo_path)
        
    def get_branches(self, repo_path, include_remote=True):
        """Get list of branches"""
        cmd = ['git', 'branch']
        if include_remote:
            cmd.append('-a')
        return self.runner.run_command(cmd, cwd=repo_path)
        
    def checkout_branch(self, repo_path, branch):
        """Switch to a branch"""
        return self.runner.run_command(['git', 'checkout', branch], cwd=repo_path)
        
    def get_status(self, repo_path):
        """Get git status"""
        return self.runner.run_command(['git', 'status', '--porcelain'], cwd=repo_path)
        
    def get_current_branch(self, repo_path):
        """Get current branch name"""
        return self.runner.run_command(['git', 'branch', '--show-current'], cwd=repo_path)