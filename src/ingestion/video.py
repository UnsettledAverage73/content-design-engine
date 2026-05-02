import cv2
import os
from pathlib import Path
from typing import List, Tuple

def extract_keyframes(video_path: Path, interval_seconds: int = 2) -> List[Tuple[float, bytes]]:
    """
    Extracts frames from a video at a specified interval.
    Returns a list of (timestamp, image_bytes) tuples.
    """
    keyframes = []
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30 # Fallback
        
    frame_interval = int(fps * interval_seconds)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            # Resize for VLM efficiency
            height, width = frame.shape[:2]
            max_dim = 1024
            if max(height, width) > max_dim:
                scale = max_dim / max(height, width)
                frame = cv2.resize(frame, (int(width * scale), int(height * scale)))
            
            # Encode to JPEG
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
            keyframes.append((timestamp, buffer.tobytes()))
            
        frame_count += 1
        
    cap.release()
    return keyframes
