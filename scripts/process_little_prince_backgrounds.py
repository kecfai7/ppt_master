import cv2
import numpy as np

def make_subtle_watermark(input_img_path, output_png_path, width=1920, height=1080, opacity=0.18):
    img = cv2.imread(input_img_path)
    if img is None:
        raise ValueError(f"Could not load {input_img_path}")
        
    # Resize / Crop to 1920x1080 with aspect ratio preserved (cover/fill)
    h, w = img.shape[:2]
    scale = max(width / w, height / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    # Center crop
    x1 = (nw - width) // 2
    y1 = (nh - height) // 2
    cropped = resized[y1:y1+height, x1:x1+width].astype(np.float32)
    
    # Paper-white / soft warm base (B, G, R)
    base = np.full((height, width, 3), 253.0, dtype=np.float32)
    base[:, :, 0] = 255.0 # B
    base[:, :, 1] = 253.0 # G
    base[:, :, 2] = 250.0 # R (subtle warm ivory)
    
    # Blend: 82% base (transparent feel) + 18% illustration
    blended = base * (1.0 - opacity) + cropped * opacity
    result = np.clip(blended, 0, 255).astype(np.uint8)
    
    cv2.imwrite(output_png_path, result)
    print(f"Created subtle watermark: {output_png_path} ({width}x{height}, opacity={opacity*100:.0f}%)")

scenes = [
    ("projects/ai_edu_roundtrip/images/lp_scene_cover.jpg", "projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png"),
    ("projects/ai_edu_roundtrip/images/lp_scene_b612_rose.jpg", "projects/ai_edu_roundtrip/images/bg_lp_subtle_b612.png"),
    ("projects/ai_edu_roundtrip/images/lp_scene_wild_birds.jpg", "projects/ai_edu_roundtrip/images/bg_lp_subtle_birds.png"),
    ("projects/ai_edu_roundtrip/images/lp_scene_fox_wheat.jpg", "projects/ai_edu_roundtrip/images/bg_lp_subtle_fox.png"),
    ("projects/ai_edu_roundtrip/images/lp_scene_desert_well.jpg", "projects/ai_edu_roundtrip/images/bg_lp_subtle_well.png"),
]

for src, dst in scenes:
    make_subtle_watermark(src, dst, opacity=0.18)

print("All subtle Little Prince backgrounds created successfully!")
