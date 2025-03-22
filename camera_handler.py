import cv2

class CameraHandler:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)
        self.set_resolution(640, 480)  # Default resolution
        self.zoom_factor = 1.0
        self.zoom_step = 0.1
        self.min_zoom = 1.0
        self.max_zoom = 3.0
        
    def set_resolution(self, width, height):
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
    def apply_zoom(self, frame):
        # Return original frame if no zoom
        if self.zoom_factor == 1.0:
            return frame
            
        # Calculate zoom window dimensions
        height, width = frame.shape[:2]
        zoom_width = int(width / self.zoom_factor)
        zoom_height = int(height / self.zoom_factor)
        
        # Calculate center crop coordinates
        x1 = (width - zoom_width) // 2
        y1 = (height - zoom_height) // 2
        x2 = x1 + zoom_width
        y2 = y1 + zoom_height
        
        # Crop and resize to original dimensions
        cropped = frame[y1:y2, x1:x2]
        return cv2.resize(cropped, (width, height))
        
    def zoom_in(self):
        self.zoom_factor = min(self.zoom_factor + self.zoom_step, self.max_zoom)
        
    def zoom_out(self):
        self.zoom_factor = max(self.zoom_factor - self.zoom_step, self.min_zoom)
        
    def get_frame(self):
        ret, frame = self.camera.read()
        if ret:
            return self.apply_zoom(frame)
        return None
        
    def release(self):
        self.camera.release() 