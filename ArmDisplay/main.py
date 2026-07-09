#!/usr/bin/env python3
import pybullet as p
import pybullet_data

# Import your channel type(s)
from DEFCOM import ChannelMulticast

#Joint Mappings:
ArmJoints = {
    0: 'rev_j0',
    1: 'rev_j1',
    2: 'rev_j2',
    3: 'rev_j3',
    4: 'rev_j4',
    5: 'rev_j5'
}

def main():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # Load the URDF
    robot = p.loadURDF("myactuator_arm_assembly/urdf/myactuator_arm_assembly.urdf", useFixedBase=True)

    # Dump the Joints loaded and build the lookup
    JointLookup = {}
    print("Loaded the following joints from urdf:")
    for i in range(p.getNumJoints(robot)):
        info = p.getJointInfo(robot, i)
        print(i, info[1].decode("utf-8"))
        JointLookup[info[1].decode("utf-8")] = i

    


    # Create the DEFCOM Connection
    channel = ChannelMulticast.MulticastSubscriber('COMFILES/ArmControl.defcom')

    #The main loop
    while True:
        # Get the message
        newPos = channel.subscribe()

        # Get the Joint Positions
        for i in range(6):
            print("Joint",i,ArmJoints[i],JointLookup[ArmJoints[i]], newPos.getFloat("jointPositions",i))
            p.resetJointState(robot, JointLookup[ArmJoints[i]], newPos.getFloat("jointPositions",i))

        #Update the simulation
        p.stepSimulation()
if __name__ == "__main__":
    main()
