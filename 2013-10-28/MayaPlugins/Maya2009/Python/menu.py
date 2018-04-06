# User interface initialization for Nuke
# -*- coding: utf-8 -*-
# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import sys
import os
import os.path
import nuke

# Create the temp directory
try:
  os.makedirs(os.environ["NUKE_TEMP_DIR"])
except OSError:
  pass

nuke.pluginAddPath("./icons", addToSysPath=False);

import nukescripts
import nukescripts.toolbars
import nukescripts.snap3d

# Set up the toolbars.
nukescripts.toolbars.setup_toolbars()

# Menu definitions

# File menu

# Build a list of read nodes which have been flagged for localisation
def doLocalise(localiseAll):
  rootNode = nuke.root()
  readKnobList = []
  nodeList = []
  if localiseAll:
    nodeList = nuke.allNodes(group=rootNode)
  else:
    nodeList = nuke.selectedNodes()
  for n in nodeList:
    readKnob = nuke.getReadFileKnob(n)
    if readKnob != None:
      if nuke.localisationEnabled(readKnob):
        readKnobList.append(readKnob)
  nuke.localiseFiles(readKnobList)

menubar = nuke.menu("Nuke");

m = menubar.addMenu("&File")
m.addCommand("&New", "nuke.scriptNew(\"\")", "^n")
m.addCommand("&Open...", "nuke.scriptOpen(\"\")", "^o")
m.addCommand("&Save", "nuke.scriptSave(\"\")", "^s")
m.addCommand("Save &As...", "nuke.scriptSaveAs(\"\")", "^+S")
m.addCommand("Save New &Version", "nukescripts.script_version_up()", "#+S")
m.addCommand("_&Recent Files/@recent_file1", "nuke.scriptOpen(nuke.recentFile(1))", "#+1")
m.addCommand("&Recent Files/@recent_file2", "nuke.scriptOpen(nuke.recentFile(2))", "#+2")
m.addCommand("&Recent Files/@recent_file3", "nuke.scriptOpen(nuke.recentFile(3))", "#+3")
m.addCommand("&Recent Files/@recent_file4", "nuke.scriptOpen(nuke.recentFile(4))", "#+4")
m.addCommand("&Recent Files/@recent_file5", "nuke.scriptOpen(nuke.recentFile(5))", "#+5")
m.addCommand("&Recent Files/@recent_file6", "nuke.scriptOpen(nuke.recentFile(6))", "#+6")
m.addCommand("-", "", "")

m.addCommand("&Import Script...", "nukescripts.import_script()", "")
m.addCommand("_&Export Nodes As Script...", "nukescripts.export_nodes_as_script()", "")
m.addCommand("Script Co&mmand...", "nukescripts.script_command('')", "x")

def tcl_file():
  try:
    s = nuke.getFilename("Source Script", "*.tcl;*.nk;*.py", "", "script")
    (root, ext) = os.path.splitext(s)
    if ext == ".py":
      execfile(s)
    else:
      nuke.tcl('source',s)
  except:
    pass

def frameForward():
  v = nuke.activeViewer()
  if v != None:
    v.frameControl( 1 )
  else:
    nuke.frame( nuke.frame()+1 )

def frameBackward():
  v = nuke.activeViewer()
  if v != None:
    v.frameControl( -1 )
  else:
    nuke.frame( nuke.frame()-1 )

m.addCommand("TCL File...", "tcl_file()", "#X")
m.addCommand("Goto Frame...", "nukescripts.goto_frame()", "#g")
m.addCommand("@;Next Frame", "frameBackward()", "Left")
m.addCommand("@;Previous Frame", "frameForward()", "Right")
m.addCommand("Script Info", "nukescripts.script_data()", "#i")
m.addCommand("-", "", "")
m.addCommand("Clear", "nuke.scriptClear()")
m.addCommand("&Close", "nuke.scriptClose()", "^w")
m.addCommand("E&xit", "nuke.scriptExit()", "^q")

