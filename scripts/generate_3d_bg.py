import numpy as np
import imageio
import math

def render_3d_background(filename="projects/ai_edu_roundtrip/images/bg_3d_loop.mp4", width=1280, height=720, duration=6, fps=30):
    total_frames = duration * fps
    print(f"Generating 3D animated background: {width}x{height}, {duration}s @ {fps}fps ({total_frames} frames)...")
    
    writer = imageio.get_writer(
        filename, 
        fps=fps, 
        codec='libx264', 
        quality=8, 
        pixelformat='yuv420p',
        macro_block_size=16
    )

    # 3D Grid parameters
    grid_x = np.linspace(-600, 600, 32)
    grid_y = np.linspace(50, 1100, 28)
    gx, gy = np.meshgrid(grid_x, grid_y)
    
    # Camera / projection setup
    cam_height = 280.0
    cam_dist = 600.0
    cx, cy = width / 2.0, height / 2.0 - 20.0
    
    # Floating particles
    np.random.seed(42)
    num_particles = 70
    p_x = np.random.uniform(-550, 550, num_particles)
    p_y = np.random.uniform(100, 1000, num_particles)
    p_base_z = np.random.uniform(20, 240, num_particles)
    p_speed = np.random.uniform(1.0, 2.0, num_particles)
    p_phase = np.random.uniform(0, 2 * math.pi, num_particles)
    p_size = np.random.uniform(2.5, 5.0, num_particles)
    p_colors = []
    palette = [
        (66, 133, 244),   # Google Blue
        (0, 229, 255),    # Cyan
        (52, 168, 83),    # Google Green
        (251, 188, 5),    # Google Yellow
        (234, 67, 53),    # Google Red
        (168, 85, 247)    # Purple
    ]
    for _ in range(num_particles):
        p_colors.append(palette[np.random.choice(len(palette), p=[0.45, 0.25, 0.1, 0.08, 0.07, 0.05])])

    # Pre-render background vignette gradient
    y_coords, x_coords = np.ogrid[:height, :width]
    dist_from_center = np.sqrt(((x_coords - cx) / (width * 0.55))**2 + ((y_coords - cy) / (height * 0.55))**2)
    vignette = np.clip(1.0 - dist_from_center * 0.65, 0.15, 1.0)
    
    # Base background: deep modern midnight gradient
    base_bg = np.zeros((height, width, 3), dtype=np.float32)
    # Top/center has deep blue/indigo ambient glow
    for c, (val_center, val_edge) in enumerate([(10, 4), (24, 8), (48, 18)]): # R, G, B
        base_bg[:, :, c] = val_edge + (val_center - val_edge) * vignette

    for f in range(total_frames):
        t = (2.0 * math.pi * f) / total_frames
        
        # Working frame (float32 for blending)
        frame = base_bg.copy()
        
        # 1. Compute 3D wave surface
        # Seamless loop: sin/cos with exact periodic frequencies
        w1 = math.sin(t)
        w2 = math.cos(t)
        w3 = math.sin(2.0 * t)
        w4 = math.cos(2.0 * t)
        
        # Wave height equation
        z_wave = (
            38.0 * np.sin(0.007 * gx + t) * np.cos(0.005 * gy + t) +
            22.0 * np.cos(0.011 * gx - t) * np.sin(0.008 * gy + 0.5 * t) +
            14.0 * np.sin(0.015 * gx + 2.0 * t)
        )
        
        # Project 3D grid points to 2D screen
        # Point: (X, Y, Z). Camera is at Y=0, looking down +Y axis.
        # Perspective: X_screen = cx + (X * cam_dist) / (Y)
        #              Y_screen = cy + ((cam_height - Z) * cam_dist) / (Y)
        denom = gy.copy()
        denom[denom < 1.0] = 1.0
        
        screen_x = cx + (gx * cam_dist) / denom
        screen_y = cy + ((cam_height - z_wave) * cam_dist) / denom
        
        # Depth factor: points closer to camera (small Y) are brighter, far are dimmer
        depth_factor = np.clip((1100.0 - gy) / 1000.0, 0.05, 1.0)
        
        # Draw grid lines: along X
        ny, nx = gx.shape
        for r in range(ny):
            alpha = float(depth_factor[r, 0] ** 1.3)
            if alpha < 0.08:
                continue
            color = np.array([40 * alpha + 15, 95 * alpha + 30, 210 * alpha + 45], dtype=np.float32)
            
            pts = np.stack([screen_x[r, :], screen_y[r, :]], axis=1).astype(np.int32)
            # Filter points in view
            valid = (pts[:, 0] >= -50) & (pts[:, 0] < width + 50) & (pts[:, 1] >= -50) & (pts[:, 1] < height + 50)
            if np.any(valid):
                import cv2
                cv2.polylines(frame, [pts], isClosed=False, color=color.tolist(), thickness=1, lineType=cv2.LINE_AA)
        
        # Draw grid lines: along Y
        for c in range(nx):
            pts = np.stack([screen_x[:, c], screen_y[:, c]], axis=1).astype(np.int32)
            import cv2
            # Average depth for column
            col_depth = float(np.mean(depth_factor[:, c]))
            color = [30 * col_depth + 10, 80 * col_depth + 25, 190 * col_depth + 40]
            cv2.polylines(frame, [pts], isClosed=False, color=color, thickness=1, lineType=cv2.LINE_AA)
            
        # 2. Draw floating 3D AI particles and light connectors
        part_screen_pts = []
        part_depths = []
        for i in range(num_particles):
            # Particle movement
            pz = p_base_z[i] + 30.0 * math.sin(t * p_speed[i] + p_phase[i])
            py = p_y[i] + 25.0 * math.cos(t + p_phase[i])
            px = p_x[i] + 20.0 * math.sin(t + p_phase[i])
            
            if py < 10.0:
                continue
            sx = int(cx + (px * cam_dist) / py)
            sy = int(cy + ((cam_height - pz) * cam_dist) / py)
            
            p_depth = (1100.0 - py) / 1000.0
            part_screen_pts.append((sx, sy))
            part_depths.append(p_depth)
            
            if 0 <= sx < width and 0 <= sy < height:
                import cv2
                rad = max(1, int(p_size[i] * p_depth * 1.5))
                c_base = p_colors[i]
                c_draw = [min(255, int(c * (0.4 + 0.6 * p_depth))) for c in c_base]
                
                # Outer glow
                cv2.circle(frame, (sx, sy), rad * 3, [c * 0.25 for c in c_draw], -1, lineType=cv2.LINE_AA)
                cv2.circle(frame, (sx, sy), rad * 2, [c * 0.55 for c in c_draw], -1, lineType=cv2.LINE_AA)
                # Core
                cv2.circle(frame, (sx, sy), rad, [min(255, c + 80) for c in c_draw], -1, lineType=cv2.LINE_AA)
                
        # Draw light strands between close particles
        for i in range(len(part_screen_pts)):
            for j in range(i + 1, min(i + 6, len(part_screen_pts))):
                x1, y1 = part_screen_pts[i]
                x2, y2 = part_screen_pts[j]
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < 110:
                    alpha_conn = (1.0 - dist / 110.0) * min(part_depths[i], part_depths[j]) * 0.7
                    if alpha_conn > 0.05:
                        import cv2
                        c_line = [int(0 * alpha_conn), int(180 * alpha_conn), int(255 * alpha_conn)]
                        cv2.line(frame, (x1, y1), (x2, y2), c_line, 1, lineType=cv2.LINE_AA)

        # Convert back to uint8
        out_frame = np.clip(frame, 0, 255).astype(np.uint8)
        writer.append_data(out_frame)
        
        if (f + 1) % 30 == 0:
            print(f"  Rendered {f + 1}/{total_frames} frames ({(f+1)/total_frames*100:.1f}%)")
            
    writer.close()
    print("3D animated background rendering finished successfully!")

if __name__ == "__main__":
    render_3d_background()
