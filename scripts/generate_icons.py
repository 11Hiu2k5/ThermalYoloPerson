"""
Script tao Icon Cyber-Thermal Vision cho du an Thermal YOLO Vision Studio.
Xuat day du cac dinh dang:
 - assets/thermal_yolo_icon.svg
 - assets/thermal_yolo_icon.png (1024x1024)
 - assets/thermal_yolo_icon_512.png (512x512)
 - assets/thermal_yolo_icon_256.png (256x256)
 - assets/thermal_yolo_icon_128.png (128x128)
 - assets/thermal_yolo_icon.ico (multi-resolution 256, 128, 64, 48, 32, 16)
"""

import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. TAO VECTOR SVG CHO ICON
# ------------------------------------------------------------------------------
def create_svg() -> str:
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19"/>
      <stop offset="50%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#070A10"/>
    </linearGradient>

    <!-- Outer Rim Glow -->
    <linearGradient id="rimGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF6A00" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#FF3B30" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#1E293B" stop-opacity="0.8"/>
    </linearGradient>

    <!-- Thermal Heat Aura (Behind Figure) -->
    <radialGradient id="thermalAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF6A00" stop-opacity="0.35"/>
      <stop offset="45%" stop-color="#FF3B30" stop-opacity="0.2"/>
      <stop offset="75%" stop-color="#9333EA" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <!-- Head Thermal Gradient (Hotspot Core) -->
    <radialGradient id="headThermal" cx="45%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="25%" stop-color="#FFD54F"/>
      <stop offset="65%" stop-color="#FF6A00"/>
      <stop offset="100%" stop-color="#E11D48"/>
    </radialGradient>

    <!-- Body Thermal Gradient -->
    <linearGradient id="bodyThermal" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFD54F"/>
      <stop offset="22%" stop-color="#FF3B30"/>
      <stop offset="55%" stop-color="#E11D48"/>
      <stop offset="85%" stop-color="#C026D3"/>
      <stop offset="100%" stop-color="#4F46E5"/>
    </linearGradient>

    <!-- Chest Hotspot Core -->
    <radialGradient id="chestCore" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="#FFD54F" stop-opacity="0.9"/>
      <stop offset="75%" stop-color="#FF3B30" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#FF3B30" stop-opacity="0"/>
    </radialGradient>

    <!-- YOLO Badge Gradient -->
    <linearGradient id="yoloBadge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6A00"/>
      <stop offset="100%" stop-color="#FF3B30"/>
    </linearGradient>

    <!-- Subtle Drop Shadow Filter -->
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- 1. Background Squircle Canvas -->
  <rect x="16" y="16" width="992" height="992" rx="224" fill="url(#bgGrad)" stroke="url(#rimGrad)" stroke-width="6"/>

  <!-- 2. Cyber Sensor Scanning Grid (Subtle) -->
  <g opacity="0.12" stroke="#475569" stroke-width="1.5">
    <line x1="160" y1="256" x2="864" y2="256"/>
    <line x1="160" y1="512" x2="864" y2="512"/>
    <line x1="160" y1="768" x2="864" y2="768"/>
    <line x1="256" y1="160" x2="256" y2="864"/>
    <line x1="512" y1="160" x2="512" y2="864"/>
    <line x1="768" y1="160" x2="768" y2="864"/>
  </g>

  <!-- 3. Thermal Camera Optical Aperture & Reticle Rings -->
  <!-- Outer Aperture Ring (Dashed) -->
  <circle cx="512" cy="512" r="416" fill="none" stroke="#334155" stroke-width="3" stroke-dasharray="16 12" opacity="0.4"/>
  <!-- Middle Thermal Optics Ring -->
  <circle cx="512" cy="512" r="348" fill="none" stroke="#FF6A00" stroke-width="2.5" stroke-opacity="0.3"/>
  <!-- Cardinal Tick Marks -->
  <line x1="512" y1="84" x2="512" y2="124" stroke="#FF6A00" stroke-width="4" stroke-linecap="round"/>
  <line x1="512" y1="900" x2="512" y2="940" stroke="#FF6A00" stroke-width="4" stroke-linecap="round"/>
  <line x1="84" y1="512" x2="124" y2="512" stroke="#FF6A00" stroke-width="4" stroke-linecap="round"/>
  <line x1="900" y1="512" x2="940" y2="512" stroke="#FF6A00" stroke-width="4" stroke-linecap="round"/>

  <!-- Camera Outer Corner Tech Brackets -->
  <path d="M 120 180 L 120 120 L 180 120" stroke="#475569" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M 904 180 L 904 120 L 844 120" stroke="#475569" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M 120 844 L 120 904 L 180 904" stroke="#475569" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M 904 844 L 904 904 L 844 904" stroke="#475569" stroke-width="4" fill="none" stroke-linecap="round"/>

  <!-- 4. Thermal Heat Aura (Behind Body) -->
  <ellipse cx="512" cy="510" rx="210" ry="330" fill="url(#thermalAura)"/>

  <!-- 5. Thermal Human Silhouette -->
  <g filter="url(#neonGlow)">
    <!-- Head -->
    <circle cx="512" cy="308" r="62" fill="url(#headThermal)"/>

    <!-- Torso and Limbs (Stylized Human Silhouette) -->
    <path d="
      M 470 382
      C 440 395, 396 425, 388 475
      C 382 510, 400 560, 422 610
      C 428 625, 436 655, 436 670
      L 442 816
      C 442 826, 452 834, 464 834
      C 476 834, 484 826, 486 816
      L 494 660
      C 496 645, 510 635, 512 635
      C 514 635, 528 645, 530 660
      L 538 816
      C 540 826, 548 834, 560 834
      C 572 834, 582 826, 582 816
      L 588 670
      C 588 655, 596 625, 602 610
      C 624 560, 642 510, 636 475
      C 628 425, 584 395, 554 382
      Z"
      fill="url(#bodyThermal)"
    />

    <!-- Internal Heat Core Hotspot on Chest -->
    <ellipse cx="512" cy="455" rx="55" ry="65" fill="url(#chestCore)"/>
  </g>

  <!-- 6. Central AI Target Crosshair Reticle -->
  <circle cx="512" cy="485" r="28" fill="none" stroke="#FFD54F" stroke-width="3" stroke-dasharray="6 4" opacity="0.9"/>
  <circle cx="512" cy="485" r="4" fill="#FFD54F"/>
  <line x1="512" y1="440" x2="512" y2="456" stroke="#FFD54F" stroke-width="3" stroke-linecap="round"/>
  <line x1="512" y1="514" x2="512" y2="530" stroke="#FFD54F" stroke-width="3" stroke-linecap="round"/>
  <line x1="467" y1="485" x2="483" y2="485" stroke="#FFD54F" stroke-width="3" stroke-linecap="round"/>
  <line x1="541" y1="485" x2="557" y2="485" stroke="#FFD54F" stroke-width="3" stroke-linecap="round"/>

  <!-- 7. YOLO Detection Bounding Box -->
  <!-- Main Bounding Box Line -->
  <rect x="256" y="200" width="512" height="660" rx="16" fill="none" stroke="#FF6A00" stroke-width="6" stroke-opacity="0.85"/>

  <!-- Thickened Corner Brackets for Object Detection Lock -->
  <!-- Top-Left -->
  <path d="M 256 270 L 256 200 L 326 200" fill="none" stroke="#FFD54F" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Top-Right -->
  <path d="M 698 200 L 768 200 L 768 270" fill="none" stroke="#FFD54F" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Bottom-Left -->
  <path d="M 256 790 L 256 860 L 326 860" fill="none" stroke="#FFD54F" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Bottom-Right -->
  <path d="M 698 860 L 768 860 L 768 790" fill="none" stroke="#FFD54F" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- 8. YOLO Detection Badge & Text -->
  <g>
    <rect x="256" y="146" width="248" height="50" rx="10" fill="url(#yoloBadge)"/>
    <!-- Small Target Icon inside badge -->
    <circle cx="282" cy="171" r="9" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
    <circle cx="282" cy="171" r="3" fill="#FFFFFF"/>
    <!-- Badge Label -->
    <text x="303" y="180" font-family="'JetBrains Mono', 'Segoe UI', monospace, sans-serif" font-size="24" font-weight="800" fill="#FFFFFF" letter-spacing="1">PERSON 0.98</text>
  </g>

  <!-- 9. Cyber AI Telemetry & Thermal Spectrum Scale -->
  <!-- Top-right LWIR sensor tag -->
  <text x="768" y="178" text-anchor="end" font-family="'JetBrains Mono', 'Segoe UI', monospace, sans-serif" font-size="20" font-weight="700" fill="#FF7A00" letter-spacing="1">● LWIR 8-14µm</text>

  <!-- Bottom AI Status Bar -->
  <g transform="translate(256, 888)">
    <text x="0" y="24" font-family="'JetBrains Mono', 'Segoe UI', monospace, sans-serif" font-size="20" font-weight="700" fill="#64748B" letter-spacing="1.5">YOLOv8n · AI THERMAL</text>
    <!-- Thermal color scale strip -->
    <rect x="360" y="8" width="24" height="18" rx="3" fill="#4F46E5"/>
    <rect x="388" y="8" width="24" height="18" rx="3" fill="#C026D3"/>
    <rect x="416" y="8" width="24" height="18" rx="3" fill="#FF3B30"/>
    <rect x="444" y="8" width="24" height="18" rx="3" fill="#FF6A00"/>
    <rect x="472" y="8" width="24" height="18" rx="3" fill="#FFD54F"/>
    <rect x="500" y="8" width="12" height="18" rx="2" fill="#FFFFFF"/>
  </g>
