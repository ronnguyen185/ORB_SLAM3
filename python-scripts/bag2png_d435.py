import sys
import subprocess
import yaml
import rosbag
import cv2
import os 
from cv_bridge import CvBridge
import numpy as np
import shutil
import time
import string

# shutil.rmtree('color')
# shutil.rmtree('infrared_L')
# shutil.rmtree('infrared_R')

# os.rmdir('color')
# os.mkdir('color infrared_L infrared_R')
# os.mkdir('infrared_L')
# os.mkdir('infrared_R')
# FILENAME = '20220426_170330.bag'
FILENAME = '2022-05-11-16-45-06.bag'
ROOT_DIR = '/home/quangnm/Desktop/rosbag_file/'



# BAGFILE = ROOT_DIR + '/' + str(sys.argv[0])
BAGFILE = ROOT_DIR + '/' + FILENAME

if __name__ == '__main__':
    bag = rosbag.Bag(BAGFILE)
    print('Succesfully load bag file')
    bagName = bag.filename
    time.sleep(1)

    # create a new directory
    folder = string.rstrip(bagName, ".bag")
    try:	#else already exists
        os.makedirs(folder)
    except:
        pass

    output_color1_dir = folder + '/color1'
    output_color2_dir = folder + '/color2'
    output_infrared_L_dir = folder + '/infrared_L'
    output_infrared_R_dir = folder + '/infrared_R'

    if os.path.exists(output_color1_dir):
        shutil.rmtree(output_color1_dir)
        os.mkdir(output_color1_dir)
    else:
        os.mkdir(output_color1_dir)

    if os.path.exists(output_color2_dir):
        shutil.rmtree(output_color2_dir)
        os.mkdir(output_color2_dir)
    else:
        os.mkdir(output_color2_dir)


    if os.path.exists(output_infrared_L_dir):
        shutil.rmtree(output_infrared_L_dir)
        os.mkdir(output_infrared_L_dir)
    else:
        os.mkdir(output_infrared_L_dir)

    if os.path.exists(output_infrared_R_dir):
        shutil.rmtree(output_infrared_R_dir)
        os.mkdir(output_infrared_R_dir)
    else:
        os.mkdir(output_infrared_R_dir)

    for i in range(4):
        if (i == 1):
            TOPIC = '/camera/infra1/image_rect_raw/compressed'
            DESCRIPTION = 'IR_L_'
        elif (i == 2):
            TOPIC = '/camera/infra2/image_rect_raw/compressed'
            DESCRIPTION = 'IR_R_'
        elif (i == 3):
            TOPIC = '/camera/color/image_raw/compressed'
            DESCRIPTION = 'color1_'
        else:
            TOPIC = '/cv_camera/image_raw/compressed'
            DESCRIPTION = "color2_"
        image_topic = bag.read_messages(TOPIC)
        # print('image topic' + image_topic)
        for k, b in enumerate(image_topic):
            bridge = CvBridge()
            if DESCRIPTION == 'color1_':
                print('encoding compressed imgmsg')
                cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding="passthrough")  #color not work
                # cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
                cv_image.astype(np.uint8)
                # im_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                cv2.imwrite(output_color1_dir + '/' + str(b.timestamp) + '.png', cv_image)
            if DESCRIPTION == 'color2_':
                print('encoding compressed imgmsg')
                cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding="passthrough")  #color not work
                # cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
                cv_image.astype(np.uint8)
                # im_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                cv2.imwrite(output_color2_dir + '/' + str(b.timestamp) + '.png', cv_image)
            elif DESCRIPTION == 'IR_L_':
                # continue
                print('encoding imgmsg IR_L')
                cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding="passthrough")
                # cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
                cv_image.astype(np.uint8)
                cv2.imwrite(output_infrared_L_dir + '/' + str(b.timestamp) + '.png', cv_image)
            elif DESCRIPTION == 'IR_R_':
                # continue
                print('encoding imgmsg IR_R')
                cv_image = bridge.compressed_imgmsg_to_cv2(b.message, desired_encoding="passthrough")
                # cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
                cv_image.astype(np.uint8)
                cv2.imwrite(output_infrared_R_dir + '/' + str(b.timestamp) + '.png', cv_image)                
            # if (DESCRIPTION == 'IR_L'):
            #     # continue
            #     # depth_colormap = cv2.aplyColorMap(cv2.convertScaleAbs(cv_image, alpha=0.03), cv2.COLORMAP_JET)
            #     print('IR_L')
            #     cv2.imwrite(ROOT_DIR + '/infrared_L/' + DESCRIPTION + str(b.timestamp) + '.png', cv_image)
            # elif (DESCRIPTION == 'IR_R'):
            #     # continue
            #     # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(cv_image, alpha=0.03), cv2.COLORMAP_JET)
            #     print('IR_R')
            #     cv2.imwrite(ROOT_DIR + '/infrared_R/' + DESCRIPTION + str(b.timestamp) + '.png', cv_image)                
            # elif (DESCRIPTION == 'color'):
            #     print('color')
            #     cv2.imwrite(ROOT_DIR + '/color/' + DESCRIPTION + str(b.timestamp) + '.png', cv_image)
            print('saved: ' + DESCRIPTION + str(b.timestamp) + '.png')


    bag.close()

    print('PROCESS COMPLETE')
