# Video Stabilization using homography matrix
This repository demonstraits a simple usage of the 2D homography matrix, obtained from feature matching between two images. This example shows a use case of this image transformation matrix to stabilize a video, while there are rotations and displacements in the camera. The main goal is to keep the scene intact and fixed.

## Desctiption
In this example, a desired frame of the video is considered to be the reference of the stabilizer algorithm. The detection of the features is executed using a feature detection algorithm called Oriented FAST and rotated BRIEF (ORB).

After finding the best matches between video frames and the reference frame, the first 200 matches are used to estimate a 3x3 homography matrix that describes the relation between the target keypoints. The homography matrix can be decomposed into **rotation**, **translation**, and **skew** components. 

$$
H =
\begin{bmatrix}
h_{11} & h_{12} & h_{13} \\
h_{21} & h_{22} & h_{23} \\
h_{31} & h_{32} & h_{33}
\end{bmatrix}
=\begin{bmatrix}
\mathbf{R} & \mathbf{T} \\
\mathbf{V} & 1 \\
\end{bmatrix}
$$

This transformation matrix shows the rotation and translation between the points. By applying this matrix to the video frames, the resulting frame is matched to the reference frame, forcing it to mimic the features of the target frame. This causes the video frames to look "stabilized".