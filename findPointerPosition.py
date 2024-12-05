import cv2
import numpy as np
import csv
import os

# Configuration
apply_smoothing = False  # Set to True to enable smoothing
window_size = 3          # Smoothing window size (only applies if smoothing is enabled)

# Paths
video_path = "./videos"
file_name = "c1-What is artificial intelligence"
video_file = os.path.join(video_path, file_name + ".mp4")

cap = cv2.VideoCapture(video_file)

# Create output directory if it doesn't exist
output_dir = "./pointer_locations"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, file_name.split(".")[0] + ".csv")

# Initialize variables
prev_frame = None
pointer_positions = []
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Processing video: {file_name}. Total frames: {total_frames}")

# Analyze the video and detect pointer positions
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 100 == 0:
        print(f"Processed {frame_count}/{total_frames} frames...")

    # Convert frame to grayscale for comparison
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_frame is not None:
        # Calculate absolute difference between frames
        diff = cv2.absdiff(prev_frame, gray_frame)

        # Threshold the difference to focus on significant changes
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Find contours of the changes
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour assuming it's the pen
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 10:  # Filter noise
                # Get the bounding box of the contour
                x, y, w, h = cv2.boundingRect(largest_contour)
                pen_x, pen_y = x + w // 2, y + h // 2  # Center of the bounding box

                # Store position
                pointer_positions.append((frame_count, pen_x, pen_y))
                prev_frame = gray_frame
                continue  # Skip adding (-1, -1) for this frame
    
    # If no change is detected, add (-1, -1)
    pointer_positions.append((frame_count, -1, -1))
    prev_frame = gray_frame

# Release the video capture
cap.release()
print("Finished processing frames. Starting proofreading...")

# Proofreading: Replace (-1, -1) with the nearest valid position (both backward and forward)
for i in range(len(pointer_positions)):
    frame, x, y = pointer_positions[i]
    if x == -1 and y == -1:
        # Search backward for the nearest valid frame
        backward_index = i
        while backward_index > 0 and pointer_positions[backward_index][1] == -1:
            backward_index -= 1

        # Search forward for the nearest valid frame
        forward_index = i
        while forward_index < len(pointer_positions) - 1 and pointer_positions[forward_index][1] == -1:
            forward_index += 1

        # Choose the closer valid position (backward or forward)
        backward_position = pointer_positions[backward_index][1:] if backward_index >= 0 and pointer_positions[backward_index][1] != -1 else None
        forward_position = pointer_positions[forward_index][1:] if forward_index < len(pointer_positions) and pointer_positions[forward_index][1] != -1 else None

        # Assign the nearest valid position
        if backward_position and forward_position:
            if (i - backward_index) <= (forward_index - i):
                pointer_positions[i] = (frame, *backward_position)
            else:
                pointer_positions[i] = (frame, *forward_position)
        elif backward_position:
            pointer_positions[i] = (frame, *backward_position)
        elif forward_position:
            pointer_positions[i] = (frame, *forward_position)

print("Proofreading completed.")

# Apply smoothing filter if enabled
if apply_smoothing:
    print("Applying smoothing filter...")
    smoothed_positions = pointer_positions.copy()

    for i in range(len(pointer_positions)):
        if pointer_positions[i][1] != -1:  # Skip smoothing for invalid positions
            x_values = []
            y_values = []
            for j in range(max(0, i - window_size), min(len(pointer_positions), i + window_size + 1)):
                if pointer_positions[j][1] != -1:  # Only include valid positions
                    x_values.append(pointer_positions[j][1])
                    y_values.append(pointer_positions[j][2])
            if x_values and y_values:
                avg_x = int(np.mean(x_values))
                avg_y = int(np.mean(y_values))
                smoothed_positions[i] = (pointer_positions[i][0], avg_x, avg_y)
    print("Smoothing filter applied.")
else:
    smoothed_positions = pointer_positions  # Use original positions if smoothing is disabled

# Save the updated positions to a CSV file
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["frame", "pen-position-x", "pen-position-y"])
    writer.writerows(smoothed_positions)

print(f"Pointer location data saved to {output_csv}")
