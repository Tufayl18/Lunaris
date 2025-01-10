import cv2
import numpy as np

# Load the image
image = cv2.imread('1.jpg')

# Define a darkening factor (between 0 and 1; lower means darker)
darkening_factor = 0.5

# Darken the image by multiplying by the factor
darkened_image = np.clip(image * darkening_factor, 0, 255).astype(np.uint8)

# Save or display the result
cv2.imwrite('darkened_image.jpg', darkened_image)
cv2.imshow('Darkened Image', darkened_image)
cv2.waitKey(0)
cv2.destroyAllWindows()