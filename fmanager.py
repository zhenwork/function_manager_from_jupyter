import imp
import json
import inspect
import os,sys
import linecache 

class FunMan:
    def __init__(self,fkeep="./temp.py",fback="./backup.json"):
        self.backups = {}
        self.nextid = -1
        self.fkeep = fkeep
        self.fback = fback
        
        if os.path.isfile(self.fkeep):
            print ("!! keeping file exists ... ")
        else:
            open(self.fkeep,"w")
        if os.path.isfile(self.fback):
            print ("!! backup file exists ... ")
            self.backups = json.load(open(self.fback,"r"))
            if len(self.backups) > 0:
                self.nextid = int(max(self.backups))
        else:
            json.dump(self.backups, open(self.fback, 'w'))
    def clean(self):
        if os.path.isfile(self.fkeep+"c"):
            os.remove(self.fkeep+"c")
    def backup(self,comments="# updated"):
        self.nextid += 1
        #self.backup = json.load(open(self.fback,"r"))
        with open(self.fkeep,"r") as f:
            wholeList = f.readlines()
        wholeList.insert(0,"##"+comments+"\n\n")
        self.backups[str(self.nextid).zfill(5)] = wholeList
        json.dump(self.backups, open(self.fback, 'w'))
        return True
    def showfun(self,fun):
        ## Display the function
        linecache.clearcache()
        self.clean()
        # modules = imp.load_source('module.name', self.fkeep)
        modules = imp.load_source('temp', self.fkeep)
        if fun not in dir(modules):
            print ("### function not exists")
            return None
        return inspect.getsource(getattr(modules,fun))
    def updatefun(self,newFun):
        ## Update the function
        newSource = inspect.getsource(newFun)
        linecache.clearcache()
        self.clean()
        modules = imp.load_source('temp', self.fkeep)
        if newFun.func_name not in dir(modules):
            print ("### function not exists, adding it now")
            self.addfun(newFun)
            self.backup()
            return 
        wholeString = inspect.getsource(modules)
        subString = inspect.getsource(getattr(modules,newFun.func_name))
        index = wholeString.index(subString)
        newString = wholeString[:index] + newSource + wholeString[(index+len(subString)):]
        with open(self.fkeep, "w") as f:
            f.writelines(newString)
        self.backup()
        linecache.clearcache()
        self.clean()
    def delfun(self,fun):
        linecache.clearcache()
        self.clean()
        modules = imp.load_source('temp', self.fkeep)
        if fun not in dir(modules):
            print ("### function not exists")
            return 
        wholeString = inspect.getsource(modules)
        subString = inspect.getsource(getattr(modules,fun))
        index = wholeString.index(subString)
        newString = wholeString[:index] + wholeString[(index+len(subString)):]
        with open(self.fkeep, "w") as f:
            f.writelines(newString)
        self.backup()
    def fun(self,fun):
        linecache.clearcache()
        self.clean()
        modules = imp.load_source('temp', self.fkeep)
        return getattr(modules,fun)
    def addfun(self,newFun,startpos=-1,after=None):
        newSource = inspect.getsource(newFun)
        newSourceLine = inspect.getsourcelines(newFun)[0]
        if (after is not None) and (self.showfun(after) is not None):
            ## save new function after the "after"
            linecache.clearcache()
            self.clean()
            modules = imp.load_source('temp', self.fkeep)
            wholeString = inspect.getsource(modules)
            subString = inspect.getsource(getattr(modules,after))
            index = wholeString.index(subString) + len(subString)
            newString = wholeString[:index] + newSource + wholeString[index:]
            with open(self.fkeep,"w") as f:
                f.writelines(newString)
            self.backup()
            return 
        if startpos<0: 
            self.addline(newSourceLine,startpos=-1)
        else:
            self.addline(newSourceLine,startpos=startpos)
        self.backup()
    def addline(self,lines,startpos=0):
        with open(self.fkeep,"r") as f:
            content = f.readlines()
        if startpos < 0:
            startpos = len(content)
        if type(lines) is str:
            newContent = content[:startpos] + [lines+"\n"] + content[startpos:]
        elif type(lines) is list:
            newContent = content[:startpos] + lines + ["\n"] + content[startpos:]
        else:
            newContent = content[:startpos] + [str(lines)+"\n"] + content[startpos:]
        with open(self.fkeep,"w") as f:
            f.writelines(newContent)
        self.backup()
#         linecache.clearcache()
        self.clean()