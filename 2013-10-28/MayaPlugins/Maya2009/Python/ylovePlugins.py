#-*-coding:utf8-*-
import nuke,nukescripts,os,re,shutil,math,string
# do it yourself####################################################################################################
#def updateScripts():
#    pathServer=r'\\192.168.0.188\plug-ins\Nuke_Plugins'
#    pathClient=r'C:\Program Files\Nuke6.3v2\plugins'
#    files=os.listdir(pathServer)
#    for i in files:
#        shutil.copy2(pathServer+'/'+i,pathClient+'/'+i)

# do it yourself####################################################################################################
def cleanNodes():
    selnodes = nuke.selectedNodes('Read')
    for node in selnodes:
        node['premultiplied'].setValue(True)
        name=node['file'].getValue()
        if name.find('Thumbs.db')!=-1:
            nuke.delete(node)

# do it yourself####################################################################################################
def updateFile():
    aim='s'+nuke.getInput('please input scenes name which you want to do')
    allReadnodes = nuke.allNodes('Read',group = nuke.root())
    if re.search('s\d+',aim)==None or len(aim)>5:
        nuke.message('please gave the right name rule')
    else:    
        for rn in allReadnodes:
            rnfile=rn['file'].getValue()
            refa=re.sub('s\d+[a-z]',aim,rnfile)
            if refa==rnfile:
                refa=re.sub('s\d+',aim,rnfile)
            getpath=os.path.dirname(refa)
            if os.path.isdir(getpath)==False:
                nuke.message('this is not a exist scenes')
            else:
                listpath=os.listdir(getpath)
                if re.search('\(\d+\)',listpath[0]):
                    getnuminput=re.findall('\(\d+\)',listpath[0])[0]
                    getnum=int(float(re.findall('\(\d+\)',listpath[0])[0][1:-1]))
                    refb=re.sub('\(\d+\)',getnuminput,refa)
                    rn['file'].setValue(refb)
                    rn['last'].setValue(getnum)
                    rn['origlast'].setValue(getnum)
# do it yourself####################################################################################################
def updateVersion():
    allReadnodes = nuke.allNodes('Read',group = nuke.root())
    for n in allReadnodes:
        oldf=n['file'].getValue()
        oldchars=re.findall('_v\d+',oldf)
        if len(oldchars)>=1:
            oldchar=oldchars[0]
            newchar=oldchar[:-1]+str(int(float(oldchar[-1])+1))
            newf=oldf.replace(oldchar,newchar)
            
            newdir=os.path.dirname(newf)
            
            if os.path.isdir(newdir):
                n['file'].setValue(newf)

# do it yourself####################################################################################################
def updatePath():
    allnode = nuke.allNodes(group = nuke.root())
    for i in allnode:
        _class=i.Class()
        if _class=="Read":
            name=i['file'].getValue()
            baseName=os.path.dirname(name)
            if os.path.isdir(baseName)==False:
                replaceName=name.replace('T:/','O:/')
                if os.path.isdir(os.path.dirname(replaceName)):
                    i['file'].setValue(replaceName)

# do it yourself####################################################################################################
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

# do it yourself####################################################################################################
menubar = nuke.menu("Nuke");
m = menubar.addMenu("&YloveScripts")
m.addCommand("&updateScripts","updateScripts()","")
m.addCommand("&cleanNodes","cleanNodes()","`")
m.addCommand("-","","")
m.addCommand("&updateFile","updateFile()","#1")
m.addCommand("&updateVersion","updateVersion()","#2")
m.addCommand("&updatePath","updatePath()","#3")
m.addCommand("-","","")
m.addCommand("&LandR","LandR()","+r")
del m
# do it yourself####################################################################################################
#add format
nuke.addFormat ("1024 576 0 0 1024 576 1 dike")
# do it yourself####################################################################################################
# 'ctrl ' --'^'
# 'shift' --'+'
# 'alt  ' --'#'
#nuke.knobDefault('Blur.size','20')
#nuke.ask('Do you like nuke?')
#nuke.message('I like nuke')

# do it yourself####################################################################################################




                