m = menubar.addMenu("&Edit")
m.addCommand("&Undo", "nuke.undo()", "^z")
m.addCommand("_&Redo", "nuke.redo()", "^y")
m.addCommand("-", "", "")
m.addCommand("&Search...", "nuke.selectPattern()", "/")
m.addCommand("Select &All", "nuke.selectAll()", "^a")
m.addCommand("Select Similar/Color", "nuke.selectSimilar(nuke.MATCH_COLOR)")
m.addCommand("Select Similar/Class", "nuke.selectSimilar(nuke.MATCH_CLASS)")
m.addCommand("Select Similar/Label", "nuke.selectSimilar(nuke.MATCH_LABEL)")
m.addCommand("Select Connected Nodes", "nuke.selectConnectedNodes()", "^#A")
m.addCommand("@;Select Connected Nodes", "nuke.selectConnectedNodes()", "^#á")   # some keyboard layouts translate Ctrl+Alt+A to Ctrl+Alt+á
m.addCommand("In&vert Selection", "nuke.invertSelection()")
m.addCommand("Cu&t", "nuke.nodeCopy(nukescripts.cut_paste_file()); nukescripts.node_delete(popupOnError=True)", "^x")
m.addCommand("&Copy", "nuke.nodeCopy(nukescripts.cut_paste_file())", "^c")
m.addCommand("&Paste", "nuke.nodePaste(nukescripts.cut_paste_file())", "^v")
# invisible item so you can shift+paste:
m.addCommand("@;Paste2", "nuke.nodePaste(nukescripts.cut_paste_file())", "+^v")
m.addCommand("&Duplicate", "nukescripts.node_copypaste()", "#c")
m.addCommand("Clo&ne", "nuke.cloneSelected()", "#k")
m.addCommand("Copy As Clones", "nuke.cloneSelected(\"copy\")", "^k")
m.addCommand("Force Clone", "nuke.forceClone()", "^#+k")
m.addCommand("Declo&ne", "\n\
selnodes = nuke.selectedNodes()\n\
for i in selnodes:\n\
  nukescripts.declone(i)", "#+k")
m.addCommand("-", "", "")

isLinux = not nuke.env['WIN32'] and not nuke.env['MACOS']

n = m.addMenu("&Node")
n.addCommand("&Filename/Show", "nukescripts.showname()", "q")
n.addCommand("&Filename/Search and Replace...", "nukescripts.search_replace()", "^+?" if isLinux else "^+/")
n.addCommand("&Filename/Set Versions", "nuke.tcl('cam_ver_panel')")
n.addCommand("&Filename/Version Up", "nukescripts.version_up()", "#Up")
n.addCommand("&Filename/Version Down", "nukescripts.version_down()", "#Down")
n.addCommand("&Filename/Version to Latest (Reads only)", "nukescripts.version_latest()", "#+Up")
n.addCommand("&Filename/Camera Up", "nukescripts.camera_up()", "#Right")
n.addCommand("&Filename/Camera Down", "nukescripts.camera_down()", "#Left")

n.addCommand("&Group/&Collapse To Group", "nuke.collapseToGroup()", "^g")
n.addCommand("&Group/&Expand Group", "nuke.expandSelectedGroup()", "^#g")
# Add another one hidden to get Ctrl+Enter (keypad) as well as Ctrl+Return
n.addCommand("&Group/&Open Group Node Graph", "nuke.showDag(nuke.selectedNode())", "^Enter")
n.addCommand("@;&Open Group Node Graph", "nuke.showDag(nuke.selectedNode())", "^Return")
n.addCommand("&Group/Copy &Nodes To Group", "nuke.makeGroup()", "^#+g")
n.addCommand("&Group/Copy Gi&zmo To Group", "nuke.tcl('copy_gizmo_to_group [ selected_node ]')", "^+g")

