
# coding=utf-8

import sys
import numpy as np
import matplotlib.pyplot as plt


class dataset:

    # imu_sync = np.zeros((1,7))
    # acc = np.zeros((1,7))
    # gyro = np.zeros((1,7))

    def __init__(self, dirName):
        self.name = dirName
        self.acc = np.zeros((1, 4))
        self.gyro = np.zeros((1, 4))
        self.timesCam = np.zeros((1, 1))

        timesName = self.name + "/cam0/times.txt"
        timeFile = open(timesName, "r")
        i = 0
        next = 0
        for line in timeFile:
            currentline = line.split(",")
            if i%2 == 0:
                self.timesCam[next] = currentline
                next = next + 1
                self.timesCam = np.pad(self.timesCam, ((0, 1), (0, 0)), mode='constant', constant_values=0)
            i = i + 1
            print(i, "/", next)


        accName = self.name + "/IMU/acc.txt"
        accFile = open(accName, "r")
        i = 0
        for line in accFile:
            currentline = line.split(",")
            for j in range(0, 4):
                self.acc[i][j] = currentline[j]
            self.acc = np.pad(self.acc, ((0, 1), (0, 0)), mode='constant', constant_values=0)
            i = i + 1

        gyroName = self.name + "/IMU/gyro.txt"
        gyroFile = open(gyroName, "r")
        i = 0
        for line in gyroFile:
            currentline = line.split(",")
            for j in range(0, 4):
                self.gyro[i][j] = currentline[j]
            self.gyro = np.pad(self.gyro, ((0, 1), (0, 0)), mode='constant', constant_values=0)
            i = i + 1

        self.timesCam = np.delete(self.timesCam, self.timesCam.shape[0] - 1, axis=0)
        self.acc = np.delete(self.acc, self.acc.shape[0] - 1, axis=0)
        self.gyro = np.delete(self.gyro, self.gyro.shape[0] - 1, axis=0)

        print("Finished")

    def interpolate(self):
        print("Start interpolation")
        self.imuSync = np.zeros((self.gyro.shape[0], 7))
        print("shape = ", self.imuSync.shape)

        totAcc = self.acc.shape[0]
        totGyro = self.gyro.shape[0]

        idxAcc = 0
        idxGyro = 0
        print(self.acc[idxAcc][0])
        print(self.gyro[idxGyro][0])
        while (self.acc[idxAcc][0] > self.gyro[idxGyro][0]):
            idxGyro = idxGyro + 1

        idxSync = 0
        while (idxAcc + 1 < totAcc and idxGyro < totGyro):
            # variables for interpolation
            deltaTimeAcc = self.acc[idxAcc + 1, 0] - self.acc[idxAcc, 0]
            deltaAcc = self.acc[idxAcc + 1, 1:4] - self.acc[idxAcc, 1:4]
            while (idxGyro < totGyro and self.acc[idxAcc + 1, 0] >= self.gyro[idxGyro, 0]):
                self.imuSync[idxSync, 0] = self.gyro[idxGyro, 0]
                # Interpolate accelerometer
                self.imuSync[idxSync, 4:7] = self.acc[idxAcc, 1:4] + (
                            self.gyro[idxGyro, 0] - self.acc[idxAcc, 0]) * deltaAcc / deltaTimeAcc

                # Load gyroscope
                self.imuSync[idxSync, 1:4] = self.gyro[idxGyro, 1:4]

                idxGyro = idxGyro + 1
                idxSync = idxSync + 1

            idxAcc = idxAcc + 1

        self.imuSync = np.delete(self.imuSync, range(idxSync, totGyro), axis=0)
        print("Finish interpolation")

    def plotGyro(self):
        for i in range(1, 4):
            plt.plot(self.imuSync[:, 0], self.imuSync[:, i], label=str("gyro ") + str(i))
        plt.xlabel("time (s)")
        plt.ylabel("ang. vel. (rad/s)")
        plt.title("Gyroscope")
        plt.legend()
        plt.show()

    def plotAcc(self):
        for i in range(4, 7):
            plt.plot(self.imuSync[:, 0], self.imuSync[:, i], label=str("acc ") + str(i))
        plt.xlabel("time (s)")
        plt.ylabel("acc (m/s^2)")
        plt.title("Accelerometer")
        plt.legend()
        plt.show()

    def saveSynchronized(self):
        print("start saving sync files")
        imuName = self.name + "/imu0.csv"
        imuFile = open(imuName, "w")
        imuFile.write("#timestamp [s],w_RS_S_x [rad s^-1],w_RS_S_y [rad s^-1],w_RS_S_z [rad s^-1],a_RS_S_x [m s^-2],a_RS_S_y [m s^-2],a_RS_S_z [m s^-2]\n")
        for row in self.imuSync:
            i = 0
            for num in row:
                if i == 0:
                    imuFile.write(str((int)(1e9 * num)))
                    i = 1
                else:
                    imuFile.write("," + str(num))

            imuFile.write("\n")
        print("finish saving sync files")            

    def saveCorrectTimes(self):
        timesName = self.name + "/cam0/corrTimes.txt"
        timesFile = open(timesName, "w")
        print("self.timesCam shape ", self.timesCam.shape)
        for row in self.timesCam:
            i = 0
            for num in row:
                timesFile.write(str((int) (num)))
                timesFile.write("\n")


if __name__ == '__main__':
    if len(sys.argv)!=2 and len(sys.argv)!=3:
        print('Number of arguments != 2 and 3')
        sys.exit()

    dirName = sys.argv[1]
    print('Processing :', dirName)

    myDataset = dataset(dirName)
    myDataset.interpolate()
    myDataset.plotAcc()
    myDataset.saveSynchronized()

    if len(sys.argv)==3:
        myDataset.saveCorrectTimes()
