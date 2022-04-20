import os
import shutil
import tempfile
import re


from krita import *
from PyQt5.QtCore import pyqtSlot


def getNodesRecursive(root):
    """Get all nodes (layers) that are decendents of a specified node. The nodes are returned in a list in a reverse depth first order."""
    results = []
    for child in root.childNodes():
        results.extend(getNodesRecursive(child))
        results.append(child)
    return results


def getOptionsFromLayerName(layerName):
    """layerName is something like 'background {key=value,key2=value}'.
    
    Returns dictionary {"key":"value","key2":"value"}
    """
    results = {}

    try:
        match = re.search('\{.{3,}\}',layerName)
        if match is not None:
            just_braces = layerName[match.start():match.end()]
            just_braces = just_braces[1:-1]
            items = just_braces.split(',')
            for item in items:
                k, v = item.split('=')
                results[k] = v
    except Exception as e:
        return results

    return results

def getJustNameFromLayerName(layerName):
    """Given the full layer name (including any options), returns the name without the options. 
    For example, a layer with full name "bush {path=/scenes/foilage}" will return "bush". """
    brace = layerName.find('{')
    if brace == -1:
        return layerName.strip()
    else:
        return layerName[:brace].strip()

def getGodotProjectPath(path):
    """Given a path (to a file or folder), traverses up until a project.godot file is found, then returns the full path of the directory that contains this file.
    In other words, returns the "encompassing" godot project folder path of a given path.
    Returns None if the path isn't in a godot project.
    """
    # base case
    for item in os.listdir(os.path.dirname(path)):
        if item == "project.godot":
            return os.path.dirname(path)
    # recursive case
    if os.path.dirname(path) != path:
        return getGodotProjectPath(os.path.dirname(path))
    return None


@pyqtSlot(str)
def onImageSaved(filename):
    """Executed when an image (any image) has been saved.
    
    What we do: If the document has a layer called "godot", we create a .png image from each one of its paint layers (excluding the one called "godot").
    """
    document = Krita.instance().activeDocument()
    project_root = getGodotProjectPath(filename)

    with open(f"{tempfile.gettempdir()}/godot_exporter_log.txt","wt") as log:
        log.write("fresh log file opened\n")
        # if there isn't a layer with name "godot" in the image, don't do anything
        layers = getNodesRecursive(document.rootNode())
        godot_layer = None
        for layer in layers:
            layer_name = getJustNameFromLayerName(layer.name())
            if layer_name == "godot":
                godot_layer = layer
        if godot_layer is None:
            log.write("no godot layer found\n")
            return

        # get options in godot layer
        godot_layer_options = getOptionsFromLayerName(godot_layer.name())
        nofolder = False
        if ("nofolder" in godot_layer_options) and (godot_layer_options["nofolder"] == "true"):
            log.write("nofolder option detected in godot layer\n")
            nofolder = True

        # generate images from layers

        Krita.instance().setBatchmode(True)

        # filename is something like .../Player/player.kra
        basename = os.path.basename(filename) # e.g. player.kra
        basename_no_ext = basename[:basename.rfind('.')] # e.g. player
        folder_path = os.path.join(os.path.dirname(filename),basename_no_ext) # e.g. .../Player/player
        base_folder_path = os.path.dirname(filename)

        # clear previous images
        if not nofolder:
            log.write("clearing previous folder (if it exists) and creating a new one\n")
            shutil.rmtree(folder_path,ignore_errors=True)
            os.mkdir(folder_path)

        # generate new images from layers
        for layer in layers:
            layerName = getJustNameFromLayerName(layer.name())
            layerOptions = getOptionsFromLayerName(layer.name())
            if layerName.lower() != 'godot' and layer.type() == 'paintlayer':
                log.write(f"processing layer {layer.name()}\n")
                if "noexport" not in layerOptions: # a layer with {noexport=true} will not be saved as png
                    if "path" in layerOptions:
                        filename = os.path.join(project_root,layerOptions["path"],f'{layerName}.png')
                    elif nofolder:
                        filename = os.path.join(base_folder_path,f'{layerName}.png')
                    else:
                        filename = os.path.join(folder_path,f'{layerName}.png')

                    log.write(f'saving {filename}\n')
                    infoObj = InfoObject()
                    infoObj.setProperty('alpha',True)
                    infoObj.setProperty('compression',5)
                    infoObj.setProperty('forceSRGB',False)
                    infoObj.setProperty('indexed',False)
                    infoObj.setProperty('interlaced',False)
                    infoObj.setProperty('saveSRGBProfile',True)
                    infoObj.setProperty('transparencyFillcolor',[255,255,255])
                    layer.save(filename,1,1,infoObj)
    
    Krita.instance().setBatchmode(False)


class GodotExporter(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        # listen for when any image has been saved
        Krita.instance().notifier().imageSaved.connect(onImageSaved)

# Add the extension to Krita's list of extensions:
Krita.instance().addExtension(GodotExporter(Krita.instance()))