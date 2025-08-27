import cv2
import os
import time
import toml
from datetime import datetime

def load_settings():
    """Load settings from settings.toml file"""
    try:
        with open('settings.toml', 'r') as f:
            settings = toml.load(f)
        return settings
    except FileNotFoundError:
        print("Warning: settings.toml not found. Using default interval of 60 seconds.")
        return {'capture': {'interval': 60}}
    except Exception as e:
        print(f"Warning: Error reading settings.toml: {e}. Using default interval of 60 seconds.")
        return {'capture': {'interval': 60}}

def create_images_folder():
    """Create the images folder if it doesn't exist"""
    if not os.path.exists('images'):
        os.makedirs('images')
        print("Created 'images' folder")

def capture_webcam_snapshots():
    """Capture webcam snapshots at configured interval"""
    # Load settings
    settings = load_settings()
    interval = settings['capture']['interval']
    
    print(f"Using capture interval: {interval} seconds")
    # Create images folder
    create_images_folder()
    
    # Initialize the webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Webcam capture started. Press Ctrl+C to stop.")
    print("Saving images to 'images' folder with timestamp names...")
    
    try:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            
            if ret:
                # Generate timestamp for filename
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"images/{timestamp}.png"
                
                # Save the frame as PNG
                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")
                
                # Wait for configured interval
                time.sleep(interval)
            else:
                print("Error: Failed to capture frame")
                break
                
    except KeyboardInterrupt:
        print("\nCapture stopped by user")
    
    finally:
        # Release the webcam
        cap.release()
        print("Webcam released")

if __name__ == "__main__":
    capture_webcam_snapshots()
