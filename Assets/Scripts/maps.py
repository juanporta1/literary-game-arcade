import arcade


layersInitialMap = {
    "Terrain": {
        "use_spatial_hash" : True,
        "hit_box_detail": 10
    },
    "Llave": {
        "use_spatial_hash" : True
    }
}
initalMap = arcade.load_tilemap("Assets/Levels/initial_map.json",1.5,layersInitialMap)
