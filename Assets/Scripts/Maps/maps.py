import arcade


layersInitialMap = {
    "Terrain": {
        "use_spatial_hash" : True
    }
}
initalMap = arcade.load_tilemap("Assets/Levels/initial_map.json",1.5,layersInitialMap)
