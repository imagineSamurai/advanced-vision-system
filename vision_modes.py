import cv2
import numpy as np
from time import time

class NightVision:
    def __init__(self):
        self.brightness_levels = {
            "high": 2.5,
            "low": 1.8,
            "green": 2.0,
            "blue": 2.0
        }
        self.noise_pattern = None
        self.last_noise_update = 0
        self.noise_update_interval = 0.03

    def create_dynamic_noise(self, shape):
        # Create dynamic noise with varying intensity
        base_noise = np.random.normal(0, 15, shape).astype(np.uint8)
        noise_intensity = np.random.uniform(0.7, 1.3)  # Random intensity multiplier
        return cv2.multiply(base_noise, noise_intensity)
    
    def add_tube_distortion(self, frame):
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # Create radial gradient
        Y, X = np.ogrid[:height, :width]
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        # Create vignette effect
        vignette = 1 - (dist_from_center / (np.sqrt(center_x**2 + center_y**2)))
        vignette = np.clip(vignette * 1.5, 0, 1)
        
        # Apply vignette
        frame = frame * vignette[:, :, np.newaxis]
        return frame.astype(np.uint8)
    
    def process(self, frame, brightness_level="high"):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Update noise pattern periodically
        current_time = time()
        if current_time - self.last_noise_update > self.noise_update_interval:
            self.noise_pattern = self.create_dynamic_noise(enhanced.shape)
            self.last_noise_update = current_time
        
        # Add dynamic noise
        if self.noise_pattern is not None:
            enhanced = cv2.add(enhanced, self.noise_pattern)
        
        # Apply brightness adjustment
        multiplier = self.brightness_levels.get(brightness_level, 1.8)
        enhanced = cv2.multiply(enhanced, multiplier)
        
        # Create tint based on mode
        zeros = np.zeros_like(enhanced)
        if brightness_level == "blue":
            tinted = cv2.merge([enhanced, zeros, zeros])  # Blue tint
        elif brightness_level == "green":
            tinted = cv2.merge([zeros, enhanced, zeros])  # Green tint
        else:
            tinted = cv2.merge([zeros, enhanced, zeros])  # Default green
        
        # Add phosphor trailing effect
        if hasattr(self, 'previous_frame'):
            tinted = cv2.addWeighted(tinted, 0.85, self.previous_frame, 0.15, 0)
        self.previous_frame = tinted.copy()
        
        # Add tube distortion and vignette
        tinted = self.add_tube_distortion(tinted)
        
        # Add light bloom effect
        blur = cv2.GaussianBlur(tinted, (0, 0), 5)
        tinted = cv2.addWeighted(tinted, 0.8, blur, 0.2, 0)
        
        # Add scan lines
        height = tinted.shape[0]
        scan_lines = np.zeros_like(tinted)
        scan_lines[::2, :] = [0, 20, 0]
        tinted = cv2.subtract(tinted, scan_lines)
        
        return tinted

class ThermalVision:
    def __init__(self):
        self.colormap_modes = {
            "hot_white": cv2.COLORMAP_HOT,
            "hot_black": cv2.COLORMAP_BONE,
            "rainbow": cv2.COLORMAP_RAINBOW,
            "ironbow": cv2.COLORMAP_INFERNO,
            "plasma": cv2.COLORMAP_PLASMA
        }
        self.noise_pattern = None
        self.last_noise_update = 0
        self.noise_update_interval = 0.05
        self.enable_noise = True
        self.enable_vignette = True
        
    def create_thermal_noise(self, shape):
        noise = np.random.normal(0, 2, shape).astype(np.uint8)
        return cv2.GaussianBlur(noise, (3, 3), 0)
    
    def apply_circular_mask(self, frame):
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        radius = min(center_x, center_y) - 10
        
        # Create circular mask
        Y, X = np.ogrid[:height, :width]
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        mask = dist_from_center <= radius
        
        # Create gradual fade at edges
        fade_width = 30
        fade_mask = (dist_from_center <= (radius + fade_width)) & (dist_from_center > radius)
        fade_values = 1 - (dist_from_center[fade_mask] - radius) / fade_width
        
        # Apply masks
        result = np.zeros_like(frame)
        result[mask] = frame[mask]
        result[fade_mask] = (frame[fade_mask].T * fade_values).T
        
        return result
    
    def process(self, frame, mode="hot_white"):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Add thermal noise if enabled
        if self.enable_noise:
            current_time = time()
            if current_time - self.last_noise_update > self.noise_update_interval:
                self.noise_pattern = self.create_thermal_noise(gray.shape)
                self.last_noise_update = current_time
            
            if self.noise_pattern is not None:
                gray = cv2.add(gray, self.noise_pattern)
        
        # Apply blur and enhance contrast
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)
        
        # Apply thermal colormap
        colormap = self.colormap_modes.get(mode, cv2.COLORMAP_HOT)
        thermal = cv2.applyColorMap(enhanced, colormap)
        
        # Add heat signature effect
        kernel = np.ones((3,3), np.uint8)
        thermal = cv2.dilate(thermal, kernel, iterations=1)
        
        # Add heat bloom effect
        heat_blur = cv2.GaussianBlur(thermal, (0, 0), 10)
        thermal = cv2.addWeighted(thermal, 0.7, heat_blur, 0.3, 0)
        
        # Apply circular mask if vignette is enabled
        if self.enable_vignette:
            thermal = self.apply_circular_mask(thermal)
        
        return thermal 