import nuke
import os
import shutil
import nukescripts
import math
import os.path
import re
import string
# do it yourself##################################################
def TtoO():
    allnode = nuke.allNodes(group = nuke.root())
    for i in allnode:
        _class=i.Class()
        if _class=="Read":
            name=i['file'].getValue()
            bsname=os.path.dirname(name)
            if os.path.isdir(bsname)==False:
                repName=name.replace('T:/','O:/')
                i['file'].setValue(repName)

# do it yourself##################################################
def LandR():
    allReadnodes = nuke.allNodes('Read',group = nuke.root())
    for Lnode in allReadnodes:
        Lnode.setSelected(1)
        addDotUp=nuke.createNode('Dot', inpanel=False)
        addDotUp.setSelected(0)
    	filePath_L=Lnode['file'].getValue()
    	fileFirst_L=Lnode['first'].getValue()
    	fileLast_L=Lnode['last'].getValue()
    	if filePath_L.find('eyeLeft')!=-1:
            nukescripts.stereo.setViewsForStereo()
            nuke.root()['views_button'].setValue(True)
            nuke.root()['views_colours'].setValue(True)
            filePath_R=filePath_L.replace('eyeLeft','eyeRight')
            Rnode=nuke.createNode('Read','file {'+filePath_R+'}', inpanel=True)
            Rnode['first'].setValue(fileFirst_L)
            Rnode['last'].setValue(fileLast_L)
            Rnode['origfirst'].setValue(fileFirst_L)
            Rnode['origlast'].setValue(fileLast_L)
            Rnode.setSelected(0)
            Lnode['ypos'].setValue(Lnode['ypos'].getValue()-150)
            Lnode['xpos'].setValue(Lnode['xpos'].getValue()-60)
            Rnode['ypos'].setValue(Lnode['ypos'].getValue())
            Rnode['xpos'].setValue(Lnode['xpos'].getValue()+120)

            JoinView=nuke.createNode('JoinViews')
            JoinView.setSelected(0)
            JoinView.setInput(0,Lnode)
            JoinView.setInput(1,Rnode)
            JoinView.setXYpos((Lnode['xpos'].getValue()+Rnode['xpos'].getValue())/2,Lnode['ypos'].getValue()+150)
            addDotUp.setInput(0,JoinView)

# do it yourself##################################################
def deldb():
    allReadnodes = nuke.allNodes('Read',group = nuke.root())
    for node in allReadnodes:
        node['premultiplied'].setValue(True)
        name=node['file'].getValue()
        if name.find('Thumbs.db')!=-1:
            nuke.delete(node)

# do it yourself##################################################
def UpDateScripts():
    pathServer=r'\\192.168.0.188\plug-ins\Nuke_Plugins'
    pathClient=r'C:\Program Files\Nuke6.3v2\plugins'
    files=os.listdir(pathServer)
    for i in files:
        shutil.copy2(pathServer+'/'+i,pathClient+'/'+i)
# do it yourself##################################################
def upFilesVersion():
    allReadnodes = nuke.allNodes('Read',group = nuke.root())
    for n in allReadnodes:
        oldf=n['file'].getValue()
        print  oldf
        oldchars=re.findall('_c\d+',oldf)
        print oldchars
        oldchar=oldchars[0]
        print oldchar
        newchar=oldchar[:-1]+str(int(float(oldchar[-1])+1))
        print newchar
        newf=oldf.replace(oldchar,newchar)
        print newf
        newdir=os.path.dirname(newf)
        print newdir
        if os.path.isdir(newdir):
            n['file'].setValue(newf)

# do it yourself##################################################
def addFile():
    allnodes = nuke.allNodes('Read',group = nuke.root())
    for node in allnodes:
        oldfile=node['file'].getValue()
        print oldfile
        Gchar1=re.findall('sc\d+',oldfile)
        print Gchar1[0] 
        char1=Gchar1[0]
        if char1[-1]=='9':
            char2=Gchar1[0][:-2]+str(int(float(Gchar1[0][-2])+1))+'0'
        else:
            char2=Gchar1[0][:-1]+str(int(float(Gchar1[0][-1])+1))
        print char2
        Gchar3=re.findall('_\D+_lr_\D+_',oldfile)
        char3=Gchar3[0]
        print char3
        midfileI=os.path.dirname(oldfile)[:-18]
        print midfileI
        midfileII=midfileI.replace(char1,char2)
        print midfileII
        upfile=os.path.dirname(midfileII)
        print upfile
        if os.path.isdir(upfile):
            listI=os.listdir(upfile)
            print listI
            for i in listI:
                if re.search(char3,i):
                    print i
                    newfile=upfile+'/'+i
                    Gchar4=re.findall('_\D+_lr_\D+_',newfile)
                    char4=Gchar4[0]
                    print char4
                    if char4==char3:
                        print char4
                        print newfile
                        if re.search(char2,newfile):
                            newfile=newfile+'/'+i[:-6]+'.%04d.tif'
                            print 'OK'+newfile
                            Gnb=re.findall('_\d+_',newfile)
                            print Gnb
                            nb=int(float(Gnb[0][1:-1]))
                            print nb
                            node['file'].setValue(newfile)
                            node['first'].setValue(100)
                            node['origfirst'].setValue(nb)
                            node['last'].setValue(nb)
                            node['origlast'].setValue(nb)
   
# do it yourself##################################################      
menubar = nuke.menu("Nuke");
m = menubar.addMenu("&AddScripts")
m.addCommand("&UpDateScripts","UpDateScripts()","")
m.addCommand("-","","")
m.addCommand("&TtoO","TtoO()","")
m.addCommand("&LandR","LandR()","")
m.addCommand("-","","")
m.addCommand("&DELdb","deldb()","`")
m.addCommand("-","","")
m.addCommand("&addFile","addFile()","")
m.addCommand("&upFilesVersion","upFilesVersion()","^`")
del m

# do it yourself##################################################
#add format
nuke.addFormat ("1024 576 0 0 1024 576 1 dike")



