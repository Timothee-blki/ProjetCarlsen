
import copy

from const import *
from piece import *
from square import Square
from move import Move

class Board:
  
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(cols)] #Creation des cases mathématiques de l'équiquier sous forme de tableau
        self.last_move = Move(Pawn('white'),Square(-1,-1),Square(-1,-1))
        self._create()
        self._add_piece("white") #on place les pieces blanches
        self._add_piece("black") #on place les pieces noires


### METHODES D'INITIALISATION

    def _create(self):
        '''
        Instancie un objet square à chaque case de l'échiquier
        '''
        for row in range(rows):
            for col in range(cols):
                self.squares[row][col]=Square(row,col)

    def _add_piece(self,color):
        '''
        Ajoute les pieces d'un des joueurs (color) sur l'echiquier à leur case de départ pour débuter la partie
        '''
        (row_pawns,row_others) = (6,7) if color=="white" else (1,0)


        #Pawns
        for col in range(cols):
            self.squares[row_pawns][col] = Square(row_pawns,col, Pawn(color))
            self.squares[row_pawns][col].piece.update_position((row_pawns,col))

        #Knights
        self.squares[row_others][1] = Square(row_pawns,1, Knight(color))
        self.squares[row_others][1].piece.update_position((row_others,1))

        self.squares[row_others][6] = Square(row_pawns,6, Knight(color))
        self.squares[row_others][6].piece.update_position((row_others,6))

        #Bishops
        self.squares [row_others][2] = Square(row_pawns,2, Bishop(color))
        self.squares[row_others][2].piece.update_position((row_others,2))

        self.squares [row_others][5] = Square(row_pawns,5, Bishop(color))
        self.squares[row_others][5].piece.update_position((row_others,5))

        #Rooks
        self.squares [row_others][0] = Square(row_pawns,0, Rook(color))
        self.squares[row_others][0].piece.update_position((row_others,0))

        self.squares [row_others][7] = Square(row_pawns,7, Rook(color))
        self.squares[row_others][7].piece.update_position((row_others,7))

        #Queen
        self.squares [row_others][3] = Square(row_pawns,5, Queen(color))
        self.squares[row_others][3].piece.update_position((row_others,3))

        #King
        self.squares [row_others][4] = Square(row_pawns,4, King(color))
        self.squares[row_others][4].piece.update_position((row_others,4))

    def switch_side(self):
        copy_board = copy.deepcopy(self)
        for row in range(rows):
            for col in range(cols):
                self.squares[row][col] = copy_board.squares[7-row][7-col]

