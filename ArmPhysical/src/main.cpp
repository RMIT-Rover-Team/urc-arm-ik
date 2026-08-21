#include <iostream>

//Include your channel type(s)
#include <ChannelLossycast.hpp> 
//#include <ChannelMulticast.hpp>
//#include <ChannelTransactional.hpp>

#include "GenericMotor.h"
#include "MyActuatorMotor.h"

#include "SocketCanWrapper.h"

int main(int argc, char *argv[]) {
    //Connect to the channel
    LossyCastSubscriber subscriber("COMFILES/ArmControl.defcom");

    //Create a canbus
    WrappedCANBus* myCan = new WrappedCANBus("can0");

    //The Motors
    GenericMotor* myMotors[6];
    myMotors[0] = new MyActuatorMotor(1, myCan);
    myMotors[1] = new MyActuatorMotor(2, myCan);
    myMotors[2] = new MyActuatorMotor(3, myCan);
    myMotors[3] = new MyActuatorMotor(4, myCan);
    myMotors[4] = new MyActuatorMotor(5, myCan);
    myMotors[5] = new MyActuatorMotor(6, myCan);

    for (int i = 0; i < 6; i++){
        myMotors[i]->calibrate();
    }

    printf("Ready!\n");

    while (true){
        MessageStructure myMessage = subscriber.subscribe();

        //Get all the joint angles
        for (int i = 0; i < 6; i++) {
            double angle = 180*(myMessage.getFloat("jointPositions",i)/3.141592);
            printf("Set J%i to %f\n", i, angle);
            myMotors[i]->setPosition(angle);
        }
        
    }

    //std::cout << "Hello World" << std::endl;
    return 0;
}
