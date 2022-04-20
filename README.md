# Krita Godot Exporter

A Krita plugin. If your image has a layer called "godot", when you save it, png files will be created from each layer (except the layer called "godot"). The png files are placed in a folder besides the .kra file. The .png files have the same name as the respective layer.

If you don't want a layer to be exported, add the following somewhere in the layer name: `{noexport=true}`

## Usefullness
When making art for Godot, you usually draw a bunch of stuff on different layers, and you usually wanna save each layer individually. This plugin will do this automatically, every time you save, thus saving you time. All you need to do is ensure your image has a layer called "godot".
