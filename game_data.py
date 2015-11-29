class Location:

    def __init__(self, brief, long):
        '''Creates a new location.

        Data that could be associated with each Location object:
        a position in the world map,
        a brief description,
        a long description,
        a list of available commands/directions to move,
        items that are available in the location,
        and whether or not the location has been visited before.
        Store these as you see fit.

        This is just a suggested starter class for Location.
        You may change/add parameters and the data available for each Location class as you see fit.
  
        The only thing you must NOT change is the name of this class: Location.
        All locations in your game MUST be represented as an instance of this class.
        '''
        self.brief = brief
        self.long = long
        self.visit = False
        self.actions = {}
        self.items = []

    def get_brief_description (self):
        '''Return str brief description of location.'''
        return self.brief

    def get_full_description (self):
        '''Return str long description of location.'''
        return self.long

    def available_actions(self, name, action_val=0):
        '''
        -- Suggested Method (You may remove/modify/rename this as you like) --
        Return list of the available actions in this location.
        The list of actions should depend on the items available in the location
        and the x,y position of this location on the world map.'''
        self.actions[name] = action_val

    def is_visited(self):
        """
        Checks if a location has been visited or not
        :return:
        """
        return self.visit

    def visited(self):
        self.visit = True

class Item:

    def __init__ (self, name, start, target, target_points):
        '''Create item referred to by string name, with integer "start"
        being the integer identifying the item's starting location,
        the integer "target" being the item's target location, and
        integer target_points being the number of points player gets
        if item is deposited in target location.

        This is just a suggested starter class for Item.
        You may change these parameters and the data available for each Item class as you see fit.
        Consider every method in this Item class as a "suggested method":
                -- Suggested Method (You may remove/modify/rename these as you like) --

        The only thing you must NOT change is the name of this class: Item.
        All item objects in your game MUST be represented as an instance of this class.
        '''

        self.name = name
        self.start = start
        self.target = target
        self.target_points = target_points

    def get_starting_location (self):
        '''Return int location where item is first found.'''

        pass

    def get_name(self):
        '''Return the str name of the item.'''

        return self.name

    def get_target_location (self):
        '''Return item's int target location where it should be deposited.'''

        pass

    def get_target_points (self):
        '''Return int points awarded for depositing the item in its target location.'''

        pass

class World:

    def __init__(self, mapdata, locdata, itemdata):
        '''
        Creates a new World object, with a map, and data about every location and item in this game world.

        You may ADD parameters/attributes/methods to this class as you see fit.
        BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES.

        :param mapdata: name of text file containing map data in grid format (integers represent each location, separated by space)
                        map text file MUST be in this format.
                        E.g.
                        1 -1 3
                        4 5 6
                        Where each number represents a different location, and -1 represents an invalid, inaccessible space.
        :param locdata: name of text file containing location data (format left up to you)
        :param itemdata: name of text file containing item data (format left up to you)
        :return:
        '''
        self.map = self.load_map(mapdata) # The map MUST be stored in a nested list as described in the docstring for load_map() below
        # self.locations ... You may choose how to store location and item data.
        self.locations = self.load_locations(locdata) # This data must be stored somewhere. Up to you how you choose to do it...
        #self.load_items(itemdata) # This data must be stored somewhere. Up to you how you choose to do it...

    def load_map(self, filename):
        '''
        THIS FUNCTION MUST NOT BE RENAMED OR REMOVED.
        Store map from filename (map.txt) in the variable "self.map" as a nested list of integers like so:
            1 2 5
            3 -1 4
        becomes [[1,2,5], [3,-1,4]]
        RETURN THIS NEW NESTED LIST.
        :param filename: string that gives name of text file in which map data is located
        :return: return nested list of integers representing map of game world as specified above
        '''
        temp_map = []
        read_file = open(filename, "r")

        for line in read_file:
            temp_map.append([int(i) for i in line.strip().split() if i.isdigit()])

        read_file.close()
        return temp_map

    def load_locations(self, filename):
        '''
        Store all locations from filename (locations.txt) into the variable "self.locations"
        however you think is best.
        Location number is based on order they come in location.txt
        How it reads it:
        brief description
        long description - lines until it reaches END, then starts a new location
        :param filename: name of file containing location data
        :return: list of locations for world class
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
        Store all items from filename (items.txt) into ... whatever you think is best.
        Make sure the Item class is used to represent each item.
        Change this docstring accordingly.
        :param filename:
        :return:
        '''

        pass

    def get_location(self, x, y, surround=False):
        '''Check if location exists at location (x,y) in world map.
        Return Location object associated with this location if it does. Else, return None.
        Remember, locations represented by the number -1 on the map should return None.
        :param x: integer x representing x-coordinate of world map
        :param y: integer y representing y-coordinate of world map
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

            return self.locations[self.map[x][y]]
        else:
            return None