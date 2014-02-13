class Config():
    def __init__(self, tilemap, screensize):
        self.isFullScreen = False
        self.bigWidth = tilemap.width * tilemap.tile_width
        self.bigHeight = tilemap.height * tilemap.tile_height
        self.screensize = screensize
        self.xtiles = tilemap.tile_width # how many grid tiles for x axis
        self.ytiles = tilemap.tile_height # how many grid tiles for y axis
        self.title = "prototype"
        self.scrollstepx = 1 # how many pixels to scroll when pressing cursor key
        self.scrollstepy = 1 # how many pixels to scroll when pressing cursor key
        self.cornerpoint = [0, 0] # left upper edge of visible screen rect inside bigmap