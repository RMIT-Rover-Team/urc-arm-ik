#!/usr/bin/env python3

# Import your channel type(s)
#from DEFCOM import ChannelTransactional
#from DEFCOM import ChannelMulticast
#from DEFCOM import ChannelLossyCast

import cv2

if __name__ == "__main__":
    import cv2

    print(cv2.__version__)
    # TODO: Verify video capture feed when implemented on Rover
    # Initialize the video capture object.
    cap = cv2.VideoCapture(0)

    # Verify if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open the camera stream.")
        exit()

    print("Streaming started. Press 'q' to exit.")

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, params)

    while True:
        # Capture frame-by-frame
        # 'ret' is a boolean (True if frame reading succeeded)
        # 'frame' is the image array data
        ret, frame = cap.read()

        # If the frame was not retrieved successfully, break the loop
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Detect and ID aruco markers
        corners, ids, rejected = detector.detectMarkers(frame)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Display the resulting frame in a window
        cv2.imshow('ArUco Detection', frame)

        # Wait for 1 millisecond and check if 'q' is pressed on the keyboard
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cleanup
    cap.release()
    cv2.destroyAllWindows()
