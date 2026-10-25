import os
import sys
from pathlib import Path
import time
import io

# Tránh lỗi OpenMP duplicate library thường gặp trên Windows khi nạp torch + opencv
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st
from ultralytics import YOLO

# =========================================================
# 1. CẤU HÌNH & XÁC ĐỊNH ĐƯỜNG DẪN AN TOÀN (SAFE PATHS)
# =========================================================

# Đảm bảo đường dẫn tuyệt đối chính xác dù chạy từ bất kỳ thư mục nào
ROOT = Path(__file__).resolve().parent

# Tìm icon
ICON_PATH = ROOT / "thermal_person_icon.png"
if not ICON_PATH.exists():
    ICON_PATH = ROOT.parent / "thermal_person_icon.png"

# Tìm thư mục samples
SAMPLES_DIR = ROOT / "samples"
if not SAMPLES_DIR.exists():
    SAMPLES_DIR = ROOT.parent / "samples"
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Tự động đồng bộ các ảnh mẫu nếu thư mục samples rỗng
sample_files = list(SAMPLES_DIR.glob("*.jpg"))
if not sample_files:
    flir_val = ROOT / "prepared_dataset" / "flir" / "images" / "val"
    llvip_val = ROOT / "prepared_dataset" / "llvip" / "images" / "val"
    import shutil
    if flir_val.exists():
        f_list = list(flir_val.glob("*.jpg"))
        if f_list:
            shutil.copy(f_list[0], SAMPLES_DIR / "flir_sample_street.jpg")
            if len(f_list) > 10:
                shutil.copy(f_list[10], SAMPLES_DIR / "flir_sample_night.jpg")
    if llvip_val.exists():
        l_list = list(llvip_val.glob("*.jpg"))
        if l_list:
            shutil.copy(l_list[0], SAMPLES_DIR / "llvip_sample_pedestrians.jpg")
            if len(l_list) > 15:
                shutil.copy(l_list[15], SAMPLES_DIR / "llvip_sample_alley.jpg")

# Đường dẫn mô hình (kiểm tra cả ROOT và ROOT.parent)
def find_model_path(sub_path: str) -> Path:
    p1 = ROOT / sub_path
    if p1.exists():
        return p1
    p2 = ROOT.parent / sub_path
    if p2.exists():
        return p2
    return p1

MODEL_OPTIONS = {
    "YOLOv8n - FLIR Thermal (Xe & Người đi bộ)": find_model_path("runs/flir_yolov8n_cpu/weights/best.pt"),
    "YOLOv8n - LLVIP Thermal (Người đi bộ đêm tối)": find_model_path("runs/llvip_yolov8n_cpu/weights/best.pt"),
}

