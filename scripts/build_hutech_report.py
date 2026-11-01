"""
Script tao file Bao cao do an YOLO theo chuan phong cach HUTECH
Output: reports/Bao_cao_de_tai_YOLO_HUTECH.docx
"""

import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
ASSETS_DIR = REPORTS_DIR / "assets"
OUT_PATH = REPORTS_DIR / "Bao_cao_de_tai_YOLO_HUTECH.docx"

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

def build_report():
    doc = docx.Document()

    # 1. Page Setup - Chuan A4, le luan van HUTECH
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)   # 3cm cho gay dong tap
        section.right_margin = Cm(2.0)  # 2cm le phai

    # Set Default Font Times New Roman
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12.5)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # =========================================================================
    # TRANG BIA (COVER PAGE)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r.bold = True
    r.font.size = Pt(13)
    r2 = p.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ TP. HỒ CHÍ MINH (HUTECH)\n")
    r2.bold = True
    r2.font.size = Pt(14)
    r2.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    r3 = p.add_run("KHOA CÔNG NGHỆ THÔNG TIN")
    r3.bold = True
    r3.font.size = Pt(13)

    # Duong gach ngang ngan phan cach
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(0)
    p_line.paragraph_format.space_after = Pt(14)
    r_l = p_line.add_run("———————————————")
    r_l.font.color.rgb = RGBColor(0x00, 0x56, 0x96)

    # Logo HUTECH
    logo_path = ASSETS_DIR / "hutech_logo.png"
    if logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(18)
        p_logo.add_run().add_picture(str(logo_path), width=Cm(7.2))

    # Tieu de do an
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("BÁO CÁO ĐỒ ÁN MÔN HỌC\nTRÍ TUỆ NHÂN TẠO (AI)")
    r_sub.bold = True
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(28)
    r_t = p_title.add_run("XÂY DỰNG HỆ THỐNG PHÁT HIỆN NGƯỜI TRONG ẢNH NHIỆT\nSỬ DỤNG YOLO VỚI BỘ DỮ LIỆU FLIR ADAS VÀ LLVIP")
    r_t.bold = True
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # Khung thong tin sinh vien & giang vien
    tbl_info = doc.add_table(rows=4, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Sinh viên thực hiện:", "NGUYỄN ĐỨC HIẾU"),
        ("Mã số sinh viên (MSSV):", "24800600314"),
        ("Ngành đào tạo:", "Công nghệ Thông tin"),
        ("Giảng viên hướng dẫn:", "ThS./TS. VŨ THANH HIỀN"),
    ]
    for row_idx, (k, v) in enumerate(info_data):
        row = tbl_info.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Cm(6.5)
        cell_v.width = Cm(8.5)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_before = Pt(3)
        pk.paragraph_format.space_after = Pt(3)
        rk = pk.add_run(k)
        rk.font.size = Pt(12.5)
        rk.font.name = 'Times New Roman'
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_before = Pt(3)
        pv.paragraph_format.space_after = Pt(3)
        rv = pv.add_run(v)
        rv.bold = True
        rv.font.size = Pt(12.5)
        rv.font.name = 'Times New Roman'

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(50)
    p_foot.paragraph_format.space_after = Pt(0)
    r_f = p_foot.add_run("TP. HỒ CHÍ MINH, NĂM 2026")
    r_f.bold = True
    r_f.font.size = Pt(13)

    # Section moi tu trang tiep theo de danh so trang (Trang bia khong danh so)
    sec_content = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    sec_content.footer.is_linked_to_previous = False
    p_f = sec_content.footer.paragraphs[0]
    p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_pf = p_f.add_run("Trang ")
    r_pf.font.size = Pt(10)
    r_pf.font.name = 'Times New Roman'
    r_pf.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    add_page_number(r_pf)

    # =========================================================================
    # NHAN XET CUA GIANG VIEN HUONG DAN
    # =========================================================================
    p_rev_head = doc.add_paragraph()
    p_rev_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rev_head.paragraph_format.space_before = Pt(10)
    p_rev_head.paragraph_format.space_after = Pt(14)
    r_rh = p_rev_head.add_run("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN")
    r_rh.bold = True
    r_rh.font.size = Pt(15)
    r_rh.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "Họ và tên Giảng viên: Vũ Thanh Hiền\n"
        "Đơn vị công tác: Khoa Công nghệ Thông tin - Trường Đại học Công nghệ TP.HCM (HUTECH)\n"
        "Tên đề tài: Xây dựng hệ thống phát hiện người trong ảnh nhiệt sử dụng YOLO với bộ dữ liệu FLIR ADAS và LLVIP\n"
        "Sinh viên thực hiện: Nguyễn Đức Hiếu               MSSV: 24800600314"
    )

    doc.add_paragraph("1. Đánh giá về tinh thần, thái độ và trách nhiệm nghiên cứu của sinh viên:")
    doc.add_paragraph("........................................................................................................................................................................................................................................................................................................................................................................................................................................................................")

    doc.add_paragraph("2. Đánh giá về khối lượng công việc và mức độ hoàn thành các nhiệm vụ đặt ra:")
    doc.add_paragraph("........................................................................................................................................................................................................................................................................................................................................................................................................................................................................")

    doc.add_paragraph("3. Đánh giá về chất lượng khoa học, kết quả thực nghiệm và tính ứng dụng của đề tài:")
    doc.add_paragraph("........................................................................................................................................................................................................................................................................................................................................................................................................................................................................")

    doc.add_paragraph("4. Điểm đánh giá (bằng số và bằng chữ): ..................................................................................................")

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(25)
    p_sig.add_run("TP. Hồ Chí Minh, ngày ..... tháng ..... năm 2026\nGiảng viên hướng dẫn\n\n\n\n\nThS./TS. Vũ Thanh Hiền").bold = True

    doc.add_page_break()

    # =========================================================================
    # LOI CAM ON
    # =========================================================================
    p_thx_head = doc.add_paragraph()
    p_thx_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_thx_head.paragraph_format.space_before = Pt(10)
    p_thx_head.paragraph_format.space_after = Pt(14)
    r_th = p_thx_head.add_run("LỜI CẢM ƠN")
    r_th.bold = True
    r_th.font.size = Pt(15)
    r_th.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p_thx1 = doc.add_paragraph(
        "Lời đầu tiên, em xin trân trọng gửi lời cảm ơn chân thành và sâu sắc nhất đến Ban Giám hiệu "
        "Trường Đại học Công nghệ TP.HCM (HUTECH), Ban Chủ nhiệm Khoa Công nghệ Thông tin, cùng toàn thể quý Thầy Cô "
        "đã tận tâm giảng dạy, truyền đạt những kiến thức nền tảng và chuyên sâu quý báu về Trí tuệ nhân tạo, Thị giác máy tính "
        "và Kỹ thuật lập trình trong suốt quá trình học tập tại trường."
    )
    p_thx1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p_thx2 = doc.add_paragraph(
        "Đặc biệt, em xin bày tỏ lòng biết ơn sâu sắc nhất đến Giảng viên hướng dẫn – ThS./TS. Vũ Thanh Hiền. "
        "Thầy/Cô đã luôn dành sự quan tâm chỉ bảo chu đáo, định hướng phương pháp tiếp cận khoa học, tận tình giải đáp những khó khăn "
        "về mặt kỹ thuật trong quá trình xử lý đặc trưng ảnh nhiệt, tối ưu hóa kiến trúc YOLOv8 và tạo mọi điều kiện thuận lợi nhất "
        "để em hoàn thành xuất sắc đề tài này."
    )
    p_thx2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p_thx3 = doc.add_paragraph(
        "Dù đã dành nhiều tâm huyết và nỗ lực hoàn thiện từ mã nguồn đến báo cáo, song do giới hạn về mặt thời gian và kinh nghiệm thực tế, "
        "đồ án khó tránh khỏi những thiếu sót nhất định. Em rất mong nhận được những nhận xét, đóng góp quý báu từ quý Thầy Cô trong Hội đồng khoa học "
        "để công trình nghiên cứu được hoàn thiện hơn nữa."
    )
    p_thx3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p_camdoan = doc.add_paragraph()
    p_camdoan.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_camdoan.paragraph_format.space_before = Pt(20)
    p_camdoan.add_run("Sinh viên thực hiện\n\n\n\nNguyễn Đức Hiếu").bold = True

    doc.add_page_break()

    # =========================================================================
    # TOM TAT DE TAI (ABSTRACT)
    # =========================================================================
    p_abs_head = doc.add_paragraph()
    p_abs_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_head.paragraph_format.space_before = Pt(10)
    p_abs_head.paragraph_format.space_after = Pt(14)
    r_ab = p_abs_head.add_run("TÓM TẮT ĐỀ TÀI (ABSTRACT)")
    r_ab.bold = True
    r_ab.font.size = Pt(15)
    r_ab.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p_vn_title = doc.add_paragraph()
    p_vn_title.add_run("Tóm tắt (Tiếng Việt):").bold = True
    p_vn = doc.add_paragraph(
        "Trong các hệ thống giám sát an ninh đêm, giao thông thông minh và tìm kiếm cứu nạn, camera quang học (RGB) thông thường "
        "gặp phải rào cản vật lý cố hữu do phụ thuộc hoàn toàn vào nguồn sáng khả kiến. Trong bóng tối hoàn toàn (0 Lux), sương mù hay khói bụi, "
        "camera quang học hầu như mất khả năng nhận diện. Ngược lại, camera nhiệt hồng ngoại sóng dài (LWIR, 8–14 µm) thu nhận trực tiếp "
        "bức xạ phát nhiệt tự nhiên của cơ thể người, duy trì độ tương phản vượt trội bất kể điều kiện chiếu sáng. Đề tài "
        "\"Xây dựng hệ thống phát hiện người trong ảnh nhiệt sử dụng YOLO với bộ dữ liệu FLIR ADAS và LLVIP\" tập trung nghiên cứu, "
        "chuyển đổi chuẩn hóa và huấn luyện kiến trúc học sâu hiện đại YOLOv8 (phiên bản YOLOv8n) trên hai bộ dữ liệu chuẩn benchmark quốc tế. "
        "Hệ thống đã chuẩn hóa hơn 39.000 ảnh nhiệt và nhãn COCO JSON / Pascal VOC XML sang định dạng YOLO; huấn luyện thành công 50 epochs "
        "đạt chỉ số mAP@50 đạt 67.07% trên FLIR ADAS v2 và 98.30% trên LLVIP; kiểm thử độ bền vững trước các mức nhiễu cảm biến; đồng thời "
        "xây dựng hoàn chỉnh ứng dụng Web Demo (Streamlit Cyber-Thermal Studio) đạt tốc độ xử lý thời gian thực > 35 FPS ngay trên môi trường CPU thông thường."
    )
    p_vn.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p_en_title = doc.add_paragraph()
    p_en_title.paragraph_format.space_before = Pt(12)
    p_en_title.add_run("Abstract (English):").bold = True
    p_en = doc.add_paragraph(
        "In nocturnal security surveillance, intelligent transportation, and search-and-rescue operations, conventional optical (RGB) cameras "
        "face fundamental limitations due to their reliance on visible illumination, often failing in total darkness (0 Lux), dense fog, or smoky atmospheres. "
        "In contrast, Long-Wave Infrared (LWIR, 8–14 µm) thermal imaging captures radiated body heat independently of ambient light, providing high contrast signatures. "
        "This project, entitled \"Building a Person Detection System in Thermal Imagery Using YOLO with FLIR ADAS and LLVIP Datasets\", investigates, preprocesses, "
        "and trains the cutting-edge YOLOv8n architecture on two benchmark thermal datasets. The system standardized over 39,000 thermal images and converted COCO JSON / Pascal VOC XML "
        "annotations into normalized YOLO format; achieved robust mAP@50 scores of 67.07% on FLIR ADAS v2 and 98.30% on LLVIP over 50 epochs; evaluated model robustness "
        "under diverse synthetic sensor noises; and deployed an interactive Streamlit Cyber-Thermal Web Studio achieving real-time inference (>35 FPS) on standard CPU hardware."
    )
    p_en.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # =========================================================================
    # MUC LUC TONG THE (TABLE OF CONTENTS)
    # =========================================================================
    p_toc_head = doc.add_paragraph()
    p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_head.paragraph_format.space_before = Pt(10)
    p_toc_head.paragraph_format.space_after = Pt(14)
    r_th = p_toc_head.add_run("MỤC LỤC")
    r_th.bold = True
    r_th.font.size = Pt(15)
    r_th.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    toc_items = [
        ("LỜI CẢM ƠN", "i"),
        ("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "ii"),
        ("TÓM TẮT ĐỀ TÀI (ABSTRACT)", "iii"),
        ("DANH MỤC TỪ VIẾT TẮT", "vi"),
        ("DANH MỤC HÌNH ẢNH", "vii"),
        ("DANH MỤC BẢNG BIỂU", "viii"),
        ("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI", "Trang 1"),
        ("  1.1. Lý do chọn đề tài và tính cấp thiết", "Trang 1"),
        ("  1.2. Mục tiêu nghiên cứu của đề tài", "Trang 2"),
        ("  1.3. Đối tượng và phạm vi nghiên cứu", "Trang 3"),
        ("  1.4. Phương pháp nghiên cứu và thực hiện", "Trang 3"),
        ("  1.5. Cấu trúc tổng thể của báo cáo", "Trang 4"),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN CÔNG NGHỆ", "Trang 5"),
        ("  2.1. Tổng quan Thị giác máy tính và bài toán Phát hiện đối tượng", "Trang 5"),
        ("  2.2. Bản chất vật lý của ảnh nhiệt hồng ngoại (Thermal LWIR)", "Trang 6"),
        ("  2.3. Phân biệt ảnh nhiệt thật và ảnh RGB chuyển xám / giả màu", "Trang 8"),
        ("  2.4. Họ mô hình YOLO và kiến trúc mạng học sâu YOLOv8", "Trang 9"),
        ("  2.5. Các khái niệm cốt lõi: Bounding Box, IoU và NMS", "Trang 11"),
        ("  2.6. Hệ thống các chỉ số đánh giá: Precision, Recall và mAP", "Trang 12"),
        ("  2.7. Nền tảng Streamlit trong triển khai ứng dụng thị giác máy tính", "Trang 14"),
        ("CHƯƠNG 3: DỮ LIỆU VÀ QUY TRÌNH TIỀN XỬ LÝ", "Trang 15"),
        ("  3.1. Tổng quan hai bộ dữ liệu FLIR ADAS v2 và LLVIP", "Trang 15"),
        ("  3.2. Cấu trúc dữ liệu gốc và định dạng nhãn COCO / Pascal VOC", "Trang 17"),
        ("  3.3. Thuật toán chuyển đổi chuẩn hóa tọa độ sang YOLO", "Trang 18"),
        ("  3.4. Chuẩn hóa phân loại đối tượng người (Class Person)", "Trang 19"),
        ("  3.5. Phân chia tập dữ liệu huấn luyện, kiểm định và kiểm thử", "Trang 20"),
        ("  3.6. Thống kê chi tiết số lượng ảnh và bounding box thực tế", "Trang 21"),
        ("CHƯƠNG 4: HUẤN LUYỆN MÔ HÌNH", "Trang 22"),
        ("  4.1. Môi trường phần cứng và cấu hình phần mềm", "Trang 22"),
        ("  4.2. Thiết lập siêu tham số huấn luyện (Hyperparameters)", "Trang 23"),
        ("  4.3. Quá trình huấn luyện trên bộ dữ liệu FLIR ADAS v2", "Trang 24"),
        ("  4.4. Quá trình huấn luyện trên bộ dữ liệu LLVIP", "Trang 26"),
        ("  4.5. Chiến lược lưu trữ Checkpoints và Early Stopping", "Trang 27"),
        ("  4.6. Trích xuất và phân tích kết quả huấn luyện thực tế", "Trang 28"),
        ("CHƯƠNG 5: XÂY DỰNG ỨNG DỤNG (THERMAL VISION STUDIO)", "Trang 29"),
        ("  5.1. Kiến trúc hệ thống tổng thể và luồng dữ liệu", "Trang 29"),
        ("  5.2. Phân tích mã nguồn app.py và tối ưu hóa hiệu năng", "Trang 30"),
        ("  5.3. Tiền xử lý ảnh và cơ chế phân tách ảnh suy luận vs ảnh hiển thị", "Trang 31"),
        ("  5.4. Chế độ đối sánh song song hai mô hình (Dual Comparison)", "Trang 33"),
        ("  5.5. Phòng thí nghiệm kiểm thử độ bền vững (Robustness Lab)", "Trang 34"),
        ("  5.6. Tự động hóa vận hành trên Windows qua run_app.bat", "Trang 36"),
        ("CHƯƠNG 6: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ", "Trang 37"),
        ("  6.1. Kết quả thực nghiệm định lượng trên FLIR ADAS v2", "Trang 37"),
        ("  6.2. Kết quả thực nghiệm định lượng trên LLVIP", "Trang 38"),
        ("  6.3. Đối chiếu chỉ số với mục tiêu đồ án đề ra", "Trang 39"),
        ("  6.4. Phân tích trực quan hình ảnh dự đoán thực tế", "Trang 40"),
        ("  6.5. Đánh giá tốc độ suy luận và hiệu năng phần cứng CPU", "Trang 41"),
        ("  6.6. Phân tích so sánh khách quan và giải thích giới hạn dữ liệu", "Trang 42"),
        ("  6.7. Đánh giá ưu điểm, hạn chế và các trường hợp biên", "Trang 43"),
        ("CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "Trang 44"),
        ("  7.1. Các nội dung chính đã hoàn thành", "Trang 44"),
        ("  7.2. Các hạn chế kỹ thuật còn tồn tại", "Trang 45"),
        ("  7.3. Hướng nghiên cứu và phát triển tiếp theo", "Trang 45"),
        ("TÀI LIỆU THAM KHẢO", "Trang 47"),
        ("PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG", "Trang 48"),
    ]

    for title_text, page_num in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        r_title = p_t.add_run(title_text)
        if title_text.startswith("CHƯƠNG") or title_text in ("TÀI LIỆU THAM KHẢO", "PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG"):
            r_title.bold = True
            r_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        
        # Tab leader
        r_dots = p_t.add_run(f" {' .' * (36 - len(title_text)//2)} ")
        r_dots.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        r_p = p_t.add_run(page_num)
        r_p.bold = True

    doc.add_page_break()

    # =========================================================================
    # DANH MUC TU VIET TAT, HINH ANH, BANG BIEU
    # =========================================================================
    p_abb_head = doc.add_paragraph()
    p_abb_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abb_head.paragraph_format.space_before = Pt(10)
    p_abb_head.paragraph_format.space_after = Pt(14)
    r_ah = p_abb_head.add_run("DANH MỤC TỪ VIẾT TẮT")
    r_ah.bold = True
    r_ah.font.size = Pt(15)
    r_ah.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    tbl_abb = doc.add_table(rows=12, cols=3)
    tbl_abb.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_abb)
    
    headers_abb = ["Từ viết tắt", "Tên tiếng Anh đầy đủ", "Ý nghĩa / Giải thích tiếng Việt"]
    for c_idx, h in enumerate(headers_abb):
        c = tbl_abb.rows[0].cells[c_idx]
        set_cell_background(c, "005696")
        set_cell_margins(c, 120, 120, 150, 150)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    abb_data = [
        ("AI", "Artificial Intelligence", "Trí tuệ nhân tạo"),
        ("CV", "Computer Vision", "Thị giác máy tính"),
        ("YOLO", "You Only Look Once", "Mô hình phát hiện đối tượng một giai đoạn thời gian thực"),
        ("LWIR", "Long-Wave Infrared", "Hồng ngoại sóng dài (dải bước sóng 8 – 14 µm)"),
        ("TIR", "Thermal Infrared", "Ảnh nhiệt hồng ngoại"),
        ("IoU", "Intersection over Union", "Chỉ số đo mức độ chồng lấn giữa hai bounding box"),
        ("NMS", "Non-Maximum Suppression", "Kỹ thuật loại bỏ các bounding box bị trùng lặp"),
        ("mAP", "Mean Average Precision", "Độ chính xác trung bình trung bình của mô hình"),
        ("FPS", "Frames Per Second", "Số khung hình xử lý được trong 1 giây (đo tốc độ)"),
        ("COCO", "Common Objects in Context", "Định dạng tập dữ liệu gán nhãn chuẩn quốc tế"),
        ("VOC", "Visual Object Classes", "Định dạng gán nhãn Pascal VOC dạng XML"),
    ]
    for row_idx, row_vals in enumerate(abb_data, 1):
        row = tbl_abb.rows[row_idx]
        for c_idx, val in enumerate(row_vals):
            c = row.cells[c_idx]
            set_cell_margins(c, 80, 80, 120, 120)
            if row_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")
            p = c.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run(val).bold = True
            else:
                p.add_run(val)

    # Danh muc Hinh anh & Bang bieu
    p_fig_head = doc.add_paragraph()
    p_fig_head.paragraph_format.space_before = Pt(24)
    p_fig_head.paragraph_format.space_after = Pt(8)
    r_fh = p_fig_head.add_run("DANH MỤC HÌNH ẢNH")
    r_fh.bold = True
    r_fh.font.size = Pt(13)
    r_fh.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    fig_items = [
        ("Hình 2.1: Phổ bức xạ điện từ và cửa sổ truyền khí quyển dải hồng ngoại sóng dài (LWIR)", "Trang 7"),
        ("Hình 2.2: So sánh nguyên lý tạo ảnh nhiệt bức xạ và ảnh quang học phản xạ ánh sáng", "Trang 8"),
        ("Hình 2.3: Kiến trúc tổng thể mạng học sâu YOLOv8 (Backbone C2f, Neck PAN-FPN, Decoupled Head)", "Trang 10"),
        ("Hình 3.1: Mẫu ảnh nhiệt và phân bố bounding box gán nhãn đối tượng người trong FLIR và LLVIP", "Trang 16"),
        ("Hình 4.1: Tiến trình hội tụ hàm mất mát (Loss) và sự tăng trưởng của mAP@50 qua 50 Epochs", "Trang 25"),
        ("Hình 4.2: Ma trận nhầm lẫn (Confusion Matrix) của mô hình trên tập kiểm định độc lập", "Trang 28"),
        ("Hình 5.1: Giao diện ứng dụng Streamlit Cyber-Thermal Studio và các bảng màu hiển thị", "Trang 32"),
        ("Hình 5.2: Phòng thí nghiệm kiểm thử độ bền vững trước các mức suy thoái nhiệt nhân tạo", "Trang 35"),
        ("Hình 6.1: Kết quả nhận diện đối tượng người thực tế trên bối cảnh ban đêm và đô thị phức tạp", "Trang 40"),
        ("Hình 6.2: Biểu đồ cột đối sánh định lượng các chỉ số Precision, Recall và mAP giữa FLIR và LLVIP", "Trang 41"),
    ]
    for ft, fp in fig_items:
        p_ft = doc.add_paragraph()
        p_ft.paragraph_format.space_before = Pt(1)
        p_ft.paragraph_format.space_after = Pt(2)
        p_ft.add_run(ft)
        p_ft.add_run(f" {' .' * (36 - len(ft)//2)} ").font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        p_ft.add_run(fp).bold = True

    p_tbl_head = doc.add_paragraph()
    p_tbl_head.paragraph_format.space_before = Pt(18)
    p_tbl_head.paragraph_format.space_after = Pt(8)
    r_th = p_tbl_head.add_run("DANH MỤC BẢNG BIỂU")
    r_th.bold = True
    r_th.font.size = Pt(13)
    r_th.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    table_items = [
        ("Bảng 3.1: Thống kê số lượng ảnh, phân chia tập dữ liệu và số lượng bounding box thực tế", "Trang 21"),
        ("Bảng 4.1: Cấu hình môi trường phần cứng và thông số siêu tham số huấn luyện YOLOv8n", "Trang 23"),
        ("Bảng 6.1: Bảng tổng hợp kết quả thực nghiệm định lượng chính thức sau 50 Epochs huấn luyện", "Trang 37"),
        ("Bảng 6.2: Kết quả đo đạc độ trễ suy luận (Latency) và tốc độ khung hình (FPS) trên phần cứng", "Trang 41"),
        ("Bảng 6.3: Kết quả kiểm thử độ bền vững của mô hình trước các dạng nhiễu nhiệt (Robustness)", "Trang 43"),
    ]
    for tt, tp in table_items:
        p_tt = doc.add_paragraph()
        p_tt.paragraph_format.space_before = Pt(1)
        p_tt.paragraph_format.space_after = Pt(2)
        p_tt.add_run(tt)
        p_tt.add_run(f" {' .' * (36 - len(tt)//2)} ").font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        p_tt.add_run(tp).bold = True

    doc.add_page_break()

    # Helper them heading co styling chuan
    def add_chapter_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(15.5)
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def add_section_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(13.5)
        r.font.color.rgb = RGBColor(0x00, 0x56, 0x96)
        return p

    def add_sub_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.italic = True
        r.font.size = Pt(12.5)
        r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_body(text):
        p = doc.add_paragraph(text)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.35
        return p

    def add_bullet(text):
        p = doc.add_paragraph(text, style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.3
        return p

    def add_figure_image(img_path, caption_text, width_cm=14.5):
        if img_path.exists():
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.paragraph_format.keep_with_next = True
            p_img.add_run().add_picture(str(img_path), width=Cm(width_cm))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            r = p_cap.add_run(caption_text)
            r.italic = True
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # =========================================================================
    # CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI
    # =========================================================================
    add_chapter_title("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI")

    add_section_title("1.1. Lý do chọn đề tài và tính cấp thiết")
    add_body(
        "Trong kỷ nguyên bùng nổ của Trí tuệ Nhân tạo (AI) và Thị giác máy tính (Computer Vision), bài toán phát hiện người đi bộ "
        "(Pedestrian Detection) giữ vai trò then chốt trong hàng loạt ứng dụng trọng yếu của đời sống: từ hệ thống xe tự hành (Autonomous Vehicles), "
        "hệ thống hỗ trợ lái xe nâng cao (ADAS), đến giám sát an ninh công cộng, cứu hộ cứu nạn trong hỏa hoạn và kiểm soát biên giới ban đêm."
    )
    add_body(
        "Tuy nhiên, đại đa số các hệ thống thị giác hiện nay dựa trên camera quang học truyền thống sử dụng cảm biến RGB. "
        "Camera quang học hoạt động theo nguyên lý thụ động thu nhận ánh sáng khả kiến phản xạ từ bề mặt vật thể. Khi môi trường rơi vào điều kiện "
        "thiếu sáng cực đoan (đêm tối hoàn toàn 0 Lux), ngược sáng chói lóa từ đèn pha xe đối diện, hoặc thời tiết khắc nghiệt như sương mù dày, "
        "mưa dông và khói lửa, tín hiệu quang học bị triệt tiêu hoặc tán xạ nghiêm trọng, khiến các thuật toán học sâu tối tân nhất trên ảnh RGB "
        "hoàn toàn mất khả năng nhận diện."
    )
    add_body(
        "Để giải quyết triệt để rào cản vật lý đó, công nghệ cảm biến nhiệt hồng ngoại (Thermal Infrared Imaging) — cụ thể là dải sóng dài LWIR "
        "(Long-Wave Infrared, 8–14 µm) — nổi lên như một giải pháp cứu cánh tối ưu. Mọi vật thể có nhiệt độ trên độ không tuyệt đối (-273.15°C) "
        "đều liên tục phát xạ sóng điện từ. Cơ thể con người luôn duy trì thân nhiệt nội tại ổn định (36.5°C – 37.5°C), tạo nên một nguồn phát xạ nhiệt "
        "liên tục và tương phản rất rõ rệt so với nền môi trường xung quanh. Camera nhiệt thu nhận trực tiếp bức xạ nhiệt này mà không phụ thuộc "
        "vào bất kỳ nguồn chiếu sáng nhân tạo nào."
    )

    add_section_title("1.2. Mục tiêu nghiên cứu của đề tài")
    add_body(
        "Mục tiêu tổng quát của đề tài là: Nghiên cứu, xây dựng và hoàn thiện một hệ thống phần mềm hoàn chỉnh ứng dụng mô hình học sâu hiện đại YOLOv8 "
        "nhằm phát hiện và định vị chính xác người đi bộ trong ảnh nhiệt hồng ngoại thời gian thực, phục vụ giám sát ban đêm và giao thông thông minh."
    )
    add_body("Các mục tiêu cụ thể cần đạt được bao gồm:")
    add_bullet("1. Khảo sát, thu thập và xây dựng pipeline tiền xử lý tự động cho hai bộ dữ liệu ảnh nhiệt chuẩn quốc tế: FLIR ADAS v2 và LLVIP.")
    add_bullet("2. Chuyển đổi định dạng gán nhãn phức tạp (COCO JSON và Pascal VOC XML) sang định dạng chuẩn hóa của mạng YOLO, hợp nhất lớp đối tượng 'person'.")
    add_bullet("3. Thiết lập môi trường huấn luyện, fine-tuning mô hình YOLOv8n (Nano) qua 50 epochs, tối ưu hóa hàm mất mát và phân tích đường cong hội tụ.")
    add_bullet("4. Đánh giá định lượng toàn diện mô hình dựa trên hệ thống chỉ số: Precision, Recall, mAP@50, mAP@50-95 và tốc độ xử lý FPS.")
    add_bullet("5. Kiểm thử độ bền vững (Robustness) của mô hình trước các dạng suy thoái cảm biến thực tế như nhiễu Gaussian, điểm ảnh chết, làm mờ và giảm tương phản.")
    add_bullet("6. Xây dựng ứng dụng Web Demo (Streamlit Cyber-Thermal Studio) trực quan, cho phép người dùng kiểm thử tức thì và so sánh đối chiếu hai mô hình.")

    add_section_title("1.3. Đối tượng và phạm vi nghiên cứu")
    add_bullet("Đối tượng nghiên cứu: Bức xạ nhiệt hồng ngoại sóng dài LWIR; đặc trưng hình thái thân nhiệt người đi bộ; kiến trúc mạng nơ-ron học sâu YOLOv8.")
    add_bullet("Phạm vi nghiên cứu: Dữ liệu ảnh nhiệt đơn sắc thu nhận từ camera vi bức xạ kế (microbolometer) trong hai bối cảnh thực tế: giao thông đường phố đô thị di động (FLIR ADAS v2) và camera giám sát an ninh cố định ban đêm (LLVIP).")

    add_section_title("1.4. Phương pháp nghiên cứu và thực hiện")
    add_body(
        "Đề tài áp dụng phương pháp nghiên cứu thực nghiệm kết hợp đối sánh lý thuyết. Quy trình triển khai bao gồm: "
        "(1) Nghiên cứu cơ sở lý thuyết vật lý nhiệt và kiến trúc mạng học sâu; "
        "(2) Thiết kế pipeline xử lý dữ liệu và chuyển đổi nhãn; "
        "(3) Huấn luyện mô hình trên môi trường phần cứng kiểm soát; "
        "(4) Đo đạc và đánh giá độc lập các chỉ số mAP và FPS; "
        "(5) Đóng gói và triển khai ứng dụng phần mềm hướng người dùng."
    )

    add_section_title("1.5. Cấu trúc tổng thể của báo cáo")
    add_body("Báo cáo đồ án được kết cấu chặt chẽ thành 7 chương nội dung chuyên sâu:")
    add_bullet("Chương 1: Giới thiệu đề tài — Tính cấp thiết, mục tiêu, đối tượng, phạm vi và phương pháp thực hiện.")
    add_bullet("Chương 2: Cơ sở lý thuyết — Bản chất vật lý ảnh nhiệt, so sánh ảnh nhiệt thật vs RGB giả màu, kiến trúc YOLOv8 và các độ đo đánh giá.")
    add_bullet("Chương 3: Dữ liệu và tiền xử lý — Khảo sát tập dữ liệu FLIR v2, LLVIP, quy trình phân tích cú pháp nhãn COCO/VOC sang chuẩn YOLO.")
    add_bullet("Chương 4: Huấn luyện mô hình — Thiết lập siêu tham số, phân tích diễn biến hàm mất mát và trích xuất kết quả 50 epochs thực tế.")
    add_bullet("Chương 5: Xây dựng ứng dụng — Phân tích chi tiết app.py, cơ chế nạp model, phân tách ảnh suy luận vs ảnh hiển thị, phòng thí nghiệm nhiễu và run_app.bat.")
    add_bullet("Chương 6: Thực nghiệm và đánh giá — Bảng số liệu nghiệm thu chính thức, so sánh FLIR vs LLVIP, phân tích hình ảnh và benchmark FPS.")
    add_bullet("Chương 7: Kết luận và hướng phát triển — Tổng kết thành tựu, các điểm hạn chế kỹ thuật và hướng mở rộng trong tương lai.")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN CÔNG NGHỆ
    # =========================================================================
    add_chapter_title("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN CÔNG NGHỆ")

    add_section_title("2.1. Tổng quan Thị giác máy tính và bài toán Phát hiện đối tượng")
    add_body(
        "Thị giác máy tính (Computer Vision) là nhánh khoa học liên ngành thuộc Trí tuệ Nhân tạo, tập trung nghiên cứu phương pháp giúp máy tính "
        "thu nhận, xử lý, phân tích và thấu hiểu thông tin từ hình ảnh hoặc video kỹ thuật số. Trong đó, Phát hiện đối tượng (Object Detection) "
        "là bài toán kinh điển và phức tạp bậc nhất, đòi hỏi mô hình phải giải quyết đồng thời hai nhiệm vụ: Định vị (Localization - xác định tọa độ "
        "hộp bao Bounding Box) và Phân loại (Classification - gán nhãn định danh cho đối tượng bên trong hộp bao)."
    )

    add_section_title("2.2. Bản chất vật lý của ảnh nhiệt hồng ngoại (Thermal LWIR)")
    add_body(
        "Quang phổ điện từ trải dài qua nhiều dải bước sóng khác nhau. Ánh sáng khả kiến mà mắt người có thể cảm nhận chỉ chiếm một dải hẹp từ 0.38 µm đến 0.75 µm. "
        "Phía trên dải khả kiến là vùng bức xạ hồng ngoại (Infrared), được chia thành 4 dải quang học chính:"
    )
    add_bullet("Hồng ngoại gần (NIR: 0.75 – 1.4 µm): Thường dùng trong camera an ninh có đèn hồng ngoại LED trợ sáng.")
    add_bullet("Hồng ngoại sóng ngắn (SWIR: 1.4 – 3.0 µm): Ứng dụng trong kiểm định vật liệu và nông nghiệp công nghệ cao.")
    add_bullet("Hồng ngoại sóng trung (MWIR: 3.0 – 5.0 µm): Ứng dụng trong quân sự, phát hiện động cơ tên lửa và máy bay.")
    add_bullet("Hồng ngoại sóng dài (LWIR: 8.0 – 14.0 µm): Dải bước sóng phát xạ tự nhiên mạnh nhất của các vật thể ở nhiệt độ môi trường và thân nhiệt con người.")

    add_body(
        "Theo định luật dịch chuyển Wien (Wien's Displacement Law), bước sóng phát xạ cực đại λ_max của một vật đen tỷ lệ nghịch với nhiệt độ tuyệt đối T (Kelvin) của vật đó:\n"
        "λ_max = b / T     (với hằng số Wien b ≈ 2897.8 µm·K)"
    )
    add_body(
        "Với cơ thể con người có nhiệt độ da dao động trong khoảng 32°C đến 37°C (tương đương 305 – 310 Kelvin), bước sóng phát xạ cực đại tập trung chính xác tại:\n"
        "λ_max = 2897.8 / 310 ≈ 9.35 µm"
    )
    add_body(
        "Bước sóng 9.35 µm nằm trọn vẹn trong 'cửa sổ truyền khí quyển' của dải LWIR (8–14 µm) — nơi các phân tử khí quyển (CO2, H2O) hầu như không hấp thụ bức xạ. "
        "Nhờ đó, camera nhiệt LWIR trang bị cảm biến vi bức xạ kế không làm lạnh (Uncooled Microbolometer) có thể ghi nhận thân nhiệt người ở cự ly xa hàng trăm mét "
        "mà không bị suy hao bởi sương mù mỏng hay bóng đêm hoàn toàn."
    )

    add_section_title("2.3. Phân biệt ảnh nhiệt thật và ảnh RGB chuyển xám / giả màu")
    add_body(
        "Một trong những nguyên tắc cốt lõi cần làm rõ trong nghiên cứu thị giác máy tính nhiệt là sự khác biệt bản chất giữa ảnh nhiệt thực tế và ảnh quang học:"
    )
    add_bullet("Ảnh quang học RGB chuyển Grayscale: Chỉ phản ánh thang độ sáng quang học (Luminance) do phản xạ ánh sáng mặt trời hoặc đèn điện. Giá trị điểm ảnh là kết quả của tích chập phổ ánh sáng với độ phản xạ bề mặt. Khi tắt đèn, giá trị điểm ảnh triệt tiêu về 0. Chuyển ảnh RGB sang Grayscale hoàn toàn KHÔNG tạo ra thông tin hồng ngoại.")
    add_bullet("Ảnh nhiệt đơn sắc thực tế (Monochrome LWIR): Mỗi điểm ảnh ghi lại mật độ thông lượng bức xạ nhiệt (Radiative Flux Density) phát ra từ chính vật thể. Dù trong bóng đêm 0 Lux, người đi bộ vẫn phát sáng rực rỡ do chênh lệch nhiệt độ với mặt đường.")
    add_bullet("Ảnh giả màu (False-Color Palettes): Để mắt người dễ quan sát gradient thân nhiệt, người ta sử dụng các bảng tra màu (Color Look-Up Tables - LUT) như Inferno, Ironbow, Jet. Cần đặc biệt lưu ý: Các màu sắc này là ánh xạ nhân tạo thuần túy để hiển thị (Display Only); mạng nơ-ron YOLO khi suy luận cần được nạp ảnh xám chuẩn hóa để phản ánh đúng phân phối vật lý.")

    add_section_title("2.4. Họ mô hình YOLO và kiến trúc mạng học sâu YOLOv8")
    add_body(
        "YOLO (You Only Look Once) do Joseph Redmon khởi xướng là bước đột phá cách mạng trong lĩnh vực Object Detection, chuyển bài toán phát hiện từ "
        "cơ chế hai giai đoạn (Two-Stage như Faster R-CNN) sang mô hình một giai đoạn (One-Stage) hồi quy trực tiếp nhãn và tọa độ từ ảnh đầu vào chỉ trong một lượt truyền thẳng."
    )
    add_body(
        "Trong đề tài này, chúng em lựa chọn phiên bản YOLOv8n (Nano) được phát triển bởi Ultralytics vào năm 2023. Kiến trúc YOLOv8 bao gồm 3 khối thành phần chủ đạo:"
    )
    add_bullet("Backbone (CSPDarknet với Module C2f): Module C2f (Cross Stage Partial with 2 Convolutions) thay thế cho module C3 cũ, tăng cường số lượng đường truyền tắt (shortcut connections) và nhánh gradient, cho phép trích xuất đặc trưng hình thái thân nhiệt sâu sắc mà vẫn giữ số lượng tham số cực thấp (~3.2 triệu).")
    add_bullet("Neck (PAN-FPN cải tiến): Kết hợp cấu trúc Kim tự tháp đặc trưng (FPN) từ trên xuống và Kim tự tháp tập hợp đường dẫn (PAN) từ dưới lên, giúp dung hợp đặc trưng ngữ nghĩa mức cao với đặc trưng vị trí mức thấp, tối ưu khả năng phát hiện người ở cả cự ly gần lẫn rất xa.")
    add_bullet("Head (Decoupled Anchor-Free Head): Khác với YOLOv5 sử dụng Anchor Box cố định, YOLOv8 tách rời hoàn toàn nhánh phân loại lớp (Classification Branch) và nhánh hồi quy tọa độ (Regression Branch), đồng thời dự đoán trực tiếp khoảng cách từ tâm đến các cạnh hộp bao (Anchor-Free), loại bỏ hoàn toàn các siêu tham số mỏ neo nhân tạo.")

    # Chen hinh kien truc
    arch_img = ASSETS_DIR / "pptx_image7_architecture.png"
    if arch_img.exists():
        add_figure_image(arch_img, "Hình 2.1: Kiến trúc tổng thể hệ thống mạng học sâu YOLOv8 (Backbone C2f, Neck PAN-FPN, Decoupled Head)")

    add_section_title("2.5. Các khái niệm cốt lõi: Bounding Box, IoU và NMS")
    add_body(
        "Bounding Box được biểu diễn dưới dạng hình chữ nhật bao quanh đối tượng. Trong định dạng chuẩn YOLO, tọa độ được chuẩn hóa về đoạn [0, 1]:\n"
        "• x_center = X_tâm / W_ảnh ; y_center = Y_tâm / H_ảnh\n"
        "• width = Chiều rộng / W_ảnh ; height = Chiều cao / H_ảnh"
    )
    add_body(
        "Chỉ số IoU (Intersection over Union) đo mức độ trùng khớp giữa hộp dự đoán (B_pred) và hộp nhãn thực tế (B_gt):\n"
        "IoU = Diện tích(B_pred ∩ B_gt) / Diện tích(B_pred ∪ B_gt)"
    )
    add_body(
        "Thuật toán NMS (Non-Maximum Suppression): Trong quá trình suy luận, mạng YOLO tạo ra hàng nghìn hộp bao ứng viên cho cùng một người. "
        "NMS thực hiện sắp xếp các hộp theo Confidence giảm dần, giữ lại hộp có điểm số cao nhất và loại bỏ các hộp lân cận có IoU vượt quá ngưỡng (IoU threshold = 0.45)."
    )

    add_section_title("2.6. Hệ thống các chỉ số đánh giá: Precision, Recall và mAP")
    add_bullet("Precision (Độ chính xác): Tỷ lệ số đối tượng nhận diện đúng trên tổng số đối tượng mà mô hình dự đoán là người: Precision = TP / (TP + FP).")
    add_bullet("Recall (Độ bao phủ / Độ nhạy): Tỷ lệ số người phát hiện được trên tổng số người thực tế có trong ảnh: Recall = TP / (TP + FN).")
    add_bullet("mAP@50 (Mean Average Precision tại IoU=0.50): Diện tích dưới đường cong Precision-Recall khi ngưỡng IoU được cố định tại 0.50. Đây là độ đo tiêu chuẩn phản ánh độ nhạy phát hiện người.")
    add_bullet("mAP@50-95: Trung bình cộng mAP tính trên 10 ngưỡng IoU từ 0.50 đến 0.95 với bước nhảy 0.05, phản ánh độ chính xác định vị tọa độ viền hộp bao.")
    add_bullet("FPS (Frames Per Second): Tốc độ xử lý số khung hình trên giây. Cần phân biệt rõ: Model Latency (độ trễ riêng của mạng YOLO) và End-to-End Latency (tổng thời gian tiền xử lý, suy luận, vẽ khung và hiển thị).")

    add_section_title("2.7. Nền tảng Streamlit trong triển khai ứng dụng thị giác máy tính")
    add_body(
        "Streamlit là framework mã nguồn mở hiện đại dựa trên Python, cho phép xây dựng ứng dụng Web tương tác dữ liệu cao cấp mà không cần "
        "phải viết mã HTML/CSS/JavaScript phức tạp. Điểm mạnh vượt trội của Streamlit là khả năng tích hợp trực tiếp với OpenCV, PyTorch và PIL, "
        "hỗ trợ cơ chế Session State Caching giúp lưu trữ tạm thời kết quả suy luận, loại bỏ hoàn toàn các lượt chạy trùng lặp khi người dùng tương tác."
    )

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 3: DỮ LIỆU VÀ QUY TRÌNH TIỀN XỬ LÝ
    # =========================================================================
    add_chapter_title("CHƯƠNG 3: DỮ LIỆU VÀ QUY TRÌNH TIỀN XỬ LÝ")

    add_section_title("3.1. Tổng quan hai bộ dữ liệu FLIR ADAS v2 và LLVIP")
    add_body(
        "Để đảm bảo tính khách quan khoa học và khả năng bao quát thực tế, đề tài tiến hành thực nghiệm trên hai bộ dữ liệu ảnh nhiệt "
        "chuẩn benchmark quốc tế có quy mô lớn bậc nhất hiện nay:"
    )
    add_bullet("1. FLIR ADAS v2 (Teledyne FLIR): Được thu thập từ camera nhiệt chuyên dụng FLIR Tau 2 (độ phân giải 640×512, dải LWIR 7.5–13.5 µm) gắn trên xe ô tô thử nghiệm di chuyển trên các tuyến phố tại Santa Barbara (California, Mỹ). Dữ liệu mang đặc trưng của bài toán giao thông đô thị phức tạp: camera rung lắc, góc nhìn di động, người đi bộ xuất hiện ở nhiều khoảng cách và góc độ khác nhau cùng nhiều nguồn nhiệt giao thông gây nhiễu (ống xả xe, bóng đèn đường).")
    add_bullet("2. LLVIP (Low-Light Visible-Infrared Pedestrians): Bộ dữ liệu giám sát an ninh người đi bộ ban đêm độ phân giải cao (1280×1024), thu thập từ các camera cảm biến nhiệt gắn cố định góc cao tại các tuyến phố đi bộ và ngõ hẻm đô thị. Độ tương phản thân nhiệt trong LLVIP cực kỳ sắc nét do nền ban đêm lạnh và góc nhìn không đổi.")

    add_section_title("3.2. Cấu trúc dữ liệu gốc và định dạng nhãn COCO / Pascal VOC")
    add_body(
        "Hai bộ dữ liệu có định dạng lưu trữ hoàn toàn khác biệt nhau, đòi hỏi phải xây dựng các bộ phân tích cú pháp (parsers) chuyên biệt:\n"
        "• FLIR ADAS v2 lưu trữ nhãn dưới dạng COCO JSON (`coco.json`), trong đó bounding box được định nghĩa theo cấu trúc tuyệt đối [x_min, y_min, width, height].\n"
        "• LLVIP lưu trữ mỗi ảnh kèm một file XML chuẩn Pascal VOC, định nghĩa tọa độ viền hộp bao dưới dạng 4 điểm góc [xmin, ymin, xmax, ymax]."
    )

    add_section_title("3.3. Thuật toán chuyển đổi chuẩn hóa tọa độ sang YOLO")
    add_body(
        "Mô hình YOLOv8 yêu cầu file nhãn văn bản (.txt) tương ứng với mỗi file ảnh, trong đó mỗi dòng biểu diễn một đối tượng theo công thức:\n"
        "<class_id> <x_center> <y_center> <width> <height>\n"
        "Thuật toán chuyển đổi đã thực hiện cắt xén (clipping) tọa độ trong biên ảnh để loại bỏ các hộp gán lỗi tràn viền:"
    )
    add_body(
        "x1 = max(0, min(W, x_min)) ; y1 = max(0, min(H, y_min))\n"
        "x2 = max(0, min(W, x_min + width)) ; y2 = max(0, min(H, y_min + height))\n"
        "x_center = (x1 + x2) / (2 * W) ; y_center = (y1 + y2) / (2 * H)\n"
        "box_w = (x2 - x1) / W ; box_h = (y2 - y1) / H"
    )

    add_section_title("3.4. Chuẩn hóa phân loại đối tượng người (Class Person)")
    add_body(
        "Bộ dữ liệu FLIR ADAS v2 nguyên bản chứa nhiều lớp đối tượng giao thông: person, car, bicycle, dog,... "
        "Trong phạm vi đề tài tập trung chuyên sâu vào bảo vệ an toàn cho con người, module tiền xử lý (`prepare_yolo.py`) đã thiết lập bộ lọc động, "
        "chỉ trích xuất duy nhất các nhãn có category_name là 'person', chuẩn hóa toàn bộ về class_id = 0. "
        "Đối với tập LLVIP vốn chuyên biệt cho người đi bộ, toàn bộ các thẻ `<name>person</name>` cũng được hợp nhất về class_id = 0."
    )

    add_section_title("3.5. Phân chia tập dữ liệu huấn luyện, kiểm định và kiểm thử")
    add_body(
        "Để đảm bảo kết quả đánh giá hoàn toàn khách quan và ngăn chặn hiện tượng rò rỉ dữ liệu (data leakage):\n"
        "• Đối với FLIR ADAS v2: Tuân thủ chặt chẽ phân chia chính thức của Teledyne FLIR thành tập Train (21.484 ảnh) và tập Validation (2.288 ảnh).\n"
        "• Đối với LLVIP: Giữ nguyên vẹn tập Test chính thức gồm 3.463 ảnh phục vụ đánh giá độc lập; tập Train (12.025 ảnh) được chia ngẫu nhiên với seed=42 thành 90% cho huấn luyện và 10% cho kiểm định nội bộ."
    )

    add_section_title("3.6. Thống kê chi tiết số lượng ảnh và bounding box thực tế")
    add_body("Bảng 3.1 tổng hợp thông số số lượng ảnh và số hộp gán nhãn thực tế sau khi hoàn tất quy trình tiền xử lý chuẩn hóa:")

    tbl_ds = doc.add_table(rows=5, cols=6)
    tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ds)
    ds_headers = ["Bộ dữ liệu", "Độ phân giải", "Tập Train", "Tập Val / Test", "Định dạng gốc", "Đặc trưng bối cảnh"]
    for c_idx, h in enumerate(ds_headers):
        c = tbl_ds.rows[0].cells[c_idx]
        set_cell_background(c, "005696")
        set_cell_margins(c, 100, 100, 100, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ds_rows = [
        ("FLIR ADAS v2", "640 × 512 (LWIR)", "21.484 ảnh", "2.288 ảnh (Val)", "COCO JSON", "Giao thông đô thị, camera xe ô tô di động"),
        ("LLVIP Infrared", "1280 × 1024 (LWIR)", "10.823 ảnh", "3.463 ảnh (Test)", "Pascal VOC XML", "Giám sát an ninh ban đêm, camera cố định"),
        ("LLVIP Val (Nội bộ)", "1280 × 1024 (LWIR)", "—", "1.202 ảnh (Val)", "Pascal VOC XML", "Kiểm tra hội tụ trong huấn luyện"),
        ("TỔNG CỘNG", "Ảnh nhiệt chuyên dụng", "32.307 ảnh", "6.953 ảnh", "Chuẩn hóa YOLO", "Đa dạng cự ly, thời tiết và bối cảnh"),
    ]
    for row_idx, r_data in enumerate(ds_rows, 1):
        row = tbl_ds.rows[row_idx]
        for c_idx, val in enumerate(r_data):
            c = row.cells[c_idx]
            set_cell_margins(c, 70, 70, 90, 90)
            if row_idx == 4:
                set_cell_background(c, "E2E8F0")
            elif row_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")
            p = c.paragraphs[0]
            if c_idx in (0, 2, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                if row_idx == 4 or c_idx == 0:
                    r.bold = True
            else:
                r = p.add_run(val)
                if row_idx == 4:
                    r.bold = True

    p_cap_ds = doc.add_paragraph()
    p_cap_ds.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_ds.paragraph_format.space_before = Pt(4)
    p_cap_ds.paragraph_format.space_after = Pt(12)
    p_cap_ds.add_run("Bảng 3.1: Thống kê quy mô hai bộ dữ liệu thực nghiệm sau khi chuẩn hóa").italic = True

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 4: HUẤN LUYỆN MÔ HÌNH
    # =========================================================================
    add_chapter_title("CHƯƠNG 4: HUẤN LUYỆN MÔ HÌNH")

    add_section_title("4.1. Môi trường phần cứng và cấu hình phần mềm")
    add_body(
        "Quá trình nghiên cứu và thực nghiệm huấn luyện được thực hiện trong môi trường kiểm soát nghiêm ngặt:\n"
        "• Hệ điều hành: Windows 11 64-bit.\n"
        "• Môi trường lập trình: Python 3.14.8 trong môi trường ảo (.venv) độc lập.\n"
        "• Framework học sâu: PyTorch 2.14.1 kết hợp Ultralytics YOLOv8 phiên bản 8.4.183.\n"
        "• Phần cứng huấn luyện cục bộ: CPU Intel đa lõi; hỗ trợ huấn luyện phân tán và GPU trên môi trường Google Colab / CUDA."
    )

    add_section_title("4.2. Thiết lập siêu tham số huấn luyện (Hyperparameters)")
    add_body("Bảng 4.1 tổng hợp chi tiết các siêu tham số huấn luyện được cấu hình thông qua `train_yolo.py`:")

    tbl_hp = doc.add_table(rows=9, cols=3)
    tbl_hp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hp)
    hp_headers = ["Siêu tham số (Hyperparameter)", "Giá trị thiết lập", "Giải thích ý nghĩa kỹ thuật"]
    for c_idx, h in enumerate(hp_headers):
        c = tbl_hp.rows[0].cells[c_idx]
        set_cell_background(c, "005696")
        set_cell_margins(c, 100, 100, 100, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    hp_rows = [
        ("Mô hình cơ sở (Base Model)", "YOLOv8n (Nano)", "Phiên bản gọn nhẹ, tốc độ cao, kích thước trọng số < 7 MB"),
        ("Trọng số khởi tạo (Pretrained)", "yolov8n.pt (COCO)", "Kế thừa đặc trưng trích xuất cạnh và hình học cơ bản"),
        ("Kích thước ảnh nạp (imgsz)", "416 × 416 pixels", "Cân bằng tối ưu giữa chi phí tính toán CPU và chi tiết đối tượng"),
        ("Số Epochs tối đa", "50 Epochs", "Đảm bảo mạng hội tụ hoàn toàn mà không bị Overfitting"),
        ("Kích thước Batch (Batch Size)", "4 / 16", "Phù hợp với giới hạn bộ nhớ đệm RAM và GPU"),
        ("Thuật toán tối ưu (Optimizer)", "AdamW / MuSGD", "Tốc độ hội tụ nhanh, kiểm soát suy giảm trọng số weight_decay=0.0005"),
        ("Tốc độ học khởi tạo (lr0)", "0.002 (AdamW) / 0.01", "Học sâu ổn định, kết hợp lịch trình Cosine Annealing"),
        ("Tăng cường dữ liệu (Augmentation)", "Mosaic=1.0, Flip=0.5", "Ghép ngẫu nhiên 4 ảnh nhiệt, mô phỏng mật độ người đa dạng"),
    ]
    for row_idx, r_data in enumerate(hp_rows, 1):
        row = tbl_hp.rows[row_idx]
        for c_idx, val in enumerate(r_data):
            c = row.cells[c_idx]
            set_cell_margins(c, 70, 70, 90, 90)
            if row_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")
            p = c.paragraphs[0]
            if c_idx in (0, 1):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
                p.add_run(val).bold = (c_idx == 0)
            else:
                p.add_run(val)

    p_cap_hp = doc.add_paragraph()
    p_cap_hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_hp.paragraph_format.space_before = Pt(4)
    p_cap_hp.paragraph_format.space_after = Pt(12)
    p_cap_hp.add_run("Bảng 4.1: Danh mục siêu tham số huấn luyện mô hình YOLOv8n trên ảnh nhiệt").italic = True

    add_section_title("4.3. Quá trình huấn luyện trên bộ dữ liệu FLIR ADAS v2")
    add_body(
        "Mô hình YOLOv8n được huấn luyện trong suốt 50 epochs trên tập FLIR ADAS v2. "
        "Diễn biến huấn luyện ghi nhận sự suy giảm mạnh mẽ của các hàm mất mát:\n"
        "• Train Box Loss giảm đều đặn từ mức 2.15 ở epoch đầu xuống 1.585 ở epoch 50.\n"
        "• Train Class Loss giảm mạnh từ 1.84 xuống 0.835, chứng tỏ mạng phân biệt rất tốt giữa người và các nguồn nhiệt nền.\n"
        "• Train DFL Loss ổn định ở mức 0.879."
    )

    tc_img = ASSETS_DIR / "training_curves.png"
    if tc_img.exists():
        add_figure_image(tc_img, "Hình 4.1: Đường cong suy giảm hàm mất mát (Loss) và tăng trưởng chỉ số mAP qua 50 Epochs huấn luyện FLIR")

    add_section_title("4.4. Quá trình huấn luyện trên bộ dữ liệu LLVIP")
    add_body(
        "Do bộ dữ liệu LLVIP có góc quan sát cố định và độ tương phản nhiệt cực lớn, mô hình hội tụ với tốc độ vượt bậc. "
        "Chỉ sau 25 epochs đầu, chỉ số mAP@50 đã vượt ngưỡng 90%. Đến epoch 50, mô hình đạt trạng thái tối ưu hóa sâu sắc với mAP@50 đạt 98.30% "
        "và mAP@50-95 đạt 68.04%."
    )

    add_section_title("4.5. Chiến lược lưu trữ Checkpoints và Early Stopping")
    add_body(
        "Hệ thống thiết lập cơ chế tự động theo dõi `val/fitness` (kết hợp tuyến tính giữa mAP50 và mAP50-95). "
        "Mỗi khi mô hình đạt đỉnh cao mới về độ chính xác, trọng số được tự động lưu đè vào file `best.pt`. "
        "Đồng thời, file `last.pt` được lưu định kỳ sau mỗi epoch nhằm bảo đảm khả năng phục hồi huấn luyện (Resume Training) "
        "nếu xảy ra sự cố ngắt nguồn điện đột ngột."
    )

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 5: XÂY DỰNG ỨNG DỤNG (THERMAL VISION STUDIO)
    # =========================================================================
    add_chapter_title("CHƯƠNG 5: XÂY DỰNG ỨNG DỤNG (THERMAL VISION STUDIO)")

    add_section_title("5.1. Kiến trúc hệ thống tổng thể và luồng dữ liệu")
    add_body(
        "Hệ thống phần mềm được thiết kế theo kiến trúc module hóa hướng người dùng. Toàn bộ quy trình từ tiếp nhận ảnh nhiệt, "
        "chuẩn hóa tiền xử lý, nạp mô hình suy luận, vẽ khung bounding box đến xuất báo cáo kết quả đều được gói gọn trong một giao diện web duy nhất."
    )

    add_section_title("5.2. Phân tích mã nguồn app.py và tối ưu hóa hiệu năng")
    add_body(
        "File `app.py` là trung tâm điều khiển của hệ thống, được thiết kế với hơn 600 dòng mã Python tiêu chuẩn cao:\n"
        "• Nạp mô hình an toàn (`load_yolo_model`): Sử dụng `@st.cache_resource` để chỉ nạp trọng số mạng YOLO vào bộ nhớ RAM đúng một lần duy nhất, triệt tiêu thời gian trễ nạp model giữa các lượt người dùng thao tác.\n"
        "• Bộ đệm suy luận (`Session State Caching`): Tính toán mã băm SHA-256 trên mảng byte của ảnh kết hợp các giá trị thanh trượt `(conf, iou, imgsz, colormap)`. Nhờ đó, nếu người dùng không thay đổi tham số, hệ thống sẽ trả kết quả tức thì mà không gọi lại mạng YOLO."
    )

    add_section_title("5.3. Tiền xử lý ảnh và cơ chế phân tách ảnh suy luận vs ảnh hiển thị")
    add_body(
        "Đây là điểm đột phá kỹ thuật nổi bật của đồ án nhằm đảm bảo cả tính khoa học lẫn trải nghiệm thị giác người dùng:\n"
        "1. Xử lý ảnh đầu vào: Kiểm tra mức chênh lệch giữa các kênh màu (R, G, B). Nếu phát hiện ảnh màu, hệ thống tự động trích xuất kênh xám 3 kênh nạp vào YOLO. Nếu là ảnh quang học thông thường, hệ thống xuất cảnh báo nhắc nhở người dùng về giới hạn vật lý.\n"
        "2. Phân tách hoàn toàn giữa Ảnh suy luận vs Ảnh hiển thị: Mạng YOLO luôn luôn nhận ảnh grayscale đơn sắc chuẩn hóa miền nhiệt. Các bảng màu như Inferno, Jet, Turbo, Bone chỉ được áp dụng lên ảnh nền hiển thị (Display Only) để người vận hành quan sát gradient nhiệt độ rõ ràng nhất."
    )

    cm_img = ASSETS_DIR / "slide_colormap_showcase.png"
    if cm_img.exists():
        add_figure_image(cm_img, "Hình 5.1: Giao diện ứng dụng Streamlit và các bảng màu hiển thị thân nhiệt chuyên dụng (Inferno, Ironbow, Jet, Bone)")

    add_section_title("5.4. Chế độ đối sánh song song hai mô hình (Dual Comparison)")
    add_body(
        "Hệ thống cung cấp tùy chọn 'So sánh cả hai mô hình (FLIR + LLVIP)'. Khi kích hoạt, trên giao diện sẽ chia thành hai cột độc lập. "
        "Mỗi mô hình thực hiện suy luận riêng rẽ trên cùng một bức ảnh, hiển thị bounding box, độ trễ và số lượng người phát hiện cạnh nhau, "
        "giúp người dùng dễ dàng so sánh điểm mạnh của từng mô hình trên các bối cảnh khác nhau."
    )

    add_section_title("5.5. Phòng thí nghiệm kiểm thử độ bền vững (Robustness Lab)")
    add_body(
        "Tích hợp tại Tab 2 của ứng dụng, phòng thí nghiệm này cho phép mô phỏng 5 dạng suy thoái cảm biến và điều kiện thời tiết khắc nghiệt:\n"
        "• Nhiễu cảm biến nhiệt Gaussian: Mô phỏng độ phân giải nhiệt độ tương đương (NETD) của cảm biến vi bức xạ kế giá rẻ.\n"
        "• Nhiễu điểm ảnh chết (Salt & Pepper): Mô phỏng các phần tử bolometer bị hỏng hoặc mất tín hiệu (đã được bọc lót mã nguồn an toàn chống lỗi ảnh nhỏ).\n"
        "• Mờ quang học & Rung lắc: Mô phỏng camera bị lệch tiêu cự hoặc xe rung lắc mạnh.\n"
        "• Suy giảm tương phản nhiệt: Mô phỏng sương mù dày, mưa dông làm mát mặt đường đột ngột.\n"
        "• Dịch chuyển bức xạ nhiệt: Mô phỏng sự thay đổi nhiệt độ môi trường xung quanh."
    )

    add_section_title("5.6. Tự động hóa vận hành trên Windows qua run_app.bat")
    add_body(
        "Để hỗ trợ người dùng và hội đồng chấm điểm khởi chạy nhanh chóng mà không cần gõ lệnh phức tạp, đồ án đã tạo file script `run_app.bat`. "
        "File này tự động chuyển đường dẫn làm việc, kích hoạt môi trường ảo `.venv`, kiểm tra sự tồn tại của thư viện Streamlit và nạp ứng dụng. "
        "Nếu phát sinh lỗi môi trường, cửa sổ terminal sẽ được giữ nguyên trạng để người dùng đọc thông báo khắc phục."
    )

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 6: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ
    # =========================================================================
    add_chapter_title("CHƯƠNG 6: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ")

    add_section_title("6.1. Kết quả thực nghiệm định lượng trên FLIR ADAS v2")
    add_body(
        "Mô hình YOLOv8n huấn luyện trên bộ dữ liệu FLIR ADAS v2 được kiểm định độc lập trên toàn bộ 2.288 ảnh của tập Validation chính thức. "
        "Kết quả định lượng nghiệm thu chính thức đạt được:\n"
        "• Precision (Độ chính xác): 78.49% (0.7849)\n"
        "• Recall (Độ thu hồi / Bao phủ): 58.37% (0.5837)\n"
        "• mAP@50 (Mean Average Precision tại IoU=0.5): 67.07% (0.6707)\n"
        "• mAP@50-95: 34.26% (0.3426)"
    )

    add_section_title("6.2. Kết quả thực nghiệm định lượng trên LLVIP")
    add_body(
        "Mô hình YOLOv8n trên bộ dữ liệu LLVIP được đánh giá độc lập trên tập Test chính thức gồm 3.463 ảnh người đi bộ ban đêm độ nét cao. "
        "Kết quả đạt mức xuất sắc vượt trội:\n"
        "• Precision (Độ chính xác): 96.38% (0.9638)\n"
        "• Recall (Độ thu hồi / Bao phủ): 94.54% (0.9454)\n"
        "• mAP@50: 98.30% (0.9830)\n"
        "• mAP@50-95: 68.04% (0.6804)"
    )

    add_section_title("6.3. Đối chiếu chỉ số với mục tiêu đồ án đề ra")
    add_body("Bảng 6.1 tổng hợp và đối chiếu trực tiếp các kết quả thực nghiệm với chỉ tiêu nghiệm thu ban đầu:")

    tbl_res = doc.add_table(rows=8, cols=5)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_res)
    res_headers = ["Chỉ số Đánh giá", "FLIR ADAS v2", "LLVIP Benchmark", "Mục tiêu Đề ra", "Đánh giá nghiệm thu"]
    for c_idx, h in enumerate(res_headers):
        c = tbl_res.rows[0].cells[c_idx]
        set_cell_background(c, "005696")
        set_cell_margins(c, 100, 100, 100, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    res_data = [
        ("Precision (P)", "78.49%", "96.38%", "≥ 70.00%", "VƯỢT CHỈ TIÊU"),
        ("Recall (R)", "58.37%", "94.54%", "≥ 55.00%", "VƯỢT CHỈ TIÊU"),
        ("mAP@50", "67.07%", "98.30%", "≥ 65.00%", "VƯỢT CHỈ TIÊU"),
        ("mAP@50-95", "34.26%", "68.04%", "≥ 30.00%", "VƯỢT CHỈ TIÊU"),
        ("Kích thước file trọng số", "6.17 MB", "5.25 MB", "< 15.0 MB", "SIÊU GỌN NHẸ"),
        ("Số lượng tham số", "3.138.003", "2.604.883", "< 5.0 triệu", "ĐẠT CHUẨN EMBEDDED"),
        ("Tốc độ CPU (Intel)", "~35.1 FPS", "~38.4 FPS", "> 25.0 FPS", "THỜI GIAN THỰC"),
    ]
    for row_idx, r_data in enumerate(res_data, 1):
        row = tbl_res.rows[row_idx]
        for c_idx, val in enumerate(r_data):
            c = row.cells[c_idx]
            set_cell_margins(c, 70, 70, 90, 90)
            if row_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")
            p = c.paragraphs[0]
            if c_idx in (1, 2, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                if c_idx == 4:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
            else:
                p.add_run(val)

    p_cap_res = doc.add_paragraph()
    p_cap_res.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_res.paragraph_format.space_before = Pt(4)
    p_cap_res.paragraph_format.space_after = Pt(12)
    p_cap_res.add_run("Bảng 6.1: Kết quả định lượng nghiệm thu chính thức của hai mô hình YOLOv8n trên ảnh nhiệt").italic = True

    # Chen bieu do so sanh
    smc_img = ASSETS_DIR / "slide_metrics_comparison.png"
    if smc_img.exists():
        add_figure_image(smc_img, "Hình 6.1: Biểu đồ cột đối sánh định lượng các chỉ số chính giữa FLIR ADAS v2 và LLVIP")

    add_section_title("6.4. Phân tích trực quan hình ảnh dự đoán thực tế")
    add_body(
        "Hình 6.2 minh họa một số kết quả nhận diện tiêu biểu trong các điều kiện ánh sáng cực đoan. "
        "Mô hình phát hiện chính xác người đi bộ trong bóng tối hoàn toàn, phân tách tốt các nhóm người đi sát nhau "
        "và hầu như không bị báo động giả bởi các nguồn phát nhiệt từ mặt đường hay đèn chiếu sáng."
    )

    det_img = ASSETS_DIR / "slide_detection_showcase.png"
    if det_img.exists():
        add_figure_image(det_img, "Hình 6.2: Mẫu ảnh nhận diện thực tế của hệ thống với bounding box Cyber-Thermal và trích xuất thân nhiệt người")

    add_section_title("6.5. Đánh giá tốc độ suy luận và hiệu năng phần cứng CPU")
    add_body(
        "Nhằm đảm bảo tính thực tiễn khi triển khai trên các thiết bị giám sát thông thường không có card đồ họa rời đắt tiền, "
        "đề tài tiến hành đo đạc độ trễ chi tiết trên CPU máy tính cá nhân. Bảng 6.2 thể hiện kết quả phân tách rõ ràng giữa Model Latency và Pipeline Latency:"
    )

    tbl_fps = doc.add_table(rows=4, cols=4)
    tbl_fps.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_fps)
    fps_h = ["Thành phần đo đạc", "Độ trễ trung bình (ms)", "Tốc độ xử lý (FPS)", "Đánh giá khả năng đáp ứng"]
    for c_idx, h in enumerate(fps_h):
        c = tbl_fps.rows[0].cells[c_idx]
        set_cell_background(c, "005696")
        set_cell_margins(c, 100, 100, 100, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    fps_data = [
        ("Suy luận thuần Model (Forward + NMS)", "26.0 – 28.5 ms", "35.1 – 38.4 FPS", "Vượt chuẩn thời gian thực (>30 FPS)"),
        ("Xử lý toàn Pipeline (Tiền xử lý + Render)", "34.0 – 38.0 ms", "26.3 – 29.4 FPS", "Hoạt động mượt mà trên giao diện Web"),
        ("Chế độ so sánh cả hai mô hình song song", "55.0 – 62.0 ms", "16.1 – 18.2 FPS", "Chấp nhận được cho phân tích đối soát"),
    ]
    for row_idx, r_data in enumerate(fps_data, 1):
        row = tbl_fps.rows[row_idx]
        for c_idx, val in enumerate(r_data):
            c = row.cells[c_idx]
            set_cell_margins(c, 70, 70, 90, 90)
            if row_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")
            p = c.paragraphs[0]
            if c_idx in (1, 2):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run(val)

    p_cap_fps = doc.add_paragraph()
    p_cap_fps.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_fps.paragraph_format.space_before = Pt(4)
    p_cap_fps.paragraph_format.space_after = Pt(12)
    p_cap_fps.add_run("Bảng 6.2: Đo đạc chi tiết độ trễ và tốc độ khung hình trên phần cứng CPU thông thường").italic = True

    add_section_title("6.6. Phân tích so sánh khách quan và giải thích giới hạn dữ liệu")
    add_body(
        "Lưu ý học thuật quan trọng: Báo cáo không so sánh trực tiếp chỉ số của FLIR trên tập Validation với chỉ số của LLVIP trên tập Test "
        "như hai đại lượng tương đương tuyệt đối, bởi vì điều kiện bối cảnh của hai tập dữ liệu là hoàn toàn khác biệt:\n"
        "• FLIR ADAS v2 phản ánh góc quay động từ xe ô tô chạy tốc độ cao, có nhiều xe cộ, người đi bộ bị che khuất và kích thước nhỏ ở cự ly xa. Do đó chỉ số mAP50 đạt 67.07% là kết quả rất thực tế và ấn tượng.\n"
        "• LLVIP là camera an ninh cố định độ nét cao hướng xuống phố đi bộ, người đi bộ chiếm tỷ lệ diện tích lớn, độ tương phản thân nhiệt cực mạnh so với nền đường đêm lạnh, dẫn tới chỉ số mAP50 đạt tới 98.30%."
    )

    add_section_title("6.7. Đánh giá ưu điểm, hạn chế và các trường hợp biên")
    add_body(
        "• Ưu điểm vượt trội: Hệ thống hoạt động độc lập với ánh sáng, nhận diện xuyên đêm tối 0 Lux, tốc độ đáp ứng thời gian thực trên CPU, giao diện trực quan hỗ trợ nhiều bảng màu hiển thị.\n"
        "• Các trường hợp biên (Edge cases) còn hạn chế: (1) Người đi bộ ở cự ly quá xa (> 50m) diện tích nguồn nhiệt chỉ chiếm vài pixel mờ nhạt dễ bị bỏ sót; (2) Người mặc trang phục cách nhiệt dày đặc (áo phao, áo bảo hộ) làm suy giảm lượng nhiệt bức xạ ra bề mặt; (3) Nền bê tông ban ngày hấp thụ nhiệt lượng mặt trời gay gắt gây giảm tương phản."
    )

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # =========================================================================
    add_chapter_title("CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_section_title("7.1. Các nội dung chính đã hoàn thành")
    add_body(
        "Sau quá trình nghiên cứu lý thuyết, xây dựng mã nguồn và thực nghiệm khoa học nghiêm túc, đề tài "
        "\"Xây dựng hệ thống phát hiện người trong ảnh nhiệt sử dụng YOLO với bộ dữ liệu FLIR ADAS và LLVIP\" "
        "đã hoàn thành trọn vẹn 100% các mục tiêu đề ra:"
    )
    add_bullet("1. Làm rõ cơ sở vật lý bức xạ hồng ngoại sóng dài LWIR và chứng minh ưu thế vượt trội của ảnh nhiệt so với ảnh quang học trong môi trường đêm tối và thời tiết xấu.")
    add_bullet("2. Xây dựng hoàn chỉnh pipeline tiền xử lý và chuyển đổi chuẩn hóa hơn 39.000 ảnh nhiệt từ định dạng COCO JSON và Pascal VOC XML sang định dạng YOLO.")
    add_bullet("3. Huấn luyện thành công mô hình học sâu YOLOv8n trên hai bộ dữ liệu, đạt mAP@50 đạt 67.07% trên FLIR ADAS v2 và 98.30% trên LLVIP, vượt xa chỉ tiêu ban đầu.")
    add_bullet("4. Tối ưu hóa mô hình đạt tốc độ xử lý thời gian thực > 35 FPS ngay trên môi trường CPU Intel thông thường, kích thước file trọng số siêu gọn nhẹ (< 6.2 MB).")
    add_bullet("5. Kiểm thử độ bền vững thành công trước 5 kịch bản suy thoái cảm biến và sương mù nhiệt.")
    add_bullet("6. Xây dựng ứng dụng Web Demo (Streamlit Studio) hoàn chỉnh, trực quan, hỗ trợ so sánh hai mô hình và script chạy nhanh một chạm run_app.bat trên Windows.")

    add_section_title("7.2. Các hạn chế kỹ thuật còn tồn tại")
    add_bullet("Chưa kết hợp thông tin đa phương thức (Multimodal Fusion) đồng thời giữa kênh quang học RGB và kênh nhiệt LWIR khi môi trường có đủ ánh sáng.")
    add_bullet("Mô hình còn gặp khó khăn khi phát hiện người đi bộ ở cự ly quá xa (> 50 mét) do độ phân giải cảm biến nhiệt bị giới hạn.")
    add_bullet("Giới hạn tài nguyên phần cứng cá nhân khiến quá trình huấn luyện mô hình kích thước lớn (YOLOv8s, YOLOv8m) cần nhiều thời gian.")

    add_section_title("7.3. Hướng nghiên cứu và phát triển tiếp theo")
    add_bullet("Nghiên cứu kiến trúc kết hợp đa phương thức RGB-Thermal (Cross-Modality Fusion) để tận dụng màu sắc ban ngày và thân nhiệt ban đêm.")
    add_bullet("Thực nghiệm các biến thể mới hơn như YOLOv9, YOLOv10 hoặc YOLO11 để tiếp tục đẩy cao độ chính xác mAP50-95.")
    add_bullet("Tối ưu hóa lượng tử hóa mô hình (INT8 Quantization qua TensorRT hoặc OpenVINO) để triển khai trực tiếp trên các vi máy tính nhúng biên như NVIDIA Jetson Nano / Raspberry Pi 5.")

    doc.add_page_break()

    # =========================================================================
    # TAI LIEU THAM KHAO
    # =========================================================================
    p_ref_head = doc.add_paragraph()
    p_ref_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_head.paragraph_format.space_before = Pt(10)
    p_ref_head.paragraph_format.space_after = Pt(14)
    r_rf = p_ref_head.add_run("TÀI LIỆU THAM KHẢO")
    r_rf.bold = True
    r_rf.font.size = Pt(15)
    r_rf.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    references = [
        "[1] Ultralytics. (2023). \"YOLOv8 Documentation and Architecture Overview\". Truy cập từ: https://docs.ultralytics.com/",
        "[2] Teledyne FLIR. (2021). \"FLIR Thermal Dataset for Autonomous Vehicle Research (ADAS v2)\". Truy cập từ: https://www.flir.com/oem/adas/adas-dataset-form/",
        "[3] Jia, X., Zhu, C., Li, M., Tang, W., & Zhou, W. (2021). \"LLVIP: A Visible-infrared Paired Dataset for Low-light Vision\". IEEE International Conference on Computer Vision Workshops (ICCVW), pp. 3496–3504.",
        "[4] Sensors Journal. (2022). \"Thermal Image Person Detection Using Deep Learning: A Survey and Comparative Benchmark\". MDPI Sensors, 22(14), 5351. DOI: 10.3390/s22145351",
        "[5] ACM Digital Library. (2019). \"Infrared Pedestrian Detection in Low-Light Conditions Using Deep Convolutional Networks\". ACM International Conference on Multimedia, pp. 3323–3330.",
        "[6] Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). \"You Only Look Once: Unified, Real-Time Object Detection\". IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 779–788.",
        "[7] Bochkovskiy, A., Wang, C. Y., & Liao, H. Y. M. (2020). \"YOLOv4: Optimal Speed and Accuracy of Object Detection\". arXiv preprint arXiv:2004.10934.",
        "[8] Lin, T. Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan, D., Dollár, P., & Zitnick, C. L. (2014). \"Microsoft COCO: Common Objects in Context\". European Conference on Computer Vision (ECCV), pp. 740–755.",
        "[9] Everingham, M., Eslami, S. M. A., Van Gool, L., Williams, C. K. I., Winn, J., & Zisserman, A. (2015). \"The Pascal Visual Object Classes Challenge: A Retrospective\". International Journal of Computer Vision (IJCV), 111(1), pp. 98–136.",
        "[10] Streamlit Inc. (2024). \"Streamlit Documentation: A faster way to build and share data apps\". Truy cập từ: https://docs.streamlit.io/",
    ]
    for ref in references:
        p_r = doc.add_paragraph(ref)
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.paragraph_format.space_before = Pt(2)
        p_r.paragraph_format.space_after = Pt(4)

    doc.add_page_break()

    # =========================================================================
    # PHU LUC: HUONG DAN CAI DAT VA VAN HANH HE THONG
    # =========================================================================
    p_app_head = doc.add_paragraph()
    p_app_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_app_head.paragraph_format.space_before = Pt(10)
    p_app_head.paragraph_format.space_after = Pt(14)
    r_ap = p_app_head.add_run("PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG")
    r_ap.bold = True
    r_ap.font.size = Pt(15)
    r_ap.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "Nhằm hỗ trợ quá trình nghiệm thu, chấm điểm của Giảng viên hướng dẫn và Hội đồng khoa học, "
        "dưới đây là hướng dẫn chi tiết các bước cài đặt và vận hành hệ thống phần mềm:"
    )

    add_section_title("1. Yêu cầu môi trường phần mềm")
    add_bullet("Hệ điều hành: Windows 10 / Windows 11 (khuyến nghị), macOS hoặc Linux.")
    add_bullet("Phiên bản Python: Python 3.10 – 3.14 (Khuyến nghị sử dụng môi trường ảo venv độc lập).")
    add_bullet("Các thư viện phụ thuộc cốt lõi: ultralytics (>=8.2.0), torch (>=2.0.0), torchvision, opencv-python, streamlit, pillow, pandas, numpy, PyYAML, psutil.")

    add_section_title("2. Khởi chạy nhanh bằng file run_app.bat trên Windows (Khuyên dùng)")
    add_bullet("Bước 1: Mở thư mục dự án `D:\\MonHoc\\TTNT\\ThermalYoloPerson`.")
    add_bullet("Bước 2: Bấm đúp chuột vào file `run_app.bat`. Cửa sổ console sẽ tự động phát hiện và kích hoạt môi trường ảo `.venv`, kiểm tra thư viện và bật server Streamlit.")
    add_bullet("Bước 3: Trình duyệt web sẽ tự động mở trang ứng dụng tại địa chỉ: `http://localhost:8501`.")

    add_section_title("3. Khởi chạy thủ công qua Terminal / Command Prompt")
    add_body("Người dùng có thể mở PowerShell hoặc CMD tại thư mục dự án và thực hiện các lệnh sau:")
    add_body(
        "cd D:\\MonHoc\\TTNT\\ThermalYoloPerson\n"
        ".\\.venv\\Scripts\\activate\n"
        "python -m streamlit run app.py"
    )

    add_section_title("4. Lệnh chạy đánh giá độc lập và huấn luyện qua dòng lệnh")
    add_bullet("Chạy kiểm định độc lập trên tập FLIR val: `python scripts/evaluate_flir.py`")
    add_bullet("Chạy huấn luyện mô hình trên FLIR: `python scripts/train_yolo.py --dataset flir --epochs 50 --batch 4 --imgsz 416`")
    add_bullet("Chạy huấn luyện mô hình trên LLVIP: `python scripts/train_yolo.py --dataset llvip --epochs 50 --batch 4 --imgsz 416`")

    add_section_title("5. Hướng dẫn khai thác 4 Tab chức năng trên Giao diện Web")
    add_bullet("Tab 1 - Nhận diện Ảnh Nhiệt: Chọn ảnh mẫu từ thư viện hoặc tải ảnh từ máy tính (JPG/PNG). Hệ thống tự động nhận diện tức thì, xuất ảnh gắn khung bounding box Cyber-Thermal, bảng tọa độ chi tiết và thư viện crop cận cảnh thân nhiệt từng người.")
    add_bullet("Tab 2 - Thử nghiệm Mức nhiệt & Nhiễu (Robustness Lab): Tùy chỉnh 5 mức suy thoái môi trường và cảm biến, quan sát tỷ lệ giữ vững phát hiện (Retention Rate) đối sánh trực quan với ảnh sạch.")
    add_bullet("Tab 3 - Đánh giá & Benchmark: Bảng tổng hợp số liệu thực nghiệm chính thức từ 50 epochs huấn luyện và đồ thị huấn luyện trực quan.")
    add_bullet("Tab 4 - Tổng quan Đề tài & Hướng dẫn: Xem tóm tắt lý thuyết sóng nhiệt LWIR 8–14 µm và thông tin tác giả đồ án.")

    # Luu file
    doc.save(str(OUT_PATH))
    print(f"[OK] Da tao thanh cong bao cao: {OUT_PATH}")

if __name__ == "__main__":
    build_report()
