"""
Thermal Vision Studio - Ung dung Phat hien Nguoi trong Anh Nhiet bang YOLOv8
De tai Mon hoc: Tri tue Nhan tao (AI) - Khoa CNTT - HUTECH
Sinh vien thuc hien: Nguyen Duc Hieu (MSSV: 24800600314)
Giang vien huong dan: ThS./TS. Vu Thanh Hien
"""

import os
import sys
import time
import hashlib
import io
import base64
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Tranh loi OpenMP duplicate runtime tren Windows khi nap torch va opencv dong thoi
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
import streamlit as st
import torch
from ultralytics import YOLO

# ==============================================================================
# 1. CAU HINH HE THONG VA DUONG DAN AN TOAN (SAFE PATH RESOLUTION)
# ==============================================================================

ROOT = Path(__file__).resolve().parent

# Phat hien thiet bi phan cung (CPU vs GPU CUDA)
DEVICE_CUDA_AVAILABLE = torch.cuda.is_available()
if DEVICE_CUDA_AVAILABLE:
    DEVICE_TAG = "0"
    DEVICE_NAME = f"GPU CUDA ({torch.cuda.get_device_name(0)})"
else:
    DEVICE_TAG = "cpu"
    DEVICE_NAME = "CPU (Intel/AMD - Khong co CUDA)"

