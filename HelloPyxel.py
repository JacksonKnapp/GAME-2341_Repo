import pyxel

class App:

    def __init__(self):
        pyxel.init(160,120,title="Pyxel Game")
        
        #x and y of a shape
        self.rect_x = 50
        self.rect_y = 50

        pyxel.run(self.update, self.draw)

    def update(self):
        print("Hi")

    def draw(self):
        #change the color of the background
        pyxel.cls(0)
        #x, y what it says, color
        pyxel.text(55,55,"Hello World",8)

        #draw a rectangle
        pyxel.rect(self.rect_x,self.rect_y,10,10,4)

App()
