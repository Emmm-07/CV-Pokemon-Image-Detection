import os

label_dir_path = 'data/labels/train'
image_dir_path = 'data/images/train'


files = os.listdir(label_dir_path)
label_list = []

for file in files:
    label_list.append(file[:-4])

print(label_list)


for image in os.listdir(image_dir_path):
    if image[:-4] not in label_list:
        os.remove(f"{image_dir_path}/{image}")

for image in os.listdir(image_dir_path):
    print(image)


print("length: ",len(os.listdir(image_dir_path)))