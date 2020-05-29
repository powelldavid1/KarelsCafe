"""
This is my final project for CS106A Code in Place.

Karel's Cafe
Karel will make a drink from a menu, the ingredients will mix around for a bit before becoming more stable.



Special thanks to our instructors Chris Piech, Mehran Sahami, my section leader, Jacob
Lehenbauer and the wonderful community that we were able to create on Ed.

Note: This is the Tea Room.
"""
import tkinter
import random

import time
from PIL import ImageTk
from PIL import Image

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
BORDER = 5

# Ingredients - these are the specific colors see "coffee guide"
# color sources https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm
ESPRESSO = 'brown'
HOT_WATER = 'alice blue'
MILK_FOAM = 'ghost white'
MILK_STEAMED = 'antique white'
CHOCOLATE_SYRUP = 'chocolate'
CREAM_WHIPPED = 'white'
EVERY_THING_NICE = 'purple'
MAGIC_DUST = 'hot pink'
MATCHA = 'lawn green'
MOTOR_OIL = 'black'

#table location
X_START = 300
Y_START = 300
X_END = 600
Y_END = CANVAS_HEIGHT - BORDER

# Standard cups
CUP_THICKNESS = 10
CUP_HEIGHT = 150
CUP_OUTER_DIAMETER = 130
CUP_HANDLE = 60  # distance from cup to inside of handle
CUP_HANDLE_HEIGHT = 70
CUP_HANDLE_OFFSET = 30  # how far down from top of cup for the handle to start
CUP_COLOR = 'orange'
CUP_INNER_DIAMETER = CUP_OUTER_DIAMETER - (2 * CUP_THICKNESS)
CUP_DEPTH = CUP_HEIGHT - CUP_THICKNESS
CUP_X_START = (X_START + X_END) // 2 - CUP_OUTER_DIAMETER // 2
CUP_Y_START = (Y_START + Y_END) // 2 - CUP_HEIGHT // 2

# drink stuff
COLS_DRINK = 10
INGREDIENT_SQUARE = CUP_INNER_DIAMETER // COLS_DRINK
ROWS_DRINK = CUP_DEPTH // INGREDIENT_SQUARE

def main():
    #make the interface
    # make canvas
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Karel's Cafe")
    # putting in two rectangles to make a border
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill='black')
    canvas.create_rectangle(BORDER, BORDER, CANVAS_WIDTH - BORDER, CANVAS_HEIGHT - BORDER, fill='white')

    # our favorite robot
    karel_file = ImageTk.PhotoImage(Image.open('images/karelLarge.png'))
    k_height = karel_file.height()
    karel = canvas.create_image(BORDER + 5, CANVAS_HEIGHT - (BORDER + k_height +5), anchor='nw', image=karel_file)

    # the cafe
    canvas.create_rectangle(X_START, Y_START, X_END, Y_END, fill='gray', tags = 'cafe')
    make_cup(CUP_X_START, CUP_Y_START, canvas)
    # opening animation: move karel from 0,0 in her space to 0,0 in drawing space (bottom left to top left)
    while is_at_top(canvas, karel):
        canvas.move(karel, 0, -3)
        canvas.update()
        time.sleep(1/50)


    #this dictionary is a recipe book with the ingredients in their approximate ratios
    recipe_bk = {}
    recipe_bk['unicorn'] = [MAGIC_DUST, EVERY_THING_NICE, HOT_WATER, CREAM_WHIPPED, CREAM_WHIPPED]
    recipe_bk['cappuccino'] = [ESPRESSO, ESPRESSO, MILK_STEAMED, MILK_FOAM, MILK_FOAM]
    recipe_bk['latte'] = [ESPRESSO, ESPRESSO, MILK_STEAMED, MILK_STEAMED, MILK_FOAM]
    recipe_bk['americano'] = [ESPRESSO, HOT_WATER, HOT_WATER]
    recipe_bk['espresso'] = [ESPRESSO]
    recipe_bk['flat white'] = [ESPRESSO, MILK_STEAMED]
    recipe_bk['matcha'] = [MATCHA, HOT_WATER]
    recipe_bk['milk'] = [MILK_STEAMED, MILK_FOAM, CREAM_WHIPPED]
    recipe_bk['mocha'] = [ESPRESSO, ESPRESSO, CHOCOLATE_SYRUP, MILK_STEAMED]
    recipe_bk['roboccino'] = [MOTOR_OIL, MOTOR_OIL, MOTOR_OIL, ESPRESSO, CREAM_WHIPPED]

    # the menu
    canvas.create_rectangle(CANVAS_WIDTH * 0.5, BORDER, CANVAS_WIDTH - 20, CANVAS_HEIGHT * 0.25)
    canvas.create_text(CANVAS_WIDTH * 0.5 + 15, BORDER + 10, text="Today's Special", anchor='nw',font=('fixedsys', 32, 'italic'))
    menu_items = list(recipe_bk.keys())
    drink_special = menu_items[random.randint(0, len(menu_items))]
    canvas.create_text(CANVAS_WIDTH * 0.5 + 75, BORDER + 100, text=drink_special, anchor='nw', font=('courier', 24, 'bold'))
    print("Welcome to my cafe, here is the menu:")
    for item in range(len(menu_items)):
        print(menu_items[item])


    # new rectangle is made with randomly filled squares in proportion to the ingredients in the selected drink
    order = recipe_bk[input("What can I get you? ")]
    make_drink(CUP_X_START, CUP_Y_START,order,canvas)
    another_drink = input("Would you like something else? y or n ")
    while another_drink != "n":
        order = recipe_bk[input("What can I make for you? ")]
        make_drink(CUP_X_START, CUP_Y_START, order, canvas)
        another_drink = input("Care to try anything else? y or n ")
    canvas.mainloop() #this has to be the last thing, any canvas-y things after this don't get shown


