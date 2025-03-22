import cv2
import numpy as np
import time

class GUIController:
    def __init__(self):
        self.window_name = "Advanced Vision System"
        cv2.namedWindow(self.window_name)
        self.mode_map = {
            ord('1'): "normal",
            ord('2'): "night_high",
            ord('3'): "night_low",
            ord('4'): "thermal_hot_white",
            ord('5'): "thermal_hot_black",
            ord('6'): "thermal_rainbow",
            ord('7'): "thermal_ironbow",
            ord('8'): "thermal_plasma",
            ord('9'): "night_green",
            ord('0'): "night_blue"
        }
        self.current_mode_index = 0
        self.modes_list = list(self.mode_map.values())
        self.current_mode = self.modes_list[0]
        self.last_key = None
        self.battery_level = 100.0
        self.enable_noise = True
        self.enable_vignette = True
        self.enable_scan_lines = True
        self.show_hud = True
        self.battery_color = (255, 255, 255)
        self.signal_strength = 100.0
        self.signal_change_speed = 0.1
        self.signal_direction = -1
        self.last_signal_change = time.time()
        self.pulse_alpha = 1.0
        self.pulse_direction = -1
        self.frame_rate = 120
        self.min_frame_rate = 30
        self.max_frame_rate = 240
        self.signal_change_time = time.time()
        self.signal_target = 100.0
        self.signal_change_interval = 3.0
        self.pulse_speed = 0.05
        
    def draw_battery_indicator(self, overlay, height):
        battery_x = 10
        battery_y = height - 30
        battery_width = 50
        battery_height = 25
        tip_width = 6
        tip_height = 12
        
        # Create a separate overlay for the battery to handle transparency
        battery_overlay = np.zeros_like(overlay)
        
        # Draw outer white rectangle with rounded corners
        cv2.rectangle(battery_overlay, 
                     (battery_x, battery_y),
                     (battery_x + battery_width, battery_y + battery_height),
                     self.battery_color, 2, cv2.LINE_AA)
        
        # Draw battery tip (filled)
        cv2.rectangle(battery_overlay,
                     (battery_x + battery_width, battery_y + (battery_height - tip_height)//2),
                     (battery_x + battery_width + tip_width, battery_y + (battery_height + tip_height)//2),
                     self.battery_color, -1)
        
        # Draw battery segments (bigger size)
        inner_padding = 3
        segment_width = 10
        segment_height = battery_height - 10
        num_segments = 3
        total_segments_width = segment_width * num_segments
        total_spacing = battery_width - 2 * inner_padding - total_segments_width
        segment_spacing = total_spacing / (num_segments + 1)
        start_x = battery_x + inner_padding + segment_spacing
        
        # Calculate vertical center position
        segment_y = battery_y + (battery_height - segment_height) // 2  # Center vertically
        
        # Determine active segments based on battery level and add pulsing near thresholds
        active_segments = 0
        is_pulsing = False
        pulse_segment = -1
        
        if self.battery_level > 75:
            active_segments = 3
            if self.battery_level < 80:  # Pulse before dropping to 2 segments
                is_pulsing = True
                pulse_segment = 2
        elif self.battery_level > 50:
            active_segments = 2
            if self.battery_level < 55:  # Pulse before dropping to 1 segment
                is_pulsing = True
                pulse_segment = 1
        elif self.battery_level > 25:
            active_segments = 1
            if self.battery_level < 30:  # Pulse before dropping to 0 segments
                is_pulsing = True
                pulse_segment = 0
        elif self.battery_level > 5:
            active_segments = 1
        
        for i in range(num_segments):
            segment_x = int(start_x + i * (segment_width + segment_spacing))
            
            if i < active_segments and i != pulse_segment:
                # Draw filled segment
                cv2.rectangle(battery_overlay,
                             (segment_x, segment_y),
                             (segment_x + segment_width, segment_y + segment_height),
                             self.battery_color, -1, cv2.LINE_AA)
            elif i == pulse_segment and is_pulsing:
                # Pulse the segment that's about to disappear
                pulse_color = (int(self.battery_color[0] * self.pulse_alpha),
                             int(self.battery_color[1] * self.pulse_alpha),
                             int(self.battery_color[2] * self.pulse_alpha))
                cv2.rectangle(battery_overlay,
                             (segment_x, segment_y),
                             (segment_x + segment_width, segment_y + segment_height),
                             pulse_color, -1, cv2.LINE_AA)
            elif self.battery_level <= 5 and i == 0:
                # Critical battery pulse
                pulse_color = (int(self.battery_color[0] * self.pulse_alpha),
                             int(self.battery_color[1] * self.pulse_alpha),
                             int(self.battery_color[2] * self.pulse_alpha))
                cv2.rectangle(battery_overlay,
                             (segment_x, segment_y),
                             (segment_x + segment_width, segment_y + segment_height),
                             pulse_color, -1, cv2.LINE_AA)
            else:
                # Draw empty segment
                cv2.rectangle(battery_overlay,
                             (segment_x, segment_y),
                             (segment_x + segment_width, segment_y + segment_height),
                             self.battery_color, 1, cv2.LINE_AA)
        
        # Blend battery overlay with main overlay
        alpha = 0.9
        mask = cv2.cvtColor(battery_overlay, cv2.COLOR_BGR2GRAY) > 0
        overlay[mask] = cv2.addWeighted(overlay, 1-alpha, battery_overlay, alpha, 0)[mask]
        
        # Draw battery percentage
        percentage = f"{int(self.battery_level)}%"
        cv2.putText(overlay, percentage,
                    (battery_x + battery_width + 15, battery_y + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.battery_color, 1)
    
    def update_signal_strength(self):
        current_time = time.time()
        
        # Update pulse effect
        self.pulse_alpha += self.pulse_speed * self.pulse_direction
        if self.pulse_alpha >= 1.0 or self.pulse_alpha <= 0.2:
            self.pulse_direction *= -1
        self.pulse_alpha = np.clip(self.pulse_alpha, 0.2, 1.0)
        
        # Randomly change target with longer intervals
        if current_time - self.signal_change_time > self.signal_change_interval:
            # More random movement
            if np.random.random() < 0.3:  # 30% chance to make a big change
                self.signal_target = np.random.uniform(25, 100)
            else:  # Small change
                change = np.random.uniform(-20, 20)
                self.signal_target = np.clip(self.signal_strength + change, 25, 100)
            self.signal_change_time = current_time
        
        # Smoothly move towards target
        diff = self.signal_target - self.signal_strength
        self.signal_strength += diff * 0.05  # Slower interpolation
        self.signal_strength = np.clip(self.signal_strength, 25, 100)
    
    def display_frame(self, frame):
        height, width = frame.shape[:2]
        overlay = frame.copy()
        
        # Determine text color based on mode
        if self.current_mode.startswith("thermal_"):
            text_color = (0, 0, 255)  # Red for thermal
        elif self.current_mode.startswith("night_"):
            text_color = (0, np.random.randint(240, 255), 0)  # Flickering green for night
        else:
            text_color = (255, 255, 255)  # White for normal
        
        if self.show_hud:
            # Draw controls menu
            controls = [
                "CONTROLS:",
                "A/D: Change Mode",
                "W/S: Change FPS",
                "+/-: Zoom In/Out",
                "1: Toggle Vintage",
                "2: Toggle Lines",
                "3: Toggle HUD",
                "4: Toggle Noise",
                "Q: Quit"
            ]
            
            # Add current settings status
            settings = [
                f"FPS: {self.frame_rate}",
                f"Noise: {'ON' if self.enable_noise else 'OFF'}",
                f"Vintage: {'ON' if self.enable_vignette else 'OFF'}",
                f"Lines: {'ON' if self.enable_scan_lines else 'OFF'}"
            ]
            
            # Draw controls
            y = 60
            for line in controls:
                cv2.putText(overlay, line, (10, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
                y += 20
            
            # Draw settings status
            y = 60
            for setting in settings:
                cv2.putText(overlay, setting, (width - 150, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
                y += 20
            
            # Add FPS and mode display
            fps_text = f"FPS: {self.frame_rate}"
            cv2.putText(overlay, fps_text, (width - 100, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            
            cv2.putText(overlay, f"MODE: {self.current_mode.upper()}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        
        # Update and draw signal strength
        self.update_signal_strength()
        
        # Add status indicators for thermal/night vision modes
        if self.current_mode != "normal":
            # Add timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(overlay, timestamp, (width - 200, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            
            # Add scanning lines if enabled
            if self.enable_scan_lines:
                for _ in range(3):
                    scan_line = np.random.randint(0, height)
                    cv2.line(overlay, (0, scan_line), (width, scan_line),
                            text_color, 1)
            
            # Add status indicators
            status_text = [
                f"NOISE: {'ON' if self.enable_noise else 'OFF'}",
                f"VIGNETTE: {'ON' if self.enable_vignette else 'OFF'}",
                f"SCAN LINES: {'ON' if self.enable_scan_lines else 'OFF'}"
            ]
            
            y = height - 80
            for status in status_text:
                cv2.putText(overlay, status, (width - 150, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
                y += 20
            
            # Draw battery indicator
            self.draw_battery_indicator(overlay, height)
            
            # Simulate battery drain
            self.battery_level = max(0.0, self.battery_level - 0.01)
            # Reset battery when empty
            if self.battery_level <= 0:
                self.battery_level = 100.0
        
        # Blend overlay with original frame
        alpha = 0.85 if self.current_mode != "normal" else 0.9
        frame = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)
        
        cv2.imshow(self.window_name, frame)
        self.last_key = cv2.waitKey(1) & 0xFF
        
    def handle_controls(self):
        if self.last_key == ord('1'):
            self.enable_vignette = not self.enable_vignette  # Vintage effect
        elif self.last_key == ord('2'):
            self.enable_scan_lines = not self.enable_scan_lines  # Lines effect
        elif self.last_key == ord('3'):
            self.show_hud = not self.show_hud  # HUD toggle
        elif self.last_key == ord('4'):
            self.enable_noise = not self.enable_noise  # Noise toggle
        elif self.last_key == ord('w'):
            self.frame_rate = min(self.frame_rate + 10, self.max_frame_rate)
        elif self.last_key == ord('s'):
            self.frame_rate = max(self.frame_rate - 10, self.min_frame_rate)
        elif self.last_key == ord('a'):  # A key
            self.current_mode_index = (self.current_mode_index - 1) % len(self.modes_list)
            self.current_mode = self.modes_list[self.current_mode_index]
        elif self.last_key == ord('d'):  # D key
            self.current_mode_index = (self.current_mode_index + 1) % len(self.modes_list)
            self.current_mode = self.modes_list[self.current_mode_index]
        
        return self.current_mode
        
    def should_exit(self):
        return self.last_key == ord('q') 