n.addCommand("&Color...", "nukescripts.color_nodes()", "^+c")
n.addCommand("&Un-color", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  i.knob(\"tile_color\").setValue(0)\n\
")
n.addCommand("Paste Knob &Values", "nukescripts.copy_knobs(\"\")", "^#V")
n.addCommand("&Input On\/Off", "nukescripts.toggle(\"hide_input\")", "#h")
n.addCommand("&Postage Stamp On\/Off", "nukescripts.toggle(\"postage_stamp\")", "#p")
n.addCommand("Force &Dope Sheet On\/Off", "nukescripts.toggle(\"dope_sheet\")", "#d")

def _autoplace():
  n = nuke.selectedNodes()
  for i in n:
    nuke.autoplace(i)

n.addCommand("Auto&place", "_autoplace()", "l")
n.addCommand("&Buffer On\/Off", "nukescripts.toggle(\"cached\")", "^b")
n.addCommand("&Disable\/Enable", "nukescripts.toggle(\"disable\")", "d")
n.addCommand("&Info Viewer", "nukescripts.infoviewer()", "i")
n.addCommand("&Open", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  nuke.show(i)\n\
", "0xff0d")
n.addCommand("&Snap to Grid", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  nuke.autoplaceSnap(i)\n\
", "|")
n.addCommand("&Snap All to Grid", "\n\
n = nuke.allNodes();\n\
for i in n:\n\
  nuke.autoplaceSnap(i)\n\
", "\\",)
n.addCommand("Swap A - B", "nukescripts.swapAB(nuke.selectedNode())", "+X")
n.addCommand("Connect", "nuke.connectNodes(False, False)", "y")
n.addCommand("Connect Backward", "nuke.connectNodes(True, False)", "+y")
n.addCommand("Connect A", "nuke.connectNodes(False, True)", "#y")
n.addCommand("Connect Backward - A", "nuke.connectNodes(True, True)", "+#y")
n.addCommand("Splay First", "nuke.splayNodes(False, False)", "u")
n.addCommand("Splay Last", "nuke.splayNodes(True, False)", "+u")
n.addCommand("Splay First to A", "nuke.splayNodes(False, True)", "#u")
n.addCommand("Splay Last to A", "nuke.splayNodes(True, True)", "+#u")

def _copyKnobsFromScriptToScript(n, m):
  k1 = n.knobs()
  k2 = m.knobs()
  excludedKnobs = ["name", "xpos", "ypos"]
  intersection = dict([(item, k1[item]) for item in k1.keys() if item not in excludedKnobs and k2.has_key(item)])
  for k in intersection.keys():
    x1 = n[k]
    x2 = m[k]
    x2.fromScript(x1.toScript(False))

def _useAsInputProcess():
  n = nuke.selectedNode()
  [i['selected'].setValue(False) for i in nuke.allNodes()]
  # FIXME: these two calls should have the arguments in the same order, or even better change the node bindings so they can go.
  if nuke.dependencies([n], nuke.INPUTS | nuke.HIDDEN_INPUTS) or nuke.dependentNodes(nuke.INPUTS | nuke.HIDDEN_INPUTS, [n]):
    m = nuke.createNode(n.Class())
  else:
    m = n
  if m is not n: _copyKnobsFromScriptToScript(n, m)
  viewer = nuke.activeViewer().node()
  viewer['input_process'].setValue(True)
  viewer['input_process_node'].setValue(m.name())

def _copyViewerProcessToDAG():
  vpNode = nuke.ViewerProcess.node()
  [i['selected'].setValue(False) for i in nuke.allNodes()]
  n = nuke.createNode(vpNode.Class())
  _copyKnobsFromScriptToScript(vpNode, n)

n.addCommand("Use as Input Process", "_useAsInputProcess()")
n.addCommand("Copy Viewer Process to Node Graph", "_copyViewerProcessToDAG()")

m.addCommand("&Remove Input", "nukescripts.remove_inputs()", "^d")
m.addCommand("&Extract", "nuke.extractSelected()", "+^x")
m.addCommand("&Branch", "nukescripts.branch()", "#b")
m.addCommand("_&Erase", "nukescripts.node_delete(popupOnError=True)", "0xffff")
m.addCommand("@;Erase", "nukescripts.node_delete(popupOnError=True)", "0xff08")

def _internal_expression_arrow_cmd():
  p = nuke.toNode("preferences")
  ea = p.knob("expression_arrows");
  ca = p.knob("clone_arrows");
  ea.setValue(not ea.value())
  ca.setValue(not ca.value())

# FIXME expression arrows needs to be a checkmark toggle.
m.addCommand("&Expression Arrows", "_internal_expression_arrow_cmd()", "#e")
m.addCommand("Preferences...", "nuke.show(nuke.toNode(\"preferences\"))", "+S")
m.addCommand("@;Preferences...", "nuke.show(nuke.toNode(\"preferences\"))", "^,")
m.addCommand("&Project Settings...", "nuke.showSettings()", "s")

# Layout menu
m = menubar.addMenu("&Layout")
m.addCommand("Restore Layout 1 (startup default)", "nuke.restoreWindowLayout(1)", "+F1")
m.addCommand("Restore Layout 2", "nuke.restoreWindowLayout(2)", "+F2")
m.addCommand("Restore Layout 3", "nuke.restoreWindowLayout(3)", "+F3")
m.addCommand("Restore Layout 4", "nuke.restoreWindowLayout(4)", "+F4")
m.addCommand("Restore Layout 5", "nuke.restoreWindowLayout(5)", "+F5")
m.addCommand("Restore Layout 6", "nuke.restoreWindowLayout(6)", "+F6")
m.addCommand("-", "", "")
m.addCommand("Save Layout 1 (startup default)", "nuke.saveWindowLayout(1)", "^F1")
m.addCommand("Save Layout 2", "nuke.saveWindowLayout(2)", "^F2")
m.addCommand("Save Layout 3", "nuke.saveWindowLayout(3)", "^F3")
m.addCommand("Save Layout 4", "nuke.saveWindowLayout(4)", "^F4")
m.addCommand("Save Layout 5", "nuke.saveWindowLayout(5)", "^F5")
m.addCommand("Save Layout 6", "nuke.saveWindowLayout(6)", "^F6")
m.addCommand("-", "", "")
m.addCommand("Show Curve Editor", "nuke.tcl('curve_editor')", "~")
m.addCommand("@;Show Curve Editor", "nuke.tcl('curve_editor')", "Shift+~")
# FIXME Hide floating viewers needs to be a checkmark toggle.
m.addCommand("Toggle Hide Floating Viewers", "nuke.toggleViewers()", "`")
m.addCommand("Toggle Full Screen", "nuke.toggleFullscreen()", "#s")
m.addCommand("-", "", "")
m.addCommand("Next Tab", "nuke.tabNext()", "Ctrl+T")
m.addCommand("Close Tab", "nuke.tabClose()", "Shift+Escape")

# Viewer menu
m = menubar.addMenu("&Viewer")
m.addCommand("&Create New Viewer", "nuke.createNode(\"Viewer\")", "^I")
m.addCommand("-", "", "")
n = m.addMenu("Connect to A Side")
n.addCommand("Using Input &1", "nukescripts.connect_selected_to_viewer(0)", "1")
n.addCommand("Using Input &2", "nukescripts.connect_selected_to_viewer(1)", "2")
n.addCommand("Using Input &3", "nukescripts.connect_selected_to_viewer(2)", "3")
n.addCommand("Using Input &4", "nukescripts.connect_selected_to_viewer(3)", "4")
n.addCommand("Using Input &5", "nukescripts.connect_selected_to_viewer(4)", "5")
n.addCommand("Using Input &6", "nukescripts.connect_selected_to_viewer(5)", "6")
n.addCommand("Using Input &7", "nukescripts.connect_selected_to_viewer(6)", "7")
n.addCommand("Using Input &8", "nukescripts.connect_selected_to_viewer(7)", "8")
n.addCommand("Using Input &9", "nukescripts.connect_selected_to_viewer(8)", "9")
n.addCommand("Using Input 1&0", "nukescripts.connect_selected_to_viewer(9)", "0")
n = m.addMenu("Connect to B Side")
n.addCommand("Using Input 1", "nukescripts.connect_selected_to_viewer(10)", "+1")
n.addCommand("Using Input 2", "nukescripts.connect_selected_to_viewer(11)", "+2")
n.addCommand("Using Input 3", "nukescripts.connect_selected_to_viewer(12)", "+3")
n.addCommand("Using Input 4", "nukescripts.connect_selected_to_viewer(13)", "+4")
n.addCommand("Using Input 5", "nukescripts.connect_selected_to_viewer(14)", "+5")
n.addCommand("Using Input 6", "nukescripts.connect_selected_to_viewer(15)", "+6")
n.addCommand("Using Input 7", "nukescripts.connect_selected_to_viewer(16)", "+7")
n.addCommand("Using Input 8", "nukescripts.connect_selected_to_viewer(17)", "+8")
n.addCommand("Using Input 9", "nukescripts.connect_selected_to_viewer(18)", "+9")
n.addCommand("Using Input 10", "nukescripts.connect_selected_to_viewer(19)", "+0")
n = m.addMenu("View")
n.addCommand("Previous", "nuke.activeViewer().previousView()", ";")
n.addCommand("Next", "nuke.activeViewer().nextView()", "\'")
if not nuke.env['ple']:
  m.addCommand("Toggle Monitor Output", "nukescripts.toggle_monitor_output()", "^u")

# Render menu
m = menubar.addMenu("&Render")
m.addCommand("&Proxy Mode", "nuke.toNode(\"root\").knob(\"proxy\").setValue(not nuke.toNode(\"root\").knob(\"proxy\").value())", "^p")
m.addCommand("-", "", "")
m.addCommand("Render &All...", "nukescripts.showRenderDialog([nuke.root()], False)", "F5")
m.addCommand("Render &Selected...", "nukescripts.showRenderDialog(nuke.selectedNodes(), False)", "F7")
m.addCommand("&Cancel", "nuke.cancel()", "0xff1b")
m.addCommand("-", "", "")
m.addCommand("&Flipbook Selected", "nukescripts.showFlipbookDialogForSelected()", "#F")

m = menubar.addMenu("&Cache")
m.addCommand("Buffer Report", "nuke.display(\"nukescripts.cache_report(str())\", nuke.root(), width = 800)")
m.addCommand("Clear Buffers", "nukescripts.cache_clear(\"\")", "F12")
m.addCommand("Clear Disk Cache", nuke.clearDiskCache)
m.addCommand("-", "", "")
n = m.addMenu("Local File Cache")
n.addCommand("Update All", "doLocalise(1)", "")
n.addCommand("Update Selected", "doLocalise(0)", "")


def FnOpenPluginInstaller():

  # MacOS is special. It needs to be done with open, or the PluginInstaller doesn't get
  # focus. The easiest way to do that is through os.system and calling open. open doesn't block, so that works fine.
  if nuke.env['MACOS']:
    path = nuke.env['ExecutablePath']
    path = "/".join(path.split("/")[:-1])
    path += "/../../../PluginInstaller.app"
    path = os.path.normpath(path)
    os.system("open " + path)
    return
	
  # get Nuke's directory
  path = nuke.env['ExecutablePath']
  path = "/".join(path.split("/")[:-1])
  path += "/PluginInstaller/PluginInstaller"
  if nuke.env['WIN32']:
    path += ".exe"
  path = os.path.normpath(path)
  
  args = []
  if nuke.env['WIN32']:
    args.append( "\"" + path + "\"" )
  else:
    args.append( path )
  os.spawnv(os.P_NOWAITO, path, args)
# do it yourself##################################################

from addPlugins import *

# do it yourself##################################################

# Help menu
m = menubar.addMenu("&Help")
m.addCommand("Key Assignments", "nuke.display(\"nuke.hotkeys()\", None, title = \"Nuke key assignments\")")
m.addCommand("-", "", "")
m.addCommand("Documentation", "TopDir = os.path.dirname(nuke.env['ExecutablePath']) + '/';\n\
if nuke.env['MACOS']:\n\
  TopDir = os.path.abspath(TopDir + '../../../') + '/'\n\
nukescripts.start(TopDir + 'Documentation/index.html')")
m.addCommand("Release Notes", "nukescripts.start('http://www.thefoundry.co.uk/nuke/releasenotes')")
m.addCommand("Training and Tutorials", "nukescripts.start('http://www.thefoundry.co.uk/nuke/training')")
m.addCommand("Nukepedia", "nukescripts.start('http://www.nukepedia.com')")
m.addCommand("Mailing Lists", "nukescripts.start('http://support.thefoundry.co.uk/cgi-bin/mailman/listinfo')")
m.addCommand("Plug-in Installer", "FnOpenPluginInstaller()")

m = nuke.menu("Animation")
m.addCommand("File/Import Ascii...", "nuke.tcl('import_ascii')")
m.addCommand("File/Import Time+value Ascii...", "nuke.tcl('import_discreet')")
m.addCommand("File/Import Discreet LUT...", "nuke.tcl('import_discreet_lut')") 
m.addCommand("File/Export Ascii...", "nuke.tcl('export_ascii')", readonly=True)
m.addCommand("File/Export Discreet LUT...", "nuke.tcl('export_discreet_lut')", readonly=True)
m.addCommand("Edit/Generate...", "nuke.tcl('animation_generate')")
m.addCommand("Edit/Move...", "nuke.tcl('animation_move')")
m.addCommand("Edit/Filter", "nuke.tcl('filter_multiple')")
m.addCommand("File/Create Curve", "nukescripts.create_curve()")
m.addCommand("Predefined/Loop", "nukescripts.animation_loop()")
m.addCommand("Predefined/Reverse", "nukescripts.animation_reverse()")
m.addCommand("Predefined/Negate", "nukescripts.animation_negate()")

m = nuke.menu("Axis")
n = m.addMenu("File")
n.addCommand("Import chan file", """nuke.tcl("import_chan_menu [node this]")""")
n.addCommand("Export chan file", """nuke.tcl("export_chan_menu [node this]")""")

n = m.addMenu("Snap")
n.addCommand("Match selection position", "nukescripts.snap3d.translateToPoints(nuke.selectedNode())")
n.addCommand("Match selection position, orientation", "nukescripts.snap3d.translateRotateToPoints(nuke.selectedNode())")
n.addCommand("Match selection position, orientation, size", "nukescripts.snap3d.translateRotateScaleToPoints(nuke.selectedNode())")

del m
del n
del isLinux

################################################################
# non-menu stuff:
#
# The stuff that lives here can't run in render mode or is
# pointless to run in render mode, so this way it only gets run
# if the GUI is starting up.

# Restore the default layout (number 1)
nuke.restoreWindowLayout(1)

# back-compatibility handling of autolabel. Load any autolabel.py we
# find and then register it so nuke.autolabel() calls it. User can
# override this by defining another version somewhere
# earlier in your NUKE_PATH, for instance $HOME/.nuke/menu.py.
from autolabel import autolabel
nuke.addAutolabel(autolabel)

# stream redirectors

class SERedirector(object):
  def __init__(self, stream):
    fileMethods = ('fileno', 'flush', 'isatty', 'read', 'readline', 'readlines',
                   'seek', 'tell', 'write', 'writelines', 'xreadlines', '__iter__')

    for i in fileMethods:
      if not hasattr(self, i) and hasattr(stream, i):
        setattr(self, i, getattr(stream, i))

    self.savedStream = stream

  def close(self):
    self.flush()

  def stream(self):
    return self.savedStream

class SESysStdIn(SERedirector, nuke.FnPySingleton):
  def readline(self):
    return ""

class SESysStdOut(SERedirector, nuke.FnPySingleton):
  def write(self, out):
    nuke.output_redirector(out)

class SESysStdErr(SERedirector, nuke.FnPySingleton):
  def write(self, out):
    nuke.stderr_redirector(out)

if nuke.GUI:
  sys.stdin  = SESysStdIn(sys.stdin)
  sys.stdout = SESysStdOut(sys.stdout)
  sys.stderr = SESysStdErr(sys.stderr)


########################################################################




