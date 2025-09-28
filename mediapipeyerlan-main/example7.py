import cv2
import mediapipe as mp
import numpy as np

mp_selfie_segmentation = mp.solutions.selfie_segmentation

selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

image = cv2.imread("person.png")
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = selfie_segmentation.process(rgb_image)

height, width, _ = image.shape
background = np.zeros((height, width, 3), dtype=np.uint8)

mask = results.segmentation_mask
condition = mask > 0.5
output_image = np.where(condition[:, :, None], image, background)

cv2.imshow("Selfie Segmentation", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
