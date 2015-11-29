from game_data import Item
class Player:

    def __init__(self, x, y, move):
        '''
        Creates a new Player.
        :param x: x-coordinate of position on map
        :param y: y-coordinate of position on map
        :param move: maximum amount of moves in the game
        :return:

        This is a suggested starter class for Player.
        You may add new parameters / attributes / methods to this class as you see fit.
        Consider every method in this Player class as a "suggested method":
                -- Suggested Method (You may remove/modify/rename these as you like) --
        '''
        self.x = x
        self.y = y
        self.score = 0
        self.inventory = [Item("TCard", 2, 5, 10),Item("CCard", 2, 5, 10),Item("BCard", 2, 5, 10)]
        self.victory = False
        self.max_moves = move
        self.moves = 0

    def move(self, dx, dy):
        '''
        Given integers dx and dy, move player to new location (self.x + dx, self.y + dy)
        :param dx: amount to move left/right
        :param dy: amount to move up/down
        '''
        self.x += dx
        self.y += dy
        self.moves += 1
        if self.moves == self.max_moves:
            print("You could not get in on time. You lose.")
            quit()

    def add_item(self, item):
        '''
        Add item to inventory.
        :param item:
        :return:
        '''

    def remove_item(self, item):
        '''
        Remove item from inventory.
        :param item:
        :return:
        '''

    def get_inventory(self):
        '''
        Return inventory.
        :return:
        '''
    def get_item(self, name):
        for item in self.inventory:
            if item.get_name() == name:
                return item
        return None

    def set_victory(self):
        self.victory = True
