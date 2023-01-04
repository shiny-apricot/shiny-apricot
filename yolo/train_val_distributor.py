import os
import shutil
import random
import argparse

parser = argparse.ArgumentParser(description='Distribute images and labels to train, val and test folders')
parser.add_argument('--input_dir', type=str, default='data', help='path to data directory')
parser.add_argument('--output_dir', type=str, default='output', help='name of output directory')
parser.add_argument('--train_ratio', type=float, default=0.8, help='ratio of train images')
parser.add_argument('--test_ratio', type=float, default=0.0, help='ratio of test images')
parser.add_argument('--val_ratio', type=float, default=0.2, help='ratio of val images')

# get files from path directory ending with .jpg
def get_images(path):
    files = []
    for f in os.listdir(path):
        if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.jpg'):
            files.append(f)
    return files


# distribute the images and corresponding labels to train, val and test folders
def distribute(images:list,
               data_dir,
               output_dir,
               train_ratio=0.8, 
               test_ratio=0.0,
               val_ratio=0.2,
               zip=True):
    """
    This function is to distribute the images and corresponding .txt annotion files.
    It is compatible with Yolo training format.

    The file structure is:
        output
        |--images
        |   |--train
        |   |--test
        |   |--val
        |--labels
            |--train
            |--test
            |--val
    """
    copy_images = images.copy()
    all_files = os.listdir(data_dir)
    
    # shuffle image list
    random.shuffle(copy_images)  
    
    # create necessary directories
    output_img_path = os.path.join(output_dir, 'images', 'train')
    output_label_path = os.path.join(output_dir, 'labels', 'train')
     
    output_img_val_path = os.path.join(output_dir, 'images', 'val')
    output_label_val_path = os.path.join(output_dir, 'labels', 'val')
   
    output_img_test_path = os.path.join(output_dir, 'images', 'test')
    output_label_test_path = os.path.join(output_dir, 'images', 'test')
    
    if not os.path.exists(output_img_path):
        os.makedirs(output_img_path)
    if not os.path.exists(output_label_path):
        os.makedirs(output_label_path)
   
    if not os.path.exists(output_img_val_path):
        os.makedirs(output_img_val_path)
    if not os.path.exists(output_label_val_path):
        os.makedirs(output_label_val_path)

    if not os.path.exists(output_img_test_path):
        os.makedirs(output_img_test_path)
    if not os.path.exists(output_label_test_path):
        os.makedirs(output_label_test_path)

        
    # divide the images and labels into train and test sets randomly
    print(train_ratio)
    train_images = random.sample(copy_images, int(len(copy_images)*train_ratio))
    for img in train_images:
        # pop the image from the list
        copy_images.remove(img)
        # get the base name of images
        label = os.path.splitext(img)[0] + '.txt'
        # check if the label exists in the folder
        if label not in all_files:
            print('Label not found for image: ', img)
            continue
        # copy the image and label to the train folder
        shutil.copy(os.path.join(data_dir, img), os.path.join(output_img_path, img))
        shutil.copy(os.path.join(data_dir, label), os.path.join(output_label_path, label))
    
    # create test dataset
    test_ratio_over_left = test_ratio/(test_ratio+val_ratio)
    test_images = random.sample(copy_images, int( len(copy_images)*test_ratio_over_left ))
    for img in test_images:
        copy_images.remove(img)
        label = os.path.splitext(img)[0] + '.txt'
        # check if the label exists in the folder
        if label not in all_files:
            print('Label not found for image: ', img)
            continue
        shutil.copy(os.path.join(data_dir, img), os.path.join(output_img_test_path, img))
        shutil.copy(os.path.join(data_dir, label), os.path.join(output_label_test_path, label))

    for img in copy_images:
        label = os.path.splitext(img)[0] + '.txt'
        # check if the label exists in the folder
        if label not in all_files:
            print('Label not found for image: ', img)
            continue
        shutil.copy(os.path.join(data_dir, img), os.path.join(output_img_val_path, img))
        shutil.copy(os.path.join(data_dir, label), os.path.join(output_label_val_path, label))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # add custom_data.yaml file if exists
    if os.path.exists(f'{base_dir}custom_data.yaml'):
        shutil.copy(f'{base_dir}/custom_data.yaml', 'output/custom_data.yaml')
        
    if zip:
        # zip output folder
        shutil.make_archive(output_dir, 'zip', output_dir)
        
        
if __name__ == '__main__':
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    
    train_ratio = args.train_ratio
    test_ratio = args.test_ratio
    val_ratio = args.val_ratio

    # covnert float
    train_ratio = float(train_ratio)
    test_ratio = float(test_ratio)
    val_ratio = float(val_ratio)
    
    images = get_images(input_dir)
    distribute(images, input_dir, output_dir,  train_ratio, test_ratio, val_ratio)

