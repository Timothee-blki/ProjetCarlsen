class Square:

    def __init__(self,row,col,piece=None):
        self.row=row
        self.col=col
        self.piece = piece

    def __eq__(self, value):
        return self.row == value.row and self.col == value.col

    def in_board(self):
        return True if 0 <= self.row < 8 and 0 <= self.col < 8 else False

    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return self.piece == None
    
    def has_enemy_piece(self, mycolor):
        return self.piece != None and self.piece.color != mycolor
    
    @staticmethod
    def in_board(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
