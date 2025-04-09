import os

class Piece:

    def __init__(self, name, color, image=None, image_rect=None):
        self.name=name
        self.color=color
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
        base_val = 1.00 if color == 'white' else -1.00
        square_val = 0.05 if color == 'white' else -0.05

        table = [
            [80,80,80,80,80,80,80,80],
            [10,10,10,10,10,10,10,10],
            [ 2, 2, 4, 6, 6, 2, 2, 0],
            [ 1, 1, 2, 5, 5, 2, 1, 1],
            [ 0, 0, 0, 4, 4, 0, 0, 0],
            [ 1,-1,-2, 0, 0,-2,-1, 1],
            [ 1, 2, 2,-4,-4, 2, 2, 1],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        if color == 'black':
            table.reverse()
        
        self.board = [
            [base_val + square_val * val for val in row] for row in table
        ]

        super().__init__('pawn',color)

class Knight(Piece):

    def __init__(self, color):
        base_val = 3.00 if color == 'white' else -3.00
        square_val = 0.05 if color == 'white' else -0.05

        table = [
            [-9,-8,-6,-6,-6,-6,-8,-9],
            [-8,-4, 0, 0, 0, 0,-4,-8],
            [-6, 0, 2, 3, 3, 2, 0,-6],
            [-6, 0, 3, 4, 4, 3, 0,-6],
            [-6, 0, 3, 4, 4, 3, 0,-6],
            [-6, 0, 2, 3, 3, 2, 0,-6],
            [-8,-4, 0, 0, 0, 0,-4,-8],
            [-9,-8,-6,-6,-6,-6,-8,-9],
        ]

        self.board = [
            [base_val + square_val * val for val in row] for row in table
        ]

        super().__init__('knight', color)

class Bishop(Piece):

    def __init__(self, color):
        base_val = 3.00 if color == 'white' else -3.00
        square_val = 0.05 if color == 'white' else -0.05

        table = [
            [-9,-2,-2,-2,-2,-2,-2,-9],
            [-2, 1, 0, 0, 0, 0, 1,-2],
            [-2, 2, 2, 2, 2, 2, 2,-2],
            [-2, 1, 2, 2, 2, 2, 1,-2],
            [-2, 1, 1, 2, 2, 1, 1,-2],
            [-2, 0, 1, 2, 2, 1, 0,-2],
            [-8,-4, 0, 0, 0, 0,-4,-8],
            [-9,-8,-6,-6,-6,-6,-8,-9],
        ]
        
        if color == 'black':
            table.reverse()

        self.board = [
            [base_val + square_val * val for val in row] for row in table
        ]
        
        super().__init__('bishop',color)

class Rook(Piece):

    def __init__(self, color):
        base_val = 5.00 if color == 'white' else -5.00
        square_val = 0.05 if color == 'white' else -0.05

        table = [
            [ 0, 0, 0, 1, 1, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0,-1],
            [-1, 0, 0, 0, 0, 0, 0,-1],
            [-1, 0, 0, 0, 0, 0, 0,-1],
            [-1, 0, 0, 0, 0, 0, 0,-1],
            [-1, 0, 0, 0, 0, 0, 0,-1],
            [ 1, 2, 2, 2, 2, 2, 2, 1],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        
        if color == 'black':
            table.reverse()

        self.board = [
            [base_val + square_val * val for val in row] for row in table
        ]

        super().__init__('rook',color)

class Queen(Piece):

    def __init__(self, color):
        base_val = 9.00 if color == 'white' else -9.00
        square_val = 0.05 if color == 'white' else -0.05

        table = [
            [-4,-2,-2,-1,-1,-2,-2,-4],
            [-2, 0, 0, 0, 0, 0, 0,-2],
            [-1, 0, 1, 1, 1, 1, 0,-1],
            [-1, 0, 1, 2, 2, 1, 0,-1],
            [-1, 0, 1, 2, 2, 1, 0,-1],
            [-1, 0, 1, 1, 1, 1, 0,-1],
            [-1, 0, 0, 0, 0, 0, 0,-1],
            [-4,-2,-2,-1,-1,-2,-2,-4]
        ]
     
        if color == 'black':
            table.reverse()

        self.board = [
            [base_val + square_val * val for val in row] for row in table
        ]

        super().__init__('queen',color)

class King(Piece):

    def __init__(self, color):
        base_val = 1000.00 if color == 'white' else -1000.00
        square_val = 0.05 if color == 'white' else -0.05

        table = [
            [-6,-8,-8,-8,-8,-8,-8,-6],
            [-6,-8,-8,-8,-8,-8,-8,-6],
            [-6,-8,-8,-8,-8,-8,-8,-6],
            [-6,-8,-8,-8,-8,-8,-8,-6],
            [-4,-6,-6,-8,-8,-6,-6,-4],
            [-2,-4,-4,-4,-4,-4,-4,-2],
            [ 2, 2, 0, 0, 0, 0, 2, 2],
            [ 4, 6, 2, 0, 0, 2, 6, 4]
        ]

        if color == 'black':
            table.reverse()

        self.board = [
            [base_val + square_val * val for val in row] for row in table
        ]

        super().__init__('king',color)
