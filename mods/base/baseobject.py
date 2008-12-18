from lib.tile import Tile

class BaseObject(Tile):
    def __init__(self, x, y, board, owner):
        super(BaseObject, self).__init__(x,y,board)
        self.owner = owner
        owner.add_object(self)
    
    def remove_from_board(self):
        self.owner.remove_object(self)
        return super(BaseObject, self).remove_from_board()