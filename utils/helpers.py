import cv2

class LowPassFilter():
    def __init__(self, alpha):
        self.alpha = alpha
        self.frame = None

    def filter(self, frame_new):

        if self.frame is None:
            self.frame = frame_new

        self.frame = self.alpha * self.frame + (1 - self.alpha) * (frame_new)

        return self.frame
    
def title_image(image, title):

    # Define font and color
    font = cv2.FONT_HERSHEY_SIMPLEX
    color_background = (255, 255, 255)  # White color in BGR format
    color = (0, 0, 0)  # White color in BGR format
    thickness = 2  # Thickness for bold text

    # Calculate the bottom center position for the text
    text_size = cv2.getTextSize(title, font, 1, thickness)[0]
    text_x = int((image.shape[1] - text_size[0]) / 2)
    text_y = int(image.shape[0] - text_size[1] - 10)  # Adjust the y-coordinate for better positioning

    # Write the text on the image
    cv2.putText(image, title, (text_x, text_y), font, 1, color_background, thickness + 2)
    cv2.putText(image, title, (text_x, text_y), font, 1, color, thickness)

    return image