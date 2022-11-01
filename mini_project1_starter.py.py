import os
import msvcrt

symbol_map = [
"""######################""",
"""#  # # ####    #     #""",
"""## #   #    ##   ### #""",
"""#  ## # # # ######   #""",
"""# #s  # # # #      ###""",
"""# ## ##   # # ## # #f#""",
"""#    ## #####  # # # #""",
"""# #     #   ## # # # #""",
"""### # ### ##     ### #""",
"""# # #     #### ### # #""",
"""#   ## ##    #       #""",
"""######################""",
]

# symbol_map = [
# """#####""",
# """#s#f#""",
# """# # #""",
# """#   #""",
# """#####""",
# ]

def create_number_map (sym_arr):
    """
    list -> list
    Interprets all # in sym_arr to 1 and all spaces to 0. So that movement functions know, where
    it is impossible to move. The player is est in position of the start and marked by 2. The
    finish marked by 3.
    """
    num_arr = [[0 for j in range(len(sym_arr[0]))] for i in range(len(sym_arr))]

    for i, element in enumerate(sym_arr):
        for j, subelement in enumerate(element):
            if subelement == '#':
                num_arr[i][j] = 1

    #indicates player's start position with 2 and finish with 3
    for i, element in enumerate(sym_arr):
        for j, subelement in enumerate(element):
            if subelement == 's':
                num_arr[i][j] = 2
            if subelement == 'f':
                num_arr[i][j] = 3

    return num_arr

def create_visible_map(num_arr):
    """
    list -> list
    Marks visible for a player spots with 1 abd invisible with 0
    """
    vis_arr = [[0 for j in range(len(num_arr[0]))] for i in range(len(num_arr))]

    #makes borders of the map visible
    for i in range(len(num_arr[0])):
        vis_arr[0][i] = 1
        vis_arr[len(num_arr) - 1][i] = 1

    for i in range(len(num_arr)):
        vis_arr[i][0] = 1
        vis_arr[i][len(num_arr[0]) - 1] = 1

    #makes finish spot visible
    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 3:
                vis_arr[i][j] = 1

    return vis_arr

def make_player_visible(num_arr, vis_arr):
    """
    (list, list) -> list
    Makes players position and closest spots visible
    """
    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 2:
                for i_videner in range(-1, 2):
                    for j_videner in range(-1, 2):
                        vis_arr[i + i_videner][j + j_videner] = 1

    return vis_arr

def clear_cmd():
    """
    Void -> Void
    Clears command line
    """
    os.system('cls')

def visualise(num_arr, vis_arr):
    """
    (list, list) -> Void
    prints map considering visible spots and players position
    """
    clear_cmd()

    for i, element in enumerate(vis_arr):
        for j, subelement in enumerate(element):
            if subelement == 0:
                print('~', end='')
            elif subelement == 1:
                if num_arr[i][j] == 1:
                    print('#', end='')
                elif num_arr[i][j] == 2:
                    print('@', end='')
                elif num_arr[i][j] == 3:
                    print('F', end='')
                else:
                    print(' ', end='')
        print()

def setup(sym_arr):
    """
    list -> (list, list)
    Creates vis_arr, num_arr
    """
    num_arr = create_number_map(sym_arr)
    vis_arr = create_visible_map(num_arr)
    vis_arr = make_player_visible(num_arr, vis_arr)

    return(num_arr, vis_arr)

def movement(num_arr, vis_arr):
    """
    (list, list) -> (list, list)
    Asks player for letter and depending on answer runs functions to change his position 
    """
    letter = msvcrt.getwch()
#    letter = input('>>> ')
    if letter.upper() == 'W' or letter.upper() == 'Ц':
        num_arr = move_up(num_arr)

    elif letter.upper() == 'S' or letter.upper() == 'І':
        num_arr = move_down(num_arr)

    elif letter.upper() == 'A' or letter.upper() == 'Ф':
        num_arr = move_left(num_arr)

    elif letter.upper() == 'D' or letter.upper() == 'В':
        num_arr = move_right(num_arr)

    else:
        print( "Error!\nYou can use only \n\n   |w|\n|a||s||d|\n")
        print("To stop game pres ctrl+C once more\nInput anything to continue")
        input(">>> ")

    vis_arr = make_player_visible(num_arr, vis_arr)

    return num_arr, vis_arr

def move_up (num_arr):
    """
    list -> list
    Moves player's position up if there is no wall
    """
    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 2 and num_arr[i - 1][j] != 1:
                num_arr[i][j] = 0
                num_arr[i - 1][j] = 2
                return num_arr

    return num_arr

def move_down (num_arr):
    """
    list -> list
    Moves player's position down if there is no wall
    """
    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 2 and num_arr[i + 1][j] != 1:
                num_arr[i][j] = 0
                num_arr[i + 1][j] = 2
                return num_arr

    return num_arr

def move_left (num_arr):
    """
    list -> list
    Moves player's position left if there is no wall
    """
    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 2 and num_arr[i][j - 1] != 1:
                num_arr[i][j] = 0
                num_arr[i][j - 1] = 2
                return num_arr

    return num_arr

def move_right (num_arr):
    """
    list -> list
    Moves player's position right if there is no wall
    """
    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 2 and num_arr[i][j + 1] != 1:
                num_arr[i][j] = 0
                num_arr[i][j + 1] = 2
                return num_arr

    return num_arr

def check_finish(num_arr, sym_arr):
    """
    Returns True if player has reached finish spot
    """
    for i, element in enumerate(sym_arr):
        for j, subelement in enumerate(element):
            if subelement == 'f':
                i_fin = i
                j_fin = j

    for i, element in enumerate(num_arr):
        for j, subelement in enumerate(element):
            if subelement == 2 and i == i_fin and j == j_fin:
                return True
    return False

number_map, visible_map = setup(symbol_map)
visualise(number_map, visible_map)

while check_finish(number_map, symbol_map) is not True:
    number_map, visible_map = movement(number_map, visible_map)

    visualise(number_map, visible_map)

print("You win!")
