######################################################################################################################################################################################################
import os,re,shutil
import maya.cmds as cmds
######################################################################################################################################################################################################
def upload():
    upMainPath=r'\\RENDERSERVER\mayapro'
    getFilePath=cmds.textField('FilePath',query=True,text=True)
    mb=0
    avi=0
    for root,dirs,files in os.walk(getFilePath):
        for uf in files:
            if re.search('[a-z]*_e[0-9][0-9][0-9]*_p[0-9][0-9][0-9]*_s[0-9][0-9][0-9]*',uf):
            
                if os.path.splitext(uf)[1]=='.mb':
                    Gpro=re.search('[a-z]+',uf).group()
                    
                    Gepisode=re.search('e\d+[a-z]',uf)
                    if Gepisode==None:
                        Gepisode=re.search('e\d+',uf)
                    Gepisode=Gepisode.group()
                    
                    Gparagraph=re.search('p\d+[a-z]',uf)
                    if Gparagraph==None:
                        Gparagraph=re.search('p\d+',uf)
                    Gparagraph=Gparagraph.group()
                    
                    Gscene=re.search('s\d+[a-z]',uf)
                    if Gscene==None:
                        Gscene=re.search('s\d+',uf)
                    Gscene=Gscene.group() 
                      
                    originalFile=os.path.join(root,uf)
                    
                    upFile=upMainPath+'\\'+Gpro+'\\'+r'animationScenes\scenes'+'\\'+Gpro+'_'+Gepisode+'\\'+Gpro+'_'+Gepisode+'_'+Gparagraph+'\\'+uf
                    
                    if os.path.isdir(upMainPath+'\\'+Gpro):
                        if os.path.isfile(upFile)==False:
                            if os.path.isdir(os.path.dirname(upFile))==False:
                                os.makedirs(os.path.dirname(upFile))
                            shutil.copy(originalFile,upFile)
                            print 'Done UP '+upFile
                            mb=mb+1
                        else:
                            originalFile_mtime=os.stat(originalFile).st_mtime
                            upFile_mtime=os.stat(upFile).st_mtime
                            
                            if originalFile_mtime>upFile_mtime:
                                shutil.copy(originalFile,upFile)
                                print 'Done MD '+upFile
                                mb=mb+1

######################################################################################################################################################################################################                    
                    
                if os.path.splitext(uf)[1]=='.avi':
                    Gpro=re.search('[a-z]+',uf).group()
                    
                    Gepisode=re.search('e\d+[a-z]',uf)
                    if Gepisode==None:
                        Gepisode=re.search('e\d+',uf)
                    Gepisode=Gepisode.group()
                    
                    Gparagraph=re.search('p\d+[a-z]',uf)
                    if Gparagraph==None:
                        Gparagraph=re.search('p\d+',uf)
                    Gparagraph=Gparagraph.group()
                    
                    Gscene=re.search('s\d+[a-z]',uf)
                    if Gscene==None:
                        Gscene=re.search('s\d+',uf)
                    Gscene=Gscene.group() 
                      
                    originalFile=os.path.join(root,uf)
                    
                    upFile=upMainPath+'\\'+Gpro+'\\'+r'animationScenes\avi'+'\\'+Gpro+'_'+Gepisode+'\\'+Gpro+'_'+Gepisode+'_'+Gparagraph+'\\'+uf
                    
                    if os.path.isdir(upMainPath+'\\'+Gpro):
                        if os.path.isfile(upFile)==False:
                            if os.path.isdir(os.path.dirname(upFile))==False:
                                os.makedirs(os.path.dirname(upFile))
                            shutil.copy(originalFile,upFile)
                            print 'Done AVI '+upFile
                            avi=avi+1
                        else:
                            originalFile_mtime=os.stat(originalFile).st_mtime
                            upFile_mtime=os.stat(upFile).st_mtime
                            
                            if originalFile_mtime>upFile_mtime:
                                shutil.copy(originalFile,upFile)
                                print 'Done AVI '+upFile
                                avi=avi+1  
######################################################################################################################################################################################################

    cmds.deleteUI('windowxp', window=True)                    
    ms='there are '+str(mb)+' MB '+str(avi)+' AVI '+'files have been uploaded'
    cmds.confirmDialog( title='FilesUpDone', message=ms, button=['Yes'], defaultButton='Yes' )
                             
######################################################################################################################################################################################################
# Make a new window
if cmds.window('windowxp',exists=True):
    cmds.deleteUI('windowxp', window=True)
cmds.window('windowxp', title='UpLoading' )
cmds.rowColumnLayout('rowlumnLayoutI', numberOfColumns=3, columnWidth=[(1, 60), (2, 350), (3, 60)] )
cmds.text('putFilePath', label='putFilePath' )
cmds.textField('FilePath')
cmds.button('FileCommand',label='Up' ,command='upload()')
cmds.separator(style='none')
cmds.setParent( '..' )
cmds.showWindow( 'windowxp' )
######################################################################################################################################################################################################
