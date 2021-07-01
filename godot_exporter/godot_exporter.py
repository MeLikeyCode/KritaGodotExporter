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

@pyqtSlot(str)
def onImageSaved(filename):
    """Executed when an image (any image) has been saved.
    
    What we do: If the document has a layer called "godot", we create a .png image from each one of its paint layers (excluding the one called "godot").
    """
    document = Krita.instance().activeDocument()

    with open(f"{tempfile.gettempdir()}/godot_exporter_log.txt","at") as log:
        # if there is at least one layer with name "godot" in the image
        layers = getNodesRecursive(document.rootNode())
        if any(filter(lambda v : v.name().lower().strip() == 'godot' ,layers)):
            # generate images from layers

            Krita.instance().setBatchmode(True)

            # filename is something like .../Player/player.kra
            basename = os.path.basename(filename) # e.g. player.kra
            basename_no_ext = basename[:basename.rfind('.')] # e.g. player
            folder_path = os.path.join(os.path.dirname(filename),basename_no_ext) # e.g. .../Player/player

            # clear previous images
            shutil.rmtree(folder_path,ignore_errors=True)
            os.mkdir(folder_path)

            # generate new images from layers
            for layer in layers:
                options = getOptionsFromLayerName(layer.name())
                if layer.name().lower().strip() != 'godot' and layer.type() == 'paintlayer':
                    if "noexport" not in options:
                        filename = os.path.join(folder_path,f'{layer.name()}.png')
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