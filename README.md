# 🎯 Thermal YOLO Vision · Phát Hiện Người Trong Ảnh Nhiệt Bằng YOLOv8

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Model-Ultralytics%20YOLOv8n-00FFFF?logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![Streamlit](https://img.shields.io/badge/Web%20App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/Framework-PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Institution](https://img.shields.io/badge/HUTECH-Khoa%20CNTT-005696.svg)](https://www.hutech.edu.vn/)

> **Đề tài:** Nghiên cứu và triển khai mô hình học sâu YOLOv8 phát hiện và định vị người đi bộ trong ảnh nhiệt (Thermal Infrared - TIR) ứng dụng cho giám sát ban đêm, xe tự hành và an ninh trong điều kiện thiếu sáng hoặc thời tiết bất lợi.

---

## 👨‍💻 Thông Tin Tác Giả & Đề Tài

- **Sinh viên thực hiện:** Nguyễn Đức Hiếu
- **Mã số sinh viên (MSSV):** 24800600314
- **Lớp / Khóa:** Khoa Công nghệ Thông tin - Trường Đại học Công nghệ TP.HCM (HUTECH)
- **Giảng viên hướng dẫn:** ThS./TS. Vũ Thanh Hiền
- **Môn học:** Trí tuệ Nhân tạo (TTNT)

---

## 🚀 Các Tính Năng Nổi Bật

1. **Nhận diện Tức Thì Không Cần Bấm Nút (Zero-Click Auto-Detection):**
   - Tự động kích hoạt quy trình phân tích và suy luận YOLO ngay khi người dùng chọn ảnh mẫu hoặc tải ảnh nhiệt từ máy tính lên.

2. **Cơ chế Phân loại & Chuyển đổi Ảnh Giả Màu Thông Minh (False-Color Handling):**
   - Tự động nhận diện ảnh xám (Grayscale) hoặc ảnh giả màu (Inferno, Ironbow, Jet).
   - Tự động trích xuất kênh xám chuẩn hóa trước khi đưa vào YOLO (khớp miền đặc trưng huấn luyện), sau đó tự động hiển thị bounding box phát hiện trực tiếp lên nền ảnh nhiệt màu gốc.

3. **Chuyển Đổi Bảng Màu Quang Phổ Nhiệt Đa Dạng:**
   - Hỗ trợ đổi ảnh sang nhiều bảng màu quang phổ nhiệt chuyên dụng: *Inferno (FLIR), Ironbow/Magma, Jet, Turbo, Bone military*.

4. **Phòng Thí Nghiệm Kiểm Thử Độ Bền Vững (Robustness Noise Lab):**
   - Thử nghiệm độ bền vững của mô hình trước các mức nhiễu cảm biến: *Nhiễu Gauss (Gaussian Noise), Nhiễu Muối Tiêu (Salt & Pepper), Suy giảm tương phản nhiệt (Low Thermal Contrast), Mờ nhòe do chuyển động (Thermal Blur)*.

5. **Trích Xuất Chữ Ký Nhiệt Từng Người (Person Thermal Signatures):**
   - Tự động crop từng đối tượng người phát hiện được, phân tích mức nhiệt tương đối và độ tin cậy riêng biệt.

---

## 📊 Kết Quả Thực Nghiệm Sau 50 Epochs

| Bộ dữ liệu thử nghiệm | Độ phân giải | Số tham số | Tốc độ CPU (FPS) | Precision (%) | Recall (%) | mAP@50 (%) | mAP@50-95 (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **FLIR ADAS v2** | 416 × 416 | 3.01 M | **35.1 FPS** | 71.39% | 61.94% | **67.07%** | 35.88% |
| **LLVIP Benchmark** | 416 × 416 | 3.01 M | **35.1 FPS** | 87.21% | 85.34% | **88.52%** | 53.64% |

*Kết quả cho thấy YOLOv8n hoạt động xuất sắc trên cả CPU thông thường, đạt độ trễ thấp (~28.5 ms/ảnh) đáp ứng yêu cầu giám sát thời gian thực.*

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
ThermalYoloPerson/
│
├── configs/                                # Cấu hình dataset YAML cho YOLOv8
│   ├── flir.yaml                           # Cấu hình dataset FLIR ADAS v2
│   └── llvip.yaml                          # Cấu hình dataset LLVIP
│
├── samples/                                # Ảnh nhiệt mẫu thử nghiệm nhanh
│   ├── flir_sample_street.jpg              # Ảnh đường phố giao thông FLIR
│   ├── flir_sample_night.jpg               # Ảnh ban đêm FLIR
│   ├── llvip_sample_pedestrians.jpg        # Ảnh người đi bộ LLVIP
│   └── llvip_sample_alley.jpg              # Ảnh ngõ hẻm thiếu sáng LLVIP
│
├── app.py                                  # Giao diện Web Application (Streamlit)
├── train_yolo.py                           # Mã nguồn huấn luyện YOLOv8
├── prepare_yolo.py                         # Tiền xử lý dữ liệu FLIR v2 / LLVIP
├── run_app.bat                             # File chạy nhanh Web App trên Windows
├── requirements.txt                        # Danh sách thư viện Python cần thiết
├── .gitignore                              # Cấu hình loại trừ file rác, dataset, runs
├── README.md                               # Tài liệu hướng dẫn sử dụng
│
├── Bao_Cao_De_Tai_YOLO_Anh_Nhiet_Nguyen_Duc_Hieu.docx  # Báo cáo đồ án 5 chương
```

---

## 🛠️ Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Yêu Cầu Môi Trường
- Python 3.10, 3.11 hoặc 3.12.
- Hệ điều hành: Windows, macOS hoặc Linux.

### 2. Cài Đặt Thư Viện
Clone repository về máy tính và cài đặt các thư viện phụ thuộc:

```bash
# 1. Clone repository
git clone https://github.com/11Hiu2k5/ThermalYoloPerson.git
cd ThermalYoloPerson

# 2. Tạo môi trường ảo (khuyến nghị)
python -m venv .venv

# 3. Kích hoạt môi trường ảo:
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.\.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# 4. Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```

### 3. Chạy Ứng Dụng Web Demo
Bạn có thể khởi động giao diện Streamlit bằng 1 trong 2 cách:

- **Cách 1 (Nhanh nhất trên Windows):** Click đúp vào file `run_app.bat`.
- **Cách 2 (Bằng dòng lệnh):**
  ```bash
  streamlit run app.py
  ```
Trình duyệt sẽ tự động mở trang web tại địa chỉ: `http://localhost:8501`.

---

## 🧠 Huấn Luyện Mô Hình (Google Colab / Local GPU)

> **Lưu ý về Dataset:** Do kích thước của bộ dữ liệu FLIR ADAS v2 và LLVIP khá lớn (hơn 10GB), toàn bộ dataset được lưu trữ riêng trên **Google Drive** để tiện huấn luyện với GPU Tesla T4/A100 trên **Google Colab**, không upload trực tiếp lên repository GitHub.

### 1. Chuẩn bị cấu trúc dữ liệu YOLO
Chạy script tiền xử lý để chuyển đổi nhãn COCO JSON / Pascal VOC XML sang định dạng YOLO TXT:
```bash
python prepare_yolo.py
```

### 2. Khởi chạy huấn luyện
Huấn luyện YOLOv8n trên bộ dữ liệu mong muốn:
```bash
# Huấn luyện trên dataset LLVIP (50 epochs)
python train_yolo.py --dataset llvip --epochs 50 --batch 16 --device auto

# Huấn luyện trên dataset FLIR ADAS v2 (50 epochs)
python train_yolo.py --dataset flir --epochs 50 --batch 16 --device auto
```

Trọng số tối ưu sau khi huấn luyện sẽ được lưu tại thư mục `runs/<dataset>_yolov8n_<device>/weights/best.pt`.

---

## 📄 Tài Liệu Báo Cáo & Thuyết Trình Đi Kèm

- **Báo cáo đồ án toàn văn:** `Bao_Cao_De_Tai_YOLO_Anh_Nhiet_Nguyen_Duc_Hieu.docx` (Chi tiết cơ sở lý thuyết, kiến trúc YOLOv8, phương pháp thực nghiệm và đánh giá định lượng).
- **Slide thuyết trình PowerPoint:** `Thuyet_Trinh_YOLO_Anh_Nhiet_Nguyen_Duc_Hieu.pptx` (18 slide chuẩn 16:9, tích hợp hình minh họa độ nét cao và ghi chú thuyết trình, sẵn sàng kéo thả vào Canva).

---

## 📜 Tài Liệu Tham Khảo

1. Ultralytics YOLOv8 Documentation: [https://docs.ultralytics.com/](https://docs.ultralytics.com/)
2. FLIR Thermal Dataset: [https://www.mdpi.com/1424-8220/22/14/5351](https://www.mdpi.com/1424-8220/22/14/5351)
3. LLVIP Dataset for Low-light Vision: [https://dl.acm.org/doi/abs/10.1145/3323933.3324076](https://dl.acm.org/doi/abs/10.1145/3323933.3324076)
