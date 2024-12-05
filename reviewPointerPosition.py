import cv2
import csv
import os

# Paths
video_path = "./videos"
csv_path = "./pointer_locations"
file_name = "c1-What is artificial intelligence"

video_file = os.path.join(video_path, file_name + ".mp4")
csv_file = os.path.join(csv_path, file_name + ".csv")

# Load pointer positions from CSV
pointer_positions = []
with open(csv_file, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        frame = int(row[0])
        x = int(row[1])
        y = int(row[2])
        pointer_positions.append((frame, x, y))

# Open the video file
cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    print(f"Error: Unable to open video file {video_file}")
    exit(1)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get the total number of frames
frame_count = 0

# Play the video with overlay
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Check if the current frame has a pointer position
    if frame_count <= len(pointer_positions):
        _, x, y = pointer_positions[frame_count - 1]
        # Draw the pointer position if it's valid
        if x != -1 and y != -1:
            cv2.circle(frame, (x, y), radius=5, color=(0, 0, 255), thickness=-1)

    # Add current frame and total frames as text overlay
    text = f"Frame: {frame_count}/{total_frames}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color = (255, 255, 255)  # White text
    thickness = 2
    position = (10, 30)  # Top-left corner
    cv2.putText(frame, text, position, font, font_scale, color, thickness)

    # Display the frame
    cv2.imshow("Video with Pointer Position", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