</svg>
'''
    return svg_content


# ------------------------------------------------------------------------------
# 2. RENDER RA HINH ANH RASTER 1024x1024 BANG PILLOW VOI ANTI-ALIASING CAO CAP
# ------------------------------------------------------------------------------
def render_png_master() -> Image.Image:
    # Render o kich thuoc 2048x2048 (Supersampling 2x) de dat do min cao nhat khi downscale ve 1024x1024
    S = 2048
    scale = S / 1024.0

    # 1. Canvas trong suot
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2. Nen squircle bo tron
    rx = int(224 * scale)
    pad = int(16 * scale)
    box = [pad, pad, S - pad, S - pad]

    # Mask bo tron
    mask = Image.new("L", (S, S), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(box, radius=rx, fill=255)

    # Gradient nen: #0B0F19 -> #111827
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 255))
    bg_arr = np.zeros((S, S, 4), dtype=np.uint8)
    for y in range(S):
        t = y / float(S)
        r = int(11 * (1 - t) + 17 * t)
        g = int(15 * (1 - t) + 24 * t)
        b = int(25 * (1 - t) + 39 * t)
        bg_arr[y, :, 0] = r
        bg_arr[y, :, 1] = g
        bg_arr[y, :, 2] = b
        bg_arr[y, :, 3] = 255
    bg = Image.fromarray(bg_arr, "RGBA")

    # Dan vien ngoai
    rim = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    rim_draw = ImageDraw.Draw(rim)
    rim_draw.rounded_rectangle(box, radius=rx, outline=(255, 106, 0, 160), width=int(6 * scale))

    # Ket hop nen va vien
    img.paste(bg, (0, 0), mask)
    img = Image.alpha_composite(img, rim)
    draw = ImageDraw.Draw(img)

    # 3. Luoi cyber sensor mo ao
    grid_color = (71, 85, 105, 30)
    for g_coord in [256, 512, 768]:
        pos = int(g_coord * scale)
        draw.line([(int(160 * scale), pos), (int(864 * scale), pos)], fill=grid_color, width=int(2 * scale))
        draw.line([(pos, int(160 * scale)), (pos, int(864 * scale))], fill=grid_color, width=int(2 * scale))

    # 4. Vong tron ong kinh camera nhiet (Aperture / Reticle Rings)
    cx, cy = int(512 * scale), int(512 * scale)
    r_outer = int(416 * scale)
    r_mid = int(348 * scale)

    # Vong ngoai cham bi / phan doan
    for angle in range(0, 360, 6):
        rad = math.radians(angle)
        x1 = cx + (r_outer - 4) * math.cos(rad)
        y1 = cy + (r_outer - 4) * math.sin(rad)
        x2 = cx + (r_outer + 4) * math.cos(rad)
        y2 = cy + (r_outer + 4) * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=(51, 65, 85, 90), width=int(3 * scale))

    # Vong giua mau cam neon mo
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=(255, 106, 0, 80), width=int(3 * scale))

    # Vach chi huong quang hoc 4 goc chinh (Cardinal Ticks)
    tick_len = int(40 * scale)
    tick_w = int(4 * scale)
    draw.line([(cx, int(84 * scale)), (cx, int(84 * scale) + tick_len)], fill=(255, 106, 0, 240), width=tick_w)
    draw.line([(cx, int(940 * scale) - tick_len), (cx, int(940 * scale))], fill=(255, 106, 0, 240), width=tick_w)
    draw.line([(int(84 * scale), cy), (int(84 * scale) + tick_len, cy)], fill=(255, 106, 0, 240), width=tick_w)
    draw.line([(int(940 * scale) - tick_len, cy), (int(940 * scale), cy)], fill=(255, 106, 0, 240), width=tick_w)

    # 4 goc hud reticle
    bracket_w = int(4 * scale)
    bracket_l = int(60 * scale)
    b_col = (71, 85, 105, 180)
    # TL
    draw.line([(int(120 * scale), int(180 * scale)), (int(120 * scale), int(120 * scale))], fill=b_col, width=bracket_w)
    draw.line([(int(120 * scale), int(120 * scale)), (int(180 * scale), int(120 * scale))], fill=b_col, width=bracket_w)
    # TR
    draw.line([(int(904 * scale), int(180 * scale)), (int(904 * scale), int(120 * scale))], fill=b_col, width=bracket_w)
    draw.line([(int(904 * scale), int(120 * scale)), (int(844 * scale), int(120 * scale))], fill=b_col, width=bracket_w)
    # BL
    draw.line([(int(120 * scale), int(844 * scale)), (int(120 * scale), int(904 * scale))], fill=b_col, width=bracket_w)
    draw.line([(int(120 * scale), int(904 * scale)), (int(180 * scale), int(904 * scale))], fill=b_col, width=bracket_w)
    # BR
    draw.line([(int(904 * scale), int(844 * scale)), (int(904 * scale), int(904 * scale))], fill=b_col, width=bracket_w)
    draw.line([(int(904 * scale), int(904 * scale)), (int(844 * scale), int(904 * scale))], fill=b_col, width=bracket_w)

    # 5. Lop phat xa nhiet (Thermal Heat Aura)
    aura_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    aura_arr = np.zeros((S, S, 4), dtype=np.uint8)
    yy, xx = np.ogrid[:S, :S]
    dist_sq = ((xx - cx) / (220 * scale)) ** 2 + ((yy - int(510 * scale)) / (340 * scale)) ** 2
    aura_mask = np.clip(1.0 - np.sqrt(dist_sq), 0.0, 1.0)
    aura_arr[:, :, 0] = 255  # Red
    aura_arr[:, :, 1] = 106  # Green
    aura_arr[:, :, 2] = 0    # Blue
    aura_arr[:, :, 3] = (aura_mask * 90).astype(np.uint8)
    aura_img = Image.fromarray(aura_arr, "RGBA").filter(ImageFilter.GaussianBlur(int(20 * scale)))
    img = Image.alpha_composite(img, aura_img)
    draw = ImageDraw.Draw(img)

    # 6. Hinh nguoi anh nhiet (Thermal Human Figure)
    # Head hotspot (Diem nhiet cuc dai: Vang ruc - Do)
    head_cx, head_cy = cx, int(308 * scale)
    head_r = int(62 * scale)

    # Ve dau voi gradient tam (radial)
    head_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    head_arr = np.zeros((S, S, 4), dtype=np.uint8)
    h_yy, h_xx = np.ogrid[:S, :S]
    h_dist = np.sqrt((h_xx - head_cx) ** 2 + (h_yy - head_cy) ** 2)
    h_mask = h_dist <= head_r

    # Noi suy mau nhiet tu tam ra vien: White/Yellow -> Orange -> Red -> Crimson
    norm_dist = np.clip(h_dist / head_r, 0.0, 1.0)
    head_arr[h_mask, 0] = np.clip(255, 0, 255)
    head_arr[h_mask, 1] = np.clip((255 * (1 - norm_dist) + 59 * norm_dist)[h_mask], 0, 255)
    head_arr[h_mask, 2] = np.clip((120 * (1 - norm_dist) * (1 - norm_dist))[h_mask], 0, 255)
    head_arr[h_mask, 3] = 255
    head_img = Image.fromarray(head_arr, "RGBA")
    img = Image.alpha_composite(img, head_img)
    draw = ImageDraw.Draw(img)

    # Than hinh nguoi (Torso & Limbs) voi toa do ti le
    body_pts = [
        (470, 382),
        (440, 395), (410, 420), (388, 475),
        (382, 510), (400, 560), (422, 610),
        (428, 625), (436, 655), (436, 670),
        (442, 816), (452, 834), (464, 834), (476, 834), (486, 816),
        (494, 660), (500, 640), (512, 635), (524, 640), (530, 660),
        (538, 816), (548, 834), (560, 834), (572, 834), (582, 816),
        (588, 670), (588, 655), (596, 625), (602, 610),
        (624, 560), (642, 510), (636, 475),
        (614, 420), (584, 395), (554, 382),
    ]
    scaled_pts = [(int(x * scale), int(y * scale)) for x, y in body_pts]

    # Tao mask cho than nguoi
    body_mask = Image.new("L", (S, S), 0)
    bm_draw = ImageDraw.Draw(body_mask)
    bm_draw.polygon(scaled_pts, fill=255)

    # Gradient mau nhiet doc theo than nguoi (Y-axis false color gradient)
    body_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    body_arr = np.zeros((S, S, 4), dtype=np.uint8)
    y_min, y_max = int(380 * scale), int(840 * scale)

    for y in range(y_min, y_max):
        frac = (y - y_min) / float(y_max - y_min)
        if frac < 0.25:  # Co & nguc: Vang -> Cam
            f2 = frac / 0.25
            r, g, b = 255, int(213 * (1 - f2) + 106 * f2), int(79 * (1 - f2))
        elif frac < 0.55:  # Bung & hong: Cam -> Do
            f2 = (frac - 0.25) / 0.30
            r, g, b = 255, int(106 * (1 - f2) + 59 * f2), int(48 * f2)
        elif frac < 0.80:  # Dui: Do -> Tim
            f2 = (frac - 0.55) / 0.25
            r, g, b = int(255 * (1 - f2) + 192 * f2), int(59 * (1 - f2) + 38 * f2), int(48 * (1 - f2) + 211 * f2)
        else:  # Chan & ban chan: Tim -> Xanh tim lanh
            f2 = (frac - 0.80) / 0.20
            r, g, b = int(192 * (1 - f2) + 79 * f2), int(38 * (1 - f2) + 70 * f2), int(211 * (1 - f2) + 229 * f2)
        body_arr[y, :, 0] = r
        body_arr[y, :, 1] = g
        body_arr[y, :, 2] = b
        body_arr[y, :, 3] = 255

    body_colored = Image.fromarray(body_arr, "RGBA")
    img.paste(body_colored, (0, 0), body_mask)
    draw = ImageDraw.Draw(img)

    # Core hotspot o tam nguc (White-Yellow Core)
    chest_cx, chest_cy = cx, int(455 * scale)
    chest_rx, chest_ry = int(55 * scale), int(65 * scale)
    c_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    c_arr = np.zeros((S, S, 4), dtype=np.uint8)
    c_dist = ((xx - chest_cx) / chest_rx) ** 2 + ((yy - chest_cy) / chest_ry) ** 2
    c_mask = c_dist <= 1.0
    c_factor = np.clip(1.0 - np.sqrt(c_dist), 0.0, 1.0)
    c_arr[c_mask, 0] = 255
    c_arr[c_mask, 1] = np.clip(255 * c_factor[c_mask] + 213 * (1 - c_factor[c_mask]), 0, 255)
    c_arr[c_mask, 2] = np.clip(180 * (c_factor[c_mask] ** 2), 0, 255)
    c_arr[c_mask, 3] = np.clip(c_factor[c_mask] * 240, 0, 255)
    c_img = Image.fromarray(c_arr, "RGBA").filter(ImageFilter.GaussianBlur(int(4 * scale)))
    img = Image.alpha_composite(img, c_img)
    draw = ImageDraw.Draw(img)

    # 7. Tam ngam AI trung tam (Central Target Reticle)
    reticle_cy = int(485 * scale)
    r_target = int(28 * scale)
    draw.ellipse(
        [cx - r_target, reticle_cy - r_target, cx + r_target, reticle_cy + r_target],
        outline=(255, 213, 79, 230),
        width=int(3 * scale),
    )
    draw.ellipse(
        [cx - int(4 * scale), reticle_cy - int(4 * scale), cx + int(4 * scale), reticle_cy + int(4 * scale)],
        fill=(255, 213, 79, 255),
    )
    # Ticks crosshair
    draw.line([(cx, reticle_cy - int(45 * scale)), (cx, reticle_cy - int(29 * scale))], fill=(255, 213, 79, 230), width=int(3 * scale))
    draw.line([(cx, reticle_cy + int(29 * scale)), (cx, reticle_cy + int(45 * scale))], fill=(255, 213, 79, 230), width=int(3 * scale))
    draw.line([(cx - int(45 * scale), reticle_cy), (cx - int(29 * scale), reticle_cy)], fill=(255, 213, 79, 230), width=int(3 * scale))
    draw.line([(cx + int(29 * scale), reticle_cy), (cx + int(45 * scale), reticle_cy)], fill=(255, 213, 79, 230), width=int(3 * scale))

    # 8. YOLO Bounding Box & Target Brackets
    bx1, by1 = int(256 * scale), int(200 * scale)
    bx2, by2 = int(768 * scale), int(860 * scale)
    box_r = int(16 * scale)

    # Duong vien hop nhan dien mau cam
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=box_r, outline=(255, 106, 0, 210), width=int(6 * scale))

    # 4 Goc ngoac day dam mau vang YOLO Target Lock
    corner_w = int(14 * scale)
    corner_l = int(70 * scale)
    c_color = (255, 213, 79, 255)

    # Top-Left
    draw.line([(bx1, by1 + corner_l), (bx1, by1)], fill=c_color, width=corner_w)
    draw.line([(bx1, by1), (bx1 + corner_l, by1)], fill=c_color, width=corner_w)
    # Top-Right
    draw.line([(bx2 - corner_l, by1), (bx2, by1)], fill=c_color, width=corner_w)
    draw.line([(bx2, by1), (bx2, by1 + corner_l)], fill=c_color, width=corner_w)
    # Bottom-Left
    draw.line([(bx1, by2 - corner_l), (bx1, by2)], fill=c_color, width=corner_w)
    draw.line([(bx1, by2), (bx1 + corner_l, by2)], fill=c_color, width=corner_w)
    # Bottom-Right
    draw.line([(bx2 - corner_l, by2), (bx2, by2)], fill=c_color, width=corner_w)
    draw.line([(bx2, by2), (bx2, by2 - corner_l)], fill=c_color, width=corner_w)

    # 9. Badge nhan dien "PERSON 0.98"
    badge_w = int(248 * scale)
    badge_h = int(50 * scale)
    badge_y = int(146 * scale)

    # Gradient cua badge: Cam -> Do
    badge_box = [bx1, badge_y, bx1 + badge_w, badge_y + badge_h]
    draw.rounded_rectangle(badge_box, radius=int(10 * scale), fill=(255, 87, 34, 255))

    # Icon tam giac / tron nho trong badge
    b_ic_x, b_ic_y = bx1 + int(26 * scale), badge_y + int(25 * scale)
    draw.ellipse([b_ic_x - int(9 * scale), b_ic_y - int(9 * scale), b_ic_x + int(9 * scale), b_ic_y + int(9 * scale)], outline=(255, 255, 255, 255), width=int(3 * scale))
    draw.ellipse([b_ic_x - int(3 * scale), b_ic_y - int(3 * scale), b_ic_x + int(3 * scale), b_ic_y + int(3 * scale)], fill=(255, 255, 255, 255))

    # Font chu
    font_size = int(24 * scale)
    font = None
    # Tim font co san tren Windows
    font_candidates = [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
    ]
    for fc in font_candidates:
        if Path(fc).exists():
            try:
                font = ImageFont.truetype(fc, font_size)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    draw.text((bx1 + int(48 * scale), badge_y + int(10 * scale)), "PERSON 0.98", fill=(255, 255, 255, 255), font=font)

    # Sensor Telemetry: Top-Right Tag
    sm_font_size = int(20 * scale)
    sm_font = None
    for fc in font_candidates:
        if Path(fc).exists():
            try:
                sm_font = ImageFont.truetype(fc, sm_font_size)
                break
            except Exception:
                pass
    if sm_font is None:
        sm_font = ImageFont.load_default()

    draw.text((int(610 * scale), int(158 * scale)), "LWIR 8-14µm", fill=(255, 122, 0, 240), font=sm_font)

    # Bottom AI Status & False-color palette strip
    draw.text((bx1, int(890 * scale)), "YOLOv8n · AI THERMAL", fill=(100, 116, 139, 240), font=sm_font)

    # Dải màu thang nhiệt ở góc dưới phải
    strip_colors = [
        (79, 70, 229),   # Indigo
        (192, 38, 211),  # Violet
        (255, 59, 48),   # Red
        (255, 106, 0),   # Orange
        (255, 213, 79),  # Yellow
        (255, 255, 255), # Hot white
    ]
    sw_x = bx1 + int(360 * scale)
    sw_y = int(895 * scale)
    sw_w = int(22 * scale)
    sw_h = int(16 * scale)
    for i, sc in enumerate(strip_colors):
        x_pos = sw_x + i * int(26 * scale)
        draw.rounded_rectangle([x_pos, sw_y, x_pos + sw_w, sw_y + sw_h], radius=int(3 * scale), fill=(*sc, 255))

    # Downsample tu 2048x2048 ve 1024x1024 bang bo loc Lanczos cao cap
    img_1024 = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    return img_1024


# ------------------------------------------------------------------------------
# 3. HAM CHINH: XUAT TAT CA CAC DINH DANG ICON
# ------------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("  KHOI TAO ICON CYBER-THERMAL CHO THERMAL YOLO VISION STUDIO")
    print("=" * 70)

    # 1. Xuat SVG
    svg_str = create_svg()
    svg_path = ASSETS_DIR / "thermal_yolo_icon.svg"
    svg_path.write_text(svg_str, encoding="utf-8")
    print(f"[OK] Da tao vector SVG: {svg_path} ({svg_path.stat().st_size:,} bytes)")

    # 2. Render Master PNG (1024x1024)
    print("[*] Dang render master PNG 1024x1024 bang thuat toan 2x Supersampling...")
    master_1024 = render_png_master()
    png_1024_path = ASSETS_DIR / "thermal_yolo_icon.png"
    master_1024.save(png_1024_path, format="PNG", optimize=True)
    print(f"[OK] Da tao master PNG (1024x1024): {png_1024_path} ({png_1024_path.stat().st_size:,} bytes)")

    # 3. Xuat cac ban thu nho: 512, 256, 128
    sizes = [512, 256, 128]
    for sz in sizes:
        resized = master_1024.resize((sz, sz), Image.Resampling.LANCZOS)
        out_p = ASSETS_DIR / f"thermal_yolo_icon_{sz}.png"
        resized.save(out_p, format="PNG", optimize=True)
        print(f"[OK] Da tao PNG ({sz}x{sz}): {out_p} ({out_p.stat().st_size:,} bytes)")

    # 4. Xuat Windows Icon (.ico) chua da tang do phan giai: 256, 128, 64, 48, 32, 16
    ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    ico_images = [master_1024.resize(s, Image.Resampling.LANCZOS) for s in ico_sizes]
    ico_path = ASSETS_DIR / "thermal_yolo_icon.ico"
    master_1024.save(ico_path, format="ICO", sizes=ico_sizes)
    print(f"[OK] Da tao Windows Icon (.ico da phan giai): {ico_path} ({ico_path.stat().st_size:,} bytes)")

    # 5. Tao ma Base64 de nhung truc tiep vao app.py (Zero-dependency fallback)
    import base64
    b64_png_128 = base64.b64encode(open(ASSETS_DIR / "thermal_yolo_icon_128.png", "rb").read()).decode("utf-8")
    b64_svg = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")

    code_snippet = f'''# AUTO-GENERATED EMBEDDED ICONS FOR ZERO-DEPENDENCY FALLBACK
ICON_PNG_B64 = "{b64_png_128}"
ICON_SVG_B64 = "{b64_svg}"
'''
    (ASSETS_DIR / "icon_data.py").write_text(code_snippet, encoding="utf-8")
    print(f"[OK] Da xuat module nhung truc tiep: {ASSETS_DIR / 'icon_data.py'}")

    print("\nHOAN TAT TOAN BO CAC FILE ICON!")


if __name__ == "__main__":
    main()