#helper functions for moving karel to the top of the canvas
#will be false when karel is at the end position
def is_at_top(canvas,karel):
    current_y = get_top_y(canvas, karel)
    max_y = BORDER + 3
    return current_y > max_y


#finds the top of the image of karel
def get_top_y(canvas, object):
    return canvas.coords(object)[1]

#creates a flashing image of the "drink ingredients" mixing
def make_drink(x, y, recipe, canvas):
    drink_x = x + CUP_THICKNESS + 1
    drink_y = y + CUP_THICKNESS
    #drink = canvas.create_rectangle(drink_x, drink_y, drink_x + CUP_INNER_DIAMETER - CUP_THICKNESS, drink_y + CUP_DEPTH)
    display_time = 200

    while display_time > 0:
        for row in range(ROWS_DRINK):
            for col in range(COLS_DRINK - 1):
                ing_sqrs(drink_x, drink_y, canvas, row, col, recipe)
        canvas.update()
        display_time -= 10
        time.sleep(1 / 50)

#squares of the ingredient are randomly colored to represent the
def ing_sqrs(drink_x, drink_y, canvas, row, col, recipe):
    x_0 = drink_x + INGREDIENT_SQUARE * col
    y_0 = drink_y + INGREDIENT_SQUARE * row + CUP_DEPTH % INGREDIENT_SQUARE
    x_1 = x_0 + INGREDIENT_SQUARE
    y_1 = y_0 + INGREDIENT_SQUARE
    ingredient_index = random.randint(0, len(recipe) - 1)
    ingredient = recipe[ingredient_index]
    canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=ingredient, outline=ingredient, tags='drink')

#makes a cutaway view of a coffee cup
def make_cup(x, y, canvas):
    p1 = [x, y]
    p2 = [x, y + CUP_HEIGHT]
    p3 = [x + CUP_INNER_DIAMETER, p2[1]]
    p4 = [p3[0], y]
    p5 = [p3[0], p1[1] + CUP_HANDLE_OFFSET]
    p6 = [p5[0] + CUP_HANDLE, p5[1]]
    p7 = [p6[0], p5[1] + CUP_HANDLE_HEIGHT]
    p8 = [p5[0], p7[1]]
    rounded_rectangle(p1[0], p1[1], p2[0], p2[1], CUP_THICKNESS, CUP_COLOR, 'cup1', canvas)
    rounded_rectangle(p2[0], p2[1], p3[0], p3[1], CUP_THICKNESS, CUP_COLOR, 'cup1', canvas)
    rounded_rectangle(p3[0], p3[1], p4[0], p4[1], CUP_THICKNESS, CUP_COLOR, 'cup1', canvas)
    # handle
    rounded_rectangle(p5[0], p5[1], p6[0], p6[1], CUP_THICKNESS, CUP_COLOR, 'cup1', canvas)
    rounded_rectangle(p6[0], p6[1], p7[0], p7[1], CUP_THICKNESS, CUP_COLOR, 'cup1', canvas)
    rounded_rectangle(p7[0], p7[1], p8[0], p8[1], CUP_THICKNESS, CUP_COLOR, 'cup1', canvas)

#makes a rounded rectangle, used to draw the cutaway view of the cup
def rounded_rectangle(start_x, start_y, end_x, end_y, thick, color, tag, canvas):
    offset = thick // 2
    # print(start_x, start_y, end_x, end_y)
    canvas.create_oval(start_x, start_y, start_x + thick, start_y + thick, fill=color, outline=color, tags=tag)
    canvas.create_oval(end_x, end_y, end_x + thick, end_y + thick, fill=color, outline=color, tags=tag)
    if start_x == end_x:
        # for vertical lines
        canvas.create_rectangle(start_x, start_y + offset, end_x + thick, end_y + thick - offset, fill=color,
                                outline=color, tags=tag)
    else:
        # for horizontal lines
        canvas.create_rectangle(start_x + offset, start_y, end_x + thick - offset, end_y + thick, fill=color,
                                outline=color, tags=tag)



######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title=None):

    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

    return canvas


if __name__ == '__main__':
    main()