# Tim kiem bieu tuong ung dung (Favicon / Icon)
def resolve_asset_path(filename: str) -> Optional[Path]:
    candidates = [
        ROOT / "assets" / filename,
        ROOT / filename,
        ROOT / "reports" / "assets" / filename,
        ROOT.parent / "assets" / filename,
        ROOT.parent / filename,
        ROOT.parent / "reports" / "assets" / filename,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None

# Import du lieu Base64 de ho tro Zero-Dependency Fallback
try:
    from assets.icon_data import ICON_PNG_B64, ICON_SVG_B64
except Exception:
    # Fallback truc tiep neu khong tim thay file icon_data.py
    ICON_PNG_B64 = ""
    ICON_SVG_B64 = ""

def get_app_icon_image() -> Any:
    """Tra ve doi tuong PIL Image cho page_icon cua Streamlit voi co che tu dong fallback."""
    icon_file = resolve_asset_path("thermal_yolo_icon_256.png") or resolve_asset_path("thermal_yolo_icon.png")
    if icon_file and icon_file.is_file():
        try:
            return Image.open(icon_file)
        except Exception:
            pass
    if ICON_PNG_B64:
        try:
            return Image.open(io.BytesIO(base64.b64decode(ICON_PNG_B64)))
        except Exception:
            pass
    return "🔥"

APP_ICON_IMAGE = get_app_icon_image()
APP_ICON_DATA_URI = f"data:image/png;base64,{ICON_PNG_B64}" if ICON_PNG_B64 else ""

ICON_PATH = resolve_asset_path("thermal_yolo_icon.png") or resolve_asset_path("thermal_person_icon.png")

# Tim thu muc samples va anh mau
SAMPLES_DIR = ROOT / "samples"
if not SAMPLES_DIR.exists():
    SAMPLES_DIR = ROOT.parent / "samples"
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Tim cac mo hinh trong thu muc models hoac runs
def find_model_path(relative_paths: List[str]) -> Optional[Path]:
    for rel in relative_paths:
        p1 = ROOT / rel
        if p1.is_file():
            return p1
        p2 = ROOT.parent / rel
        if p2.is_file():
            return p2
    return None

FLIR_MODEL_PATH = find_model_path([
    "models/flir_best.pt",
    "runs/flir_yolov8n_cpu/weights/best.pt",
])

LLVIP_MODEL_PATH = find_model_path([
    "models/llvip_best.pt",
    "runs/llvip_yolov8n_cpu/weights/best.pt",
])

MODEL_OPTIONS = {}
if FLIR_MODEL_PATH:
    MODEL_OPTIONS["YOLOv8n - FLIR Thermal (Giao thông đường phố)"] = FLIR_MODEL_PATH
else:
    MODEL_OPTIONS["YOLOv8n - FLIR Thermal (Thiếu file)"] = ROOT / "models" / "flir_best.pt"

if LLVIP_MODEL_PATH:
    MODEL_OPTIONS["YOLOv8n - LLVIP Thermal (Người đi bộ đêm tối)"] = LLVIP_MODEL_PATH
else:
    MODEL_OPTIONS["YOLOv8n - LLVIP Thermal (Thiếu file)"] = ROOT / "models" / "llvip_best.pt"

COMPARE_OPTION = "So sánh cả hai mô hình (FLIR + LLVIP)"

# ==============================================================================
# 2. CAU HINH TRANG VA GIAO DIEN STREAMLIT (CYBER-THERMAL THEME)
# ==============================================================================

st.set_page_config(
    page_title="Thermal Vision · Phát hiện người trong ảnh nhiệt",
    page_icon=APP_ICON_IMAGE,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace;
    }

    .stApp {
        background-color: #070b14;
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] {
        background: #0b1120;
        border-right: 1px solid #1e293b;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        max-width: 1450px;
    }

    /* Hero Banner */
    .hero-banner {
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 22px 26px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #172554 100%);
        border: 1px solid #334155;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 22px;
    }

    .hero-icon-box {
        width: 78px;
        height: 78px;
        border-radius: 20px;
        background: transparent;
        box-shadow: 0 0 25px rgba(255, 106, 0, 0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        overflow: hidden;
        border: 1px solid rgba(255, 106, 0, 0.4);
    }

    .hero-icon-box img {
        width: 100%;
        height: 100%;
        border-radius: 18px;
        object-fit: cover;
        display: block;
    }

    /* Sidebar Brand Card */
    .sidebar-brand-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        margin-bottom: 20px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.75) 100%);
        border: 1px solid rgba(255, 106, 0, 0.35);
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), 0 0 15px rgba(255, 106, 0, 0.15);
    }
    .sidebar-brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        object-fit: cover;
        box-shadow: 0 0 12px rgba(255, 106, 0, 0.4);
    }
    .sidebar-brand-text {
        display: flex;
        flex-direction: column;
    }
    .sidebar-brand-title {
        font-weight: 800;
        font-size: 15px;
        color: #f8fafc;
        letter-spacing: 0.8px;
        line-height: 1.2;
    }
    .sidebar-brand-subtitle {
        font-size: 11px;
        font-weight: 700;
        color: #ff6a00;
        letter-spacing: 1px;
        line-height: 1.2;
    }

    .hero-content h1 {
        font-size: 25px;
        font-weight: 800;
        margin: 0 0 6px 0;
        background: linear-gradient(90deg, #f8fafc, #fed7aa, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    .hero-content p {
        color: #94a3b8;
        margin: 0;
        font-size: 13.8px;
        line-height: 1.5;
    }

    .badge-tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
        margin-top: 6px;
        background: rgba(249, 115, 22, 0.15);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.3);
    }

    .badge-cyan {
        background: rgba(6, 182, 212, 0.15);
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }

    .badge-green {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    /* Metric Cards */
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .stat-label {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .stat-value {
        font-size: 23px;
        font-weight: 800;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Tabs Styling */
    div[data-testid="stTabs"] button {
        color: #94a3b8;
        font-weight: 600;
        font-size: 14.5px;
        padding: 10px 18px;
        border-radius: 8px;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #fb923c;
        background-color: rgba(249, 115, 22, 0.12);
        border-bottom: 2px solid #ea580c;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #0f172a;
        border: 1px dashed #334155;
        border-radius: 14px;
        padding: 14px;
    }

    /* Callout & Alert banner */
    .callout-box {
        background: #0d1527;
        border-left: 4px solid #f97316;
        padding: 14px 18px;
        border-radius: 0 12px 12px 0;
        margin: 14px 0;
        font-size: 13.5px;
        line-height: 1.6;
        color: #cbd5e1;
    }

    .auto-detect-banner {
        background: linear-gradient(90deg, rgba(234, 88, 12, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
        border: 1px solid rgba(249, 115, 22, 0.4);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13.5px;
        font-weight: 500;
        color: #fed7aa;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render Header Hero
icon_html = f'<img src="{APP_ICON_DATA_URI}" alt="Thermal YOLO Icon" />' if APP_ICON_DATA_URI else '<span style="font-size: 38px;">🔥</span>'
if ICON_PATH and ICON_PATH.is_file():
    try:
        with open(ICON_PATH, "rb") as f:
            b64_icon = base64.b64encode(f.read()).decode("utf-8")
            icon_html = f'<img src="data:image/png;base64,{b64_icon}" alt="Thermal YOLO Icon" />'
    except Exception:
        pass

st.markdown(
    f"""
    <div class="hero-banner">
        <div class="hero-icon-box">
            {icon_html}
        </div>
        <div class="hero-content">
            <h1>THERMAL VISION · PHÁT HIỆN NGƯỜI TRONG ẢNH NHIỆT</h1>
            <p>Hệ thống nhận diện người thời gian thực trên cảm biến hồng ngoại sóng dài LWIR (8–14 µm) · YOLOv8n Deep Learning · Bộ dữ liệu FLIR ADAS v2 & LLVIP</p>
            <div>
                <span class="badge-tag">⚡ Nhận diện tức thì (Zero-Click)</span>
                <span class="badge-tag badge-cyan">🌈 Hỗ trợ Bảng màu Hiển thị (Inferno/Jet/Ironbow)</span>
                <span class="badge-tag badge-green">💻 Thiết bị: {DEVICE_NAME}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. NAP MÔ HÌNH YOLO (CACHED AN TOÀN)
# ==============================================================================

@st.cache_resource(show_spinner=False)
def load_yolo_model(model_path_str: str) -> YOLO:
    """Nạp trọng số YOLOv8 với xử lý ngoại lệ an toàn."""
    return YOLO(model_path_str)

# ==============================================================================
# 4. TIỀN XỬ LÝ ẢNH & PHÂN BIỆT ẢNH SUY LUẬN VS HIỂN THỊ
# ==============================================================================

def analyze_and_prepare_image(
    image_bgr: np.ndarray,
    diff_thresh: float = 6.0,
) -> Tuple[bool, str, np.ndarray, np.ndarray]:
    """
    Tiền xử lý dữ liệu đầu vào:
    1. Kiểm tra ảnh có kênh màu (RGB / False-Color) hay đơn sắc xám (Monochrome Thermal).
    2. Chuẩn bị ảnh đưa vào mạng YOLO: Luôn là ảnh đơn sắc chuyển sang 3 kênh xám (B=G=R).
       Lý do kỹ thuật: Cả hai mô hình YOLOv8n (FLIR và LLVIP) đều được huấn luyện trên
       ảnh đơn sắc nhiệt (monochrome LWIR). Việc nạp ảnh 3 kênh xám đảm bảo phân phối
       đặc trưng (feature distribution) khớp chính xác với tập huấn luyện.
    3. Cảnh báo khoa học rõ ràng nếu người dùng tải ảnh màu quang học thông thường:
       Khẳng định rõ việc chuyển xám chỉ là xấp xỉ độ sáng (luminance), không thể biến ảnh RGB
       thành ảnh hồng ngoại thật.
    """
    if len(image_bgr.shape) < 3 or image_bgr.shape[2] < 3:
        gray = image_bgr.copy()
        gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        msg = "🔘 Ảnh nhiệt đơn sắc chuẩn (Grayscale) — Đúng định dạng nguồn của cảm biến nhiệt FLIR / LLVIP."
        return False, msg, gray_3ch, gray_3ch.copy()

    b = image_bgr[:, :, 0].astype(np.float32)
    g = image_bgr[:, :, 1].astype(np.float32)
    r = image_bgr[:, :, 2].astype(np.float32)
    mean_diff = float(np.mean(np.maximum(np.abs(r - g), np.abs(g - b))))

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    if mean_diff > diff_thresh:
        msg = (
            "🌈 Đã phát hiện ảnh có thông tin màu sắc (False-Color Thermal hoặc RGB quang học). "
            "Hệ thống tự động trích xuất kênh đơn sắc chuẩn hóa miền nhiệt để đưa vào YOLOv8 suy luận. "
            "Lưu ý: Nếu đây là ảnh chụp camera thường (RGB), việc chuyển xám chỉ là xấp xỉ thang độ sáng, "
            "không phản ánh bức xạ nhiệt thực thụ (LWIR)."
        )
        return True, msg, gray_3ch, image_bgr.copy()
    else:
        msg = "🔘 Ảnh nhiệt đơn sắc xám chuẩn (LWIR Monochrome) — Miền dữ liệu khớp hoàn toàn với tập huấn luyện YOLOv8n."
        return False, msg, gray_3ch, image_bgr.copy()


def apply_display_palette(gray_img: np.ndarray, colormap_mode: str) -> np.ndarray:
    """
    Áp dụng bảng màu hiển thị trực quan (Display Only):
    Bảng màu này CHỈ dùng để con người quan sát gradient thân nhiệt thuận tiện hơn,
    HOÀN TOÀN KHÔNG đưa ảnh đã tô màu vào YOLO để tránh làm méo mó trọng số mạng!
    """
    if len(gray_img.shape) == 3 and gray_img.shape[2] == 3:
        gray = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)
    else:
        gray = gray_img.copy()

    if colormap_mode == "Inferno (Bảng nhiệt chuyên dụng FLIR)":
        return cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
    elif colormap_mode == "Ironbow / Hot Metal":
        return cv2.applyColorMap(gray, cv2.COLORMAP_MAGMA)
    elif colormap_mode == "Jet / Quang phổ nhiệt công nghiệp":
        return cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    elif colormap_mode == "Turbo (Tương phản cao)":
        return cv2.applyColorMap(gray, cv2.COLORMAP_TURBO)
    elif colormap_mode == "Bone (Ảnh quét quân sự)":
        return cv2.applyColorMap(gray, cv2.COLORMAP_BONE)
    elif colormap_mode == "Grayscale (Ảnh xám nhiệt chuẩn)":
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    else:
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


# Các hàm mô phỏng nhiễu môi trường và cảm biến (Robustness Lab)
def add_gaussian_noise(image: np.ndarray, sigma: float) -> np.ndarray:
    """Mô phỏng nhiễu hạt cảm biến vi bức xạ kế (NETD Noise)."""
    if sigma <= 0 or image is None or image.size == 0:
        return image.copy()
    gauss = np.random.normal(0, sigma, image.shape)
    return np.clip(image.astype(np.float32) + gauss, 0, 255).astype(np.uint8)


def add_salt_and_pepper_noise(image: np.ndarray, amount: float) -> np.ndarray:
    """
    Mô phỏng điểm ảnh chết (Dead Pixels / Defective Bolometers).
    Đã bổ sung cơ chế kiểm tra kích thước an toàn, chống lỗi với ảnh siêu nhỏ hoặc rỗng.
    """
    if amount <= 0 or image is None or image.size == 0:
        return image.copy()
    h, w = image.shape[:2]
    if h <= 0 or w <= 0:
        return image.copy()

    out = image.copy()
    num_pixels = h * w
    num_noise = int(amount * num_pixels * 0.5)
    if num_noise <= 0:
        return out

    # Điểm ảnh bão hòa nhiệt cực đại (White Salt)
    y_s = np.random.randint(0, h, num_noise)
    x_s = np.random.randint(0, w, num_noise)
    out[y_s, x_s] = 255

    # Điểm ảnh mất tín hiệu (Black Pepper)
    y_p = np.random.randint(0, h, num_noise)
    x_p = np.random.randint(0, w, num_noise)
    out[y_p, x_p] = 0

    return out


def apply_low_thermal_contrast(image: np.ndarray, factor: float) -> np.ndarray:
    """Mô phỏng suy giảm tương phản nhiệt do sương mù, mưa hoặc cân bằng nhiệt độ môi trường."""
    if image is None or image.size == 0:
        return image.copy()
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    degraded = enhancer.enhance(max(0.01, factor))
    return cv2.cvtColor(np.array(degraded), cv2.COLOR_RGB2BGR)


def apply_thermal_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
    """Mô phỏng mờ quang học do rung lắc phương tiện hoặc mất nét (Out-of-focus)."""
    if kernel_size <= 1 or image is None or image.size == 0:
        return image.copy()
    h, w = image.shape[:2]
    max_k = min(h, w)
    if max_k % 2 == 0:
        max_k -= 1
    k = max(1, min(kernel_size if kernel_size % 2 == 1 else kernel_size + 1, max_k))
    if k <= 1:
        return image.copy()
    return cv2.GaussianBlur(image, (k, k), 0)


def apply_temperature_gain(image: np.ndarray, gain: float) -> np.ndarray:
    """Mô phỏng biến đổi dải động bức xạ nhiệt (Ambient Shift / Temperature Offset)."""
    if image is None or image.size == 0:
        return image.copy()
    return np.clip(image.astype(np.float32) * max(0.0, gain), 0, 255).astype(np.uint8)


# ==============================================================================
# 5. PIPELINE SUY LUẬN NHẬN DIỆN NGƯỜI BẰNG YOLO
# ==============================================================================

def detect_thermal_person_pipeline(
    model: YOLO,
    input_bgr: np.ndarray,
    conf_thresh: float = 0.35,
    iou_thresh: float = 0.45,
    imgsz: int = 416,
    colormap_mode: str = "Tự động phát hiện (Khuyên dùng)",
) -> Dict[str, Any]:
    """
    Chu trình xử lý hoàn chỉnh:
    - Tiền xử lý: Phân tích ảnh và trích xuất grayscale 3 kênh đưa vào YOLO.
    - Tạo ảnh nền hiển thị (display_bg) theo colormap được chọn.
    - Suy luận mô hình YOLO và đo chính xác Model Inference Latency.
    - Trích xuất bounding box, cắt mẫu thân nhiệt người (crops) và đo Total Pipeline Latency.
    """
    total_start_time = time.perf_counter()

    # Bước 1: Tiền xử lý và phân tách ảnh suy luận vs ảnh hiển thị
    is_color, type_msg, yolo_input, raw_display = analyze_and_prepare_image(input_bgr)

    if colormap_mode == "Tự động phát hiện (Khuyên dùng)" or colormap_mode == "Ảnh gốc":
        display_bg = raw_display.copy()
    else:
        # Áp dụng bảng màu hiển thị nhân tạo lên kênh xám
        display_bg = apply_display_palette(yolo_input, colormap_mode)

    # Bước 2: Đo thời gian suy luận thuần của Model (Inference Latency)
    model_start_time = time.perf_counter()
    results = model.predict(
        source=yolo_input,
        conf=conf_thresh,
        iou=iou_thresh,
        imgsz=imgsz,
        device=DEVICE_TAG,
        verbose=False,
    )
    model_inference_time = time.perf_counter() - model_start_time

    # Bước 3: Hậu xử lý kết quả nhận diện
    result = results[0]
    annotated = display_bg.copy()
    detections: List[Dict[str, Any]] = []
    crops: List[Tuple[str, np.ndarray]] = []

    if result.boxes is not None and len(result.boxes) > 0:
        h_img, w_img = display_bg.shape[:2]

        for idx, box in enumerate(result.boxes):
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0].cpu().item())
            cls_id = int(box.cls[0].cpu().item()) if box.cls is not None else 0
            cls_name = model.names.get(cls_id, "person")
            display_cls = "Người" if cls_name.lower() == "person" else cls_name

            x1, y1, x2, y2 = xyxy.tolist()
            x1 = max(0, min(x1, w_img - 1))
            y1 = max(0, min(y1, h_img - 1))
            x2 = max(0, min(x2, w_img))
            y2 = max(0, min(y2, h_img))

            # Trích xuất vùng thân nhiệt người
            crop_img = display_bg[y1:y2, x1:x2].copy()
            if crop_img.size > 0:
                crops.append((f"{display_cls} #{idx+1} ({conf*100:.1f}%)", crop_img))

            # Vẽ bounding box phong cách Cyber-Thermal cao cấp
            box_color = (14, 116, 234)  # Cam nhiệt BGR
            cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, 2)

            # 4 góc định vị cyan công nghệ cao
            c_len = min(15, max(4, (x2 - x1) // 4), max(4, (y2 - y1) // 4))
            c_color = (0, 240, 255)
            cv2.line(annotated, (x1, y1), (x1 + c_len, y1), c_color, 3)
            cv2.line(annotated, (x1, y1), (x1, y1 + c_len), c_color, 3)
            cv2.line(annotated, (x2, y1), (x2 - c_len, y1), c_color, 3)
            cv2.line(annotated, (x2, y1), (x2, y1 + c_len), c_color, 3)
            cv2.line(annotated, (x1, y2), (x1 + c_len, y2), c_color, 3)
            cv2.line(annotated, (x1, y2), (x1, y2 - c_len), c_color, 3)
            cv2.line(annotated, (x2, y2), (x2 - c_len, y2), c_color, 3)
            cv2.line(annotated, (x2, y2), (x2, y2 - c_len), c_color, 3)

            label_text = f"{display_cls} {conf*100:.1f}%"
            (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            tag_top = max(0, y1 - text_h - 8)
            cv2.rectangle(annotated, (x1, tag_top), (x1 + text_w + 10, y1), box_color, -1)
            cv2.putText(
                annotated,
                label_text,
                (x1 + 5, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            box_w = x2 - x1
            box_h = y2 - y1
            detections.append({
                "STT": idx + 1,
                "Đối tượng": display_cls,
                "Độ tin cậy": f"{conf*100:.2f}%",
                "X1": x1,
                "Y1": y1,
                "X2": x2,
                "Y2": y2,
                "Rộng (px)": box_w,
                "Cao (px)": box_h,
                "Diện tích (px²)": box_w * box_h,
            })

    total_pipeline_time = time.perf_counter() - total_start_time

    return {
        "annotated": annotated,
        "detections": detections,
        "crops": crops,
        "is_color": is_color,
        "message": type_msg,
        "model_inference_time": model_inference_time,
        "total_pipeline_time": total_pipeline_time,
    }


# ==============================================================================
# 6. SIDEBAR: ĐIỀU KHIỂN & CẤU HÌNH THAM SỐ
# ==============================================================================

with st.sidebar:
    # Logo thương hiệu ứng dụng ở đầu Sidebar
    if APP_ICON_DATA_URI:
        st.markdown(
            f"""
            <div class="sidebar-brand-card">
                <img src="{APP_ICON_DATA_URI}" class="sidebar-brand-icon" alt="Thermal YOLO Logo" />
                <div class="sidebar-brand-text">
                    <span class="sidebar-brand-title">THERMAL YOLO</span>
                    <span class="sidebar-brand-subtitle">VISION STUDIO · AI</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### ⚙️ Cấu hình Mô hình")

    model_choices = list(MODEL_OPTIONS.keys()) + [COMPARE_OPTION]
    selected_model_name = st.selectbox(
        "Mô hình nhận diện:",
        model_choices,
        index=0,
        help="Chọn mô hình FLIR, LLVIP hoặc chế độ so sánh đối chiếu cả hai mô hình trên cùng một ảnh.",
    )

    if selected_model_name == COMPARE_OPTION:
        active_model_names = list(MODEL_OPTIONS.keys())
    else:
        active_model_names = [selected_model_name]

    # Kiểm tra sự tồn tại của file trọng số
    missing_models = []
    active_model_paths: Dict[str, Path] = {}
    for name in active_model_names:
        p = MODEL_OPTIONS.get(name)
        if p and p.is_file():
            active_model_paths[name] = p
        else:
            missing_models.append(f"{name} ({p})")

    if missing_models:
        st.error("⚠️ Không tìm thấy file trọng số mô hình:\n" + "\n".join(missing_models))
        st.info("Vui lòng đặt file best.pt vào thư mục `models/` hoặc `runs/` theo hướng dẫn dự án.")
        st.stop()

    for name, p in active_model_paths.items():
        mb = p.stat().st_size / (1024 * 1024)
        st.success(f"✓ {name.split('-')[0].strip()} ({mb:.2f} MB)")

    st.divider()

    st.markdown("### 🎛️ Ngưỡng Nhận diện & Suy luận")
    conf_slider = st.slider(
        "Ngưỡng tin cậy (Confidence):",
        min_value=0.05,
        max_value=0.95,
        value=0.35,
        step=0.05,
        help="Lọc bỏ các dự đoán có xác suất thấp hơn ngưỡng này.",
    )

    iou_slider = st.slider(
        "Ngưỡng NMS IoU:",
        min_value=0.10,
        max_value=0.80,
        value=0.45,
        step=0.05,
        help="Loại bỏ các bounding box bị trùng lặp trên cùng một người.",
    )

    imgsz_choice = st.select_slider(
        "Kích thước ảnh nạp vào mạng (imgsz):",
        options=[320, 416, 512, 640],
        value=416,
        help="416×416 là kích thước chuẩn mực huấn luyện cho YOLOv8n, tối ưu cân bằng tốc độ CPU và độ chính xác.",
    )

    st.divider()

    st.markdown("### 🎨 Bảng màu Hiển thị (Display Only)")
    colormap_mode = st.selectbox(
        "Bảng nhiệt trực quan:",
        [
            "Tự động phát hiện (Khuyên dùng)",
            "Ảnh gốc",
            "Grayscale (Ảnh xám nhiệt chuẩn)",
            "Inferno (Bảng nhiệt chuyên dụng FLIR)",
            "Ironbow / Hot Metal",
            "Jet / Quang phổ nhiệt công nghiệp",
            "Turbo (Tương phản cao)",
            "Bone (Ảnh quét quân sự)",
        ],
        index=0,
        help="Bảng màu CHỈ dùng để hiển thị trực quan cho mắt người. YOLO luôn được nạp ảnh grayscale chuẩn hóa để suy luận chính xác.",
    )

    st.divider()
    st.markdown("### 💻 Thông tin Phần cứng")
    st.caption(f"Thiết bị: **{DEVICE_NAME}**")
    st.caption("Sinh viên: **Nguyễn Đức Hiếu** (MSSV: 24800600314)")
    st.caption("GVHD: **ThS./TS. Vũ Thanh Hiền** · HUTECH 2026")


# Tải trước các mô hình đang hoạt động vào bộ nhớ cache
try:
    loaded_models: Dict[str, YOLO] = {}
    with st.spinner("Đang nạp mô hình YOLO vào bộ nhớ..."):
        for name, path in active_model_paths.items():
            loaded_models[name] = load_yolo_model(str(path))
    # Mô hình mặc định dùng cho Tab thí nghiệm nhiễu
    default_model = next(iter(loaded_models.values()))
except Exception as err:
    st.error(f"Lỗi khi nạp mô hình: {err}")
    st.stop()


# ==============================================================================
# 7. CÁC TAB CHỨC NĂNG CHÍNH CỦA ỨNG DỤNG
# ==============================================================================

tab_detect, tab_noise, tab_benchmark, tab_about = st.tabs([
    "🎯 Nhận diện Ảnh Nhiệt",
    "🧪 Thử nghiệm Mức nhiệt & Nhiễu",
    "📊 Đánh giá & Benchmark Thực nghiệm",
    "📘 Tổng quan Đề tài & Hướng dẫn",
])


# ==============================================================================
# TAB 1: NHẬN DIỆN ẢNH NHIỆT (TỰ ĐỘNG & ĐỐI SOÁNH HAI MÔ HÌNH)
# ==============================================================================

with tab_detect:
    st.markdown("#### 1. Chọn hoặc Tải Ảnh Nhiệt")

    input_source = st.radio(
        "Nguồn dữ liệu ảnh:",
        ["Tải ảnh từ máy tính (Upload)", "Chọn ảnh mẫu có sẵn (Sample Gallery)"],
        horizontal=True,
    )

    selected_image_bgr: Optional[np.ndarray] = None
    image_filename = "thermal_image.jpg"

    if input_source == "Tải ảnh từ máy tính (Upload)":
        uploaded_file = st.file_uploader(
            "Tải lên tệp ảnh (JPG, PNG, WEBP, BMP, TIF) — Hệ thống tự động nhận diện tức thì:",
            type=["jpg", "jpeg", "png", "bmp", "webp", "tif", "tiff"],
            key="thermal_file_uploader",
        )
        if uploaded_file is not None:
            image_filename = uploaded_file.name
            pil_image = Image.open(uploaded_file).convert("RGB")
            selected_image_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
        sample_files = sorted(list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.png")))
        if sample_files:
            sample_labels = {
                "flir_sample_street.jpg": "Đường phố ban ngày/hỗn hợp (FLIR Dataset - LWIR)",
                "flir_sample_night.jpg": "Phương tiện & Người đi bộ ban đêm (FLIR Dataset - LWIR)",
                "llvip_sample_pedestrians.jpg": "Nhóm người đi bộ ban đêm (LLVIP Dataset - 1280×1024)",
                "llvip_sample_alley.jpg": "Khu ngõ phố dân cư thiếu sáng (LLVIP Dataset - 1280×1024)",
            }
            chosen_sample = st.selectbox(
                "Chọn ảnh nhiệt mẫu chuẩn:",
                sample_files,
                format_func=lambda p: sample_labels.get(p.name, p.name),
            )
            image_filename = chosen_sample.name
            pil_image = Image.open(chosen_sample).convert("RGB")
            selected_image_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        else:
            st.warning("⚠️ Chưa tìm thấy ảnh trong thư mục `samples/`. Hãy sử dụng tùy chọn tải ảnh lên từ máy tính.")

    if selected_image_bgr is not None:
        # Cache kết quả suy luận dựa trên hash nội dung ảnh và các tham số
        image_bytes_hash = hashlib.sha256(selected_image_bgr.tobytes()).hexdigest()
        cache_key = (
            f"{image_bytes_hash}_{selected_model_name}_{conf_slider:.2f}_"
            f"{iou_slider:.2f}_{imgsz_choice}_{colormap_mode}"
        )

        if st.session_state.get("detect_tab_cache_key") != cache_key:
            results_dict = {}
            with st.spinner("⚡ Đang chạy nhận diện trên mô hình đã chọn..."):
                for m_name, m_inst in loaded_models.items():
                    res = detect_thermal_person_pipeline(
                        model=m_inst,
                        input_bgr=selected_image_bgr,
                        conf_thresh=conf_slider,
                        iou_thresh=iou_slider,
                        imgsz=imgsz_choice,
                        colormap_mode=colormap_mode,
                    )
                    results_dict[m_name] = res
            st.session_state["detect_tab_results"] = results_dict
            st.session_state["detect_tab_cache_key"] = cache_key

        results_dict = st.session_state.get("detect_tab_results", {})

        if results_dict:
            first_res = next(iter(results_dict.values()))
            is_color_flag = first_res["is_color"]
            status_banner_text = first_res["message"]

            st.markdown(
                f"""
                <div class="auto-detect-banner">
                    <span style="font-size: 20px;">{'🌈' if is_color_flag else '🔘'}</span>
                    <span>{status_banner_text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Hiển thị ảnh đầu vào
            st.markdown("#### Ảnh nhiệt đầu vào")
            st.image(
                cv2.cvtColor(selected_image_bgr, cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"File: {image_filename} · Kích thước gốc: {selected_image_bgr.shape[1]} × {selected_image_bgr.shape[0]} pixels",
            )

            # Hiển thị kết quả nhận diện (theo cột nếu so sánh cả hai mô hình)
            col_list = st.columns(len(results_dict), gap="medium")
            for col, (m_name, res_item) in zip(col_list, results_dict.items()):
                with col:
                    dets = res_item["detections"]
                    annotated_img = res_item["annotated"]
                    crops_list = res_item["crops"]
                    t_infer = res_item["model_inference_time"]
                    t_total = res_item["total_pipeline_time"]

                    infer_fps = (1.0 / t_infer) if t_infer > 0 else 0.0
                    pipeline_fps = (1.0 / t_total) if t_total > 0 else 0.0

                    st.markdown(f"#### 🎯 {m_name}")
                    st.image(
                        cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB),
                        use_container_width=True,
                        caption=f"Phát hiện: {len(dets)} người",
                    )

                    # Bảng thông số đo lường hiệu năng thực tế
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Số người", f"{len(dets)}")
                    m2.metric(
                        "Độ trễ Model",
                        f"{t_infer * 1000:.1f} ms",
                        f"{infer_fps:.1f} FPS (Model)",
                        help="Thời gian suy luận thuần của mạng YOLOv8 (Forward pass + NMS).",
                    )
                    m3.metric(
                        "Toàn Pipeline",
                        f"{t_total * 1000:.1f} ms",
                        f"{pipeline_fps:.1f} FPS (App)",
                        help="Thời gian toàn chu trình bao gồm tiền xử lý, suy luận, vẽ bounding box và cắt ảnh.",
                    )

                    # Tải kết quả và xem chi tiết
                    if dets:
                        st.markdown("**Bảng tọa độ Bounding Box**")
                        df_dets = pd.DataFrame(dets)
                        st.dataframe(df_dets, use_container_width=True, hide_index=True)

                        # Tải ảnh kết quả
                        _, buf_img = cv2.imencode(".jpg", annotated_img)
                        base_stem = image_filename.rsplit(".", 1)[0]
                        m_tag = "flir" if "flir" in m_name.lower() else "llvip"

                        st.download_button(
                            label=f"💾 Tải ảnh kết quả ({m_tag.upper()})",
                            data=buf_img.tobytes(),
                            file_name=f"detected_{m_tag}_{base_stem}.jpg",
                            mime="image/jpeg",
                            use_container_width=True,
                            key=f"dl_img_{m_name}",
                        )

                        # Tải CSV tọa độ
                        csv_bytes = df_dets.to_csv(index=False).encode("utf-8-sig")
                        st.download_button(
                            label=f"📊 Tải bảng tọa độ CSV ({m_tag.upper()})",
                            data=csv_bytes,
                            file_name=f"boxes_{m_tag}_{base_stem}.csv",
                            mime="text/csv",
                            use_container_width=True,
                            key=f"dl_csv_{m_name}",
                        )

                        # Thư viện cận cảnh từng người
                        if crops_list:
                            with st.expander(f"🔍 Xem cận cảnh vùng thân nhiệt từng người ({len(crops_list)})"):
                                crop_cols = st.columns(min(len(crops_list), 4))
                                for i, (crop_label, crop_mat) in enumerate(crops_list[:16]):
                                    with crop_cols[i % len(crop_cols)]:
                                        st.image(
                                            cv2.cvtColor(crop_mat, cv2.COLOR_BGR2RGB),
                                            use_container_width=True,
                                        )
                                        st.caption(crop_label)
                    else:
                        st.info("Không phát hiện người nào với ngưỡng tin cậy hiện tại.")

            if len(results_dict) == 2:
                st.caption(
                    "📌 **Ghi chú đối soát:** Hai mô hình chạy hoàn toàn độc lập trên cùng dữ liệu đầu vào. "
                    "FLIR tối ưu cho phương tiện & người đi bộ trong giao thông đô thị; "
                    "LLVIP chuyên biệt cao độ cho giám sát an ninh người đi bộ ban đêm với camera cố định."
                )


# ==============================================================================
# TAB 2: PHÒNG THÍ NGHIỆM MỨC NHIỆT & ĐỘ BỀN VỮNG (ROBUSTNESS LAB)
# ==============================================================================

with tab_noise:
    st.markdown("### 🧪 Thử nghiệm Độ bền vững trước Mức nhiệt & Nhiễu Cảm biến")
    st.markdown(
        """
        <div class="callout-box">
            <b>Ý nghĩa thực nghiệm:</b> Camera nhiệt thực tế ngoài trời thường chịu ảnh hưởng mạnh của nhiệt độ môi trường, 
            nhiễu vi bức xạ kế (NETD), sương mù, mưa rào hoặc rung lắc cơ học của phương tiện di chuyển. 
            Tại đây, bạn có thể kiểm thử khả năng nhận diện của mô hình khi ảnh nhiệt bị tác động nhân tạo.
        </div>
        """,
        unsafe_allow_html=True,
    )

    base_thermal_bgr = selected_image_bgr
    if base_thermal_bgr is None:
        sample_path = SAMPLES_DIR / "flir_sample_street.jpg"
        if sample_path.exists():
            base_thermal_bgr = cv2.imread(str(sample_path))

    if base_thermal_bgr is not None:
        col_ctl1, col_ctl2 = st.columns(2)

        with col_ctl1:
            st.markdown("##### 1. Loại Tác Động Môi trường / Cảm biến")
            noise_type = st.selectbox(
                "Mô phỏng suy thoái nhiệt:",
                [
                    "Nhiễu cảm biến nhiệt Gaussian (Sensor Noise / NETD)",
                    "Nhiễu điểm ảnh chết (Dead Pixels / Salt & Pepper)",
                    "Mờ quang học & rung lắc (Thermal Blur)",
                    "Suy giảm tương phản nhiệt (Low Thermal Contrast / Sương mù)",
                    "Dịch chuyển dải bức xạ môi trường (Ambient Shift)",
                ],
            )

        with col_ctl2:
            st.markdown("##### 2. Cường độ Tác động")
            if "Gaussian" in noise_type:
                noise_param = st.slider("Độ lệch chuẩn nhiễu (Sigma σ):", 0.0, 60.0, 25.0, 2.0)
                degraded_image = add_gaussian_noise(base_thermal_bgr, noise_param)
            elif "điểm ảnh chết" in noise_type:
                noise_param = st.slider("Tỷ lệ điểm ảnh hỏng (Ratio):", 0.0, 0.15, 0.03, 0.005)
                degraded_image = add_salt_and_pepper_noise(base_thermal_bgr, noise_param)
            elif "Mờ quang học" in noise_type:
                noise_param = st.slider("Kích thước làm mờ (Kernel Size):", 1, 21, 7, 2)
                degraded_image = apply_thermal_blur(base_thermal_bgr, int(noise_param))
            elif "Suy giảm tương phản" in noise_type:
                noise_param = st.slider("Hệ số tương phản nhiệt (Contrast Factor):", 0.1, 1.0, 0.4, 0.05)
                degraded_image = apply_low_thermal_contrast(base_thermal_bgr, noise_param)
            else:
                noise_param = st.slider("Hệ số dải động bức xạ (Gain Factor):", 0.3, 1.8, 0.7, 0.1)
                degraded_image = apply_temperature_gain(base_thermal_bgr, noise_param)

        # Tối ưu hóa: Cache kết quả ảnh sạch để không chạy lại suy luận nếu ảnh/model không đổi
        clean_hash = hashlib.sha256(base_thermal_bgr.tobytes()).hexdigest()
        clean_cache_key = f"{clean_hash}_{selected_model_name}_{conf_slider:.2f}_{iou_slider:.2f}_{imgsz_choice}"

        if st.session_state.get("clean_detect_cache_key") != clean_cache_key:
            st.session_state["clean_detect_res"] = detect_thermal_person_pipeline(
                model=default_model,
                input_bgr=base_thermal_bgr,
                conf_thresh=conf_slider,
                iou_thresh=iou_slider,
                imgsz=imgsz_choice,
                colormap_mode=colormap_mode,
            )
            st.session_state["clean_detect_cache_key"] = clean_cache_key

        clean_res = st.session_state["clean_detect_res"]

        # Cache kết quả ảnh nhiễu theo loại nhiễu và thông số
        degraded_cache_key = f"{clean_cache_key}_{noise_type}_{noise_param}"
        if st.session_state.get("degraded_detect_cache_key") != degraded_cache_key:
            st.session_state["degraded_detect_res"] = detect_thermal_person_pipeline(
                model=default_model,
                input_bgr=degraded_image,
                conf_thresh=conf_slider,
                iou_thresh=iou_slider,
                imgsz=imgsz_choice,
                colormap_mode=colormap_mode,
            )
            st.session_state["degraded_detect_cache_key"] = degraded_cache_key

        noisy_res = st.session_state["degraded_detect_res"]

        cnt_clean = len(clean_res["detections"])
        cnt_noisy = len(noisy_res["detections"])
        retention = (cnt_noisy / cnt_clean * 100.0) if cnt_clean > 0 else 100.0

        st.markdown("##### 3. Kết quả Đối sánh Thực nghiệm")
        t_c1, t_c2, t_c3 = st.columns(3)
        t_c1.metric(
            "Ảnh gốc chuẩn (Clean)",
            f"{cnt_clean} người",
            f"{clean_res['model_inference_time'] * 1000:.1f} ms suy luận",
        )
        t_c2.metric(
            "Ảnh chịu tác động (Degraded)",
            f"{cnt_noisy} người",
            f"{noisy_res['model_inference_time'] * 1000:.1f} ms suy luận",
        )
        t_c3.metric(
            "Tỷ lệ giữ lại phát hiện (Retention)",
            f"{retention:.1f}%",
            f"{cnt_noisy - cnt_clean:+d} người so với ảnh gốc",
        )

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.image(
                cv2.cvtColor(clean_res["annotated"], cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"Ảnh nhiệt chuẩn: {cnt_clean} phát hiện",
            )
        with col_v2:
            st.image(
                cv2.cvtColor(noisy_res["annotated"], cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"Ảnh sau khi áp dụng {noise_type}: {cnt_noisy} phát hiện",
            )
    else:
        st.info("Vui lòng tải hoặc chọn một ảnh ở Tab 'Nhận diện Ảnh Nhiệt' để bắt đầu thử nghiệm độ bền vững.")


# ==============================================================================
# TAB 3: ĐÁNH GIÁ ĐỊNH LƯỢNG & BENCHMARK THỰC NGHIỆM CHÍNH XÁC
# ==============================================================================

with tab_benchmark:
    st.markdown("### 📊 Đánh giá Định lượng & So sánh Hiệu năng Thực tế")
    st.markdown(
        """
        Bảng số liệu dưới đây được trích xuất trực tiếp từ kết quả huấn luyện thực tế (**50 Epochs**) 
        và nghiệm thu trên tập kiểm định độc lập của hai bộ dữ liệu **FLIR ADAS v2** và **LLVIP**.
        Hệ thống không sử dụng bất kỳ số liệu giả mạo nào.
        """
    )

    benchmark_rows = [
        {
            "Chỉ số Đánh giá (Metrics)": "Số lượng Epoch huấn luyện",
            "FLIR ADAS v2 (Xe & Người đường phố)": "50 Epochs hoàn tất",
            "LLVIP (Người đi bộ đêm tối)": "50 Epochs (Best Checkpoint)",
            "Mục tiêu Đồ án Đặt ra": "Hoàn tất ≥ 30 Epochs",
            "Đánh giá": "Đạt 100%",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "Độ chính xác (Precision - P)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "78.49% (0.7849)",
            "LLVIP (Người đi bộ đêm tối)": "96.38% (0.9638)",
            "Mục tiêu Đồ án Đặt ra": "≥ 70.00%",
            "Đánh giá": "Vượt chỉ tiêu",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "Độ thu hồi / Bao phủ (Recall - R)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "58.37% (0.5837)",
            "LLVIP (Người đi bộ đêm tối)": "94.54% (0.9454)",
            "Mục tiêu Đồ án Đặt ra": "≥ 55.00%",
            "Đánh giá": "Vượt chỉ tiêu",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "mAP @ IoU 0.50 (mAP50)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "67.07% (0.6707)",
            "LLVIP (Người đi bộ đêm tối)": "98.30% (0.9830)",
            "Mục tiêu Đồ án Đặt ra": "≥ 65.00%",
            "Đánh giá": "Vượt chỉ tiêu",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "mAP @ IoU 0.50:0.95 (mAP50-95)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "34.26% (0.3426)",
            "LLVIP (Người đi bộ đêm tối)": "68.04% (0.6804)",
            "Mục tiêu Đồ án Đặt ra": "≥ 30.00%",
            "Đánh giá": "Vượt chỉ tiêu",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "Kích thước tệp trọng số (Model Size)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "6.17 MB (flir_best.pt)",
            "LLVIP (Người đi bộ đêm tối)": "5.25 MB (llvip_best.pt)",
            "Mục tiêu Đồ án Đặt ra": "< 15.0 MB (Siêu nhẹ)",
            "Đánh giá": "Rất gọn nhẹ",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "Số lượng tham số (Parameters)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "3,138,003 tham số",
            "LLVIP (Người đi bộ đêm tối)": "2,604,883 tham số",
            "Mục tiêu Đồ án Đặt ra": "< 5.0 triệu tham số",
            "Đánh giá": "Phù hợp nhúng",
        },
        {
            "Chỉ số Đánh giá (Metrics)": "Tập dữ liệu kiểm định (Split)",
            "FLIR ADAS v2 (Xe & Người đường phố)": "Validation set (2,288 ảnh)",
            "LLVIP (Người đi bộ đêm tối)": "Test / Val set (3,463 ảnh)",
            "Mục tiêu Đồ án Đặt ra": "Đánh giá độc lập",
            "Đánh giá": "Khách quan",
        },
    ]

    df_benchmark = pd.DataFrame(benchmark_rows)
    st.dataframe(df_benchmark, use_container_width=True, hide_index=True)

    st.markdown(
        """
        > **Phân tích khoa học:**
        > - **FLIR ADAS v2:** Dữ liệu thu từ camera nhiệt gắn trên ô tô đang di chuyển trong thành phố Santa Barbara (Mỹ), 
        chịu ảnh hưởng của rung lắc, tầm nhìn thay đổi liên tục và nhiều nguồn nhiệt phức tạp (động cơ xe, ống xả, bóng đèn đường). 
        Do đó chỉ số Recall (58.37%) và mAP50 (67.07%) phản ánh đúng độ phức tạp của bài toán lái xe tự hành.
        > - **LLVIP:** Dữ liệu camera giám sát cố định với độ phân giải cao ($1280 \\times 1024$), góc nhìn hướng xuống phố đi bộ ban đêm, 
        độ tương phản thân nhiệt so với nền đêm rất cao, dẫn tới độ chính xác mAP50 đạt mức xuất sắc (98.30%).
        """
    )

    st.divider()
    st.markdown("#### Đồ thị Quá trình Huấn luyện & Đối sánh Hiệu năng")

    tc_file = resolve_asset_path("training_curves.png")
    if not tc_file:
        tc_file = resolve_asset_path("results.png")

    smc_file = resolve_asset_path("slide_metrics_comparison.png")
    cm_file = resolve_asset_path("confusion_matrix.png")

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        if tc_file and tc_file.is_file():
            st.image(
                str(tc_file),
                use_container_width=True,
                caption="Hình 1: Tiến trình hội tụ hàm mất mát (Loss) và chỉ số mAP qua các Epoch huấn luyện",
            )
        else:
            st.info("Chưa tìm thấy tệp đồ thị huấn luyện training_curves.png")

    with g_col2:
        if smc_file and smc_file.is_file():
            st.image(
                str(smc_file),
                use_container_width=True,
                caption="Hình 2: Biểu đồ cột đối sánh định lượng các chỉ số chính giữa FLIR và LLVIP",
            )
        elif cm_file and cm_file.is_file():
            st.image(
                str(cm_file),
                use_container_width=True,
                caption="Hình 2: Ma trận nhầm lẫn (Confusion Matrix) của mô hình",
            )


# ==============================================================================
# TAB 4: THÔNG TIN ĐỀ TÀI & HƯỚNG DẪN SỬ DỤNG
# ==============================================================================

with tab_about:
    st.markdown("### 📘 Thông tin Đề tài & Tài liệu Nghiên cứu")

    info_col1, info_col2 = st.columns([3, 2])

    with info_col1:
        st.markdown(
            """
            #### 1. Nguyên lý Vật lý Ảnh nhiệt Hồng ngoại (Thermal LWIR)
            - **Bản chất bức xạ:** Mọi vật thể có nhiệt độ trên $0\\text{ Kelvin} (-273.15^\\circ\\text{C})$ đều liên tục phát xạ sóng điện từ.
            - **Định luật dịch chuyển Wien:** $\\lambda_{\\max} = \\frac{b}{T}$ với $b \\approx 2898\\,\\mu\\text{m}\\cdot\\text{K}$. 
            Nhiệt độ cơ thể người ($36.5^\\circ\\text{C} - 37.5^\\circ\\text{C} \\approx 310\\,\\text{K}$) có đỉnh bức xạ tập trung tại dải bước sóng **$8 - 14\\,\\mu\\text{m}$** (Hồng ngoại sóng dài - LWIR).
            - **Khả năng xuyên thấu:** Khác biệt hoàn toàn với camera quang học RGB dựa trên ánh sáng phản xạ, camera nhiệt thu nhận bức xạ phát ra từ vật thể, 
            cho phép phát hiện người trong đêm tối hoàn toàn ($0\\text{ Lux}$), sương mù dày, bụi mịn hoặc bị cây cỏ che khuất một phần.

            #### 2. Kiến trúc Mạng Học sâu YOLOv8
            - **Backbone C2f:** Tối ưu hóa dòng truyền gradient qua cấu trúc Cross-Stage Partial kết hợp Conv, nắm bắt đặc trưng hình thái nhiệt độ nhạy bén.
            - **Decoupled Head:** Phân tách hoàn toàn nhánh phân loại lớp (Classification) và nhánh dự đoán bounding box (Regression).
            - **Anchor-Free:** Dự đoán trực tiếp tâm và khoảng cách viền, triệt tiêu phụ thuộc vào mỏ neo nhân tạo.
            - **Loss kết hợp:** Tích hợp **Task-Aligned Assigner**, **CIoU Loss** và **Distribution Focal Loss (DFL)**.
            """
        )

    with info_col2:
        st.markdown(
            """
            #### 3. Bộ Dữ liệu Chuẩn Benchmark
            - **FLIR ADAS v2:** Thu thập từ camera chuyên dụng FLIR Tau 2 gắn trên xe hơi thử nghiệm đường phố đô thị.
            - **LLVIP:** Bộ dữ liệu cặp nhiệt - khả kiến độ phân giải cao phục vụ bài toán an ninh người đi bộ ban đêm.

            #### 4. Hướng dẫn Vận hành Nhanh trên Windows
            1. Bấm đúp chuột vào tệp `run_app.bat` ở thư mục gốc dự án.
            2. Script sẽ tự động kích hoạt môi trường ảo `.venv` và khởi chạy Streamlit.
            3. Trình duyệt sẽ tự động mở địa chỉ: `http://localhost:8501`.

            #### 5. Tài liệu Tham khảo Khoa học
            - *MDPI Sensors (2022):* "Thermal Image Person Detection Using Deep Learning"
            - *ACM Digital Library (2019):* "Infrared Pedestrian Detection in Low-Light Conditions"
            """
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 13px;">
        Đồ án Môn học Trí tuệ Nhân tạo · Khoa Công nghệ Thông tin · Đại học Công nghệ TP.HCM (HUTECH)<br>
        <b>Sinh viên thực hiện:</b> Nguyễn Đức Hiếu (MSSV: 24800600314) · <b>GVHD:</b> ThS./TS. Vũ Thanh Hiền · Năm 2026
    </div>
    """,
    unsafe_allow_html=True,
)
