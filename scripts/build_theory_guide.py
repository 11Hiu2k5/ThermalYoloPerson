"""
Script tao file Tai lieu ly thuyet va giai thich he thong YOLO
Output: reports/Ly_thuyet_va_giai_thich_he_thong_YOLO.docx
"""

import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
ASSETS_DIR = REPORTS_DIR / "assets"
OUT_PATH = REPORTS_DIR / "Ly_thuyet_va_giai_thich_he_thong_YOLO.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def build_theory_document():
    doc = docx.Document()

    # Page setup
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.5)
        sec.bottom_margin = Cm(2.5)
        sec.left_margin = Cm(3.0)
        sec.right_margin = Cm(2.0)

    # Style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Title Banner
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = p_header.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ TP. HỒ CHÍ MINH (HUTECH)\n")
    r_h1.bold = True
    r_h1.font.size = Pt(13)
    r_h1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    r_h2 = p_header.add_run("KHOA CÔNG NGHỆ THÔNG TIN — BỘ MÔN TRÍ TUỆ NHÂN TẠO\n")
    r_h2.bold = True
    r_h2.font.size = Pt(12)

    logo_path = ASSETS_DIR / "hutech_logo.png"
    if logo_path.exists():
        p_l = doc.add_paragraph()
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_l.add_run().add_picture(str(logo_path), width=Cm(6.5))

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(12)
    p_t.paragraph_format.space_after = Pt(4)
    r_t = p_t.add_run("TÀI LIỆU LÝ THUYẾT VÀ HƯỚNG DẪN KỸ THUẬT HỆ THỐNG\n")
    r_t.bold = True
    r_t.font.size = Pt(17)
    r_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    r_sub = p_t.add_run("Phát hiện Người trong Ảnh nhiệt bằng YOLOv8 (FLIR ADAS v2 & LLVIP)")
    r_sub.italic = True
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(6)
    p_meta.paragraph_format.space_after = Pt(20)
    p_meta.add_run("Sinh viên thực hiện: Nguyễn Đức Hiếu (MSSV: 24800600314) · GVHD: ThS./TS. Vũ Thanh Hiền\nNăm 2026").font.size = Pt(11.5)

    doc.add_paragraph("—" * 45).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Helper functions
    def add_ch_head(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(f"{num_str}. {title_str.upper()}")
        r.bold = True
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    def add_sec_head(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(f"{num_str} {title_str}")
        r.bold = True
        r.font.size = Pt(12.5)
        r.font.color.rgb = RGBColor(0x00, 0x56, 0x96)

    def add_body(text):
        p = doc.add_paragraph(text)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.3
        return p

    def add_bullet(text):
        p = doc.add_paragraph(text, style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.25
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.rows[0].cells[0]
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c, 100, 100, 150, 150)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(code_text)
        r.font.name = 'Courier New'
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    # =========================================================================
    # PHẦN 1: ẢNH NHIỆT VÀ NGUYÊN LÝ CẢM BIẾN
    # =========================================================================
    add_ch_head("Phần 1", "Ảnh nhiệt và Nguyên lý Vật lý Cảm biến Hồng ngoại (LWIR)")
    add_body(
        "Khác biệt căn bản với ảnh quang học khả kiến dựa trên ánh sáng phản xạ, ảnh nhiệt hồng ngoại (Thermal Infrared) "
        "được tạo nên từ hiện tượng bức xạ điện từ tự nhiên của các nguyên tử và phân tử cấu tạo nên vật thể."
    )
    add_sec_head("1.1.", "Các Định luật Vật lý Nhiệt nền tảng")
    add_body(
        "1. Định luật Stefan-Boltzmann: Năng lượng phát xạ toàn phần (P) của một vật thể tỷ lệ thuận với lũy thừa bậc 4 của nhiệt độ tuyệt đối T (Kelvin):\n"
        "   P = ε · σ · A · T^4\n"
        "   Trong đó: ε là độ phát xạ bề mặt (Emissivity, với da người ε ≈ 0.98 – rất gần vật đen lý tưởng); "
        "σ là hằng số Stefan-Boltzmann (5.67 × 10^-8 W/m²·K⁴); A là diện tích bề mặt tiếp xúc."
    )
    add_body(
        "2. Định luật dịch chuyển Wien (Wien's Displacement Law):\n"
        "   λ_max = b / T     (với b ≈ 2897.8 µm·K)\n"
        "   Với nhiệt độ cơ thể người (T ≈ 310 K ~ 37°C), đỉnh bước sóng bức xạ phát ra cực đại tại:\n"
        "   λ_max = 2897.8 / 310 ≈ 9.35 µm (nằm trọn vẹn trong dải LWIR 8–14 µm)."
    )
    add_body(
        "3. Định luật phân bố bức xạ Planck (Planck's Law):\n"
        "   E(λ, T) = (2π·h·c²) / [ λ⁵ · (exp(h·c / (λ·k_B·T)) - 1) ]\n"
        "   Định luật Planck giải thích vì sao ở nhiệt độ phòng (khoảng 300 K), mật độ phổ bức xạ tập trung chủ yếu ở dải hồng ngoại sóng dài "
        "chứ hoàn toàn không phát xạ trong dải khả kiến (0.4 – 0.7 µm)."
    )

    add_sec_head("1.2.", "Cơ chế hoạt động của Cảm biến Vi bức xạ kế (Uncooled Microbolometer)")
    add_body(
        "Camera nhiệt phổ thông và thương mại (như FLIR Tau 2) sử dụng cảm biến vi bức xạ kế không làm lạnh (Uncooled Microbolometer). "
        "Mỗi điểm ảnh trên cảm biến là một màng mỏng làm từ Vanadium Oxide (VOx) hoặc Amorphous Silicon (a-Si) treo lơ lửng trên cầu nhiệt cách ly. "
        "Khi bức xạ hồng ngoại LWIR đi qua thấu kính Germanium đập vào màng mỏng, nhiệt độ màng tăng lên làm thay đổi điện trở của vật liệu. "
        "Mạch đọc điện tử (ROIC) đo đạc độ biến thiên điện trở này và chuyển đổi thành tín hiệu số 14-bit hoặc 8-bit mức xám."
    )

    # =========================================================================
    # PHẦN 2: HAI BỘ DỮ LIỆU FLIR ADAS VÀ LLVIP
    # =========================================================================
    add_ch_head("Phần 2", "Hai Bộ Dữ liệu Chuẩn Benchmark: FLIR ADAS v2 và LLVIP")
    add_body(
        "Để đảm bảo mô hình có khả năng tổng quát hóa cao trên nhiều điều kiện quan sát khác nhau, đề tài đã lựa chọn hai tập dữ liệu đại diện cho hai trường hợp ứng dụng thực tế:"
    )
    add_bullet("FLIR ADAS v2 (Giao thông đô thị di động): Thu thập từ camera FLIR Tau 2 gắn trên xe ô tô chạy ngoài đường phố ban ngày và ban đêm tại Mỹ. Đặc điểm dữ liệu: Độ phân giải 640×512, góc nhìn thấp di động, chịu rung lắc phương tiện, mật độ người đi bộ dày đặc kèm nhiều phương tiện giao thông và nguồn nhiệt phát xạ từ động cơ, ống xả.")
    add_bullet("LLVIP (Giám sát an ninh ban đêm cố định): Thu thập từ camera nhiệt gắn trên cao quan sát các tuyến phố đi bộ ban đêm tại Trung Quốc. Đặc điểm dữ liệu: Độ phân giải cao 1280×1024, góc nhìn cố định từ trên xuống, nền ban đêm lạnh đồng nhất, độ tương phản nhiệt của người đi bộ cực cao so với mặt đường.")

    # =========================================================================
    # PHẦN 3: ĐỊNH DẠNG NHÃN COCO, PASCAL VOC VÀ YOLO
    # =========================================================================
    add_ch_head("Phần 3", "Các Định dạng Nhãn: COCO JSON, Pascal VOC XML và Chuẩn YOLO TXT")
    add_body(
        "Mỗi hệ sinh thái thị giác máy tính sử dụng một cấu trúc biểu diễn tọa độ đối tượng khác nhau. Việc nắm vững quy tắc chuyển đổi là điều kiện tiên quyết để xây dựng dataset chuẩn:"
    )
    add_sec_head("3.1.", "So sánh 3 định dạng gán nhãn phổ biến")
    add_bullet("1. COCO JSON: Dùng trong FLIR ADAS v2. Lưu toàn bộ nhãn của hàng chục nghìn ảnh trong 1 file JSON duy nhất. Tọa độ bounding box lưu dưới dạng pixel tuyệt đối: [x_min, y_min, width, height].")
    add_bullet("2. Pascal VOC XML: Dùng trong LLVIP. Mỗi file ảnh đi kèm 1 file XML riêng biệt. Tọa độ lưu theo 4 điểm góc biên: <xmin>, <ymin>, <xmax>, <ymax>.")
    add_bullet("3. YOLO TXT: Mỗi file ảnh `image.jpg` đi kèm 1 file text `image.txt` cùng tên. Mỗi dòng đại diện cho 1 bounding box gồm 5 giá trị float cách nhau bởi dấu cách: `<class_id> <x_center> <y_center> <width> <height>` (được chuẩn hóa về đoạn [0.0, 1.0]).")

    add_sec_head("3.2.", "Ví dụ tính toán số học cụ thể")
    add_body(
        "Giả sử ta có bức ảnh nhiệt kích thước: Chiều rộng W = 1280 px, Chiều cao H = 1024 px.\n"
        "Trong file XML của Pascal VOC, nhãn người được ghi nhận với tọa độ:\n"
        "   xmin = 400, ymin = 200, xmax = 560, ymax = 620"
    )
    add_body("Quy trình chuyển đổi sang chuẩn YOLO như sau:")
    add_bullet("Bước 1: Tính chiều rộng và chiều cao hộp bao:\n"
               "   bw = xmax - xmin = 560 - 400 = 160 px\n"
               "   bh = ymax - ymin = 620 - 200 = 420 px")
    add_bullet("Bước 2: Tính tọa độ tâm hộp bao (Center X, Center Y):\n"
               "   cx = (xmin + xmax) / 2 = (400 + 560) / 2 = 480 px\n"
               "   cy = (ymin + ymax) / 2 = (200 + 620) / 2 = 410 px")
    add_bullet("Bước 3: Chuẩn hóa chia cho kích thước ảnh W và H:\n"
               "   x_center = 480 / 1280 = 0.375000\n"
               "   y_center = 410 / 1024 ≈ 0.400391\n"
               "   width    = 160 / 1280 = 0.125000\n"
               "   height   = 420 / 1024 ≈ 0.410156")
    add_body("Kết quả dòng nhãn ghi vào file .txt chuẩn YOLO (với class person = 0):")
    add_code_block("0 0.375000 0.400391 0.125000 0.410156")

    # =========================================================================
    # PHẦN 4: KIẾN TRÚC MÔ HÌNH YOLOV8 VÀ CÁC THÀNH PHẦN
    # =========================================================================
    add_ch_head("Phần 4", "Kiến trúc Mạng Nơ-ron Học sâu YOLOv8 Chi tiết")
    add_body(
        "YOLOv8 là kiến trúc phát hiện đối tượng hàng đầu thế giới của Ultralytics, được tối ưu hóa toàn diện về cả độ chính xác lẫn tốc độ suy luận:"
    )
    add_sec_head("4.1.", "Backbone C2f (Cross-Stage Partial with 2 Convolutions)")
    add_body(
        "Module C2f là cải tiến vượt bậc so với module C3 của YOLOv5. C2f chia nhỏ luồng đặc trưng đầu vào thành nhiều nhánh "
        "song song và cho đi qua các khối Bottleneck liên tiếp trước khi ghép lại (Concat). Cấu trúc này tối đa hóa số lượng luồng thông tin "
        "gradient truyền ngược (Gradient Flow Paths) mà không làm gia tăng đáng kể số lượng tham số, giúp mạng nắm bắt các vân nhiệt vi mô của cơ thể người cực kỳ hiệu quả."
    )

    add_sec_head("4.2.", "Neck PAN-FPN (Feature Pyramid Network)")
    add_body(
        "Ảnh nhiệt người ở cự ly xa có kích thước rất nhỏ (chỉ vài chục pixel), trong khi người ở gần chiếm diện tích lớn. "
        "Cấu trúc FPN (từ trên xuống) bổ sung ngữ nghĩa trừu tượng vào các tầng nông, kết hợp với PAN (từ dưới lên) truyền thông tin định vị tọa độ sắc nét "
        "lên các tầng sâu. Nhờ đó, mạng trích xuất được đặc trưng đa tỉ lệ (Multi-scale Features) tại 3 mức phân giải (P3: nhỏ, P4: vừa, P5: lớn)."
    )

    add_sec_head("4.3.", "Decoupled Anchor-Free Head")
    add_body(
        "Khác biệt với các thế hệ trước, YOLOv8 phân tách nhánh phân loại và nhánh định vị riêng biệt. "
        "Đồng thời, mạng loại bỏ Anchor Boxes nhân tạo (Anchor-Free), thay vào đó dự đoán trực tiếp tọa độ tâm và 4 khoảng cách từ tâm đến biên hộp. "
        "Điều này giúp mô hình giảm mạnh số lượng siêu tham số nhạy cảm và tăng tốc độ xử lý NMS."
    )

    # =========================================================================
    # PHẦN 5: CÁC HÀM MẤT MÁT TRONG HUẤN LUYỆN
    # =========================================================================
    add_ch_head("Phần 5", "Các Hàm Mất Mát (Loss Functions) trong Huấn Luyện")
    add_body(
        "Hàm mất mát tổng thể của YOLOv8 là sự kết hợp có trọng số của 3 thành phần mất mát độc lập:\n"
        "   L_total = λ_box · L_box + λ_cls · L_cls + λ_dfl · L_dfl"
    )
    add_sec_head("5.1.", "Complete IoU Loss (L_box / CIoU)")
    add_body(
        "CIoU đo lường mức độ sai lệch tọa độ hộp bao dựa trên 3 yếu tố hình học đồng thời:\n"
        "   L_CIoU = 1 - IoU + [ ρ²(b, b_gt) / c² ] + α · v\n"
        "Trong đó: ρ²(b, b_gt) là bình phương khoảng cách Euclidean giữa hai tâm hộp; c là độ dài đường chéo của hộp bao nhỏ nhất chứa cả hai hộp; "
        "v là tham số đo lường tính nhất quán về tỷ lệ khung hình (Aspect Ratio); α là hệ số cân bằng."
    )

    add_sec_head("5.2.", "Distribution Focal Loss (L_dfl / DFL)")
    add_body(
        "Thay vì xem tọa độ biên của hộp bao là một số thực cố định, DFL mô hình hóa tọa độ như một phân phối xác suất tổng quát (General Distribution). "
        "DFL tập trung tối ưu hóa các giá trị xác suất xung quanh tọa độ thực tế, giúp mạng học được ranh giới mờ nhạt đặc thù của vùng phát nhiệt trong ảnh hồng ngoại."
    )

    add_sec_head("5.3.", "Binary Cross-Entropy Loss (L_cls / BCE)")
    add_body(
        "Sử dụng hàm mất mát phân loại nhị phân BCE để đánh giá xác suất phân loại nhãn đối tượng (người vs không phải người)."
    )

    # =========================================================================
    # PHẦN 6: HỆ THỐNG CÁC ĐỘ ĐO ĐÁNH GIÁ ĐỊNH LƯỢNG
    # =========================================================================
    add_ch_head("Phần 6", "Hệ Thống Độ Đo Đánh Giá: Precision, Recall, IoU và mAP")
    add_body(
        "Để đánh giá khách quan năng lực phát hiện, thị giác máy tính sử dụng ma trận nhầm lẫn (Confusion Matrix) gồm 4 đại lượng:\n"
        "• TP (True Positive): Phát hiện đúng người có trong ảnh (IoU ≥ ngưỡng).\n"
        "• FP (False Positive): Báo động nhầm (dự đoán là người nhưng thực tế là vật thể nhiệt khác hoặc nền).\n"
        "• FN (False Negative): Bỏ sót người thực tế có trong ảnh.\n"
        "• TN (True Negative): Vùng nền không bị nhận nhầm."
    )
    add_sec_head("6.1.", "Precision, Recall và F1-Score")
    add_body(
        "• Precision = TP / (TP + FP) — Trả lời câu hỏi: Trong số những người mà mô hình tìm thấy, có bao nhiêu phần trăm là người thật?\n"
        "• Recall = TP / (TP + FN) — Trả lời câu hỏi: Trong số toàn bộ người có trong ảnh, mô hình đã bao quát được bao nhiêu phần trăm?\n"
        "• F1-Score = 2 · (Precision · Recall) / (Precision + Recall) — Trung bình điều hòa giữa Precision và Recall."
    )

    add_sec_head("6.2.", "Ý nghĩa của mAP@50 và mAP@50-95")
    add_body(
        "Đường cong Precision-Recall (P-R Curve) được vẽ bằng cách thay đổi ngưỡng Confidence từ 0 đến 1. "
        "Diện tích dưới đường cong P-R chính là AP (Average Precision). Khi tính toán trên 1 lớp (person), mAP tương đương AP.\n"
        "• mAP@50: AP tính khi ngưỡng IoU cố định tại 0.50. Phản ánh khả năng phát hiện người nhạy bén.\n"
        "• mAP@50-95: Trung bình cộng AP trên 10 ngưỡng IoU [0.50, 0.55, 0.60, ..., 0.95]. Đây là tiêu chuẩn khắt khe nhất của COCO, "
        "đòi hỏi hộp bao dự đoán phải khít sát hoàn hảo với ranh giới cơ thể người."
    )

    # =========================================================================
    # PHẦN 7: CÁCH HOẠT ĐỘNG CỦA APP.PY VÀ GIAO DIỆN STREAMLIT
    # =========================================================================
    add_ch_head("Phần 7", "Phân Tích Cơ Chế Hoạt Động Của app.py và Giao Diện Web")
    add_body(
        "Ứng dụng Streamlit được tối ưu hóa chuyên sâu để đáp ứng yêu cầu vận hành ổn định trên Windows:"
    )
    add_bullet("1. Safe Path Resolution: Sử dụng module `pathlib.Path` kết hợp hàm `resolve_asset_path` để tự động dò tìm tài nguyên (icon, sample images, weights), ngăn chặn triệt để lỗi đường dẫn khi chạy từ các thư mục làm việc khác nhau.")
    add_bullet("2. Cached Model Loading (@st.cache_resource): Mô hình YOLOv8n được nạp vào bộ nhớ duy nhất một lần. Các lượt người dùng tải ảnh sau đó sẽ gọi trực tiếp mô hình trong RAM, giảm độ trễ khởi động từ vài giây xuống 0 miligiây.")
    add_bullet("3. Phân tách Ảnh Suy luận vs Ảnh Hiển thị: Mạng YOLO luôn nhận ảnh Grayscale 3 kênh chuẩn hóa. Bảng màu nhiệt (Inferno, Jet, Magma, Turbo, Bone) chỉ áp dụng lên ảnh hiển thị trực quan cho mắt người.")
    add_bullet("4. Session State Hash Caching: Tính toán mã băm SHA-256 trên dữ liệu ảnh kết hợp bộ tham số (model, conf, iou, imgsz, colormap). Kết quả suy luận được lưu trong bộ đệm phiên làm việc, loại bỏ các phép tính toán dư thừa.")
    add_bullet("5. Thuật toán vẽ Bounding Box Cyber-Thermal: Vẽ khung chữ nhật cam nhiệt (14, 116, 234) kết hợp 4 góc định vị cyan (0, 240, 255) mang lại phong cách thị giác công nghệ cao.")

    # =========================================================================
    # PHẦN 8: FILE KHỞI CHẠY RUN_APP.BAT TRÊN WINDOWS
    # =========================================================================
    add_ch_head("Phần 8", "Cơ Chế Script Khởi Chạy Nhanh run_app.bat")
    add_body(
        "File `run_app.bat` được thiết kế theo chuẩn kịch bản tự động hóa doanh nghiệp với các bước kiểm tra an toàn nghiêm ngặt:"
    )
    add_bullet("Bước 1: `cd /d \"%~dp0\"` — Chuyển thư mục làm việc về đúng thư mục chứa file bat, giải quyết triệt để lỗi đường dẫn tương đối khi chạy qua shortcut.")
    add_bullet("Bước 2: `call .\\.venv\\Scripts\\activate.bat` — Tự động kích hoạt môi trường ảo Python cục bộ (.venv).")
    add_bullet("Bước 3: `where python` — Kiểm tra tính khả dụng của Python trên hệ điều hành. Nếu thiếu, xuất thông báo hướng dẫn cài đặt từ python.org.")
    add_bullet("Bước 4: `python -c \"import streamlit\"` — Kiểm tra thư viện Streamlit. Nếu thiếu, xuất hướng dẫn chạy lệnh `pip install -r requirements.txt`.")
    add_bullet("Bước 5: `python -m streamlit run app.py` — Khởi chạy ứng dụng Web.")
    add_bullet("Bước 6: `if errorlevel 1 pause` — Bắt mã lỗi hệ thống. Nếu có lỗi, giữ cửa sổ terminal không đóng để người dùng kịp đọc thông điệp thông báo.")

    # =========================================================================
    # PHẦN 9: QUY TRÌNH QUẢN LÝ MÃ NGUỒN BẰNG GIT & GITHUB
    # =========================================================================
    add_ch_head("Phần 9", "Quy Trình Quản Lý Mã Nguồn Bằng Git & Đẩy Lên GitHub")
    add_body(
        "Quản trị mã nguồn trong các dự án Trí tuệ Nhân tạo đòi hỏi các nguyên tắc khắt khe để tránh làm phình to kho chứa (Repository Bloat) do dataset và weights lớn:"
    )
    add_sec_head("9.1.", "Cấu hình .gitignore chuẩn mực cho Deep Learning")
    add_body(
        "Các thư mục và tệp tin TUYỆT ĐỐI KHÔNG ĐƯỢC đưa lên Git:\n"
        "• Thư mục môi trường ảo: `.venv/`, `venv/` (hàng chục nghìn file thư viện phụ thuộc).\n"
        "• Bộ dữ liệu gốc & ảnh chuẩn bị: `FLIR_ADAS_v2/`, `LLVIP/`, `prepared_dataset/` (dung lượng > 10GB, vượt giới hạn 100MB/file của GitHub).\n"
        "• Checkpoints mô hình kích thước lớn: `*.pt`, `runs/` (chỉ lưu trữ trên Google Drive hoặc Release assets).\n"
        "• Bytecode và cache tạm: `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`."
    )

    add_sec_head("9.2.", "Quy trình dòng lệnh Git chuẩn để đẩy lên GitHub")
    add_code_block(
        "# 1. Kiem tra trang thai cac file thay doi\n"
        "git status\n\n"
        "# 2. Kiem tra dia chi remote repository\n"
        "git remote -v\n\n"
        "# 3. Them cac file bao cao va ma nguon da sua\n"
        "git add reports/ app.py run_app.bat README.md scripts/\n\n"
        "# 4. Commit voi thong diep ro rang, chuyen nghiep\n"
        "git commit -m \"docs: hoan thien bao cao do an HUTECH va tai lieu ly thuyet\"\n\n"
        "# 5. Day len branch main tren GitHub\n"
        "git push origin main"
    )

    # =========================================================================
    # PHẦN 10: NGUYÊN TẮC TỔ CHỨC VÀ DỌN DẸP THƯ MỤC DỰ ÁN
    # =========================================================================
    add_ch_head("Phần 10", "Nguyên Tắc Tổ Chức và Dọn Dẹp Thư Mục Dự Án")
    add_body(
        "Một dự án khoa học dữ liệu đạt chuẩn kỹ thuật phần mềm cần tuân thủ cấu trúc phân tầng rõ ràng:"
    )
    add_bullet("Root level: Chỉ chứa các file điều hướng cốt lõi (`app.py`, `run_app.bat`, `requirements.txt`, `README.md`, `.gitignore`).")
    add_bullet("models/: Lưu trữ các checkpoint mô hình tốt nhất phục vụ suy luận (`flir_best.pt`, `llvip_best.pt`, `yolov8n.pt`).")
    add_bullet("samples/: Lưu trữ các bức ảnh nhiệt mẫu tiêu biểu để người dùng kiểm thử nhanh mà không cần tải thêm dữ liệu bên ngoài.")
    add_bullet("configs/: Chứa các file cấu hình YAML định nghĩa đường dẫn dataset và danh mục nhãn (`flir.yaml`, `llvip.yaml`).")
    add_bullet("scripts/: Tập trung toàn bộ mã nguồn tiền xử lý dữ liệu (`prepare_yolo.py`), huấn luyện (`train_yolo.py`) và đánh giá độc lập (`evaluate_flir.py`).")
    add_bullet("reports/: Lưu trữ hồ sơ học thuật hoàn chỉnh (Báo cáo toàn văn DOCX, slide thuyết trình PPTX, kịch bản thuyết trình và thư mục assets đồ thị hình ảnh).")
    add_bullet("runs/: Lưu vết toàn bộ lịch sử huấn luyện phục vụ việc tái lập kết quả khoa học (Reproducibility).")

    # Add page numbers to header/footer
    sec = doc.sections[0]
    p_f = sec.footer.paragraphs[0]
    p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_pf = p_f.add_run("Trang ")
    r_pf.font.size = Pt(10)
    r_pf.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    add_page_number(r_pf)

    doc.save(str(OUT_PATH))
    print(f"[OK] Da tao thanh cong tai lieu ly thuyet: {OUT_PATH}")

if __name__ == "__main__":
    build_theory_document()
