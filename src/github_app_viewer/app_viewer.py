from .git_utils import Git

import psutil
import subprocess
import os

class AppViewer:
    def __init__(self, github:Git):
        self.github = github
        self.server_process = None
        self.last_host_url = None
        self.next_port = 9000
    def download_app(self):
        self.github.set_tmp_local_path()

    def execute_app(self):
        django_manage_file = self.github.find_file_in_repo("manage.py")
        if django_manage_file:
            return self.execute_django(django_manage_file)

        notebook_file = self.github.find_ext_file_in_repo(".ipynb")
        if notebook_file:
            return self.to_github_url(notebook_file)

        html_file = self.github.find_ext_file_in_repo(".html")
        if html_file:
            return self.to_local_browse(html_file)
        
        return "https://"+self.github.url
    
    def to_local_browse(self, file):
        return f"file://{file}"

    def to_github_url(self, path):
        gitub_path = path.replace(self.github.localPath, "") 
        return "https://"+self.github.url+"/blob/master/"+gitub_path


    def execute_django(self, manage_file):
        manage_dir_path = "/".join(manage_file.split("/")[:-1])
        os.chdir(manage_dir_path)

        host = f"127.0.0.1:{self.next_port}"
        self.server_process = subprocess.Popen(["python3", manage_file, "runserver", host], shell=False)
        self.last_host_url = f"http://{host}"
        self.next_port += 1
        return self.last_host_url

    def kill_server(self):
        if self.server_process:
            proc_pid = self.server_process.pid
            process = psutil.Process(proc_pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()

            self.server_process = None
        