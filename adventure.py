from game_data import World, Item, Location
from player import Player

if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(1,0) # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]

    while not PLAYER.victory:
        # check for actions and set up location
        location = WORLD.get_location(PLAYER.x, PLAYER.y, True)
        if PLAYER.inventory:
            #for item in PLAYER.inventory:
                #location.available_actions("use {}".format(item.get_name()), item)
            location.available_actions("use [item]")

        # ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        if location.is_visited():
            print(location.get_brief_description())
        else:
            print(location.get_full_description())
            location.visited()

        print("What to do? \n")
        print("[menu]", end=" | ")
        # only does movement
        for action in sorted(location.actions.keys()):
            print(action, end=" | ")
        choice = input("\nEnter action: ")
        #we're going on a trip

        if (choice == "[menu]"):
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            if choice == "look":
                print(location.get_full_description())
        #use item
        elif choice.startswith("use") and len(choice) > 4:
            selection = PLAYER.get_item(choice[4:len(choice)])
            if selection:
                print("{} was used.".format(selection.get_name()))
            else:
                print("'{}' does not exist within you.".format(choice[4:]))

        elif choice in location.actions.keys():
            print("You went somewhere!")
            PLAYER.move(location.actions[choice][0], location.actions[choice][1])
        else:
            print("You tried calling out: '{}', but nothing happened.".format(choice))

        # CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON USER'S CHOICE
        #    REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if the
        #               choice the user made was just a movement, so only updating player's position is enough to change
        #               the location to the next appropriate location
        # Possibilities: a helper function do_action(WORLD, PLAYER, location, choice)
        # OR A method in World class WORLD.do_action(PLAYER, location, choice)
        # OR Check what type of action it is, then modify only player or location accordingly
        # OR Method in Player class for move or updating inventory
        # OR Method in Location class for updating location item info, or other location data
        # etc....
