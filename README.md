# 🎯 Thermal YOLO Vision · Phát Hiện Người Trong Ảnh Nhiệt Bằng YOLOv8

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Model-Ultralytics%20YOLOv8n-00FFFF?logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![Streamlit](https://img.shields.io/badge/Web%20App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/Framework-PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Institution](https://img.shields.io/badge/HUTECH-Khoa%20CNTT-005696.svg)](https://www.hutech.edu.vn/)

> **Đề tài:** Nghiên cứu và triển khai mô hình học sâu YOLOv8 phát hiện và định vị người đi bộ trong ảnh nhiệt hồng ngoại sóng dài (Long-Wave Infrared - LWIR, 8–14 µm) ứng dụng cho giám sát an ninh ban đêm, giao thông đô thị và cứu nạn trong điều kiện thiếu sáng hoặc thời tiết bất lợi.

---

## 👨‍💻 Thông Tin Tác Giả & Đề Tài

- **Sinh viên thực hiện:** Nguyễn Đức Hiếu
- **Mã số sinh viên (MSSV):** 24800600314
- **Lớp / Khóa:** Khoa Công nghệ Thông tin - Trường Đại học Công nghệ TP.HCM (HUTECH)
- **Giảng viên hướng dẫn:** ThS./TS. Vũ Thanh Hiền
- **Môn học:** Trí tuệ Nhân tạo (TTNT) · Năm thực hiện: 2026

---

## 🚀 Các Tính Năng Nổi Bật của Ứng Dụng

1. **Nhận diện Tức Thì Không Cần Bấm Nút (Zero-Click Inference):**
   - Tự động kích hoạt chu trình phân tích và suy luận YOLO ngay khi người dùng chọn ảnh mẫu hoặc tải ảnh nhiệt từ máy tính lên.
2. **Đối Sánh Song Song Hai Mô Hình (Dual Model Comparison):**
   - Hỗ trợ chạy độc lập và đặt cạnh nhau kết quả của mô hình **FLIR ADAS v2** (đường phố giao thông) và **LLVIP** (giám sát ban đêm) trên cùng một ảnh.
3. **Phân Tách Rõ Ràng Ảnh Suy Luận vs Ảnh Hiển Thị (Display Only Palettes):**
   - Ảnh nạp vào mạng YOLOv8 luôn là ảnh đơn sắc xám 3 kênh chuẩn hóa miền nhiệt, bảo toàn nguyên vẹn miền phân phối đặc trưng huấn luyện.
   - Hỗ trợ đổi bảng màu hiển thị trực quan cho mắt người: *Inferno (FLIR), Ironbow/Magma, Jet, Turbo, Bone military*.
4. **Đo Lường Hiệu Năng Minh Bạch:**
   - Phân biệt rõ ràng giữa **Thời gian suy luận thuần của Model (Inference Latency & FPS)** và **Thời gian toàn chu trình (End-to-End Pipeline Latency & FPS)**.
   - Tự động nhận diện chính xác phần cứng đang thực thi: **CPU (Intel/AMD)** hoặc **GPU CUDA**.
5. **Phòng Thí Nghiệm Kiểm Thử Độ Bền Vững (Thermal Robustness Lab):**
   - Kiểm chứng khả năng chịu lỗi của mô hình trước các tác nhân thực tế: *Nhiễu cảm biến vi bức xạ kế Gaussian (NETD), Điểm ảnh chết (Dead Pixels / Salt & Pepper), Mờ quang học & rung lắc, Suy giảm tương phản sương mù, Dịch chuyển bức xạ nhiệt môi trường*.
   - Tính toán tỷ lệ duy trì phát hiện (*Retention Rate*).
6. **Xuất Báo Cáo & Dữ Liệu:**
   - Tải về ảnh kết quả gắn khung bounding box chất lượng cao (JPG).
   - Tải bảng tọa độ bounding box chuẩn hóa (CSV).
   - Trích xuất cận cảnh chữ ký nhiệt từng người (*Person Thermal Signatures Gallery*).

---

## 📊 Kết Quả Thực Nghiệm Chính Thức Sau 50 Epochs

Số liệu nghiệm thu chính thức từ file nhật ký huấn luyện `results.csv` và kiểm định độc lập trên tập test/val:

| Tiêu chí Đánh giá | FLIR ADAS v2 (Xe & Người đô thị) | LLVIP (Người đi bộ đêm tối) | Mục tiêu Đề tài Đặt ra | Trạng thái Nghiệm thu |
| :--- | :---: | :---: | :---: | :---: |
| **Tập dữ liệu kiểm định** | Validation set (2,288 ảnh) | Test/Val set (3,463 ảnh) | Đánh giá độc lập | Khách quan |
| **Kích thước ảnh đầu vào** | 416 × 416 pixels | 416 × 416 pixels | 416 × 416 pixels | Chuẩn mực |
| **Độ chính xác (Precision - P)** | **78.49%** (0.7849) | **96.38%** (0.9638) | ≥ 70.00% | **Vượt chỉ tiêu** |
| **Độ thu hồi (Recall - R)** | **58.37%** (0.5837) | **94.54%** (0.9454) | ≥ 55.00% | **Vượt chỉ tiêu** |
| **mAP @ IoU 0.50 (mAP50)** | **67.07%** (0.6707) | **98.30%** (0.9830) | ≥ 65.00% | **Vượt chỉ tiêu** |
| **mAP @ IoU 0.50:0.95 (mAP50-95)** | **34.26%** (0.3426) | **68.04%** (0.6804) | ≥ 30.00% | **Vượt chỉ tiêu** |
| **Kích thước tệp trọng số (Size)** | **6.17 MB** (`flir_best.pt`) | **5.25 MB** (`llvip_best.pt`) | < 15.0 MB | **Siêu gọn nhẹ** |
| **Số lượng tham số (Parameters)** | 3,138,003 tham số | 2,604,883 tham số | < 5.0 triệu | **Tối ưu suy luận** |
| **Tốc độ suy luận CPU (Intel)** | ~28.5 ms (~35 FPS) | ~26.0 ms (~38 FPS) | > 25 FPS | **Thời gian thực** |

---

## 📂 Cấu Trúc Thư Mục Dự Án Đã Chuẩn Hóa

```text
ThermalYoloPerson/
│
├── app.py                                  # Giao diện Web Application chính (Streamlit Cyber-Thermal)
├── run_app.bat                             # File chạy nhanh ứng dụng trên Windows (tự kích hoạt .venv)
├── requirements.txt                        # Danh sách thư viện Python cần thiết
├── README.md                               # Tài liệu hướng dẫn sử dụng và báo cáo tổng quan
├── .gitignore                              # Cấu hình loại trừ file rác, dataset lớn, runs
│
├── configs/                                # Cấu hình dataset YAML cho YOLOv8
│   ├── flir.yaml                           # Cấu hình dataset FLIR ADAS v2
│   └── llvip.yaml                          # Cấu hình dataset LLVIP
│
├── models/                                 # Trọng số mô hình đã huấn luyện hoàn tất
│   ├── flir_best.pt                        # Mô hình tốt nhất trên FLIR ADAS v2 (6.17 MB)
│   ├── llvip_best.pt                       # Mô hình tốt nhất trên LLVIP (5.25 MB)
│   └── yolov8n.pt                          # Trọng số khởi tạo pre-trained COCO (6.55 MB)
│
├── samples/                                # Thư viện ảnh nhiệt mẫu thử nghiệm nhanh
│   ├── flir_sample_street.jpg              # Ảnh đường phố giao thông FLIR (LWIR)
│   ├── flir_sample_night.jpg               # Ảnh ban đêm FLIR (LWIR)
│   ├── llvip_sample_pedestrians.jpg        # Ảnh người đi bộ LLVIP (1280×1024)
│   └── llvip_sample_alley.jpg              # Ảnh ngõ hẻm thiếu sáng LLVIP (1280×1024)
│
├── scripts/                                # Các kịch bản Python độc lập
│   ├── prepare_yolo.py                     # Tiền xử lý dữ liệu FLIR v2 / LLVIP sang chuẩn YOLO
│   ├── train_yolo.py                       # Huấn luyện mô hình YOLOv8 trên CPU/GPU
│   └── evaluate_flir.py                    # Đánh giá độc lập mô hình FLIR trên tập validation
│
├── reports/                                # Toàn bộ hồ sơ báo cáo đề tài và tài liệu
│   ├── Bao_cao_de_tai_YOLO_HUTECH.docx     # Báo cáo đồ án đại học HUTECH chuẩn 7 chương
│   ├── Ly_thuyet_va_giai_thich_he_thong_YOLO.docx # Tài liệu lý thuyết và giải thích hệ thống chi tiết
│   ├── Thuyet_Trinh_YOLO_Anh_Nhiet_Nguyen_Duc_Hieu.pptx    # Slide thuyết trình PowerPoint 16:9
│   ├── Noi_Dung_Slide_Thuyet_Trinh_YOLO_Anh_Nhiet.docx    # Kịch bản thuyết trình chi tiết
│   └── assets/                             # Đồ thị huấn luyện (curves), confusion matrix, icon
│
├── prepared_dataset/                       # Dữ liệu ảnh nhiệt đã chuẩn hóa tọa độ YOLO
│   ├── flir/                               # Tập images và labels (train/val) FLIR
│   └── llvip/                              # Tập images và labels (train/val/test) LLVIP
│
└── runs/                                   # Chi tiết tiến trình huấn luyện và checkpoint gốc
    ├── flir_yolov8n_cpu/                   # Kết quả huấn luyện 50 epochs FLIR (results.csv, curves)
    ├── llvip_yolov8n_cpu/                  # Kết quả huấn luyện LLVIP (weights/best.pt)
    └── evaluation/                         # Kết quả đánh giá độc lập (flir_val curves)
```

---

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Yêu Cầu Môi Trường
- **Hệ điều hành:** Windows 10/11, macOS hoặc Linux.
- **Python:** Python 3.10 – 3.14 (Khuyến nghị dùng môi trường ảo `.venv`).

### 2. Khởi Động Nhanh Trên Windows (Khuyên Dùng)
Chỉ cần **bấm đúp chuột vào file `run_app.bat`** tại thư mục gốc `ThermalYoloPerson/` (hoặc tại thư mục cha `TTNT/`).
File script sẽ tự động:
1. Chuyển thư mục làm việc về đúng thư mục dự án.
2. Kiểm tra và kích hoạt môi trường ảo `.venv` (nếu có).
3. Kiểm tra tính khả dụng của Python và thư viện Streamlit.
4. Tự động mở trình duyệt web tại địa chỉ: `http://localhost:8501`.
5. Nếu có lỗi, script sẽ giữ cửa sổ terminal và hiển thị hướng dẫn khắc phục chi tiết.

### 3. Khởi Động Bằng Dòng Lệnh Thủ Công
```bash
# 1. Di chuyển vào thư mục dự án
cd ThermalYoloPerson

# 2. Kích hoạt môi trường ảo (nếu có)
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.\.venv\Scripts\activate.bat

# 3. Chạy ứng dụng Streamlit
python -m streamlit run app.py
```

---

## 🔬 Kịch Bản Kiểm Thử & Huấn Luyện Thêm

### 1. Đánh giá độc lập mô hình FLIR
```bash
python scripts/evaluate_flir.py
```

### 2. Huấn luyện lại hoặc Fine-tune tiếp tục
```bash
# Huấn luyện trên dataset FLIR ADAS v2
python scripts/train_yolo.py --dataset flir --epochs 50 --batch 4 --imgsz 416

# Huấn luyện trên dataset LLVIP
python scripts/train_yolo.py --dataset llvip --epochs 50 --batch 4 --imgsz 416

# Tiếp tục huấn luyện từ checkpoint gần nhất:
python scripts/train_yolo.py --dataset flir --resume
```

---

## 📜 Tài Liệu Tham Khảo Khoa Học

1. **MDPI Sensors (2022):** *"Thermal Image Person Detection Using Deep Learning"*, Sensors 2022, 22(14), 5351. [DOI: 10.3390/s22145351](https://www.mdpi.com/1424-8220/22/14/5351)
2. **ACM Digital Library (2019):** *"Infrared Pedestrian Detection in Low-Light Conditions"*, ACM Multimedia 2019. [DOI: 10.1145/3323933.3324076](https://dl.acm.org/doi/abs/10.1145/3323933.3324076)
3. **Ultralytics YOLOv8 Documentation:** [https://docs.ultralytics.com/](https://docs.ultralytics.com/)
