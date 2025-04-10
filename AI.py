import random as rd

from move import Move
from square import Square


class AI():

    def __init__(self,color):
        self.color = color

    def random_choose(self,board):
        possible_moves = board.calculate_all_possible_moves(self.color) 
        if len(possible_moves)>0:
            random_move = rd.choice(possible_moves)
            return random_move
        else:
            return Move(None,Square(0,0),Square(0,0))
        
    def choose_promotion(self,move):
        possible_promotion = [
                 0, #Tour
                 1, #Reine
                 2, #Cavalier
                 3, #Fou
                    ]
        promotion_choice = rd.choice(possible_promotion)
        return promotion_choice
        


    def minimax(self,depth):
        pass
