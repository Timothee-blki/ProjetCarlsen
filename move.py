
class Move :

    def __init__(self,piece,initial_cell,final_cell,type = 'move'):
        self.piece = piece
        self.initial_cell = initial_cell
        self.final_cell = final_cell
        self.type = type

    def __eq__(self, value):
        return self.initial_cell == value.initial_cell and self.final_cell == value.final_cell