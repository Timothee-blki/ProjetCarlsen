from AI import AI

class Player:

    def __init__(self,color,type):
        self.color = color
        self.type = type
        if self.type == 'AI':
            self.AI = AI(color)
    
    def is_AI(self):
        return self.type == 'AI'
    
    def is_human(self):
        return self.type =='human'
    
    def change_color(self):
        self.color = 'white' if self.color == 'black' else 'black'
        if self.type == 'AI':
            self.AI.color = self.color