#-*-coding:utf8-*-
import os,re,Tkinter,shutil
RENuploading = Tkinter.Tk()
######################################################################################################################################################################################################
def upload():
    upMainPath=r'\\RENDERSERVER\mayapro'
            
    getFilePath=pathEntry.get()
    mb=0
    tif=0
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
                    
                    upFile=upMainPath+'\\'+Gpro+'\\'+'renderScenes'+'\\'+Gpro+'_'+Gepisode+'\\'+Gpro+'_'+Gepisode+'_'+Gparagraph+'\\'+Gpro+'_'+Gepisode+'_'+Gparagraph+'_'+Gscene+'\\'+uf
                    
                    if os.path.isdir(upMainPath+'\\'+Gpro):
                        if os.path.isfile(upFile)==False:
                            if os.path.isdir(os.path.dirname(upFile))==False:
                                os.makedirs(os.path.dirname(upFile))
                            shutil.copy(originalFile,upFile)
                            print 'Done MB '+upFile
                            mb=mb+1
                        else:
                            originalFile_mtime=os.stat(originalFile).st_mtime
                            upFile_mtime=os.stat(upFile).st_mtime
                            
                            if originalFile_mtime>upFile_mtime:
                                shutil.copy(originalFile,upFile)
                                print 'Done MB '+upFile
                                mb=mb+1

######################################################################################################################################################################################################                    
                    
                if os.path.splitext(uf)[1]=='.tif':
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
                    
                    Glayer=re.search('\(\w+\)',uf)
                    Glayer=Glayer.group()[1:-1]
                      
                    originalFile=os.path.join(root,uf)
                    
                    upFile=upMainPath+'\\'+Gpro+'\\'+'renderimages'+'\\'+Gpro+'_'+Gepisode+'\\'+Gpro+'_'+Gepisode+'_'+Gparagraph+'\\'+Gpro+'_'+Gepisode+'_'+Gparagraph+'_'+Gscene+'\\'+Glayer+'\\'+uf
                    
                    if os.path.isdir(upMainPath+'\\'+Gpro):
                        if os.path.isfile(upFile)==False:
                            if os.path.isdir(os.path.dirname(upFile))==False:
                                os.makedirs(os.path.dirname(upFile))
                            shutil.copy(originalFile,upFile)
                            print 'Done TIF '+upFile
                            tif=tif+1
                        else:
                            originalFile_mtime=os.stat(originalFile).st_mtime
                            upFile_mtime=os.stat(upFile).st_mtime
                            
                            if originalFile_mtime>upFile_mtime:
                                shutil.copy(originalFile,upFile)
                                print 'Done TIF '+upFile
                                tif=tif+1 

    print str(mb)+' files and '+str(tif)+' files have been uploaded'                               
      
######################################################################################################################################################################################################
# Make a new window
mainFrame=Tkinter.Frame(RENuploading)
mainFrame.pack()

pathLabel=Tkinter.Label(mainFrame,text='getFilePath')
pathLabel.pack(fill='both',side='top')

pathEntry=Tkinter.Entry(mainFrame)
#pathEntry.insert('insert','your mov path')
pathEntry.pack(fill='both')

pathBut=Tkinter.Button(mainFrame,text="upload",command=upload)
pathBut.pack(fill='both',side='bottom')

RENuploading.mainloop()
######################################################################################################################################################################################################
