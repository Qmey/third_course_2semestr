import cv2

dog_cascade = cv2.CascadeClassifier(r'C:\Users\Yerlan\Downloads\dog-cascade_40x40_rev2.xml')

image_path = r'C:\Users\Yerlan\Downloads\dog3.jpeg'
output_path = r'C:\Users\Yerlan\Downloads\dog_detected3.jpeg'

image = cv2.imread(image_path)
if image is None:
    print(f"Error loading image: {image_path}")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dogs = dog_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    num_dogs = len(dogs)
    print(f"Detected dogs: {num_dogs}")

    for (x, y, w, h) in dogs:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(image, "Dog Detected!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(
        image,
        f"Detected dogs: {num_dogs}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imwrite(output_path, image)
    print(f"Result saved: {output_path}")

    scale_percent = 50
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(image, (800, 600), interpolation=cv2.INTER_AREA)


    cv2.imshow('Dog Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
