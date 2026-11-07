from PIL import Image, ImageDraw, ImageFont
import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)
import perfect_briefings_core_v25 as core

def generate_clean_standalone_poi_map(
    map_base_path: str,
    target_x_norm: float,
    target_y_norm: float,
    poi_label: str,
    pin_color=(245, 200, 60),
    zoom_radius: int = 700
) -> Image.Image:
    """Generates a clean tactical map crop centered on the target POI with NO sidebar and NO extraneous points."""
    base_img = Image.open(map_base_path).convert("RGBA")
    w, h = base_img.size

    # Convert coordinates if normalized or in pixel scale
    px = int(target_x_norm if target_x_norm > 1.0 else target_x_norm * w)
    py = int(target_y_norm if target_y_norm > 1.0 else target_y_norm * h)

    # If coordinates are in 0..2048 scale from DB
    if px < 2500 and w == 4096:
        # Check if coordinates need scale 2x
        px = int(px * 2)
        py = int(py * 2)

    crop_box = (
        max(0, px - zoom_radius),
        max(0, py - zoom_radius),
        min(w, px + zoom_radius),
        min(h, py + zoom_radius)
    )
    cropped = base_img.crop(crop_box)
    draw = ImageDraw.Draw(cropped)

    # Pin center in cropped image
    cx = px - crop_box[0]
    cy = py - crop_box[1]

    # Draw pulsing tactical ring
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(pin_color[0], pin_color[1], pin_color[2], 60), outline=pin_color, width=3)
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=pin_color, outline=(255, 255, 255), width=2)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(20, 20, 20))

    # Clean label below pin
    lbl_w = int(draw.textlength(poi_label, font=core.F_CARD_TITLE)) + 30
    lbl_box = [cx - lbl_w // 2, cy + 22, cx + lbl_w // 2, cy + 58]
    draw.rounded_rectangle(lbl_box, radius=6, fill=(16, 16, 18, 230), outline=pin_color, width=2)
    draw.text((cx - lbl_w // 2 + 15, cy + 28), poi_label, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

    return cropped

# Test Gavroche crop
crop_gav = generate_clean_standalone_poi_map("jacques-bridge.webp", 1479, 313, "CAMPEMENT GAVROCHE")
crop_gav.save("output_maps/test_gavroche_clean_map.png")
print("Gavroche clean crop saved:", crop_gav.size)

# Test Jacques Folly crop
crop_jf = generate_clean_standalone_poi_map("jacques-bridge.webp", 1850, 1520, "ENTRÉE LA FOLIE DE JACQUES", pin_color=(240, 70, 70))
crop_jf.save("output_maps/test_jf_clean_map.png")
print("Jacques Folly clean crop saved:", crop_jf.size)
