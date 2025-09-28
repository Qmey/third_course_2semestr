import cv2
import matplotlib.pyplot as plt

simple_image = cv2.imread("flower.jpeg", cv2.IMREAD_GRAYSCALE)
medium_image = cv2.imread("human.jpg", cv2.IMREAD_GRAYSCALE)
hard_image = cv2.imread("nature.jpg", cv2.IMREAD_GRAYSCALE)

def apply_canny(image, low_threshold, high_threshold):
    return cv2.Canny(image, low_threshold, high_threshold)

simple_canny = apply_canny(simple_image, 50, 150)
medium_canny = apply_canny(medium_image, 100, 200)
hard_canny = apply_canny(hard_image, 150, 250)

plt.figure(figsize=(18, 12))

plt.subplot(3, 2, 1)
plt.title("Original: Simple Image")
plt.imshow(simple_image, cmap='gray')
plt.axis('off')

plt.subplot(3, 2, 2)
plt.title("Canny Edges: Simple Image")
plt.imshow(simple_canny, cmap='gray')
plt.axis('off')

plt.subplot(3, 2, 3)
plt.title("Original: Medium Image")
plt.imshow(medium_image, cmap='gray')
plt.axis('off')

plt.subplot(3, 2, 4)
plt.title("Canny Edges: Medium Image")
plt.imshow(medium_canny, cmap='gray')
plt.axis('off')

plt.subplot(3, 2, 5)
plt.title("Original: Hard Image")
plt.imshow(hard_image, cmap='gray')
plt.axis('off')

plt.subplot(3, 2, 6)
plt.title("Canny Edges: Hard Image")
plt.imshow(hard_canny, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
