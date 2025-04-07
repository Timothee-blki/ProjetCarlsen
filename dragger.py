import pygame 

class Dragger:

    def __init__(self):
        self.dragging = False
        self.piece = None

        self.x = 0
        self.y = 0

    def update_drag_position(self,position,player_color):
            self.x,self.y = position

    def start_drag(self,sel_piece):
        self.dragging = True
        self.piece = sel_piece

    def stop_drag(self):
        self.dragging = False
        self.piece = None

    def show_drag(self,surface):

        img = pygame.image.load(self.piece.image)
        self.piece.image_rect = img.get_rect(center = (self.x,self.y)) 
        surface.blit(img, self.piece.image_rect) #affiche l'image
