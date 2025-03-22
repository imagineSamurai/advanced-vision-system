import cv2
from vision_modes import NightVision, ThermalVision
from camera_handler import CameraHandler
from gui_controller import GUIController
import time

def main():
    # Initialize core components
    camera = CameraHandler()
    night_vision = NightVision()
    thermal_vision = ThermalVision()
    gui = GUIController()
    current_mode = "normal"
    
    while True:
        start_time = time.time()
        
        frame = camera.get_frame()
        if frame is None:
            break
            
        # Handle zoom controls
        if gui.last_key == ord('+') or gui.last_key == ord('='):
            camera.zoom_in()
        elif gui.last_key == ord('-') or gui.last_key == ord('_'):
            camera.zoom_out()
            
        # Apply vision effects based on mode
        if current_mode.startswith("night_"):
            processed_frame = night_vision.process(frame, brightness_level=current_mode.split("_")[1])
            night_vision.enable_noise = gui.enable_noise
        elif current_mode.startswith("thermal_"):
            processed_frame = thermal_vision.process(frame, mode=current_mode.split("_", 1)[1])
            thermal_vision.enable_noise = gui.enable_noise
            thermal_vision.enable_vignette = gui.enable_vignette
        else:
            processed_frame = frame
            
        # Update display and handle user input
        gui.display_frame(processed_frame)
        current_mode = gui.handle_controls()
        
        if gui.should_exit():
            break
        
        # Maintain consistent frame rate
        elapsed = time.time() - start_time
        wait_time = max(1, int((1.0 / gui.frame_rate - elapsed) * 1000))
        cv2.waitKey(wait_time)
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 