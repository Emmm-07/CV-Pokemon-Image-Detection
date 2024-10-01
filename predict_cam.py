# import cvlib as cv
# from cvlib.object_detection import draw_bbox
import cv2
from ultralytics import YOLO



model = YOLO('models/last.pt')
cap = cv2.VideoCapture(0)
threshold = 0.5

# result = results = model('images257.jpg')[0]
# print(result)

# # Extracting information from the result
# boxes = result.boxes  # Get the bounding boxes


# Load the image using OpenCV
# image = cv2.imread('Squirtle.PNG.jpg')

# # Check if the image is loaded
# if image is None:
#     print("Failed to load the image.")

# results = model(image)[0]
# print(results)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 (MPEG-4)
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))  # Save at 20 FPS with frame size of 640x480

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break

    results = model(frame)[0]
    print(results)
    annotated_frame = results


    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
 
    cv2.imshow("POKEMON", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()