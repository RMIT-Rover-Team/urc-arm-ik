#!/usr/bin/env python3
import ikpy
from ikpy.chain import Chain
from ikpy.link import URDFLink
import pybullet as p
import pybullet_data

#IKPY needs a special format so we need to convert from urdf
def convertURDFtoChain():
    p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # Load the URDF
    #robot = p.loadURDF("myactuator_arm_assembly/urdf/myactuator_arm_assembly.urdf", useFixedBase=True)
    robot = p.loadURDF("simplified.urdf", useFixedBase=True)


    num_joints = p.getNumJoints(robot)

    joint_info = []
    for j in range(num_joints):
        info = p.getJointInfo(robot, j)
        joint_type = info[2]
        name = info[1].decode()

        if joint_type == p.JOINT_FIXED:
            continue

        #Need to convert from global to local coordinates
        print
        state = p.getLinkState(robot, j, computeForwardKinematics=True)

        pos = state[0]      #position
        orn = state[1]      #orientation as quaternion

        joint_info.append((name, pos, orn, info[13]))  # axis = info[13]
    
    
    links = []
    for name, pos, orn, axis in joint_info:
        links.append(
            URDFLink(
                name=name,
                origin_translation=pos,
                origin_orientation=p.getEulerFromQuaternion(orn),
                rotation=axis
            )
        )

    chain = Chain(name="robot_chain", links=links)
    return chain

# Import your channel type(s)
#from DEFCOM import ChannelTransactional
#from DEFCOM import ChannelMulticast
#from DEFCOM import ChannelLossyCast


if __name__ == "__main__":
    print("Hello World")
    robot = convertURDFtoChain()
    print("Loaded URDF as chain")
