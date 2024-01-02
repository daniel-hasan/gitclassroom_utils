'''
Created on 16 de ago de 2018

@author: profhasan
'''
import os
import re
from requests.exceptions import InvalidURL
import shutil
import tempfile
import time
import uuid

from git.repo.base import Repo


class Git(object):
    '''
    classdocs
    '''


    def __init__(self, urlGithub,localPath = None):
        '''
        Constructor
        '''
        if(urlGithub.startswith("http://") or urlGithub.startswith("https://")):
            urlGithub = urlGithub.replace("http://","")
            urlGithub = urlGithub.replace("https://","")
        strGitCom = urlGithub if urlGithub.find("github.io") < 0 else  Git.toGitHubCom(urlGithub)
        self.localPath = localPath
        
        dictGitProps = Git.git_props_from_gitcom(strGitCom)
        self.url = "github.com/"+dictGitProps["user"]+"/"+dictGitProps["repo"]
        self.path = dictGitProps["path"]
        self.remote = None

        

    @staticmethod
    def git_props_from_url(strUrlRegExp,strURLGithub):
        match = re.search(strUrlRegExp, strURLGithub)
        if(match and len(match.groups())>=2):
            user = match.group(1)
            repo = match.group(2)
            if(repo.endswith(".git")):
                repo = repo[:len(repo)-4]
                
            path = match.group(3) if len(match.groups())>2 else ""
            return {"user":user,"repo":repo,"path":path}
        
        return None
    
    @staticmethod
    def git_props_from_gitcom(strURLGithubCom):
        return Git.git_props_from_url("github\\.com/([-_.a-zA-Z0-9]+)/([-_.a-zA-Z0-9]+)(/[-/._a-zA-Z0-9]*)?",strURLGithubCom)
    
    @staticmethod
    def git_props_from_gitpagesurl(strURLGithubPages):
        return Git.git_props_from_url("([-_.a-zA-Z0-9]+)\\.github\\.io/([-_.a-zA-Z0-9]+)(/[-/._a-zA-Z0-9]*)?",strURLGithubPages)    
    
    @staticmethod
    def toGitHubPages(strURLGithubCom):
        dictProps = Git.git_props_from_gitcom(strURLGithubCom)
        if(dictProps):
            strPath = dictProps["path"] if dictProps["path"] != None else ""
            return dictProps["user"]+".github.io/"+dictProps["repo"]+strPath
        
        raise InvalidURL()
    
    @staticmethod
    def toGitHubCom(strURLGithubPages):
        dictProps = Git.git_props_from_gitpagesurl(strURLGithubPages)
        if(dictProps):
            strPath = dictProps["path"] if dictProps["path"] != None else ""
            return "github.com/"+dictProps["user"]+"/"+dictProps["repo"]+strPath
        
        raise InvalidURL()
    def clone(self,strTargetPath):
        #url = self.url+".git" if not self.url.endswith(".git") else self.url
        
        Repo.clone_from("https://"+self.url+".git", strTargetPath)
        self.localPath = strTargetPath
        
    def set_tmp_local_path(self):
        self.localPath = tempfile.gettempdir()+"/"+str(uuid.uuid1())
        self.clone(self.localPath)
    
    @property
    def last_commit_date(self):
        if(self.localPath == None):
            self.set_tmp_local_path()
        if(self.remote == None):
            repo = git.Repo(self.localPath)
            self.remote = git.remote.Remote(repo,"origin")
        
        info = self.remote.fetch()[0]
        return time.localtime(info.commit.committed_date)
    
    @property 
    def url_git_pages(self):
        return Git.toGitHubPages(self.url)
    
    
    def preproc_file_server(self,strPath):
        
        return strPath[len(self.localPath):]
    
    @property 
    def url_git_pages_complete_path(self):
        if(self.path != "" and self.path != None):
            return self.url_git_pages+self.path
        
        arrFilesToFind = ["index.php","default.php","index.html"]
        #tenta index.php ou default.php
        for strFileToFind in arrFilesToFind:
            strFile = self.find_file_in_repo(strFileToFind)
            if(strFile):
                return self.url_git_pages+self.preproc_file_server(strFile)
            
        #tenta extensoes
        arrExtsToFind = [".php",".html"]
        for strExtToFind in arrExtsToFind:
            strFile = self.find_ext_file_in_repo(strExtToFind)
            if(strFile):
                return self.url_git_pages+self.preproc_file_server(strFile)
        return self.url_git_pages
    def find_file_in_repo(self,strFile):
        if(self.localPath == None):
            self.set_tmp_local_path()
            
        for root, dirs, files in os.walk(self.localPath):
            for arq in files:
                if(arq == strFile):
                    return os.path.join(root, arq)
        return None
    def find_ext_file_in_repo(self,strExt):
        if(self.localPath == None):
            self.set_tmp_local_path()
            
        for root, dirs, files in os.walk(self.localPath):
            for arq in files:
                if(arq.endswith(strExt)):
                    return os.path.join(root, arq)
        return None

    
    def deleteLocalPath(self):
        if(self.localPath==None or self.localPath == "/" or self.localPath == "/home"
           or self.localPath == "/home/hasan" or self.localPath == "/home/profhasan"):
            return
        shutil.rmtree(self.localPath)
        self.localPath = None