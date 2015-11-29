from game_data import World, Item, Location
from player import Player

if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(1,0, 20) # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]

    while not PLAYER.victory:
        # check for actions and set up location
        location = WORLD.get_location(PLAYER.x, PLAYER.y, True)
        if PLAYER.inventory:
            #for item in PLAYER.inventory:
                #location.available_actions("use {}".format(item.get_name()), item)
            location.available_actions("use [item]")
            location.available_actions("drop [item]")

        # ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        if location.is_visited():
            print("\n" + location.get_brief_description())
        else:
            print("\n" + location.get_full_description())
            location.visited()

        print("What to do? \n")
        print("[menu]", end=" | ")

        for action in sorted(location.actions.keys()):
            print(action, end=" | ")
        choice = input("\nEnter action: ")

        if (choice == "[menu]"):
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            if choice == "look":
                print(location.get_full_description())
                if location.items:
                    print("On the ground there is:")
                    for item in location.items:
                        print(item.get_name())
            elif choice == "inventory":
                for item in PLAYER.inventory:
                    print(item.get_name())
            elif choice == "score":
                print(PLAYER.score)
            elif choice == "quit":
                quit()

        # use item
        elif choice.startswith("use") and len(choice) > 4:
            selection = PLAYER.get_item(choice[4:len(choice)])
            if selection:
                print("{} was used.".format(selection.get_name()))
            else:
                print("'{}' does not exist within you.".format(choice[4:]))
        elif choice.startswith("drop") and len(choice) > 5:
            selection = PLAYER.get_item((choice[5:]))
            if selection:
                print("{} was dropped.".format(selection.get_name()))
                location.items.append(selection)
                # remove item from player

            else:
                print("{} does not exist within you.".format(selection.get_name))
        # movement
        elif choice in location.actions.keys():
            print("You went somewhere!")
            PLAYER.move(location.actions[choice][0], location.actions[choice][1])
        else:
            print("You tried calling out: '{}', but nothing happened.".format(choice))
