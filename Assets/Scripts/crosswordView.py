import arcade

class CrosswordView(arcade.View):
    def __init__(self, window: arcade.Window,word,crossWords):
        super().__init__(window)
        self.word = word
        self.crossWords = crossWords