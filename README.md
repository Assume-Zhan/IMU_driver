# IMU_driver
> For MPU 6050

### :golf: Before using
- Download the complementary filter for IMU
```bash=1
sudo apt-get install ros-noetic-imu-tools
```
- Git clone the the package for [IMU calibration](https://github.com/sunfu-chou/imu_calib)

  > By [sunfu-chou](https://github.com/sunfu-chou)

- Modify
  
  - In package imu_calib cloned above, modify the file : ```src/apply_calib.cpp```
  
    :warning: In line 80, change the topic name : "corrected" to "/imu/data_raw"
    - Since the filter will subscribe the topic : "/imu/data_raw"
  
### :rocket: Launch file
- **First usage**
  - When you launch the file, the program will ask you to rotate the imu. 
  - After the system tell you 'Saving calibration file... Success!', you can directly shutdown it.
```bash=1
roslaunch imu_driver imu_before.launch
```
- **After**

  After you successfully finished the launch file, you can only run the launch file below each time.
  
  :warning: Before it tell you 'Acceleration calibration complete! (bias = ...', you shouldn't move the IMU

```bash=1
roslaunch imu_driver imu.launch
```
  
### :rocket: Simulation
- Open rviz
```
rviz
```
- In the left bar : Displays -> Global Options -> Fixed Frame
  - Change 'map' to 'world'
- In the left bar : Displays -> Add  (click it)
  - Choose TF to add in it
