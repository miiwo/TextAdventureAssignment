class Location:

    def __init__(self, brief, long):
        '''
        Creates an instance of a Location object that has a brief description, and a long description of the location.
        It initializes the available actions in the location, and sets its visited to False.
        :param brief: string containing the brief description of the location
        :param long: string containing the long description of the location
        :return: None
        '''
        self.brief = brief
        self.long = long
        self.visit = False
        self.actions = {}

    def get_brief_description (self):
        '''
        Returns the brief description of the location
        :return: str brief description of location.
        '''
        return self.brief

    def get_full_description (self):
        '''
        Returns long description of the location
        :return: str long description of location.
        '''
        return self.long

    def available_actions(self, name, action_val=0):
        '''
        Adds actions that can be performed at this location.
        :param name: str of an action that can be performed
        :param action_val: value of that action
        :return: None
        '''
        self.actions[name] = action_val

    def is_visited(self):
        """
        Checks if a location has been visited or not
        :return: True or False depending on if location has been visited or not
        """
        return self.visit

    def visited(self):
        '''
        Sets the location to be "visited"
        :return: None
        '''
        self.visit = True

class Item:

    def __init__ (self, name, start, target, target_points, description, use_descript):
        '''
        Create item referred to by string name, with integer "start"
        being the integer identifying the item's starting location,
        the integer "target" being the item's target location, and
        integer target_points being the number of points player gets
        if item is deposited in target location.

        :param name: Name of the item
        :param start: integer of the location position it can be found in at first
        :param target: integer of the location position that it must go to be deposited
        :param target_points: integer that is given when the item reaches its target
        :param description: str describing the item in a location
        :return: None
        '''

        self.name = name
        self.start = start
        self.target = target
        self.target_points = target_points
        self.description = description
        self.use_descript = use_descript.replace("\n", "")

    def get_starting_location (self):
        '''Return int location where item is first found.'''
        return self.start

    def get_name(self):
        '''Return the str name of the item.'''
        return self.name

    def get_target_location (self):
        '''Return item's int target location where it should be deposited.'''
        return self.target

    def get_target_points (self):
        '''Return int points awarded for depositing the item in its target location.'''
        return self.target_points

class World:

    def __init__(self, mapdata, locdata, itemdata):
        '''
        Creates a new World object, with a map, and data about every location and item in this game world.
        :param mapdata: name of text file containing map data in grid format (integers represent each location, separated by space)
                        map text file MUST be in this format.
                        E.g.
                        1 -1 3
                        4 5 6
                        Where each number represents a different location, and -1 represents an invalid, inaccessible space.
        :param locdata: name of text file containing location data
        :param itemdata: name of text file containing item data
        :return: None
        '''
        self.map = self.load_map(mapdata)
        self.locations = self.load_locations(locdata)
        self.items = self.load_items(itemdata)

    def load_map(self, filename):
        '''
        Store map from filename (map.txt) in the variable "self.map" as a nested list of integers like so:
            1 2 5
            3 -1 4
        becomes [[1,2,5], [3,-1,4]]
        :param filename: string that gives name of text file in which map data is located
        :return: return nested list of integers representing map of game world as specified above
        '''
        temp_map = []
        read_file = open(filename, "r")

        for line in read_file:
            temp_map.append([int(i) for i in line.strip().split()])

        read_file.close()
        return temp_map

    def load_locations(self, filename):
        '''
        Store all locations from filename (locations.txt) into the variable "self.locations"
        Location number is based on order they come in location.txt
        How it reads it:
        brief description
        long description - lines until it reaches END, then starts a new location
        :param filename: name of file containing location data
        :return: list of Location objects
        '''

        temp_location = []
        read_file = open(filename, "r")
        for line in read_file:

            brief = line.strip()
            long = next(read_file)

            # for multiple lines in long description
            hold_long = next(read_file)
            while hold_long != "END\n":
                long += hold_long
                hold_long = next(read_file)

            temp_location.append(Location(brief, long))

        read_file.close()
        return temp_location

    def load_items(self, filename):
        '''
        Store all items from filename (items.txt) into a nested list of item information
        :param filename: name of file containing item data
        :return: nested list of item data
        '''

        temp_item = []
        read_item_file = open(filename, "r")
        for line in read_item_file:
            itemlist = line.split("_____")
            temp_item.append(itemlist)
        read_item_file.close()
        return temp_item

    def load_special_items(self, filename):

        spec_item = []
        read_special_file = open(filename, "r")
        for line in read_special_file:
            speciallist = line.split("_____")
            spec_item.append(speciallist)
        read_special_file.close()
        return spec_item

    def get_location(self, x, y, surround=False, player=None):
        '''Check if location exists at location (x,y) in world map.
        Return Location object associated with this location if it does. Else, return None.
        If surround = True, it will check if the surrounding locations exist, and add them to available actions for
        that location
        Ex. if location to the west exists,
        :param x: integer x representing x-coordinate of world map
        :param y: integer y representing y-coordinate of world map
        :param surround: boolean used to check the surroundings of the location.
        :param player: player object representing the Player.
        :return: Return Location object associated with this location if it does. Else, return None.
        '''

        if len(self.map) > x >= 0 and len(self.map[x]) > y >= 0 and self.map[x][y] != -1:

            if surround:
                if self.get_location(x, y + 1):
                    self.locations[self.map[x][y]].available_actions("go east", [0, 1])
                if self.get_location(x, y - 1):
                    self.locations[self.map[x][y]].available_actions("go west", [0, -1])
                if self.get_location(x + 1, y):
                    self.locations[self.map[x][y]].available_actions("go south", [1, 0])
                if self.get_location(x - 1, y):
                    self.locations[self.map[x][y]].available_actions("go north", [-1, 0])

                for i in self.items:
                    if int(i[1]) == self.locations.index(self.get_location(x,y)) and Item(i[0], i[1], i[2], i[3], i[4], i[5]) not in player.inventory:
                        self.locations[self.map[x][y]].available_actions("pick up [item]", i)
                    else:
                        if "pick up [item]" in self.locations[self.map[x][y]].actions:
                            del self.locations[self.map[x][y]].actions["pick up [item]"]

            return self.locations[self.map[x][y]]
        else:
            return None