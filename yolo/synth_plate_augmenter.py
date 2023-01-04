import albumentations as A
import cv2
import os
import shutil


image_folder = 'data_utils/LP_OCR_ds_false_detections'
augmented_folder = 'data_utils/LP_OCR_ds_false_detections_augmented'

NUM_AUGMENT_VARIATION = 10 # number of augmented images per image

# read '{image_folder}/classes.txt' as list
with open(os.path.join(image_folder, 'classes.txt')) as f:
    classes = f.read().splitlines()

print(f"classes= {classes}")


# This part is important.
# To make the synthetic data similar to real-life data,
# I made a pipeline using "albumentations" library.
# The order of the pipeline is so important.
transform = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.5, contrast_limit=0.5, p=1),
    A.Sequential([
        A.GaussNoise(var_limit=(100.0, 800.0), p=0.9),
        A.PixelDropout (dropout_prob=0.2, p=0.75),
        A.Blur(blur_limit=10, p=1),
        ], p=0.9),
    A.OneOf([
        A.Rotate(limit=4, p=0.6, border_mode=0),
        A.Perspective(scale=(0.02, 0.08), fit_output=True, p=1),
        ]),
    A.Downscale (scale_min=0.1, scale_max=0.8,  p=0.8),
    A.ImageCompression (quality_lower=1, quality_upper=40, p=0.8),
    A.InvertImg(p=0.1),
    ], bbox_params=A.BboxParams(format='yolo', min_visibility=0.99))


if not os.path.exists(augmented_folder):
    os.mkdir(augmented_folder)

file_list = os.listdir(image_folder)
file_list.sort()

img_ext = ('jpg', 'png', 'jpeg')


for file_name in file_list:
    print(f":: {file_name}")

    # continue if it not an image.
    if not file_name.lower().endswith(img_ext):
        continue

    img = cv2.imread( os.path.join(image_folder, file_name) )

    # make different variations of image,
    # in every iteration, a different image will be generated.
    for idx in range(NUM_AUGMENT_VARIATION):
        # get base name of file_name
        base_name = os.path.splitext(file_name)[0]
        new_base_name = os.path.join(augmented_folder, f"{base_name}_{idx}") 
        # copy the annotation file of the image
        annot_file = os.path.join(image_folder, f"{base_name}.txt")

        # fetch bboxes from annotation file 
        # The important part is that:
            # in yolo format, the class is at the beginning of annotation.
            # but albumentation ask for the class to be at the end. (whyyy albumentations whyyy)
            # so we need to shift its place. 
        try:
            with open(annot_file) as f:
                bboxes = f.read().splitlines()
                bboxes = [bbox.split() for bbox in bboxes]
                bboxes = [ [ *list(map(float,bbox[1:])), bbox[0] ] for bbox in bboxes]

            augmented = transform(image=img, bboxes=bboxes, label_fields=classes)
            cv2.imwrite( f"{new_base_name}.png", augmented['image'] )
            # write new annotations into .txt file
            with open(f'{new_base_name}.txt', 'w') as f:
                for bbox in augmented['bboxes']:
                    f.write(f"{bbox[4]} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")
        except Exception as e:
            print(f"Error: {e}")
            continue



