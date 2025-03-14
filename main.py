import cv2
import numpy as np
from utils.helpers import LowPassFilter, title_image
from utils.video_writer import VideoWriter

if __name__ == "__main__":

    orb = cv2.ORB_create()
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    lpf = LowPassFilter(0.7)
    cap = cv2.VideoCapture('/home/omid/Codes/camera_stabilizer/src/vid_car.mp4')
    writer = VideoWriter('results')
    
    frame_first = None
    shape_desired = (640, 480)
    idx_frame = 120 # reference frame index
    idx = 0 # counter

    while True:

        ret, src = cap.read()

        if not ret:
            break

        if idx < idx_frame:
            idx += 1
            continue

        frame = cv2.resize(src, shape_desired)

        if frame_first is None:
            frame_first = frame
            continue

        # Detect keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(frame, None)
        kp2, des2 = orb.detectAndCompute(frame_first, None)

        matches = matcher.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # pick at most 200 keypoints for homography matrix estimation
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:min(len(matches), 200)]]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:min(len(matches), 200)]]).reshape(-1, 1, 2)

        # Compute homography matrix using RANSAC
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Filter the homography matrix for a smooth video
        H_filtered = lpf.filter(H)

        # "Stabilize" the image
        frame_stabilized = cv2.warpPerspective(frame, H_filtered, [frame.shape[1], frame.shape[0]])

        # Display the result
        frame = title_image(frame, 'Actual')
        frame_stabilized = title_image(frame_stabilized, 'Stabilized')

        compare_stabilized = cv2.hconcat([frame, frame_stabilized])
        compare_stabilized = cv2.drawMatches(frame,
                                     kp1,
                                     frame_stabilized,
                                     kp2, matches[:20],
                                     None,
                                     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        cv2.imshow("Stabilized", compare_stabilized)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

        writer.record(compare_stabilized)