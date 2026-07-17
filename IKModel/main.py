#!/usr/bin/env python3
import ikpy
from ikpy.chain import Chain
from ikpy.link import URDFLink
import pybullet as p
import pybullet_data
from DEFCOM import ChannelMulticast
import numpy as np
from ikpy.utils import geometry
import time

class motionplanner:
    def __init__(self):
        print("Loading URDF")
        self.chain = self.convertURDFtoChain()
        print("URDF Loaded and converted to chain")


    # Cartesian X, Y, Z for the arm to home to
    def translatePosToAngles(self,x,y,z) -> list[float]:
        angles = self.chain.inverse_kinematics([x,y,z])
        print(angles)
        return angles

    # Cartesian X Y Z with orientation too as roll pitch yaw
    def translatePosOrientToAngles(self, x, y, z, rl, pt, yw):
        #Need to convert to a rotation matrix 4x4
        rot = geometry.rpy_matrix(rl, pt, yw)

        target_frame = np.eye(4)
        target_frame[:3, :3] = rot
        target_frame[:3, 3] = [x, y, z]

        angles = self.chain.inverse_kinematics_frame(
            target=target_frame,
            orientation_mode="all"
        )

        print(angles)
        return angles


    #IKPY needs a special format so we need to convert from urdf
    def convertURDFtoChain(self):
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

            #if joint_type == p.JOINT_FIXED:
            #    continue

            #Need to convert from global to local coordinates
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


class IKServer:
    def __init__(self, planner: motionplanner):
        self.inChannel = ChannelMulticast.MulticastSubscriber("COMFILES/ArmIKControl.defcom")
        self.outChannel = ChannelMulticast.MulticastPublisher("COMFILES/ArmControl.defcom")
        self.planner = planner

    def run(self):
        last = time.time()
        while True:
            target = self.inChannel.subscribe()

            # We throttle to 100ms
            now = time.time()
            if (now - last) > 0.1:
                last = now

                #Compute the angles
                #angles = self.planner.translatePosOrientToAngles(
                #    target.getFloat('endPosition',0), target.getFloat('endPosition',1), target.getFloat('endPosition',2), 
                #    target.getFloat('endOrientation',0), target.getFloat('endOrientation',1), target.getFloat('endOrientation',2)
                #    )
                angles = self.planner.translatePosToAngles(target.getFloat('endPosition',0), target.getFloat('endPosition',1), target.getFloat('endPosition',2))

                outgoing = self.outChannel.getNewMessageObject()

                for i, a in enumerate(angles):
                    outgoing.setFloat("jointPositions",a,i)
                print(angles)

                #Send the message
                self.outChannel.publish(outgoing)


if __name__ == "__main__":
    plan = motionplanner()

    print("Self Test")
    plan.translatePosToAngles(1,2,3)
    plan.translatePosOrientToAngles(4,5,6,0.4, 0.3, 0.1)

    print("Starting Comms")
    srv = IKServer(plan)
    srv.run()

