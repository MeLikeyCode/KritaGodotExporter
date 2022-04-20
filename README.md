# Krita Godot Exporter

A Krita plugin that makes exporting images drawn/edited in krita to a Godot project as automated as possible.

If your Krita image has a layer called "godot", when you save the image, png files will be created from each layer (except the layer called "godot"). The png files are placed in a folder besides the .kra file. The .png files have the same name as the respective layer.

You can add options in the layer name, inside curly braces, the syntax is like so:
`layerName {option1=value1,option2=value2,option3=value3}`

The following options are supported at this time:
- `path=<path>` specifies the folder to save the layer to. Path is relative to the godot project folder that encompasses the .kra file. By default (i.e. if the path option isn't specified), layers are saved in a folder that is placed besides the .kra file. With this option, you can specifically choose a folder (relative to the godot project) to save the layer to. 
    - example: `player {path=Scenes/Characters}`, will make the layer save to `<GodotProject>/Scenes/Characters/player.png`
- `noexport=true` makes it so the layer does not get exported automatically (i.e. it does not get saved as a png when the .kra file is saved)

## Usefullness
When making art for Godot, you usually draw a bunch of stuff on different layers, and you usually wanna save each layer individually. This plugin will do this automatically, every time you save, thus saving you time. All you need to do is ensure your image has a layer called "godot".
