import cv2
import os
import time
import toml
import threading
from datetime import datetime
from flask import Flask, jsonify, render_template, send_from_directory

def load_settings():
    """Load settings from settings.toml file"""
    try:
        with open('settings.toml', 'r') as f:
            settings = toml.load(f)
        return settings
    except FileNotFoundError:
        print("Warning: settings.toml not found. Using default settings.")
        return {
            'capture': {'interval': 60},
            'server': {'address': '0.0.0.0', 'port': 8000}
        }
    except Exception as e:
        print(f"Warning: Error reading settings.toml: {e}. Using default settings.")
        return {
            'capture': {'interval': 60},
            'server': {'address': '0.0.0.0', 'port': 8000}
        }

def create_images_folder():
    """Create the images folder if it doesn't exist"""
    if not os.path.exists('images'):
        os.makedirs('images')
        print("Created 'images' folder")

def create_flask_app():
    """Create and configure Flask application"""
    # Configure Flask to look for templates in current directory
    app = Flask(__name__, template_folder='.')
    
    @app.route('/ping', methods=['GET'])
    def ping():
        """Simple ping endpoint that returns pong"""
        return jsonify({"message": "pong"})
    
    @app.route('/', methods=['GET'])
    def index():
        """Main page showing list of captured images"""
        images_dir = 'images'
        if not os.path.exists(images_dir):
            image_files = []
        else:
            # Get all PNG files in the images directory
            image_files = [f for f in os.listdir(images_dir) if f.lower().endswith('.png')]
            image_files.sort(reverse=True)  # Show newest first
        
        # Load template from file
        return render_template('index.html', 
                             image_files=image_files, 
                             image_count=len(image_files),
                             latest_image=image_files[0] if image_files else None)
    
    @app.route('/images/<filename>')
    def serve_image(filename):
        """Serve individual image files"""
        return send_from_directory('images', filename)
    
    return app

def start_web_server(settings):
    """Start the Flask web server in a separate thread"""
    server_config = settings.get('server', {'address': '0.0.0.0', 'port': 8000})
    address = server_config.get('address', '0.0.0.0')
    port = server_config.get('port', 8000)
    
    app = create_flask_app()
    
    print(f"Starting web server on {address}:{port}")
    print(f"Image gallery available at: http://{address}:{port}/")
    print(f"Ping endpoint available at: http://{address}:{port}/ping")
    
    # Suppress Flask's startup messages by setting host and port
    app.run(host=address, port=port, debug=False, use_reloader=False)

def capture_webcam_snapshots():
    """Capture webcam snapshots at configured interval"""
    # Load settings
    settings = load_settings()
    interval = settings['capture']['interval']
    
    print(f"Using capture interval: {interval} seconds")
    # Create images folder
    create_images_folder()
    
    # Start web server in a separate thread
    server_thread = threading.Thread(target=start_web_server, args=(settings,))
    server_thread.daemon = True  # Thread will die when main program exits
    server_thread.start()
    
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
        print("Web server will shut down...")

if __name__ == "__main__":
    capture_webcam_snapshots()
