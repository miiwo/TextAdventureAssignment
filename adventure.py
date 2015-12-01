from game_data import World, Item, Location
from player import Player

if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(1,0, 20) # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]

    init_item_list = WORLD.load_items('items.txt')

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
            print("\n" + location.get_brief_description())
        else:
            print("\n" + location.get_full_description())
            location.visited()
        #print if item
        for items in WORLD.items:
            if int(items[1]) == WORLD.locations.index(location) and items[0] not in [i.name for i in PLAYER.inventory]:
                print(items[4])

        print("What to do? \n")
        print("| [menu]", end=" | ")

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

        elif choice.startswith("pick up") and len(choice) > 8:
            pickup = False
            lchoice = choice.split(' ', 2)
            for i in WORLD.items:
                if i[0] == lchoice[2] and int(i[1]) == WORLD.locations.index(location):
                    for j in init_item_list:
                        if lchoice[2] == j[0]:
                            print("{} was picked up".format(lchoice[2]))
                            PLAYER.inventory.append(Item(i[0], i[1], i[2], i[3], i[4]))
                            init_item_list.remove(WORLD.items[WORLD.items.index(i)])
                            pickup = True
            if pickup == False:
                print("You do not see a(n) {} nearby that is able to be picked up".format(lchoice[2]))
        # use item
        elif choice.startswith("use") and len(choice) > 4:
            selection = PLAYER.get_item(choice[4:len(choice)])
            if selection:
                if int(selection.target) == WORLD.locations.index(location):
                    print("{} was used.".format(selection.get_name()))
                    PLAYER.remove_item(selection)
                    PLAYER.score += int(selection.target_points)
                    for items in WORLD.items:
                        if selection.name is items[0]:
                            WORLD.items.remove(items)
            else:
                print("'{}' does not exist within you.".format(choice[4:]))
        # movement
        elif choice in location.actions.keys():
            print("You went somewhere!")
            PLAYER.move(location.actions[choice][0], location.actions[choice][1])
        else:
            print("You tried calling out: '{}', but nothing happened.".format(choice))


