#!/usr/bin/env python3
from DEFCOM import ChannelLossyCast
import tkinter as tk
import math

class slider_app:
    def send_values(self,v=None):
            values = [s.get() for s in self.sliders]
            print("Current joint angles:", values)
            
            #Send a message
            message = self.channel.getNewMessageObject()
            for i in range(len(values)):
                 message.setFloat("jointPositions", math.radians(values[i]),i)
            self.channel.publish(message)



    def __init__(self, n):
        #Start the multicast channel
        self.channel = ChannelLossyCast.LossyCastPublisher("COMFILES/ArmControl.defcom")


        #Set up tkinter
        self.root = tk.Tk()
        self.root.title("Joint Angle Controller")

        self.sliders = []

   

        for i in range(n):
            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"Joint {i+1}")
            label.pack()

            slider = tk.Scale(
                frame,
                from_=0,
                to=360,
                orient=tk.HORIZONTAL,
                length=300,
                command=self.send_values
            )
            slider.pack()
            self.sliders.append(slider)

    

    def run(self):
        self.root.mainloop()





if __name__ == "__main__":
    a = slider_app(6)
    a.run()