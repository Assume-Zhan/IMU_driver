# IMU_driver
> For MPU 6050

### :golf: Before using
- Setup your hardware ---> [watch this](https://blog.gtwang.org/iot/raspberry-pi-mpu6050-six-axis-gyro-accelerometer-1/)
- Download the complementary filter for IMU
```bash=1
sudo apt-get install ros-noetic-imu-tools
```
- Git clone the the package for [IMU calibration](https://github.com/sunfu-chou/imu_calib)

  > By [sunfu-chou](https://github.com/sunfu-chou)
  
- Setup smBus
  > For the i2c communication between IMU and Raspberry pi
```bash=1
sudo apt-get install python3-smbus
```
  
### :rocket: Launch file
- **First usage**
  - When you launch the file, the program will ask you to rotate the imu. 
  - After the system tells you 'Saving calibration file... Success!', you can directly shutdown it.
```bash=1
roslaunch imu_driver imu_before.launch
```
- **After**

  After you successfully finished the launch file, you can only run the launch file below each time.
  
  :warning: Before it tells you 'Acceleration calibration complete! (bias = ...', you shouldn't move the IMU

```bash=1
roslaunch imu_driver imu.launch
```
  
### :rocket: Simulation
- Open rviz
```
rviz
```
- Open the configure file in "rviz/imu_rviz.rviz"

### :eye_speech_bubble: Procedure
- imu_readRaw.py read imu raw data and publish to topic "/raw"
- apply_calib subscribe the topic "/raw", calibrate the raw data and publish to topic "/imu/data_raw"
- madgwick filter subscribe the topic "/imu/data_raw" and publish the filtered data to "/imu/data"

