from doctest import FAIL_FAST
import os

class Agent:
    def __init__(self) -> None:
        self.userInfo = ""
        pass

    def _ProcessCMD(self, cmd):
        return os.system(cmd)

    def SetUser(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.userInfo = ""
        if self.username != None:
            self.userInfo += " --username " + self.username

        if self.pwd != None:
            self.userInfo += " --password " + self.pwd

    def Update(self, path):
        self._ProcessCMD("svn update " + path + self.userInfo)

    def Commit(self, path, commit):
        self._ProcessCMD('''svn commit -m "''' + commit + '''" "''' + path + '''" ''' + self.userInfo)
    
    def Revert(self, path, bRecursion=True):
        paramStr = " "
        if bRecursion:
            paramStr = " -R "
        self._ProcessCMD('''svn revert"''' + paramStr + path + '''" ''' + self.userInfo)

    def CleanUp(self, path, bRemoveIgnore=False, bRemoveUnversion=False, bVacuumPristines=False):
        paramStr = " "
        if bRemoveIgnore:
            paramStr += "--remove-ignored "
        if bRemoveUnversion:
            paramStr += "--remove-unversioned "
        if bVacuumPristines:
            paramStr += "--vacuum-pristines "
        self._ProcessCMD("svn cleanup " + paramStr + path)

        
