# Video Change Detector
From Khan Academy Style Blackboard or Whiteboard Sketch Animation, find the pen position by analyzing video frames for changes and save the detected positions as a CSV file.

## Demo
![REview Screen shot](demo.png)
Yellow Dot is the digital pointer in the original video, and the red dot is the detected position.

## Output CSV Example
| Frame | Pen Position X | Pen Position Y |
|-------|----------------|----------------|
| 1     | 2              | 340            |
| 2     | 2              | 340            |
| 3     | 2              | 340            |


## How to Use
1. Install Dependencies
Ensure you have Python 3.13.1 installed. Install required libraries using pip:
```
pip install opencv-python numpy
```

2. Detect Pen Pointer Position
This script processes a video file to identify the pen's position and saves the results in a CSV file: 
```
python findPointerPosition.py
```

3. Review the Detected Pointer Positions
Visualize the pointer positions overlaid on the original video:
```
python reviewPointerPosition.py
```
4. Check the Output
The detected pointer positions are saved in a CSV file located in the pointer_locations folder:
```
pointer_locations/<file_name>.csv
```

## Credit
test video from the Khan Academy video Introduction to Artificial Intelligence : https://youtu.be/OmtkvAp2OL0?si=jkHkfswZAUI85OGd