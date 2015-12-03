from game_data import World, Item, Location
from player import Player
import winsound

if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(6, 1, 20)

    menu = ["look", "inventory", "score", "quit", "back"]
    choice = ""
    init_item_list = WORLD.load_items('items.txt')
    spec_item_list = WORLD.load_special_items('special.txt')

    item1 = False
    item2 = False
    item3 = False
    locationc = False

    while not PLAYER.victory:
        # check for actions and set up location
        location = WORLD.get_location(PLAYER.x, PLAYER.y, True, PLAYER)

        # depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        # don't print it if the look command was used
        if choice != "looked at":
            if location.is_visited():
                print("\n" + location.get_brief_description())
            else:
                print("\n" + location.get_full_description()[:len(location.get_full_description()) - 1])
                location.visited()

        # print if item in location
        if WORLD.items:
            for items in WORLD.items:
                if int(items[1]) == WORLD.locations.index(location) and items[0] not in [i.name for i in PLAYER.inventory]:
                    print(items[4].replace("\n", ""))
                    location.available_actions("pick up [item]")
        else:
            if "pick up [item]" in location.actions:
                del location.actions["pick up [item]"]

        if PLAYER.inventory:
            location.available_actions("use [item]")
        else:
            if "use [item]" in location.actions:
                del location.actions["use [item]"]

        print("\nWhat to do? \n")
        print("| [menu]", end=" | ")

        for action in sorted(location.actions.keys()):
            print(action, end=" | ")


        choice = input("\nEnter action: ")
        winsound.Beep(1500, 100)
        winsound.Beep(1500, 100)

        # menu options
        if (choice == "[menu]"):
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            if choice == "look":
                print("\n" + location.get_full_description()[:len(location.get_full_description()) - 1])
                choice += "ed at"
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
            for i in init_item_list:
                if i[0] == lchoice[2] and int(i[1]) == WORLD.locations.index(location):
                    for j in WORLD.items:
                        if lchoice[2] == j[0]:
                            print("{} was picked up".format(lchoice[2]))
                            PLAYER.inventory.append(Item(i[0], i[1], i[2], i[3], i[4], i[5]))
                            WORLD.items.remove(init_item_list[init_item_list.index(i)])
                            pickup = True
                            break
            if pickup == False:
                print("You do not see a(n) {} nearby that is able to be picked up".format(lchoice[2]))
        # use item
        elif choice.startswith("use") and len(choice) > 4:
            selection = PLAYER.get_item(choice[4:len(choice)])
            if selection:
                if int(selection.target) == WORLD.locations.index(location):
                    print(selection.use_descript)
                    PLAYER.remove_item(selection)
                    PLAYER.score += int(selection.target_points)
                    for items in WORLD.items:
                        if selection.name is items[0]:
                            WORLD.items.remove(items)
                    for u in spec_item_list:
                        if selection == u[0]:
                            PLAYER.inventory.append(Item(u[1], u[2], u[3], u[4], u[5], u[6]))
                else:
                    print("\nYou tried to use {}, it didn't quite work here.".format(selection.name))
            else:
                print("'{}' does not exist within you.".format(choice[4:]))

        # movement
        elif choice in location.actions.keys():
            print("You went somewhere!")
            PLAYER.move(location.actions[choice][0], location.actions[choice][1])
        else:
            print("You tried calling out: '{}', but nothing happened.".format(choice))

        for itemcheck in PLAYER.inventory:
            if itemcheck.name == "T Card":
                item1 = True
            elif itemcheck.name == "Lucky Pen":
                item2 = True
            elif itemcheck.name == "Cheat Sheet":
                item3 = True
        if WORLD.locations.index(location) == 2:
            locationc = True

        if item1 == True and item2 == True and item3 == True and locationc == True:
            PLAYER.victory = True