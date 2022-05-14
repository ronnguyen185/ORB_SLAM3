import os 
import glob 
import cv2 
import numpy as np
from natsort import natsorted

# ###### rename file with 6 leading zeros ########
# ### image0 ###
# images = glob.glob('cam0/infrared_L/*.png') 

# output_dir = 'cam0/image_0'
# if os.path.exists(output_dir):
#     os.rmdir(output_dir)
#     os.mkdir(output_dir)
# else:
#     os.mkdir(output_dir)

# # images = glob.glob('1280_800_30/1612_2020__11_44_59/D455_1/Color/*.jpg')
# images.sort()
# images = natsorted(images)

# cnt = 0 
# for image in images:
#     img = cv2.imread(image)
#     print(image)
#     _, tail = os.path.split(image) 
#     cnt_str = str(cnt)
#     zero_filled_cnt = cnt_str.zfill(6)
#     image_filename = output_dir + '/' + zero_filled_cnt + '.png'
#     img = img.copy()
#     cv2.imwrite(image_filename, img)
#     cnt +=1 

# ## image1 ###
# images = glob.glob('cam0/infrared_R/*.png') 

# output_dir = 'cam0/image_1'
# if os.path.exists(output_dir):
#     os.rmdir(output_dir)
#     os.mkdir(output_dir)
# else:
#     os.mkdir(output_dir)
 
# # images = glob.glob('1280_800_30/1612_2020__11_44_59/D455_1/Color/*.jpg')
# images.sort()
# images = natsorted(images)

# print(len(images))
# cnt = 0 
# for image in images:
#     img = cv2.imread(image)
#     print(image)
#     _, tail = os.path.split(image) 
#     cnt_str = str(cnt)
#     zero_filled_cnt = cnt_str.zfill(6)
#     image_filename = output_dir + '/' + zero_filled_cnt + '.png'
#     img = img.copy()
#     cv2.imwrite(image_filename, img)
#     cnt +=1 

# create a timestamp file 
images = glob.glob('cam0/infrared_R/*.png') 
print(len(images))

time = 0 
with open('cam0/times.txt', 'w') as f:
    for i in range(len(images)+1):
        time += 0.033
        print(time)
        f.write(str(time)+'\n')
    f.close()




