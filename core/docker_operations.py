"""
Docker operations wrapper
"""

from .command_runner import CommandRunner

class DockerOperations:
    """Docker operations handler"""
    
    def __init__(self):
        self.runner = CommandRunner()
        
    def is_docker_available(self):
        """Check if docker is available in system PATH"""
        return self.runner.check_command_available('docker')
        
    def build_image(self, image_name, dockerfile_path, build_args=None):
        """
        Build a Docker image
        
        Args:
            image_name (str): Name and tag for the image
            dockerfile_path (str): Path to Dockerfile or build context
            build_args (dict): Build arguments
            
        Returns:
            tuple: (success: bool, output: str, error: str)
        """
        cmd = ['docker', 'build', '-t', image_name]
        
        if build_args:
            for key, value in build_args.items():
                cmd.extend(['--build-arg', f'{key}={value}'])
                
        cmd.append(dockerfile_path)
        
        return self.runner.run_command(cmd, timeout=600)  # 10 minute timeout for builds
        
    def run_container(self, image, ports=None, environment=None, name=None, detached=True):
        """
        Run a Docker container
        
        Args:
            image (str): Image name to run
            ports (dict): Port mappings {host_port: container_port}
            environment (dict): Environment variables
            name (str): Container name
            detached (bool): Run in detached mode
            
        Returns:
            tuple: (success: bool, output: str, error: str)
        """
        cmd = ['docker', 'run']
        
        if detached:
            cmd.append('-d')
            
        if ports:
            for host_port, container_port in ports.items():
                cmd.extend(['-p', f'{host_port}:{container_port}'])
                
        if environment:
            for key, value in environment.items():
                cmd.extend(['-e', f'{key}={value}'])
                
        if name:
            cmd.extend(['--name', name])
            
        cmd.append(image)
        
        return self.runner.run_command(cmd)
        
    def list_containers(self, all_containers=False):
        """List Docker containers"""
        cmd = ['docker', 'ps']
        if all_containers:
            cmd.append('-a')
        cmd.extend(['--format', '{{.ID}}|{{.Image}}|{{.Status}}|{{.Names}}|{{.Ports}}'])
        
        return self.runner.run_command(cmd)
        
    def stop_container(self, container_id):
        """Stop a running container"""
        return self.runner.run_command(['docker', 'stop', container_id])
        
    def remove_container(self, container_id, force=False):
        """Remove a container"""
        cmd = ['docker', 'rm']
        if force:
            cmd.append('-f')
        cmd.append(container_id)
        
        return self.runner.run_command(cmd)
        
    def get_container_logs(self, container_id, tail=None):
        """Get container logs"""
        cmd = ['docker', 'logs']
        if tail:
            cmd.extend(['--tail', str(tail)])
        cmd.append(container_id)
        
        return self.runner.run_command(cmd)
        
    def list_images(self):
        """List Docker images"""
        return self.runner.run_command([
            'docker', 'images', 
            '--format', '{{.Repository}}:{{.Tag}}|{{.ID}}|{{.Size}}'
        ])
        
    def remove_image(self, image_id, force=False):
        """Remove a Docker image"""
        cmd = ['docker', 'rmi']
        if force:
            cmd.append('-f')
        cmd.append(image_id)
        
        return self.runner.run_command(cmd)
        
    def get_docker_info(self):
        """Get Docker system information"""
        return self.runner.run_command(['docker', 'info'])