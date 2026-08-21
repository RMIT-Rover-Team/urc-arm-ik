#include <iostream>
#include <chrono>
#include <thread>

//Include your channel type(s)
#include <ChannelLossycast.hpp> 
//#include <ChannelMulticast.hpp>
//#include <ChannelTransactional.hpp>

#include "SimpleController.h"

//The Default Position
const double jointDefaults[6] = {
    0,
    0,
    0,
    0,
    0,
    0
};

//Input Scales
const double jointScales[6] = {
    1,
    1,
    1,
    1,
    1,
    1
};

// Stick Drift Reject Value
const double stickDriftReject = 0.05;

float vabs(float x){
    return x > 0 ? x : -x;
}

float toRadians(float x){
    return (x/180.0)*3.141592;
}

double actualJoints[6];
void directControl(LossyCastPublisher* myPub, SimpleController* myControl){
    //New Message for outgoing
    MessageStructure myMessage = myPub->getNewMessageObject();

    double convSpeed;
    //Read the inputs
    if (true) { // (myControl.axisAvailable(0)){
        //Base joint
        convSpeed = (double)myControl->getAxis(0) / 32768.0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[0] += convSpeed * jointScales[0];
        std::cout << "Base joint pos: " << actualJoints[0] << std::endl;
    }
    if (true) { //(myControl.axisAvailable(1)){
        //Base Up down
        convSpeed = (double)myControl->getAxis(1) / 32768.0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[1] += convSpeed * jointScales[1];
        std::cout << "Elb1 joint pos: " << actualJoints[1] << std::endl;
    }
    if (true) { //(myControl.axisAvailable(3)){
        //Spin
        convSpeed = (double)myControl->getAxis(3) / 32768.0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[4] += convSpeed * jointScales[4];
        std::cout << "Spin joint pos: " << actualJoints[4] << std::endl;
    }
    if (true) { //(myControl.axisAvailable(4)){
        //Elbow
        convSpeed = (double)myControl->getAxis(4) / 32768.0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[2] += convSpeed * jointScales[2];
        std::cout << "Elb2 joint pos: " << actualJoints[2] << std::endl;
    }

    if (true) { //(myControl.buttonAvailable(11)){
        convSpeed = (myControl->getButton(11)) ? -1 : 0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[3] += convSpeed * jointScales[3];
        std::cout << "Wr 2 joint pos: " << actualJoints[3] << std::endl;
    }
    if (true) { //(myControl.buttonAvailable(12)){
        convSpeed = (myControl->getButton(12)) ? 1 : 0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[3] += convSpeed * jointScales[3];
        std::cout << "Wr 2 joint pos: " << actualJoints[3] << std::endl;

    }

    if (true) { //(myControl.buttonAvailable(13)){
        convSpeed = (myControl->getButton(13)) ? 1 : 0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[5] += convSpeed * jointScales[5];
        std::cout << "Wr 1 joint pos: " << actualJoints[5] << std::endl;
    }
    if (true) { //(myControl.buttonAvailable(14)){
        convSpeed = (myControl->getButton(14)) ? -1 : 0;
        convSpeed = (vabs(convSpeed) > stickDriftReject) ? convSpeed : 0;
        actualJoints[5] += convSpeed * jointScales[5];
        std::cout << "Wr 1 joint pos: " << actualJoints[5] << std::endl;
    }

    // Pack and Send
    for (int i = 0; i < 6; i++){
        myMessage.setFloat("jointPositions",toRadians(actualJoints[i]),i);
    }
     myPub->publish(myMessage);
}

double ikpos[3] = {0};
double ikang[3] = {0};
const int readOrder[3] = {0, 1, 4};
void ikControl(LossyCastPublisher* myPub, SimpleController* myControl){
    //New Message for outgoing
    MessageStructure myMessage = myPub->getNewMessageObject();

    // Check if we are in angle or position mode
    if (myControl->getButton(2)){
        printf("Angle Mode\n");

        // Axis are 0, 1, 3, 4
        for (int i = 0; i < 3; i++){
            ikang[i] += (double)myControl->getAxis(readOrder[i]) / 32768.0;
        }
        

    }
    else {
        printf("Position Mode\n");
        for (int i = 0; i < 3; i++){
            ikpos[i] += (double)myControl->getAxis(readOrder[i]) / 32768.0;
        }
    }

    // Send the message
    for (int i = 0; i < 3; i++){
        myMessage.setFloat("endPosition",ikpos[i],i);
        myMessage.setFloat("endOrientation",toRadians(ikang[i]),i);

        printf("IK Index %i Angle %f Pos %f\n",i,ikang[i],ikpos[i]);
    }

    myPub->publish(myMessage);
}



int main(int argc, char *argv[]) {
    // Set Up Controller
    SimpleController myControl(16,16);
    printf("Controller Ready\n");
    
    //Start the Publisher
    LossyCastPublisher myCast("COMFILES/ArmControl.defcom");
    LossyCastPublisher myIKCast("COMFILES/ArmIKControl.defcom");
    printf("Channel Up\n");
    

    // Load the default values into the joints
    for (int i = 0; i < 6; i++){
        actualJoints[i] = jointDefaults[i];
    }

    double convSpeed;
    int IKMode = 0;
    while (true){
        myControl.tick();

        //First Check if Quit button pressed
        if (myControl.buttonAvailable(0)){
            break;
        }

        //If Button 1, then switch to IK
        if (myControl.buttonAvailable(1)){
            //Await unpress
            myControl.getButton(1);
            while (!myControl.buttonAvailable(1));
            myControl.getButton(1);
            IKMode = ~IKMode;
        }


        if (IKMode){
            ikControl(&myIKCast, &myControl);
        }
        else {
            directControl(&myCast, &myControl);
        }

        



        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    return 0;
}