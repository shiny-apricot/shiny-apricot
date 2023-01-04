import cv2
import os
import pathlib
import numpy as np
import sys
from pprint import pprint


generation_count = 800

# get the path of the current file
base_path = pathlib.Path(__file__).parent.absolute()
# get the path of the characters folder
char_path = os.path.join(base_path, "characters")
# get characters from the characters folder
characters = os.listdir(char_path)
char_image_path_list = [[char.split("_")[0], char] for char in characters]
# pprint(char_image_path_list)

# read classes.txt as a list    
with open(os.path.join(base_path, "classes.txt"), "r") as f:
    classes = f.read().splitlines()


for _ in range(generation_count):
    ###### CREATE RANDOM PLATE STRING ########
    # create the first part of the plate randomly between 10-99
    first_part = str( np.random.randint(10, 100) )

    len_second = np.random.randint(1, 4)
    second_part = ""
    for i in range(len_second):
        # add a random letter between A-Z to the second part of the plate
        second_part += chr( np.random.randint(65, 91) )

    len_third = np.random.randint(1, 4)
    third_part = ""
    for i in range(len_third):
        # add a random number between 0-9 to the third part of the plate
        third_part += str( np.random.randint(0, 10) )
        
    final_plate_str = first_part + " " + second_part + " " + third_part
    print(f"final plate string: {final_plate_str}")
    ############################################

    # initialize the left offset of the first character
    width_offset = np.random.randint(0, 60)
    HEIGHT_OFFSET = 20
    
    # create a blank canvas
    total_width = len(final_plate_str)*40 + 2*width_offset
    canvas = np.zeros((100, total_width), dtype="uint8")
    canvas.fill(255)

    for char in final_plate_str:
        if char == " ":
            width_offset += 30
            continue
        
        chars_found = []
        # find the char in the char_image_path_list
        for char_in_folder, char_image_path  in char_image_path_list:
            if char_in_folder == char:
                chars_found.append(char_image_path)

        # pick one of the characters randomly
        selected_char_filename = np.random.choice(chars_found)
        
        # get the path of the character
        char_path = os.path.join(base_path, "characters", selected_char_filename)
        
        # get the character image
        char_img = cv2.imread(char_path)
        # turn into grayscale
        char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
        char_height, char_width = char_img.shape
        
        CHAR_HEIGHT = 60
        
        new_char_width = CHAR_HEIGHT*char_width//char_height
        new_char_height=CHAR_HEIGHT
        
        # resize the character image
        char_img = cv2.resize(char_img, (new_char_width, new_char_height))
        
        # print(f"char_img shape: {char_img.shape}")
        # print(f"new_char_width: {new_char_width}")
        # print(f"new_char_height: {new_char_height}")
        # print(f"width offset: {width_offset}")
        # print(f"width_offset+new_char_width : {width_offset+new_char_width }\n")
        
        # add the character to the canvas
        canvas[HEIGHT_OFFSET:HEIGHT_OFFSET+new_char_height, width_offset:width_offset+new_char_width] = char_img
        
        width_offset += new_char_width
        
        char_index = classes.index(selected_char_filename.split("_")[0])
        
        x = (width_offset-new_char_width/2)/canvas.shape[1]
        y = (HEIGHT_OFFSET+new_char_height/2)/canvas.shape[0]
        w = new_char_width/canvas.shape[1]
        h = new_char_height/canvas.shape[0]
        
        # save the bounding box of the character in yolo format and .6f precision
        with open(os.path.join(base_path, "generated_images", final_plate_str+".txt"), "a") as f:
            f.write(f"{char_index} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
        
        width_offset += 5

    # save the canvas
    cv2.imwrite(os.path.join(base_path, "generated_images", final_plate_str+".jpg"), canvas)

    # imshow
    # cv2.imshow("canvas", canvas)
    # cv2.waitKey(0)