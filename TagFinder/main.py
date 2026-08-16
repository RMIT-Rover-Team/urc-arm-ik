#!/usr/bin/env python3

from DEFCOM import ChannelMulticast

import cv2

if __name__ == "__main__":
    import cv2

    # Initialise DEFCOM publisher
    publisher = ChannelMulticast.MulticastPublisher("COMFILES/template.defcom")

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
    frame_counter = 0

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
        frame_counter += 1

        # print(f"corners type: {type(corners)}")
        # print(f"ids type: {type(ids)}")

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Display the resulting frame in a window
        cv2.imshow('ArUco Detection', frame)

        # Wait for 1 millisecond and check if 'q' is pressed on the keyboard
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Write message and publish to DEFCOM
        if len(corners) > 0 and len(corners[0]) > 0:
            for i in range(len(corners)):
                message = publisher.getNewMessageObject()
                message.setInt("frame_count", frame_counter)
                message.setInt("num_markers", len(corners))
                message.setInt("marker", i)
                for j in range(4):
                    message.setFloat(f"corner_{j}_x", corners[i][0][j][0])
                    message.setFloat(f"corner_{j}_y", corners[i][0][j][1])
                publisher.publish(message)

    # cleanup
    cap.release()
    cv2.destroyAllWindows()
