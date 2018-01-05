#Author-Bram Hendrickx
#Description-Mass export scetches to DXF

import adsk.core, adsk.fusion, adsk.cam, traceback
import os

debug = False
handlers = []
# Event handler for the commandCreated event.
class ShowDxfExportCommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()              
    def notify(self, args):
        ui = None
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            app = adsk.core.Application.get()
            ui  = app.userInterface
            cmd = eventArgs.command

            # Connect to the execute event.
            onExecute = DxfExportExecuteCommandHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))  

def GetFilename(folder, filename):
    dxfFileName = os.path.join(folder, '{}.dxf'.format(filename)) 
    index = 0
    while os.path.isfile(dxfFileName) == True:
        index += 1
        dxfFileName = os.path.join(folder, '{}({}).dxf'.format(filename,index)) 
    return dxfFileName

# Event handler for the execute event.
class DxfExportExecuteCommandHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        ui = None
        try: 
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            app = adsk.core.Application.get()
            ui  = app.userInterface

            selectedSketches = []
            for selection in ui.activeSelections:
                selectedEnt = selection.entity
                if selectedEnt is None:
                    pass
                elif selectedEnt.objectType == adsk.fusion.Sketch.classType():
                    selectedSketches.append(selectedEnt)
                elif selectedEnt.objectType == adsk.fusion.Sketches.classType():
                    if selectedEnt.count > 0:
                        for item in selectedEnt:
                            selectedSketches.append(item)

            if len(selectedSketches) == 0:
                ui.messageBox('You need to select at least one sketch from the browser', 'Error')
                return

            if debug:
                ui.messageBox('You selected {} sketch(es).'.format(len(selectedSketches)))

            # Set styles of file dialog.
            folderDlg = ui.createFolderDialog()
            folderDlg.title = 'Select a folder to save to' 
        
            # Show folder dialog
            dlgResult = folderDlg.showDialog()
            if dlgResult != adsk.core.DialogResults.DialogOK:
                return
                                 
            if debug:
                ui.messageBox('selected folder: {}'.format(folderDlg.folder))
            
            # Dxf saving 
            for sketchObj in selectedSketches:
                dxfFileName = GetFilename(folderDlg.folder, sketchObj.name)
                sketchObj.saveAsDXF(dxfFileName);  
                if debug:
                    ui.messageBox('saved file: {}'.format(dxfFileName)) 
                    
            ui.messageBox('Exported {} DXF files'.format(len(selectedSketches)))
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc())) 

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Add a command that displays the panel.
        showExporterCmdDef = ui.commandDefinitions.itemById('showDxfExport')
        if not showExporterCmdDef:
            showExporterCmdDef = ui.commandDefinitions.addButtonDefinition('showDxfExport', 'Export DXF', 'Export selected sketches to DXF', '')
            # Connect to Command Created event.
            onCommandCreated = ShowDxfExportCommandHandler()
            showExporterCmdDef.commandCreated.add(onCommandCreated)
            handlers.append(onCommandCreated)

        # Add the command to the toolbar.
        panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cntrl = panel.controls.itemById('showDxfExport')
        if not cntrl:
            panel.controls.addCommand(showExporterCmdDef)

        if debug:
            ui.messageBox('Loaded', 'Setup')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cmd = panel.controls.itemById('showDxfExport')
        if cmd:
            cmd.deleteMe()
        cmdDef = ui.commandDefinitions.itemById('showDxfExport')
        if cmdDef:
            cmdDef.deleteMe() 
        
        if debug:
            ui.messageBox('Unloaded', 'Setup')
        adsk.terminate()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))