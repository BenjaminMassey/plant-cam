# Webcam Snapshot Capture

A Python program that automatically captures snapshots from your default webcam every 5 seconds and saves them as PNG files with timestamp names.

## Features

- **Configurable Capture**: Takes webcam snapshots at customizable intervals (default: 5 seconds)
- **Timestamp Naming**: Files are saved with descriptive timestamp names
- **Folder Management**: Automatically creates an 'images' folder for organized storage
- **Error Handling**: Graceful handling of webcam errors and user interruption
- **User-Friendly**: Clear console output showing each saved image
- **Easy Control**: Stop anytime with Ctrl+C
- **Settings File**: Configure capture interval via settings.toml file

## Requirements

- **Python**: 3.6 or higher
- **Webcam**: Default system webcam (camera index 0)
- **Dependencies**: OpenCV for Python (opencv-python)

## Installation

1. **Clone or download** this project to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd plant-cam
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the program**:
   ```bash
   python plant-cam.py
   ```

2. **The program will**:
   - Create an 'images' folder if it doesn't exist
   - Start capturing from your default webcam
   - Save a snapshot every 5 seconds
   - Display console messages for each saved image
   - Continue until you stop it

3. **Stop the program**:
   - Press `Ctrl+C` to gracefully stop the capture process

## File Naming

Images are saved with the following naming convention:
```
snapshot_YYYYMMDD_HHMMSS.png
```

**Examples:**
- `snapshot_20250826_222122.png` - captured on August 26, 2025 at 10:21:22 PM
- `snapshot_20250826_222127.png` - captured 5 seconds later

## Configuration

The program uses a `settings.toml` file to configure capture settings. The file will be created automatically with default values if it doesn't exist.

### settings.toml

```toml
# Webcam Capture Settings

[capture]
# Interval between snapshots in seconds
interval = 5
```

**Configuration Options:**
- `capture.interval`: Time in seconds between snapshots (default: 5)

To change the capture interval, simply edit the `interval` value in `settings.toml` and restart the program.

## Project Structure

```
plant-cam/
├── plant-cam.py    # Main program file
├── requirements.txt     # Python dependencies
├── settings.toml        # Configuration file
├── README.md           # This documentation
└── images/             # Created automatically for storing snapshots
    ├── snapshot_20250826_222122.png
    ├── snapshot_20250826_222127.png
    └── ...
```

## Troubleshooting

### Common Issues

1. **"Could not open webcam" error**:
   - Ensure your webcam is connected and not being used by another application
   - Try closing other applications that might be using the camera
   - Check if your system has multiple cameras (the program uses index 0)

2. **Permission denied errors**:
   - On some systems, you may need to grant camera permissions
   - Run the program as administrator if necessary

3. **Module not found errors**:
   - Ensure you've installed the requirements: `pip install -r requirements.txt`
   - Verify you're using the correct Python environment

4. **ImportError: numpy.core.multiarray failed to import**:
   - This is a version compatibility issue between NumPy and OpenCV
   - Reinstall with compatible versions: `pip uninstall -y opencv-python numpy && pip install -r requirements.txt`
   - The requirements.txt file specifies tested compatible versions

### System Compatibility

- **Windows**: Fully supported
- **macOS**: Supported (may require camera permissions)
- **Linux**: Supported (may require additional camera drivers)

## Technical Details

- **Image Format**: PNG (lossless compression)
- **Capture Interval**: Configurable via settings.toml (default: 5 seconds)
- **Camera Source**: Default system camera (index 0)
- **Image Quality**: Full resolution of your webcam
- **Storage**: Local filesystem in 'images' folder
- **Configuration**: TOML format for easy editing

## Customization

You can easily customize the program:

**Via Configuration File (Recommended):**
- Change the capture interval by editing `interval` in `settings.toml`

**Via Code Modification:**
- Change the image format (modify the file extension and `cv2.imwrite()` parameters)
- Use a different camera (change the camera index in `cv2.VideoCapture(0)`)
- Modify the timestamp format (adjust the `strftime()` format string)
- Add new configuration options to the settings.toml structure

## License

This project is provided as-is for educational and personal use.
