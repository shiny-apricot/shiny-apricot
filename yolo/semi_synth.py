import cv2
import os
import pathlib
import numpy as np
import sys
from PIL import ImageFont, Image, ImageDraw


generate_count = 1

# get the path of the current file
base_path = pathlib.Path(__file__).parent.absolute()

# get the .ttf files
fonts_path = os.path.join(base_path, "fonts")
fonts = os.listdir(fonts_path)

font_list = []
# read the .ttf files
for font in fonts:
    font_path = os.path.join(fonts_path, font)
    font = ImageFont.truetype(font_path, 32)
    font_list.append(font)


char_list = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)] + [" "]*10

# save char_list as labels.txt
with open("labels.txt", "w") as f:
    for char in char_list[:-1]:
        f.write(char)
        f.write("\n")

for i in range(generate_count):
    # choose the number of total character between 8-12
    num_char = np.random.randint(5, 12)

    plate_str = ""
    for j in range(num_char):
        # choose a character from char_list
        char = np.random.choice(char_list)
        plate_str += char
    
    # create a blank image in shape of a license plate
    img = np.zeros((64, 256, 3), dtype=np.uint8)
    img.fill(255)    

    offset=0
    # iterate plate_str
    for index, char in enumerate(plate_str):
        # choose a font from font_list
        font = np.random.choice(font_list)
        if char == " ":
            # calculate offset size for space
            w, h = font.getsize(char)
            offset += w
            continue
        
        # get the width of the character 
        w, h = font.getsize(char)
        
        # if the offset is greater than the width of the image, break the loop
        if offset + w > img.shape[1]:
            break
        
        # draw the character on the image
        #TODO: do in numpy
        

        # calculate the middle x,y of the character in the image
        x = offset + w/2
        # calculate y with the adjusted height  
        y = img.shape[0]/2 - h/2
                
        offset += w                
        
        # hold the bounding box of the character in yolo format as a numpy array
        # along with the index of the character
        index = char_list.index(char)
        # convert x,y,w,h to relative values
        x /= img.shape[1]
        y /= img.shape[0]
        w /= img.shape[1]
        h /= img.shape[0]
        bbox = np.array([index, x, y, w, h])
        
        # save the bounding box in the text file named as the plate_str
        # mkdir if not exists
        if not os.path.exists("generated_images"):
            os.mkdir("generated_images")
        with open("generated_images/" + plate_str + ".txt", "a") as f:
            # save float with 6 decimal places
            np.savetxt(f, bbox.reshape(1,5), fmt="%d %.6f %.6f %.6f %.6f")

    
    # save the image
    cv2.imwrite("generated_images/" + plate_str + ".jpg", img)
        

        
            
    





