import arcade


layersInitialMap = {
    "Floor": {
        "use_spatial_hash" : True,
        "hit_box_detail": 10
    },
    "Key": {
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