### METHODE DE CALCUL ET MISES A JOUR

    def calculate_score(self):
        score = 0
        for row in range(rows):
            for col in range(cols):
                piece = self.squares[row][col].piece
                if piece != None:
                    piece_value = piece.board[row][col]
                    score += piece_value
        return round(score,3)

    def calculate_all_possible_moves(self,player_color):
        possible_moves=[]
        for row in range(rows):
            for col in range(cols):
                piece = self.squares[row][col].piece
                if piece != None and piece.color == player_color:

                    self.calculate_possible_moves(piece)
                    for move in piece.moves:
                        possible_moves.append(move)

        return possible_moves     

    def calculate_possible_moves(self,piece, check_check=True):
        piece.moves =[]
        row,col = piece.row,piece.col
        piece_name = piece.name

        # Fonction donnant les règles de déplacement des pieces
        def pawn_moves():

            # Avance d'une case
            if Square.in_board(row + piece.dir, col) and self.squares[row + piece.dir][col].is_empty():
                move_row = row + piece.dir
                move_col = col
                move = Move(piece,Square(row, col), Square(move_row, move_col))
                if move_row in [0,7]:
                    move.type = 'promote'
                if not self.will_check(piece, move) if check_check else True:
                    piece.moves.append(move)

                # Avance de deux cases (seulement si la première est vide et le pion n'a pas bougé)
                if not piece.moved and Square.in_board(row + 2 * piece.dir, col) and self.squares[row + 2 * piece.dir][col].is_empty():
                    move_row = row + 2 * piece.dir
                    move_col = col
                    move = Move(piece,Square(row, col), Square(move_row,move_col))
                    if not self.will_check(piece, move) if check_check else True:
                        piece.moves.append(move)

            # Capture diagonale gauche
            if Square.in_board(row + piece.dir, col - 1):
                target_square = self.squares[row + piece.dir][col - 1]
                move_row = row + piece.dir
                move_col = col -1
                move = Move(piece,Square(row, col), Square(move_row,move_col, target_square.piece),'capture')
                if move_row in [0,7]:
                    move.type = 'promote'

                if target_square.has_enemy_piece(piece.color) : #prise classique
                    if not self.will_check(piece, move) if check_check else True:
                        piece.moves.append(move)

                if piece.moved and self.is_en_passant_valid(move) : #prise en passant
                    move.type = 'en passant'
                    if not self.will_check(piece, move) if check_check else True:
                        piece.moves.append(move)

            # Capture diagonale droite
            if Square.in_board(row + piece.dir, col + 1):
                target_square = self.squares[row + piece.dir][col + 1]
                move_row = row + piece.dir
                move_col = col +1
                move = Move(piece,Square(row, col), Square(move_row,move_col, target_square.piece),'capture')
                if move_row in [0,7]:
                    move.type = 'promote'

                if target_square.has_enemy_piece(piece.color): #prise classique
                    if not self.will_check(piece, move) if check_check else True:
                        piece.moves.append(move)

                if piece.moved and self.is_en_passant_valid(move): #prise en passant
                    move.type = 'en passant'
                    if not self.will_check(piece, move) if check_check else True:
                        piece.moves.append(move)

        def knight_moves():
            piece.moves = []
            potential_moves = [
                (row - 2, col - 1), (row - 2, col + 1),
                (row - 1, col - 2), (row - 1, col + 2),
                (row + 1, col - 2), (row + 1, col + 2),
                (row + 2, col - 1), (row + 2, col + 1)
            ]

            for pos in potential_moves:
                move_row, move_col = pos
                if Square.in_board(move_row, move_col):
                    target_square = self.squares[move_row][move_col]

                    if target_square.is_empty() or target_square.has_enemy_piece(piece.color):
                        move_type = "capture" if target_square.has_enemy_piece(piece.color) else "move"
                        move = Move(piece,Square(piece.row, piece.col), Square(move_row, move_col,target_square.piece),move_type)
                        
                        
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)

        def bishop_moves():
            directions = [
                (1, 1),   # Diagonale bas-droite
                (1, -1),  # Diagonale bas-gauche
                (-1, 1),  # Diagonale haut-droite
                (-1, -1)  # Diagonale haut-gauche
            ]

            for direction in directions:

                move_row = piece.row
                move_col = piece.col

                while True:
                    move_row += direction[0]
                    move_col += direction[1]

                    # Vérifier si le mouvement reste dans l'échiquier
                    if not Square.in_board(move_row, move_col):
                        break  # Sortir de la boucle si hors du plateau

                    # Vérifier si la case est libre
                    target_square = self.squares[move_row][move_col]
                    if target_square.is_empty():


                        move = Move(piece,Square(row,col), Square(move_row, move_col,target_square.piece))
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)

                    else:
                        # Verifier si la case a une piece adverse
                        if target_square.has_enemy_piece(piece.color):
                            # On peut capturer cette pièce
                            move = Move(piece,Square(row,col), Square(move_row, move_col,target_square.piece),"capture")
                            if not self.will_check(piece, move) if check_check else True:
                                piece.moves.append(move)


                        break  # Arrêter d'explorer cette direction

        def rook_moves():
            directions = [
                (-1, 0),  # Ligne direction gauche
                (1, 0),   # Ligne direction droite
                (0, 1),   # colonne direction bas
                (0,-1)    # colonne direction haut
            ]

            for direction in directions:

                move_row = piece.row
                move_col = piece.col

                while True:
                    move_row += direction[0]
                    move_col += direction[1]

                    # Vérifier si le mouvement reste dans l'échiquier
                    if not Square.in_board(move_row, move_col):
                        break  # Sortir de la boucle si hors du plateau

                    # Vérifier si la case est libre
                    target_square = self.squares[move_row][move_col]
                    if target_square.is_empty():

                        move = Move(piece,Square(row, col), Square(move_row, move_col))
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)

                    else:
                        # Verifier si la case a une piece adverse
                        if target_square.has_enemy_piece(piece.color):
                            
                            # On peut capturer cette pièce
                            move = Move(piece,Square(row, col), Square(move_row, move_col,target_square.piece),"capture")
                            if not self.will_check(piece, move) if check_check else True:
                                piece.moves.append(move)

                        break  # Arrêter d'explorer cette direction

        def queen_moves():
            directions = [
                (1, 1),   # Diagonale bas-droite
                (1, -1),  # Diagonale bas-gauche
                (-1, 1),  # Diagonale haut-droite
                (-1, -1), # Diagonale haut-gauche
                (-1, 0),  # Ligne direction gauche
                (1, 0),   # Ligne direction droite
                (0, 1),   # colonne direction bas
                (0,-1)    # colonne direction haut                
            ]

            for direction in directions:

                move_row = piece.row
                move_col = piece.col

                while True:
                    move_row += direction[0]
                    move_col += direction[1]

                    # Vérifier si le mouvement reste dans l'échiquier
                    if not Square.in_board(move_row, move_col):
                        break  # Sortir de la boucle si hors du plateau

                    # Vérifier si la case est libre
                    target_square = self.squares[move_row][move_col]
                    if target_square.is_empty():

                        move = Move(piece,Square(row, col), Square(move_row, move_col,target_square.piece))
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)

                    else:
                        # Verifier si la case a une piece adverse
                        if target_square.has_enemy_piece(piece.color):
                            
                            # On peut capturer cette pièce
                            move = Move(piece,Square(row, col), Square(move_row, move_col,target_square.piece),"capture")
                            if not self.will_check(piece, move) if check_check else True:
                                piece.moves.append(move)

                        break  # Arrêter d'explorer cette direction

        def king_moves():
            moves = [
                (row+1, col+1), # Diagonale bas-droite
                (row+1, col-1), # Diagonale bas-gauche
                (row-1, col+1), # Diagonale haut-droite
                (row-1, col-1), # Diagonale haut-gauche
                (row-1, col),   # Ligne direction gauche
                (row+1, col),   # Ligne direction droite
                (row, col+1),   # colonne direction bas
                (row,col-1)     # colonne direction haut                
            ]

            for move in moves:
                if Square.in_board(move[0],move[1]):
                    move_row,move_col = move
                    target_square = self.squares[move_row][move_col]
                    if target_square.is_empty() or target_square.has_enemy_piece(piece.color):
                        
                        #creation des squares du déplacement
                        move_type = "capture" if target_square.has_enemy_piece(piece.color) else "move"
                        move=Move(piece,Square(row,col),Square(move_row,move_col,target_square.piece),move_type)
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)
            
            if not piece.moved and not self.check(piece.color) if check_check else True:
                right_rook = self.squares[row][7].piece if self.squares[row][7].piece != None and self.squares[row][7].piece.name == 'rook' else None
                left_rook = self.squares[row][0].piece if self.squares[row][0].piece != None and self.squares[row][0].piece.name == 'rook' else None
                
                #Roque coté roi
                king_path = [(row,col+1),((row,col+2))]
                if right_rook != None and not right_rook.moved and (not self.is_path_threatened(king_path,piece.color) if check_check else True):
                    for c in range (5,7):
                        if self.squares[row][c].has_piece():
                            break
                    else:
                        #déplacement de la tour
                        move = Move(right_rook,Square(row,right_rook.col),Square(row,5),'none')
                        if not self.will_check(right_rook, move) if check_check else True:
                            right_rook.moves.append(move)

                        #déplacement du roi
                        move = Move(piece,Square(row,col),Square(row,6),'king castle')
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)

                # Roque coté reine
                king_path = [(row,col-1),(row,col-2)]
                if left_rook != None and not left_rook.moved and (not self.is_path_threatened(king_path,piece.color)if check_check else True):
                    for c in range (1,4):
                        if self.squares[row][c].has_piece():
                            break
                    else:
                        #déplacement de la tour 
                        move = Move(left_rook,Square(row,left_rook.col),Square(row,3),'none')
                        if not self.will_check(left_rook, move) if check_check else True:
                            left_rook.moves.append(move)

                        #déplacement du roi
                        move = Move(piece,Square(row,col),Square(row,2),'queen castle')
                        if not self.will_check(piece, move) if check_check else True:
                            piece.moves.append(move)


        #On determine quelle fonction utiliser
        if piece_name =='pawn':pawn_moves()
        if piece_name =='knight':knight_moves()
        if piece_name =='bishop':bishop_moves()        
        if piece_name =='rook':rook_moves()
        if piece_name =='queen': queen_moves()
        if piece_name =='king': king_moves()

    def confirm_move(self,piece,move):
        initial_cell = move.initial_cell
        final_cell = move.final_cell

        #Quel est le type du déplacement ? 
        if move.type == "capture":
            pass
        elif move.type == "queen castle":
            left_rook = self.squares[piece.row][0].piece
            self.confirm_move(left_rook,left_rook.moves[-1])
        elif move.type == "king castle":
            right_rook = self.squares[piece.row][7].piece
            self.confirm_move(right_rook,right_rook.moves[-1])
        elif move.type =="en passant":
            self.squares[initial_cell.row][final_cell.col].piece = None
        
    

        #mise à jour de la position des pieces
        self.squares[initial_cell.row][initial_cell.col].piece = None
        self.squares[final_cell.row][final_cell.col].piece = piece
        piece.update_position((final_cell.row, final_cell.col))

        self.last_move = move
        piece.moved=True

    def valid_move(self,piece,move):
        for possible_move in piece.moves:
            if move == possible_move:
                move.type = possible_move.type
                return True
        return False

        #return move in piece.moves

    def promote(self,piece,row):
        chosen_piece = [
            'rook',
            'queen',
            'knight',
            'bishop',
            'rook',
            'queen',
            'knight',
            'bishop'           
        ]

        self.squares[piece.row][piece.col] = Square(piece.row,piece.col,Piece(chosen_piece[row],piece.color))
        self.squares[piece.row][piece.col].piece.update_position((piece.row,piece.col))

    def check(self,player_color):
        '''
        Retourne True si l'un des moves du joueur adverse met le roi en echec
        Retourne False sinon
        '''
        for row in range(rows):
            for col in range(cols):
                piece = self.squares[row][col].piece

                if piece != None:
                    if  piece.color != player_color:
                        self.calculate_possible_moves(piece,check_check = False)
                        
                        for move in piece.moves:
                            if move.final_cell.piece != None and move.final_cell.piece.name =='king' and move.final_cell.piece.color == player_color:
                                return True
        return False
    
    def will_check(self,piece,move):
        temp_board = copy.deepcopy(self)
        temp_piece = temp_board.squares[piece.row][piece.col].piece

        temp_board.confirm_move(temp_piece,move)
        if temp_board.check(piece.color):
            return True
        return False
    
    def is_path_threatened(self,path,player_color):
        for row in range(rows):
            for col in range(cols):
                piece = self.squares[row][col].piece

                if piece != None:
                    if  piece.color != player_color:
                        self.calculate_possible_moves(piece,check_check=False)
                        
                        for move in piece.moves : 
                            if (move.final_cell.row,move.final_cell.col) in path:
                                return True
        return False

    def is_en_passant_valid(self,move):
        if self.last_move.piece.name =='pawn' and  self.last_move.piece == self.squares[move.initial_cell.row][move.final_cell.col].piece:
            diff = abs(self.last_move.final_cell.row - self.last_move.initial_cell.row) 
            if diff >1:
                return True
        return False
    
    def is_checkmate(self,player_color):
        '''
        Verifie si le joueur correspondant à la couleur donnée est en echec et mat
        '''
        if self.check(player_color) and self.calculate_all_possible_moves(player_color) == []:  
            return True
        return False

    def is_pat(self,player_color):
        if self.calculate_all_possible_moves(player_color) == []:
            return True
        return False

    def is_promoting(self,move):
        if move.type == 'promote':
            return True
        return False
