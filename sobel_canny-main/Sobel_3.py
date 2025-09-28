import cv2
import matplotlib.pyplot as plt
import numpy as np

simple_image = cv2.imread("flower.jpeg", cv2.IMREAD_GRAYSCALE)
medium_image = cv2.imread("human.jpg", cv2.IMREAD_GRAYSCALE)
hard_image = cv2.imread("nature.jpg", cv2.IMREAD_GRAYSCALE)

def apply_sobel(image):
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = cv2.magnitude(sobel_x, sobel_y)
    return sobel_x, sobel_y, sobel_combined

simple_sobel_x, simple_sobel_y, simple_sobel_combined = apply_sobel(simple_image)
medium_sobel_x, medium_sobel_y, medium_sobel_combined = apply_sobel(medium_image)
hard_sobel_x, hard_sobel_y, hard_sobel_combined = apply_sobel(hard_image)

plt.figure(figsize=(18, 18))

plt.subplot(3, 4, 1)
plt.title("Original: Simple Image")
plt.imshow(simple_image, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 2)
plt.title("Sobel X: Simple")
plt.imshow(np.abs(simple_sobel_x), cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 3)
plt.title("Sobel Y: Simple")
plt.imshow(np.abs(simple_sobel_y), cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 4)
plt.title("Sobel Combined: Simple")
plt.imshow(np.abs(simple_sobel_combined), cmap='gray')
plt.axis('off')

# Medium image
plt.subplot(3, 4, 5)
plt.title("Original: Medium Image")
plt.imshow(medium_image, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 6)
plt.title("Sobel X: Medium")
plt.imshow(np.abs(medium_sobel_x), cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 7)
plt.title("Sobel Y: Medium")
plt.imshow(np.abs(medium_sobel_y), cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 8)
plt.title("Sobel Combined: Medium")
plt.imshow(np.abs(medium_sobel_combined), cmap='gray')
plt.axis('off')

# Hard image
plt.subplot(3, 4, 9)
plt.title("Original: Hard Image")
plt.imshow(hard_image, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 10)
plt.title("Sobel X: Hard")
plt.imshow(np.abs(hard_sobel_x), cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 11)
plt.title("Sobel Y: Hard")
plt.imshow(np.abs(hard_sobel_y), cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 12)
plt.title("Sobel Combined: Hard")
plt.imshow(np.abs(hard_sobel_combined), cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