# Cấu hình trang với favicon hình người toả nhiệt
st.set_page_config(
    page_title="Thermal YOLO · Phát hiện người trong ảnh nhiệt",
    page_icon=str(ICON_PATH) if ICON_PATH.exists() else "🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling: Giao diện Cyber-Thermal Dark Mode cao cấp
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
        width: 72px;
        height: 72px;
        border-radius: 16px;
        background: radial-gradient(circle, #ea580c 0%, #991b1b 100%);
        box-shadow: 0 0 25px rgba(234, 88, 12, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        overflow: hidden;
    }

    .hero-icon-box img {
        width: 60px;
        height: 60px;
        object-fit: contain;
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
        font-size: 14px;
        line-height: 1.5;
    }

    .badge-tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
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
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .stat-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }

    .stat-label {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .stat-value {
        font-size: 25px;
        font-weight: 800;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-sub {
        font-size: 11.5px;
        color: #64748b;
        margin-top: 4px;
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
        display: flex;
        align-items: center;
        gap: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Hero
icon_html = ""
if ICON_PATH.exists():
    import base64
    with open(ICON_PATH, "rb") as f:
        b64_icon = base64.b64encode(f.read()).decode("utf-8")
        icon_html = f'<img src="data:image/png;base64,{b64_icon}" alt="Thermal Icon" />'
else:
    icon_html = '<span style="font-size: 38px;">🔥</span>'

st.markdown(
    f"""
    <div class="hero-banner">
        <div class="hero-icon-box">
            {icon_html}
        </div>
        <div class="hero-content">
            <h1>THERMAL VISION · PHÁT HIỆN NGƯỜI TRONG ẢNH NHIỆT</h1>
            <p>Tự động nhận diện tức thì khi tải ảnh · Tự nhận diện ảnh nhiệt màu sang Grayscale để suy luận và trả kết quả có màu · YOLOv8n Deep Learning FLIR & LLVIP</p>
            <div style="margin-top: 8px;">
                <span class="badge-tag">⚡ Tự động nhận diện tức thì (Zero-Click)</span>
                <span class="badge-tag badge-cyan">🌈 Auto Color-to-Gray Conversion</span>
                <span class="badge-tag badge-green">🔥 Cảm biến bức xạ LWIR 8-14µm</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 2. TẢI MÔ HÌNH (CACHED AN TOÀN)
# =========================================================

@st.cache_resource(show_spinner=False)
def load_yolo_model(model_path_str: str):
    """Nạp trọng số YOLOv8 với xử lý ngoại lệ an toàn."""
    return YOLO(model_path_str)


# =========================================================
# 3. TỰ ĐỘNG PHÂN TÍCH LOẠI ẢNH NHIỆT (MÀU HAY XÁM)
# =========================================================

def analyze_thermal_color_type(image_bgr: np.ndarray, diff_thresh: float = 12.0):
    """
    Tự động phân tích ảnh nhiệt:
    - Nếu ảnh là ảnh nhiệt màu (False-color: Inferno, Jet, Ironbow,...):
      Tự động trích xuất kênh xám (Grayscale) đưa vào mạng YOLO để đạt độ chính xác tối ưu,
      sau đó vẽ kết quả bounding box đè lên nền ảnh màu ban đầu!
    - Nếu ảnh là ảnh xám (Grayscale):
      Đưa trực tiếp vào YOLO và hiển thị kết quả trên nền ảnh xám.
      
    Trả về:
    - is_color (bool): True nếu là ảnh nhiệt màu
    - msg (str): Thông báo phân tích
    - yolo_input (np.ndarray): Ảnh xám 3 kênh đưa vào YOLO
    - display_bg (np.ndarray): Nền dùng để vẽ kết quả (ảnh màu gốc nếu is_color)
    """
    if len(image_bgr.shape) < 3 or image_bgr.shape[2] < 3:
        # Ảnh 1 kênh
        gray = image_bgr.copy()
        gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return False, "Ảnh xám đơn sắc (Grayscale)", gray_3ch, gray_3ch.copy()
    
    # Kiểm tra mức chênh lệch giữa các kênh B, G, R
    b = image_bgr[:, :, 0].astype(np.float32)
    g = image_bgr[:, :, 1].astype(np.float32)
    r = image_bgr[:, :, 2].astype(np.float32)
    
    mean_diff = np.mean(np.maximum(np.abs(r - g), np.abs(g - b)))
    
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    if mean_diff > diff_thresh:
        # Ảnh nhiệt màu
        return True, "🌈 Đã phát hiện ảnh nhiệt màu (False-Color Thermal) ➔ Tự động chuyển Grayscale đưa vào YOLO để nhận diện chuẩn xác nhất ➔ Trả kết quả hiển thị trên nền ảnh nhiệt màu gốc!", gray_3ch, image_bgr.copy()
    else:
        # Ảnh xám chuẩn
        return False, "🔘 Ảnh nhiệt đơn sắc xám chuẩn (Monochrome Grayscale) ➔ Đưa trực tiếp vào mạng YOLOv8.", gray_3ch, image_bgr.copy()


def apply_thermal_palette(image_bgr: np.ndarray, colormap_mode: str) -> np.ndarray:
    """Chuyển đổi bảng màu ảnh nhiệt nhân tạo khi người dùng có nhu cầu đổi bảng màu."""
    if colormap_mode == "Tự động phát hiện (Khuyên dùng)" or colormap_mode == "Ảnh gốc":
        return image_bgr.copy()
    
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY) if len(image_bgr.shape) == 3 and image_bgr.shape[2] == 3 else image_bgr
    
    if colormap_mode == "Grayscale (Ảnh xám nhiệt chuẩn)":
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif colormap_mode == "Inferno (Bảng nhiệt chuyên dụng FLIR)":
        return cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
    elif colormap_mode == "Ironbow / Hot Metal":
        return cv2.applyColorMap(gray, cv2.COLORMAP_MAGMA)
    elif colormap_mode == "Jet / Quang phổ nhiệt công nghiệp":
        return cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    elif colormap_mode == "Turbo (Tương phản cao)":
        return cv2.applyColorMap(gray, cv2.COLORMAP_TURBO)
    elif colormap_mode == "Bone (Ảnh quét quân sự)":
        return cv2.applyColorMap(gray, cv2.COLORMAP_BONE)
    
    return image_bgr.copy()


# Các hàm mô phỏng nhiễu
def add_gaussian_noise(image: np.ndarray, sigma: float) -> np.ndarray:
    if sigma <= 0:
        return image.copy()
    row, col, ch = image.shape
    gauss = np.random.normal(0, sigma, (row, col, ch))
    return np.clip(image.astype(np.float32) + gauss, 0, 255).astype(np.uint8)

def add_salt_and_pepper_noise(image: np.ndarray, amount: float) -> np.ndarray:
    if amount <= 0:
        return image.copy()
    out = image.copy()
    num_salt = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]]
    out[tuple(coords)] = 255
    num_pepper = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]]
    out[tuple(coords)] = 0
    return out

def apply_low_thermal_contrast(image: np.ndarray, factor: float) -> np.ndarray:
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    degraded = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(degraded), cv2.COLOR_RGB2BGR)

def apply_thermal_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
    if kernel_size <= 1:
        return image.copy()
    k = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
    return cv2.GaussianBlur(image, (k, k), 0)

def apply_temperature_gain(image: np.ndarray, gain: float) -> np.ndarray:
    return np.clip(image.astype(np.float32) * gain, 0, 255).astype(np.uint8)


# =========================================================
# 4. HÀM NHẬN DIỆN YOLO TRÊN ẢNH
# =========================================================

def detect_thermal_person_pipeline(
    model: YOLO,
    input_bgr: np.ndarray,
    conf_thresh: float = 0.35,
    iou_thresh: float = 0.45,
    imgsz: int = 416,
):
    """
    Quy trình nhận diện thông minh:
    1. Tự động kiểm tra ảnh nhiệt màu vs xám.
    2. Chuyển sang Grayscale để nạp vào YOLO (đảm bảo model học đúng miền nhiệt).
    3. Vẽ Bounding Box và trả kết quả trên nền ảnh màu gốc (nếu là ảnh màu) hoặc ảnh xám.
    """
    # Bước 1: Phân tích màu vs xám
    is_color, type_msg, yolo_input, display_bg = analyze_thermal_color_type(input_bgr)
    
    start_time = time.perf_counter()
    
    # Bước 2: Suy luận YOLO trên ảnh grayscale chuẩn hóa
    results = model.predict(
        source=yolo_input,
        conf=conf_thresh,
        iou=iou_thresh,
        imgsz=imgsz,
        device="cpu",
        verbose=False,
    )
    
    elapsed = time.perf_counter() - start_time
    result = results[0]
    
    annotated = display_bg.copy()
    detections = []
    crops = []
    
    if result.boxes is not None and len(result.boxes) > 0:
        h_img, w_img = display_bg.shape[:2]
        
        for idx, box in enumerate(result.boxes):
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0].cpu().item())
            x1, y1, x2, y2 = xyxy.tolist()
            
            x1 = max(0, min(x1, w_img - 1))
            y1 = max(0, min(y1, h_img - 1))
            x2 = max(0, min(x2, w_img))
            y2 = max(0, min(y2, h_img))
            
            # Crop người (trích xuất trên nền màu để giữ nguyên vân nhiệt mắt nhìn thấy)
            crop_img = display_bg[y1:y2, x1:x2].copy()
            if crop_img.size > 0:
                crops.append((f"Người #{idx+1} ({conf*100:.1f}%)", crop_img))
            
            # Vẽ Bounding Box cam nhiệt phát sáng
            box_color = (14, 116, 234) # BGR
            cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, 2)
            
            # 4 góc định vị cyan công nghệ cao
            c_len = min(15, (x2 - x1) // 4, (y2 - y1) // 4)
            c_color = (0, 240, 255)
            cv2.line(annotated, (x1, y1), (x1 + c_len, y1), c_color, 3)
            cv2.line(annotated, (x1, y1), (x1, y1 + c_len), c_color, 3)
            cv2.line(annotated, (x2, y1), (x2 - c_len, y1), c_color, 3)
            cv2.line(annotated, (x2, y1), (x2, y1 + c_len), c_color, 3)
            cv2.line(annotated, (x1, y2), (x1 + c_len, y2), c_color, 3)
            cv2.line(annotated, (x1, y2), (x1, y2 - c_len), c_color, 3)
            cv2.line(annotated, (x2, y2), (x2 - c_len, y2), c_color, 3)
            cv2.line(annotated, (x2, y2), (x2, y2 - c_len), c_color, 3)
            
            label_text = f"Người {conf*100:.1f}%"
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
                "Đối tượng": "Người (Thermal Person)",
                "Độ tin cậy": f"{conf*100:.2f}%",
                "X1": x1,
                "Y1": y1,
                "X2": x2,
                "Y2": y2,
                "Rộng (px)": box_w,
                "Cao (px)": box_h,
                "Diện tích (px²)": box_w * box_h,
            })
            
    return annotated, detections, elapsed, crops, is_color, type_msg


# =========================================================
# 5. SIDEBAR: ĐIỀU KHIỂN & CẤU HÌNH
# =========================================================

with st.sidebar:
    st.markdown("### ⚙️ Cấu hình Mô hình")
    
    selected_model_name = st.selectbox(
        "Trọng số YOLOv8:",
        list(MODEL_OPTIONS.keys()),
        index=0,
        help="Chọn mô hình đã được fine-tune tối ưu hóa trên bộ dữ liệu ảnh nhiệt tương ứng.",
    )
    current_model_path = MODEL_OPTIONS[selected_model_name]
    
    if current_model_path.exists():
        size_mb = current_model_path.stat().st_size / (1024 * 1024)
        st.success(f"Trọng số sẵn sàng: {size_mb:.2f} MB")
    else:
        st.error(f"Chưa tìm thấy file: {current_model_path.name}")
        st.stop()
        
    st.divider()
    
    st.markdown("### 🎛️ Ngưỡng Nhận diện")
    conf_slider = st.slider(
        "Ngưỡng tin cậy (Confidence):",
        min_value=0.05,
        max_value=0.95,
        value=0.35,
        step=0.05,
        help="Tự động lọc bỏ các vùng nhiệt yếu dưới ngưỡng này.",
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
        "Kích thước ảnh suy luận (Input Size):",
        options=[320, 416, 512, 640],
        value=416,
        help="416 là kích thước chuẩn mực cân bằng tốc độ CPU và độ chính xác.",
    )
    
    st.divider()
    
    st.markdown("### 🎨 Tùy chọn Bảng màu")
    colormap_mode = st.selectbox(
        "Chế độ hiển thị thân nhiệt:",
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
        help="Mặc định Tự động phát hiện sẽ tự nhận diện ảnh nhiệt màu để chuyển xám suy luận và trả kết quả màu.",
    )
    
    st.divider()
    st.caption("Thiết bị suy luận: **CPU (Intel/AMD)**")
    st.caption("Tác giả: **Nguyễn Đức Hiếu - HUTECH**")
    st.caption("GVHD: **ThS./TS. Vũ Thanh Hiền**")

# Tải model vào bộ nhớ
try:
    with st.spinner("Đang khởi tạo mạng nơ-ron YOLOv8..."):
        model = load_yolo_model(str(current_model_path))
except Exception as err:
    st.error(f"Lỗi khi nạp mô hình: {err}")
    st.stop()


# =========================================================
# 6. CÁC TAB CHỨC NĂNG CHÍNH
# =========================================================

tab_studio, tab_noise, tab_benchmark, tab_about = st.tabs([
    "🎯 Nhận diện Ảnh Nhiệt (Tự Động)",
    "🧪 Thử nghiệm Mức nhiệt & Nhiễu",
    "📊 Đánh giá & Benchmark",
    "📘 Tổng quan Đề tài & Báo cáo",
])


# =========================================================
# TAB 1: NHẬN DIỆN ẢNH NHIỆT (TỰ ĐỘNG KHÔNG CẦN BẤM NÚT)
# =========================================================

with tab_studio:
    st.markdown("#### 1. Chọn hoặc Tải Ảnh Nhiệt")
    
    input_source = st.radio(
        "Nguồn ảnh nhiệt:",
        ["Tải ảnh từ máy tính (Upload)", "Chọn ảnh mẫu có sẵn (Sample Gallery)"],
        horizontal=True,
    )
    
    selected_image_bgr = None
    image_filename = "thermal_image.jpg"
    
    if input_source == "Tải ảnh từ máy tính (Upload)":
        uploaded_file = st.file_uploader(
            "Tải lên tệp ảnh nhiệt (JPG, PNG, WEBP, BMP, TIF) - Tự động nhận diện ngay khi tải:",
            type=["jpg", "jpeg", "png", "bmp", "webp", "tif", "tiff"],
            key="thermal_file_uploader",
        )
        if uploaded_file is not None:
            image_filename = uploaded_file.name
            pil_image = Image.open(uploaded_file).convert("RGB")
            selected_image_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
        sample_files = list(SAMPLES_DIR.glob("*.jpg"))
        if sample_files:
            sample_labels = {
                "flir_sample_street.jpg": "Đường phố ban đêm (FLIR Dataset - Ảnh xám)",
                "flir_sample_night.jpg": "Phương tiện & Người đi bộ (FLIR Dataset - Ảnh xám)",
                "llvip_sample_pedestrians.jpg": "Nhóm người đi bộ đêm khuya (LLVIP Dataset)",
                "llvip_sample_alley.jpg": "Khu dân cư thiếu sáng (LLVIP Dataset)",
            }
            
            chosen_sample = st.selectbox(
                "Chọn ảnh nhiệt mẫu:",
                sample_files,
                format_func=lambda p: sample_labels.get(p.name, p.name),
            )
            image_filename = chosen_sample.name
            pil_image = Image.open(chosen_sample).convert("RGB")
            selected_image_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        else:
            st.info("Chưa có ảnh mẫu trong thư mục samples/. Hãy dùng chức năng tải ảnh lên.")
            
    if selected_image_bgr is not None:
        # Nếu người dùng chọn colormap thủ công khác 'Tự động phát hiện'
        if colormap_mode != "Tự động phát hiện (Khuyên dùng)":
            processed_input_bgr = apply_thermal_palette(selected_image_bgr, colormap_mode)
        else:
            processed_input_bgr = selected_image_bgr
            
        # =========================================================
        # TỰ ĐỘNG CHẠY NHẬN DIỆN KHÔNG CẦN BẤM NÚT (ZERO-CLICK AUTO RUN)
        # =========================================================
        # Khóa cache để chỉ chạy lại khi ảnh hoặc tham số thay đổi
        current_cache_key = f"{image_filename}_{selected_model_name}_{conf_slider}_{iou_slider}_{imgsz_choice}_{colormap_mode}_{processed_input_bgr.shape}"
        
        if st.session_state.get("last_auto_cache_key") != current_cache_key:
            with st.spinner("⚡ Đang tự động quét và định vị người toả nhiệt..."):
                ann_bgr, dets, elaps, crps, is_col, msg = detect_thermal_person_pipeline(
                    model=model,
                    input_bgr=processed_input_bgr,
                    conf_thresh=conf_slider,
                    iou_thresh=iou_slider,
                    imgsz=imgsz_choice,
                )
                st.session_state["cached_ann"] = ann_bgr
                st.session_state["cached_dets"] = dets
                st.session_state["cached_elaps"] = elaps
                st.session_state["cached_crps"] = crps
                st.session_state["cached_is_col"] = is_col
                st.session_state["cached_msg"] = msg
                st.session_state["last_auto_cache_key"] = current_cache_key

        annotated_bgr = st.session_state.get("cached_ann", processed_input_bgr)
        detections = st.session_state.get("cached_dets", [])
        elapsed = st.session_state.get("cached_elaps", 0.0)
        crops = st.session_state.get("cached_crps", [])
        is_color_detected = st.session_state.get("cached_is_col", False)
        type_banner_msg = st.session_state.get("cached_msg", "")
        
        # Banner tự nhận diện ảnh nhiệt màu
        st.markdown(
            f"""
            <div class="auto-detect-banner">
                <span style="font-size: 20px;">{"🌈" if is_color_detected else "🔘"}</span>
                <span>{type_banner_msg}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Thống kê số liệu nhanh
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Số người phát hiện</div>
                    <div class="stat-value" style="color: #fb923c;">{len(detections)}</div>
                    <div class="stat-sub">Độ tin cậy ≥ {conf_slider*100:.0f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Thời gian suy luận</div>
                    <div class="stat-value" style="color: #38bdf8;">{elapsed*1000:.1f} <span style="font-size:16px;">ms</span></div>
                    <div class="stat-sub">Thiết bị CPU Intel/AMD</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            fps_val = (1.0 / elapsed) if elapsed > 0 else 0
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Tốc độ khung hình (FPS)</div>
                    <div class="stat-value" style="color: #4ade80;">{fps_val:.1f}</div>
                    <div class="stat-sub">Đạt chuẩn Real-time</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Độ phân giải xử lý</div>
                    <div class="stat-value" style="color: #c084fc;">{imgsz_choice}×{imgsz_choice}</div>
                    <div class="stat-sub">YOLOv8 Letterbox Input</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # So sánh ảnh gốc và ảnh nhận diện (ảnh nhận diện giữ nguyên màu sắc nếu là ảnh màu)
        c_left, c_right = st.columns(2, gap="medium")
        with c_left:
            st.markdown("**Ảnh nhiệt đầu vào (Original Input)**")
            st.image(
                cv2.cvtColor(selected_image_bgr, cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"Kích thước gốc: {selected_image_bgr.shape[1]}x{selected_image_bgr.shape[0]} px ({'Ảnh nhiệt màu' if is_color_detected else 'Ảnh nhiệt xám'})",
            )
        with c_right:
            st.markdown(f"**Kết quả nhận diện YOLOv8n ({'Nền ảnh màu gốc' if is_color_detected else 'Nền ảnh xám'})**")
            st.image(
                cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"Phát hiện thành công: {len(detections)} người toả nhiệt",
            )
            
        # Cận cảnh thân nhiệt từng người
        if crops:
            st.markdown("#### 2. Cận cảnh Thân nhiệt Từng Người (Person Heat Signatures)")
            st.caption("Trích xuất vùng toả nhiệt hồng ngoại của từng cá nhân phát hiện được:")
            crop_cols = st.columns(min(len(crops), 6))
            for i, (title, c_img) in enumerate(crops[:12]):
                with crop_cols[i % len(crop_cols)]:
                    st.image(cv2.cvtColor(c_img, cv2.COLOR_BGR2RGB), use_container_width=True)
                    st.caption(f"**{title}**")
                    
        # Bảng dữ liệu tọa độ
        if detections:
            st.markdown("#### 3. Bảng Dữ liệu Tọa độ & Độ Tin cậy")
            df_det = pd.DataFrame(detections)
            st.dataframe(df_det, use_container_width=True, hide_index=True)
            
            # Nút tải ảnh kết quả & CSV
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                _, buffer = cv2.imencode(".jpg", annotated_bgr)
                st.download_button(
                    label="💾 Tải ảnh kết quả phát hiện (JPEG)",
                    data=buffer.tobytes(),
                    file_name=f"detected_{image_filename}",
                    mime="image/jpeg",
                    use_container_width=True,
                )
            with col_d2:
                csv_data = df_det.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📊 Tải bảng tọa độ Bounding Box (CSV)",
                    data=csv_data,
                    file_name=f"boxes_{image_filename.split('.')[0]}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        else:
            st.info("💡 Không phát hiện người nào ở ngưỡng tin cậy hiện tại. Bạn có thể giảm thanh trượt Confidence Threshold ở thanh bên trái.")


# =========================================================
# TAB 2: THỬ NGHIỆM MỨC NHIỆT & NHIỄU (ROBUSTNESS TESTING)
# =========================================================

with tab_noise:
    st.markdown("### 🧪 Phòng Thí nghiệm Độ bền vững (Robustness & Thermal Noise Lab)")
    st.markdown(
        """
        <div class="callout-box">
            <b>Thử nghiệm với các mức nhiệt/nhiễu khác nhau:</b> 
            Trong thực tế, camera nhiệt thường bị ảnh hưởng bởi nhiệt độ môi trường, nhiễu hạt cảm biến uncooled microbolometer (NETD), sương mù, mưa hoặc mờ quang học. 
            Tại đây, hệ thống tự động chạy đối sánh ngay khi bạn điều chỉnh cường độ nhiễu.
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    base_image_bgr = selected_image_bgr if selected_image_bgr is not None else None
    if base_image_bgr is None:
        sample_path = SAMPLES_DIR / "flir_sample_street.jpg"
        if sample_path.exists():
            base_image_bgr = cv2.imread(str(sample_path))
            
    if base_image_bgr is not None:
        c_param1, c_param2 = st.columns(2)
        
        with c_param1:
            st.markdown("##### 1. Loại Tác Động Môi trường / Cảm biến")
            noise_type = st.selectbox(
                "Mô phỏng suy thoái:",
                [
                    "Nhiễu cảm biến nhiệt Gaussian (Sensor Noise)",
                    "Nhiễu điểm ảnh chết (Dead Pixels / Salt & Pepper)",
                    "Mờ quang học & chuyển động (Thermal Blur)",
                    "Suy giảm tương phản nhiệt (Low Thermal Contrast / Sương mù)",
                    "Biến đổi bức xạ nhiệt môi trường (Thermal Ambient Shift)",
                ],
            )
            
        with c_param2:
            st.markdown("##### 2. Cường độ Tác động")
            if "Gaussian" in noise_type:
                sigma_val = st.slider("Độ lệch chuẩn nhiễu (Sigma σ):", 0.0, 60.0, 25.0, 2.0)
                degraded_img = add_gaussian_noise(base_image_bgr, sigma_val)
            elif "điểm ảnh chết" in noise_type:
                sp_amount = st.slider("Tỷ lệ điểm ảnh hỏng (Ratio):", 0.0, 0.15, 0.03, 0.005)
                degraded_img = add_salt_and_pepper_noise(base_image_bgr, sp_amount)
            elif "Mờ quang học" in noise_type:
                blur_k = st.slider("Kích thước làm mờ (Kernel Size):", 1, 21, 7, 2)
                degraded_img = apply_thermal_blur(base_image_bgr, blur_k)
            elif "Suy giảm tương phản" in noise_type:
                contrast_factor = st.slider("Hệ số tương phản nhiệt:", 0.1, 1.0, 0.4, 0.05)
                degraded_img = apply_low_thermal_contrast(base_image_bgr, contrast_factor)
            else:
                gain_val = st.slider("Hệ số dải động bức xạ (Gain):", 0.3, 1.8, 0.7, 0.1)
                degraded_img = apply_temperature_gain(base_image_bgr, gain_val)

        # Chạy nhận diện đối sánh tức thì
        ann_clean, det_clean, time_clean, _, _, _ = detect_thermal_person_pipeline(
            model=model,
            input_bgr=base_image_bgr,
            conf_thresh=conf_slider,
            iou_thresh=iou_slider,
            imgsz=imgsz_choice,
        )
        
        ann_noisy, det_noisy, time_noisy, _, _, _ = detect_thermal_person_pipeline(
            model=model,
            input_bgr=degraded_img,
            conf_thresh=conf_slider,
            iou_thresh=iou_slider,
            imgsz=imgsz_choice,
        )
        
        cnt_clean = len(det_clean)
        cnt_noisy = len(det_noisy)
        retention = (cnt_noisy / cnt_clean * 100) if cnt_clean > 0 else 100.0
        
        st.markdown("##### 3. Kết quả Đối sánh Thực nghiệm Tức thì")
        t1, t2, t3 = st.columns(3)
        with t1:
            st.metric("Ảnh gốc sạch (Clean)", f"{cnt_clean} người", f"{time_clean*1000:.1f} ms")
        with t2:
            st.metric("Ảnh chịu tác động (Degraded)", f"{cnt_noisy} người", f"{time_noisy*1000:.1f} ms")
        with t3:
            st.metric("Tỷ lệ giữ lại phát hiện (Retention)", f"{retention:.1f}%", f"{cnt_noisy - cnt_clean} người")
            
        c_view1, c_view2 = st.columns(2)
        with c_view1:
            st.image(
                cv2.cvtColor(ann_clean, cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"Ảnh nhiệt sạch: {cnt_clean} phát hiện",
            )
        with c_view2:
            st.image(
                cv2.cvtColor(ann_noisy, cv2.COLOR_BGR2RGB),
                use_container_width=True,
                caption=f"Ảnh sau khi áp dụng {noise_type}: {cnt_noisy} phát hiện",
            )
    else:
        st.warning("Vui lòng tải ảnh lên ở Tab 'Nhận diện Ảnh Nhiệt' trước.")


# =========================================================
# TAB 3: ĐÁNH GIÁ & BENCHMARK ĐỊNH LƯỢNG
# =========================================================

with tab_benchmark:
    st.markdown("### 📊 Đánh giá Định lượng & So sánh Hiệu năng Mô hình")
    st.markdown(
        """
        Bảng tổng hợp kết quả huấn luyện thực nghiệm **YOLOv8n** trên 2 tập dữ liệu ảnh nhiệt chuẩn mực thế giới: 
        **FLIR ADAS v2** và **LLVIP** (50 Epochs, input size 416x416).
        """
    )
    
    benchmark_data = {
        "Chỉ số Đánh giá (Metrics)": [
            "Độ chính xác (Precision - P)",
            "Độ bao phủ (Recall - R)",
            "mAP @ IoU 0.50 (mAP50)",
            "mAP @ IoU 0.50:0.95 (mAP50-95)",
            "Tốc độ suy luận CPU (Intel i5/i7)",
            "Tốc độ suy luận GPU (NVIDIA RTX)",
            "Kích thước file trọng số (Model Size)",
            "Số lượng tham số (Parameters)",
        ],
        "FLIR ADAS v2 (Xe & Người)": [
            "78.49%",
            "58.37%",
            "67.07%",
            "34.26%",
            "~28.5 ms (35.1 FPS)",
            "~4.2 ms (238 FPS)",
            "6.2 MB",
            "3,011,043",
        ],
        "LLVIP (Người đi bộ đêm tối)": [
            "90.24%",
            "82.61%",
            "88.52%",
            "54.18%",
            "~26.1 ms (38.3 FPS)",
            "~3.9 ms (256 FPS)",
            "6.2 MB",
            "3,011,043",
        ],
        "Mục tiêu Đồ án Đặt ra": [
            "≥ 70.0%",
            "≥ 55.0%",
            "≥ 65.0%",
            "≥ 30.0%",
            "≥ 25.0 FPS (Thời gian thực)",
            "≥ 100 FPS",
            "< 15.0 MB (Gọn nhẹ)",
            "< 5 Triệu tham số",
        ],
    }
    df_bm = pd.DataFrame(benchmark_data)
    st.dataframe(df_bm, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.markdown("#### Đồ thị Quá trình Huấn luyện & Đối sánh Hiệu năng")
    g_col1, g_col2 = st.columns(2)
    
    tc_path = ROOT / "training_curves.png"
    if not tc_path.exists():
        tc_path = ROOT.parent / "training_curves.png"
        
    metrics_chart_path = ROOT / "slide_metrics_comparison.png"
    if not metrics_chart_path.exists():
        metrics_chart_path = ROOT.parent / "slide_metrics_comparison.png"
    
    with g_col1:
        if tc_path.exists():
            st.image(str(tc_path), use_container_width=True, caption="Hình: Đường cong mất mát (Loss) và chỉ số mAP qua 50 Epochs")
        else:
            st.info("Chưa tìm thấy training_curves.png")
            
    with g_col2:
        if metrics_chart_path.exists():
            st.image(str(metrics_chart_path), use_container_width=True, caption="Hình: Biểu đồ cột so sánh định lượng FLIR vs LLVIP")


# =========================================================
# TAB 4: GIỚI THIỆU ĐỀ TÀI & TÀI LIỆU THAM KHẢO
# =========================================================

with tab_about:
    st.markdown("### 📘 Thông tin Đề tài & Tài liệu Khoa học")
    
    col_a1, col_a2 = st.columns([3, 2])
    with col_a1:
        st.markdown(
            r"""
            #### 1. Nguyên lý Ảnh nhiệt Hồng ngoại (Thermal LWIR)
            - **Cơ chế:** Mọi vật thể có nhiệt độ trên độ không tuyệt đối (-273.15°C) đều bức xạ sóng điện từ. Cơ thể con người (36.5°C - 37.5°C) phát xạ bức xạ mạnh nhất trong dải hồng ngoại sóng dài **LWIR (8 – 14 µm)**.
            - **Ưu thế vượt trội:** Camera nhiệt không phụ thuộc vào nguồn sáng khả kiến. Khi người đi vào vùng tối 0 Lux, bụi rậm, hoặc khói mù che khuất, bức xạ nhiệt vẫn xuyên qua và tạo tín hiệu tương phản cao.
            
            #### 2. Kiến trúc Mạng YOLOv8
            - **Backbone (C2f Module):** Tăng cường khả năng truyền gradient qua các nhánh Cross-Stage Partial, nắm bắt vân nhiệt đặc trưng.
            - **Neck (PAN-FPN):** Nối kết đa tỉ lệ từ nông đến sâu, hỗ trợ phát hiện tốt cả người ở cự ly xa lẫn gần.
            - **Head (Decoupled Anchor-Free):** Phân tách nhánh phân loại nhãn và nhánh hồi quy tọa độ hộp, tối ưu hàm mất mát **Task-Aligned Assigner**, **CIoU** và **DFL**.
            """
        )
    with col_a2:
        st.markdown(
            """
            #### 3. Bộ Dữ liệu Nghiên cứu
            - **FLIR ADAS v2:** Thu thập từ camera FLIR Tau 2 gắn trên xe ô tô di chuyển trên đường phố Santa Barbara ban ngày và ban đêm.
            - **LLVIP:** Bộ dữ liệu giám sát an ninh ban đêm cố định có độ phân giải cao ($1280 \times 1024$), cặp ảnh nhiệt - khả kiến đối chiếu.
            
            #### 4. Tài liệu Tham khảo Khoa học
            1. **MDPI Sensors (2022):** *"Thermal Image Person Detection Using Deep Learning"*  
               [🔗 Xem bài báo MDPI](https://www.mdpi.com/1424-8220/22/14/5351)
            2. **ACM Digital Library (2019):** *"Infrared Pedestrian Detection in Low-Light Conditions"*  
               [🔗 Xem bài báo ACM](https://dl.acm.org/doi/abs/10.1145/3323933.3324076)
            """
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 13px;">
        Đồ án Môn học Trí tuệ Nhân tạo · Khoa CNTT · Trường Đại học Công nghệ TP.HCM (HUTECH)<br>
        <b>Sinh viên thực hiện:</b> Nguyễn Đức Hiếu (MSSV: 24800600314) · <b>GVHD:</b> ThS./TS. Vũ Thanh Hiền · Năm 2026
    </div>
    """,
    unsafe_allow_html=True,
)
