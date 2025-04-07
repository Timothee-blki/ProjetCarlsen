import os

class Piece:

    def __init__(self, name, color, value, image=None, image_rect=None):
        self.name=name
        self.color=color
        self.value = value
        self.image = image
        self.image_rect = image_rect
        self.set_image()
        self.moved = False
        self.moves = []

    def set_image(self):
        '''
        Methode pour donner l'image correspondante à la piece
        '''
        self.image = os.path.join(f'images/{self.color}_{self.name}.png')
    
    def update_position(self,position):
        '''
        Methode pour mettre à jour la position d'une piece 
        '''
        self.row = position[0]
        self.col = position[1]
        self.moves = []
        
class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == "white" else 1
        super().__init__('pawn',color, 1.0)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight',color, 3.0)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop',color, 3.0)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook',color, 5.0)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen',color, 9.0)

class King(Piece):

    def __init__(self, color):
        super().__init__('king',color, 100000.0)
