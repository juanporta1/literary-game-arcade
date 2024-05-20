import arcade

#El tiled no puede tener ningun sprite en blanco, como espacios vacios de un tilemap, porque genera un error. Tener cuidado al pintar en tiled. Si se quiere hacer un sprite invisible editar el .json del mapa.

layersInitialMap = {
    "Floor": {
        "use_spatial_hash" : True
    },
    "Key": {
        "use_spatial_hash" : True
    },
    "EntryDoor":{
        "use_spatial_hash" : True
    },
    "ExitDoor": {
        "use_spatial_hash" : True
    }
}
initalMap = arcade.load_tilemap("Assets/Levels/initial_map.json",1.5,layersInitialMap)

layersInitialMap = {
    "Floor": {
        "use_spatial_hash" : True,
        "hit_box_detail": 10
    }
    
}
levelOne = arcade.load_tilemap("Assets/Levels/levelOne.json",1.5,layersInitialMap)
