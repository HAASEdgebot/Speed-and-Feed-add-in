#Author-Ryan Perez
#Description- THis add-in will create a command event for speed/feeds

import adsk.core, adsk.fusion, adsk.cam, traceback
handlers = []

class SFButtonPressedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface
            cmd = args.command
            inputs = cmd.commandInputs

            #adding different features to the dialouge box
            Speed = inputs.addValueInput('Speed Value', 'Speed Rate', 'mm/s', adsk.core.ValueInput.createByReal(1.0))

            #inputs.addTextBoxCommandInput('textbox1', 'Speed Rate', '', 1, True)
            #onInputChanged = SFDialogInputChangedHandler()
            #cmd.inputChanged.add(onInputChanged)
            #handlers.append(onInputChanged)

            onExecute = SFDialogOKEventHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class SFDialogOKEventHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        app = adsk.core.Application.get()
        ui  = app.userInterface
        try:
            cmd = args.firingEvent.sender
            SpeedInput = cmd.commandInputs.itemById('Speed Value')
            Speedrate = SpeedInput.realValue

            ui.messageBox(Speedrate)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))





def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        #defining the command
        commandDefinitions = ui.commandDefinitions
        SFButtonDefinition = commandDefinitions.addButtonDefinition('SFButton', 'Speed and Feeds', 'Input the Speed and Feed rates for Edgebot machine', 'SFresources')
         #grabbing the correct toolbar panel to add the button to
        addinsToolbarPanel = ui.allToolbarPanels.itemById('HAAS EdgeBot')
        #Adding the Edgebot button to the toolbar panel
        SFButtonControl =addinsToolbarPanel.controls.addCommand(SFButtonDefinition, 'SFButtonControl')

        #attaching event handler to button
        SFButtonPressed = SFButtonPressedEventHandler()
        SFButtonDefinition.commandCreated.add(SFButtonPressed)
        handlers.append(SFButtonPressed)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Stop addin SFbutton')
        

        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
