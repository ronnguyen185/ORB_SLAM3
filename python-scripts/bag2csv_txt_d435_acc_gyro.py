import imp
import sys
import rosbag
import os
import shutil
import time 
import string
import csv

# FILENAME = '20220426_170330.bag'
FILENAME = '2022-05-06-18-23-42.bag'
ROOT_DIR = '/home/ron/Desktop/test'
# BAGFILE = ROOT_DIR + '/' + str(sys.argv[0])
BAGFILE = ROOT_DIR + '/' + FILENAME

numberOfFiles = 0
if __name__ == '__main__':

    bag = rosbag.Bag(BAGFILE)
    print('Succesfully load bag file')
    time.sleep(1)

    for i in range(2):
        if (i == 0):
            TOPIC = '/device_0/sensor_2/Accel_0/imu/data'
            DESCRIPTION = 'acc'
        elif (i == 1):
            TOPIC = '/device_0/sensor_2/Gyro_0/imu/data'
            DESCRIPTION = 'gyro'
        imuContents = bag.read_messages(TOPIC)
        bagName = bag.filename

        # create a new directory
        folder = string.rstrip(bagName, ".bag")
        try:	#else already exists
            os.makedirs(folder)
        except:
            pass
        # shutil.copyfile(bagName, folder + '/' + FILENAME)
        
        # print(folder)

        filename = folder + '/' + DESCRIPTION + '.csv'
        with open(filename, 'w+') as csvfile:
            filewriter = csv.writer(csvfile, delimiter = ',')
            firstIteration = True	#allows header row                
            for subtopic, msg, t in bag.read_messages(TOPIC):
                msgString = str(msg)
                # print(msgString)
                msgList = string.split(msgString, '\n')
                # print(msgList)
                instantListOfData = []
                for nameValuePair in msgList:
                    splitPair = string.split(nameValuePair, ':')
                    for i in range(len(splitPair)):	#should be 0 to 1
                        splitPair[i] = string.strip(splitPair[i])
                    instantListOfData.append(splitPair)
                # print(len(instantListOfData))
                if DESCRIPTION == 'acc':
                    accelListOfData = instantListOfData[18:21] #take the value of linear accel with covariance
                    print(accelListOfData)
                    if firstIteration:	# header
                        headers = ["rosbagTimestamp"]	#first column header
                        for pair in accelListOfData:
                            headers.append(pair[0])
                        filewriter.writerow(headers)
                        firstIteration = False
                    # write the value from each pair to the file
                    seconds = t.to_sec()
                    values = [str(seconds)] #first column will have rosbag timestamp
                    for pair in accelListOfData:
                        if len(pair) > 1:
                            values.append(pair[1])
                    filewriter.writerow(values)
                else: 
                    gyroListOfData = instantListOfData[13:16] #take the value of gyro with covariance
                    print(gyroListOfData)
                    if firstIteration:	# header
                        headers = ["rosbagTimestamp"]	#first column header
                        for pair in gyroListOfData:
                            headers.append(pair[0])
                        filewriter.writerow(headers)
                        firstIteration = False
                    # write the value from each pair to the file
                    seconds = t.to_sec()
                    values = [str(seconds)]	#first column will have rosbag timestamp
                    for pair in gyroListOfData:
                        if len(pair) > 1:
                            values.append(pair[1])
                    filewriter.writerow(values)
            numberOfFiles+=1
        # convert csv to txt 
        output_txt_file = string.replace(filename, '.csv', '.txt')
        with open(output_txt_file, "w") as my_output_file:
            with open(filename,"r") as my_input_file:
                csv_reader = csv.reader(my_input_file)
                next(csv_reader) #skip the header row 
                for row in csv_reader:
                    my_output_file.write(",".join(row)+'\n')
        my_output_file.close()
    bag.close()
print ('Done reading all ' + str(numberOfFiles) + ' bag files.')
    # listOfTopics = []
    # for topic, msg, t in bagContents:
    #    if topic not in listOfTopics:
    #        listOfTopics.append(topic)
    # print(listOfTopics)
