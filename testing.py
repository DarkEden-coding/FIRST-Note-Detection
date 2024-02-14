import cv2
from time import time
from ultralytics import YOLO


def detect(frame):
    start = time() 

    # Resize frame directly using the interpolation method for better quality
    frame = cv2.resize(frame, (640, 640))

    # Detect notes
    results = model(frame, show=show, device="cpu")

    print(f"Time taken in ms: {(time() - start) * 1000}ms")
    print(f"Estimated FPS: {1 / (time() - start)}")

    return results


# Load video
cap = cv2.VideoCapture("IMG_1273.MOV")

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # You can also use 'MJPG' or 'MP4V'
out = cv2.VideoWriter("color_v1.mp4", fourcc, fps, (640, 640))  # Adjust the resolution if needed

# Load base model to setup environment
model = YOLO("yolov5n.pt")

# Load model
model = YOLO("color_model.pt")

show = True

# Loop through video
while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    results = detect(frame)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = round(box.conf[0].item(), 2)
            class_num = box.cls[0].item()

            x1, y1, x2, y2 = (
                int(box.xyxy[0][0].item()),
                int(box.xyxy[0][1].item()),
                int(box.xyxy[0][2].item()),
                int(box.xyxy[0][3].item()),
            )

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                str(conf),
                (x1, y1),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

    # Write frame with bounding boxes and confidences to video
    out.write(frame)

    if show:
        # show frame
        cv2.imshow("Frame", frame)

    # Break on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release VideoCapture and VideoWriter objects
cap.release()
out.release()

# Close all windows
cv2.destroyAllWindows()
