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

    #print("You wake up realizing you have an exam in 3 hours. You rush out of bed only to realize you forgot your T Card.\nNot to mention, you can't seem to find your cheat sheet and lucky pen.")
    print("\nYou've got an important exam coming up this evening, and you've been studying for weeks. Last night was a particularly late \nnight on campus. You had difficulty focusing, so rather than staying in one place, you studied in various places throughout the \nbuilding as the night progressed. Unfortunately, when you woke up this morning, you were missing some important exam-\nrelated items. You cannot find your T-card, and you're pretty sure that you're not going to get into tonight's exam without it.\nAlso, you seem to have misplaced your lucky exam pen -- even if they let you in, you can't possibly write with another pen!\nFinally, your instructor for the course is nicer than your CSC108 instructors in that they are allowing you one handwritten page\nof information in the exam. Last night, you painstakingly crammed as much material onto a single page as humanly possible,\nbut that's missing, too! All of this stuff must be around the building somewhere! Can you find all of it before your exam starts tonight?")
    while True:
        # check for actions and set up location
        location = WORLD.get_location(PLAYER.x, PLAYER.y, True, PLAYER)
        if item1 == True and item2 == True and item3 == True and WORLD.locations.index(location) == 2:
            break

        # depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        # don't print it if the look command was used
        if choice != "looked at":
            if location.is_visited():
                print("\n" + location.get_brief_description())
            else:
                print("\n" + location.get_full_description()[:len(location.get_full_description()) - 1])
                location.visited()

        # print item description and allow pick up if item in location
        for items in spec_item_list:
            if int(items[2]) == WORLD.locations.index(location):
                print(items[5])
        if WORLD.items:
            for items in WORLD.items:
                if int(items[1]) == WORLD.locations.index(location) and items[0] not in [i.name for i in PLAYER.inventory]:
                    print(items[4].replace("\n", ""))
                    location.available_actions("pick up [item]")
        else:
            if "pick up [item]" in location.actions:
                del location.actions["pick up [item]"]

        # allow player to use items if they have something in their inventory
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
                print("You have {} pts.".format(PLAYER.score))
            elif choice == "quit":
                quit()

        # pick up command
        elif choice.startswith("pick up") and len(choice) > 8:
            pickup = False
            lchoice = choice.split(' ', 2)
            for item in init_item_list:

                # if the player picks up a valid item in the world at the right location, add it to inventory
                if item[0] == lchoice[2] and int(item[1]) == WORLD.locations.index(location):
                    for location_items in WORLD.items:

                        if lchoice[2] == location_items[0]:
                            print("{} was picked up".format(lchoice[2]))
                            PLAYER.inventory.append(Item(item[0], item[1], item[2], item[3], item[4], item[5]))
                            WORLD.items.remove(init_item_list[init_item_list.index(item)])
                            pickup = True
                            break

            if pickup == False:
                print("You do not see a(n) {} nearby that is able to be picked up".format(lchoice[2]))

        # use item
        elif choice.startswith("use") and len(choice) > 4:
            selection = PLAYER.get_item(choice[4:len(choice)])
            # if there is an item, attempt to use it, and get rid of it has been successfully used
            if selection:
                if int(selection.target) == WORLD.locations.index(location):
                    print(selection.use_descript)
                    PLAYER.remove_item(selection)
                    PLAYER.score += int(selection.target_points)
                    for u in spec_item_list:
                        if selection.name == u[0]:
                            PLAYER.inventory.append(Item(u[1], u[2], u[3], u[4], u[5], u[6]))
                            spec_item_list.remove(u)
                    for items in WORLD.items:
                        if selection.name == items[0]:
                            WORLD.items.remove(items)

                else:
                    print("\nA voice echoes in your head. 'There is a time and place to use {}, but not here.'".format(selection.name))
            else:
                print("'{}' does not exist within you.".format(choice[4:]))

        # movement
        elif choice in location.actions.keys():
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


    print("With only {} left remaining, you made it to the exam room in time with the required items.".format("a few seconds" if PLAYER.max_moves == PLAYER.moves  else "{} minutes".format(PLAYER.max_moves - PLAYER.moves)))
#asdf