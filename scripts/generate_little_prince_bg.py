import numpy as np
import imageio
import math
import cv2

def render_little_prince_background(
    filename="projects/ai_edu_roundtrip/images/bg_little_prince_loop.mp4",
    poster_filename="projects/ai_edu_roundtrip/images/bg_little_prince_poster.png",
    width=1280, height=720, duration=6, fps=30
):
    total_frames = duration * fps
    print(f"Generating Little Prince animated background: {width}x{height}, {duration}s @ {fps}fps ({total_frames} frames)...")
    
    writer = imageio.get_writer(
        filename, 
        fps=fps, 
        codec='libx264', 
        quality=8, 
        pixelformat='yuv420p',
        macro_block_size=16
    )

    np.random.seed(123)

    # 1. Twinkling Stars
    num_stars = 140
    star_x = np.random.uniform(20, width - 20, num_stars)
    star_y = np.random.uniform(20, height * 0.75, num_stars)
    star_base_r = np.random.uniform(1.0, 3.2, num_stars)
    star_freq = np.random.uniform(1.0, 3.0, num_stars)
    star_phase = np.random.uniform(0, 2 * math.pi, num_stars)
    star_is_gold = np.random.choice([False, True], size=num_stars, p=[0.75, 0.25])

    # 2. Floating Golden Stardust Particles
    num_particles = 45
    part_x = np.random.uniform(width * 0.45, width * 0.95, num_particles)
    part_base_y = np.random.uniform(height * 0.35, height * 0.90, num_particles)
    part_speed_y = np.random.uniform(15.0, 40.0, num_particles)
    part_amp_x = np.random.uniform(10.0, 25.0, num_particles)
    part_phase = np.random.uniform(0, 2 * math.pi, num_particles)
    part_size = np.random.uniform(1.5, 3.5, num_particles)

    # 3. Base Background Gradient: Deep Midnight Indigo to Warm Cosmic Twilight
    base_bg = np.zeros((height, width, 3), dtype=np.float32)
    y_norm = np.linspace(0, 1, height)[:, None] # (height, 1)
    
    # Gradient colors (BGR for OpenCV operations)
    # Top: Deep Indigo Blue (B=40, G=15, R=10)
    # Mid: Twilight Purple-Navy (B=70, G=30, R=25)
    # Bottom: Warm Horizon Stardust (B=60, G=35, R=45)
    for c, (val_top, val_mid, val_bot) in enumerate([(42, 70, 55), (16, 32, 38), (10, 26, 45)]):
        col_curve = np.where(y_norm < 0.6,
                             val_top + (val_mid - val_top) * (y_norm / 0.6),
                             val_mid + (val_bot - val_mid) * ((y_norm - 0.6) / 0.4))
        base_bg[:, :, c] = col_curve

    # Soft ambient nebula glow in upper right and center
    y_coords, x_coords = np.ogrid[:height, :width]
    nebula_dist = np.sqrt(((x_coords - width * 0.75) / (width * 0.45))**2 + ((y_coords - height * 0.35) / (height * 0.45))**2)
    nebula_mask = np.clip(1.0 - nebula_dist, 0.0, 1.0) ** 2
    base_bg[:, :, 0] += nebula_mask * 45  # Blue
    base_bg[:, :, 1] += nebula_mask * 20  # Green
    base_bg[:, :, 2] += nebula_mask * 35  # Red (Amethyst glow)

    # Pre-render Asteroid B612 Geometry
    # B612 is a gentle rounded celestial body positioned at bottom-right (center around x=1050, y=980, radius=480)
    ast_cx, ast_cy, ast_r = 1040, 960, 450
    dist_ast = np.sqrt((x_coords - ast_cx)**2 + (y_coords - ast_cy)**2)
    asteroid_mask = dist_ast <= ast_r

    # Asteroid surface shading
    ast_shading = np.clip((ast_r - dist_ast) / ast_r, 0, 1)
    asteroid_b = 60 + ast_shading * 40
    asteroid_g = 55 + ast_shading * 35
    asteroid_r = 65 + ast_shading * 45

    # Little Prince coordinates on Asteroid
    # LP stands atop the curved horizon of B612 around x=820
    lp_x = 830
    # y coordinate on asteroid surface:
    lp_feet_y = int(ast_cy - math.sqrt(max(0, ast_r**2 - (lp_x - ast_cx)**2)))

    # Rose location on asteroid (x=960)
    rose_x = 950
    rose_feet_y = int(ast_cy - math.sqrt(max(0, ast_r**2 - (rose_x - ast_cx)**2)))

    # Small volcano location on asteroid (x=1110)
    volcano_x = 1110
    volcano_feet_y = int(ast_cy - math.sqrt(max(0, ast_r**2 - (volcano_x - ast_cx)**2)))

    first_frame = None

    for f in range(total_frames):
        t = (2.0 * math.pi * f) / total_frames
        frame = base_bg.copy()

        # A. Draw Shooting Star (Periodic comets)
        # Comet 1: passes during t in [0.2, 0.45]
        progress_c1 = (f % total_frames) / total_frames
        if 0.15 < progress_c1 < 0.40:
            c1_t = (progress_c1 - 0.15) / 0.25
            c1_x = int(width * 0.95 - c1_t * 600)
            c1_y = int(height * 0.10 + c1_t * 180)
            c1_tail_x = int(c1_x + 90)
            c1_tail_y = int(c1_y - 27)
            alpha_comet = math.sin(c1_t * math.pi)
            if alpha_comet > 0.05:
                cv2.line(frame, (c1_tail_x, c1_tail_y), (c1_x, c1_y),
                         [int(220 * alpha_comet), int(235 * alpha_comet), int(255 * alpha_comet)], 2, lineType=cv2.LINE_AA)
                cv2.circle(frame, (c1_x, c1_y), 3,
                           [int(240 * alpha_comet), int(250 * alpha_comet), int(255 * alpha_comet)], -1, lineType=cv2.LINE_AA)

        # B. Twinkling Stars
        for i in range(num_stars):
            # Pulse intensity
            brightness = 0.5 + 0.5 * math.sin(t * star_freq[i] + star_phase[i])
            sx = int(star_x[i])
            sy = int(star_y[i])
            
            # Don't draw stars inside the solid asteroid
            if dist_ast[sy, sx] < ast_r - 5:
                continue

            r = max(1, int(star_base_r[i] * (0.7 + 0.5 * brightness)))
            if star_is_gold[i]:
                color = [int(120 * brightness + 60), int(190 * brightness + 50), int(255 * brightness)] # BGR Gold
            else:
                color = [int(255 * brightness), int(240 * brightness + 15), int(220 * brightness + 35)] # BGR Diamond White

            cv2.circle(frame, (sx, sy), r, color, -1, lineType=cv2.LINE_AA)
            if star_base_r[i] > 2.2 and brightness > 0.7:
                # 4-point subtle star twinkle glint
                glint_len = int(star_base_r[i] * 3 * brightness)
                c_glint = [c * 0.4 for c in color]
                cv2.line(frame, (sx - glint_len, sy), (sx + glint_len, sy), c_glint, 1, lineType=cv2.LINE_AA)
                cv2.line(frame, (sx, sy - glint_len), (sx, sy + glint_len), c_glint, 1, lineType=cv2.LINE_AA)

        # C. Draw Constellation lines (AI Stellar Network)
        constellation_pairs = [
            (5, 12), (12, 19), (19, 27), (27, 34),
            (42, 50), (50, 61), (61, 72),
            (83, 91), (91, 102), (102, 114)
        ]
        alpha_net = 0.28 + 0.12 * math.sin(t)
        for p1, p2 in constellation_pairs:
            x1, y1 = int(star_x[p1]), int(star_y[p1])
            x2, y2 = int(star_x[p2]), int(star_y[p2])
            if dist_ast[y1, x1] >= ast_r and dist_ast[y2, x2] >= ast_r:
                cv2.line(frame, (x1, y1), (x2, y2), [int(180 * alpha_net), int(150 * alpha_net), int(220 * alpha_net)], 1, lineType=cv2.LINE_AA)

        # D. Render Asteroid B612
        frame[asteroid_mask, 0] = asteroid_b[asteroid_mask]
        frame[asteroid_mask, 1] = asteroid_g[asteroid_mask]
        frame[asteroid_mask, 2] = asteroid_r[asteroid_mask]

        # Asteroid rim atmospheric glow
        rim_width = 8
        rim_mask = (dist_ast <= ast_r) & (dist_ast >= ast_r - rim_width)
        frame[rim_mask, 0] += 40
        frame[rim_mask, 1] += 50
        frame[rim_mask, 2] += 70

        # E. Draw Volcano on Asteroid (with rising warm embers)
        vx, vy = volcano_x, volcano_feet_y
        volc_pts = np.array([[vx - 22, vy + 10], [vx + 22, vy + 10], [vx + 14, vy - 28], [vx - 14, vy - 28]], np.int32)
        cv2.fillPoly(frame, [volc_pts], (45, 40, 50), lineType=cv2.LINE_AA)
        cv2.ellipse(frame, (vx, vy - 28), (14, 4), 0, 0, 360, (20, 80, 220), -1, lineType=cv2.LINE_AA) # Ember crater

        # F. Draw The Rose under the Glass Cloche
        rx, ry = rose_x, rose_feet_y
        # Stem & leaf
        cv2.line(frame, (rx, ry), (rx, ry - 35), (60, 140, 70), 2, lineType=cv2.LINE_AA)
        cv2.ellipse(frame, (rx + 6, ry - 18), (6, 3), 25, 0, 360, (50, 130, 60), -1, lineType=cv2.LINE_AA)
        # Rose blossom with gentle breathing glow
        rose_pulse = 0.8 + 0.2 * math.sin(t * 2.0)
        cv2.circle(frame, (rx, ry - 38), int(8 * rose_pulse), (70, 70, 240), -1, lineType=cv2.LINE_AA) # Outer rose
        cv2.circle(frame, (rx, ry - 38), int(5 * rose_pulse), (100, 120, 255), -1, lineType=cv2.LINE_AA) # Rose core
        # Glass cloche dome
        cv2.ellipse(frame, (rx, ry - 28), (16, 26), 0, 180, 360, (210, 190, 160), 1, lineType=cv2.LINE_AA)
        cv2.line(frame, (rx - 16, ry - 28), (rx - 16, ry + 2), (210, 190, 160), 1, lineType=cv2.LINE_AA)
        cv2.line(frame, (rx + 16, ry - 28), (rx + 16, ry + 2), (210, 190, 160), 1, lineType=cv2.LINE_AA)
        # Cloche knob
        cv2.circle(frame, (rx, ry - 54), 3, (220, 200, 180), -1, lineType=cv2.LINE_AA)

        # G. Draw The Little Prince
        # Feet: (lp_x, lp_feet_y)
        # Body coordinates
        lpx = lp_x
        lpy = lp_feet_y
        
        # Legs / Pants (Emerald Green suit / classic Little Prince)
        cv2.line(frame, (lpx - 5, lpy), (lpx - 4, lpy - 30), (70, 150, 80), 3, lineType=cv2.LINE_AA)
        cv2.line(frame, (lpx + 5, lpy), (lpx + 4, lpy - 30), (70, 150, 80), 3, lineType=cv2.LINE_AA)
        
        # Torso / Tunic
        torso_pts = np.array([[lpx - 8, lpy - 30], [lpx + 8, lpy - 30], [lpx + 10, lpy - 62], [lpx - 10, lpy - 62]], np.int32)
        cv2.fillPoly(frame, [torso_pts], (75, 160, 85), lineType=cv2.LINE_AA)
        # Golden Belt
        cv2.line(frame, (lpx - 9, lpy - 42), (lpx + 9, lpy - 42), (40, 200, 255), 2, lineType=cv2.LINE_AA)
        
        # Head (facing slightly left towards the cosmos)
        head_cx = lpx
        head_cy = lpy - 74
        cv2.circle(frame, (head_cx, head_cy), 10, (180, 210, 245), -1, lineType=cv2.LINE_AA)
        
        # Golden Tousled Hair (Iconic yellow curls blowing gently in wind)
        hair_wave = 2.0 * math.sin(t * 2.0)
        hair_pts = np.array([
            [head_cx - 10, head_cy], 
            [head_cx - 13, head_cy - 12 + int(hair_wave)], 
            [head_cx - 4, head_cy - 17 + int(hair_wave * 0.8)],
            [head_cx + 8, head_cy - 15 - int(hair_wave)],
            [head_cx + 12, head_cy - 4],
            [head_cx + 4, head_cy + 2]
        ], np.int32)
        cv2.fillPoly(frame, [hair_pts], (50, 210, 255), lineType=cv2.LINE_AA) # Golden Yellow (BGR)

        # Fluttering Golden Scarf (Periodic fluid wave physics)
        # Flows from neck (lpx - 4, lpy - 64) towards left (into the space)
        scarf_pts = []
        scarf_len = 55
        for s_idx in range(scarf_len):
            sx = (lpx - 4) - s_idx * 1.1
            # Wave propagation
            sy = (lpy - 64) + 6.0 * math.sin(t * 3.0 + s_idx * 0.18) + (s_idx * 0.15)
            scarf_pts.append([int(sx), int(sy)])
            
        scarf_pts = np.array(scarf_pts, np.int32)
        cv2.polylines(frame, [scarf_pts], isClosed=False, color=(40, 215, 255), thickness=4, lineType=cv2.LINE_AA)
        # Scarf inner highlight
        cv2.polylines(frame, [scarf_pts], isClosed=False, color=(120, 235, 255), thickness=2, lineType=cv2.LINE_AA)

        # H. Golden Stardust Particles Floating Upward (Laughing Stars)
        for i in range(num_particles):
            # Upward motion with loop wrap-around
            p_y = (part_base_y[i] - (f / total_frames) * part_speed_y[i] * 3.0) % height
            p_x = part_x[i] + part_amp_x[i] * math.sin(t * 1.5 + part_phase[i])
            
            p_alpha = 0.4 + 0.6 * math.sin(t * 2.0 + part_phase[i])
            cv2.circle(frame, (int(p_x), int(p_y)), int(part_size[i]),
                       [int(40 * p_alpha), int(200 * p_alpha), int(255 * p_alpha)], -1, lineType=cv2.LINE_AA)

        # Convert float32 to uint8
        out_frame = np.clip(frame, 0, 255).astype(np.uint8)
        writer.append_data(out_frame)

        if f == 0:
            first_frame = out_frame.copy()

        if (f + 1) % 30 == 0:
            print(f"  Rendered {f + 1}/{total_frames} frames ({(f+1)/total_frames*100:.1f}%)")

    writer.close()
    
    # Save poster frame (imageio uses RGB)
    imageio.imwrite(poster_filename, first_frame)
    print(f"Little Prince dynamic background generated: {filename} & poster: {poster_filename}")

if __name__ == "__main__":
    render_little_prince_background()
