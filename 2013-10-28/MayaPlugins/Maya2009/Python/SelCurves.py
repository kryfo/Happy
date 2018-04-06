import maya.cmds as cmds
import re
def SelCurves():
    sel=cmds.ls(sl=1)
    cmds.select(cl=1)
    if sel:
        if re.search('.*:',sel[0]):
            nameSpace=re.search('.*:',sel[0]).group()[0:-1]
            nurbsCurves=cmds.ls(type='nurbsCurve')
            for nurbs in nurbsCurves:
                if re.search(nameSpace,nurbs):
                    try:
                        Curve=cmds.listRelatives(nurbs,p=1)[0]
                        cmds.select(Curve,add=1)
                    except:
                        pass
