#include <iostream>

//Include your channel type(s)
//#include <ChannelLossycast.hpp> 
#include <ChannelMulticast.hpp>
//#include <ChannelTransactional.hpp>

int main(int argc, char *argv[]) {
    //Connect to the channel
    MulticastSubscriber subscriber("COMFILES/ArmControl.defcom");

    while (true){
        MessageStructure myMessage = subscriber.subscribe();
        
    }

    //std::cout << "Hello World" << std::endl;
    return 0;
}
