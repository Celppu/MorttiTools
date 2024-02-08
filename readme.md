# Mortti bot


## Description
Mortti is puma560 robot arm owned by AS-guild. In this repository you can find python scripts for controlling and simulating the robot arm.

Note: Always simulate before running the robot arm! Shutdown button's wire is shorter than the robot arm's reach 💀
![Alt Text](media/mortti.gif)

## Installation
1. Install python
2. jupyter notebook extensions etc
3. install requirements.txt TODO
4. Get wild with mortti

## Known issues
- Mortti's reach is not enough to press the shutdown button
- Roboticstoolbox uses swift library to render Mortti. There is small filepath parsing bug on windows. 
- Mortti's joint j3 is not limitet to 0-180 degrees. Libraries usually assume this and have to be manually fixed.
(fix file in C:\Users\Emil\AppData\Local\Programs\Python\Python310\Lib\site-packages\rtbdata\xacro\puma560_description\urdf)
```xml
  <joint name="j3" type="revolute">
    <parent link="link3"/>
    <child link="link4"/>
    <origin xyz="${l3_3} 0 ${l3_2}" rpy="0 0 ${M_PI/2}"/><!-- X-forward, Y-Up, Z-right -->
    <axis xyz="0 0 1"/> <!-- This is descibed in child frame -->
    <!--<limit effort="1000.0" lower="${-M_PI/2}" upper="${M_PI/2}" velocity="0"/>-->
    <limit effort="1000.0" lower="${-M_PI}" upper="${M_PI}" velocity="0"/>
  </joint>
```
- Mortti's joint j1 is turned 90 degrees left (+ pi/2) compared to the default puma560 model. This has to be taken into account when using libraries that assume default puma560 model.
- Mortti is slow to reach the target position. This is related to used pid values and feedback being potentiometer based? -> Solution: Do not spam whole trajectory, filter out unnecessary points.

Fix: TODO add link to fix

## Mortti

More info about Mortti and communication protocol can be found from https://github.com/tkln/motor-controller-fw

Example move routes and scripts can be found from
https://github.com/tkln/motor-controller-fw/tree/master/roboscripts

TODO parse these automatically and simulate them