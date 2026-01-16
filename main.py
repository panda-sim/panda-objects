import pybullet as p
import pybullet_data
import numpy as np
import os
import time
import config
from objects import objects


# create simulation and place camera
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.resetDebugVisualizerCamera(cameraDistance=config.cameraDistance, 
                                cameraYaw=config.cameraYaw,
                                cameraPitch=config.cameraPitch, 
                                cameraTargetPosition=config.cameraTargetPosition)

# load the objects
plane = objects.PyBulletObject("plane.urdf", basePosition=[0, 0, -0.625])
table = objects.PyBulletObject("table/table.urdf", basePosition=[0.5, 0, -0.625])
cube = objects.SimpleObject("cube.urdf", basePosition=[0.5, 0.1, 0.05])
banana = objects.YCBObject("011_banana.urdf", basePosition=[0.5, -0.2, 0.05])
cabinet = objects.CollabObject("cabinet.urdf", basePosition=[0.9, 0.0, 0.2], baseOrientation=p.getQuaternionFromEuler([0, 0, np.pi]))

# load the robot and set its home position
urdfRootPath = pybullet_data.getDataPath()
panda = p.loadURDF(os.path.join(urdfRootPath,"franka_panda/panda.urdf"), 
                        basePosition=config.baseStartPosition,
                        baseOrientation=p.getQuaternionFromEuler(config.baseStartOrientationE),
                        useFixedBase=True)
jointStartPositions = config.jointStartPositions
for idx in range(len(jointStartPositions)):
    p.resetJointState(panda, idx, jointStartPositions[idx])

# run simulation
while True:
    cube_state = cube.get_state()
    banana_state = banana.get_state()
    cabinet_state = cabinet.get_state()
    p.stepSimulation()
    time.sleep(config.control_dt)