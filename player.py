from game_data import Item
class Player:

    def __init__(self, x, y, move):
        '''
        Creates a new Player.
        :param x: x-coordinate of position on map
        :param y: y-coordinate of position on map
        :param move: maximum amount of moves in the game
        :return: None
        '''
        self.x = x
        self.y = y
        self.score = 0
        self.inventory = [Item("Bus Pass", 0, 13, 0, "Your bus pass.", "You have given up on life. You left your life at UTM with {} pts. in tow".format(self.score))]
        self.victory = False
        self.max_moves = move
        self.moves = 0

    def move(self, dx, dy):
        '''
        Given integers dx and dy, move player to new location (self.x + dx, self.y + dy)
        :param dx: amount to move left/right
        :param dy: amount to move up/down
        :return: None

        Example: move(1,0) >> Player object's x is added to 1.
        '''
        self.x += dx
        self.y += dy
        self.moves += 1
        if self.moves == self.max_moves + 1:
            print("The exam started without you. You lose.")
            quit()

    def add_item(self, item):
        '''
        Add item to inventory.
        :param item: item to be added
        :return: None
        '''
        self.inventory.append(Item)


    def remove_item(self, item):
        '''
        Remove item from inventory.
        :param item: item to be removed
        :return: None
        '''
        self.inventory.remove(item)

    def get_item(self, name):
        '''
        Return inventory names.
        :return:
        Example:
        Player.inventory = [Item("Cheese", 1, 2, 30, "It is a great piece of cheese"]
        get_item returns ["Cheese"]
        '''
        for item in self.inventory:
            if item.get_name() == name:
                return item
        return None

    def set_victory(self):
        '''
        Set player's victory to true
        :return: None
        '''
        self.victory = True
