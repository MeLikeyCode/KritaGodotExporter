# Krita Godot Exporter

A Krita plugin that makes exporting images drawn/edited in krita to a Godot project as automated as possible (happens upon saving the image).

If your Krita image has a layer called "godot", when you save the image, png files will be created from each layer (except the layer called "godot"). By default (see options below), the png files are placed in a folder besides the saved .kra file. The .png files have the same name as the respective layer.

You can add options in the layer names, inside curly braces, the syntax is like so:
`layerName {option1=value1,option2=value2,option3=value3}`

The options control where the layer is saved (as well as if it is saved at all). Future options might do additional things.

The following options are currently supported in the layer names at this time:
- `noexport=true` makes it so the layer does not get exported automatically (i.e. it does not get saved as a png when the .kra file is saved)
- `nofolder=true` put this option in the layer named "godot" if you want the layers to be saved in the same folder as the saved .kra file instead of in their own dedicated sub-folder. This option only has an affect if it is put in the layer named "godot".
- `path=<path>` specifies the folder to save the layer to. Path is relative to the godot project folder that encompasses the saved .kra file.
    - example: a layer name of `player {path=Scenes/Characters}`, will make the layer save to `<GodotProject>/Scenes/Characters/player.png`


## Usefullness
When making art for Godot, you usually draw a bunch of stuff on different layers, and you usually wanna save each layer individually. This plugin will do this automatically, every time you save, thus saving you time. All you need to do is ensure your image has a layer called "godot". Options (which can be embedded in layer names) allow for some flexibility to the default behavior.
