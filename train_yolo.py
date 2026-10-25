
import argparse
from pathlib import Path
import torch
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Huấn luyện YOLOv8 cho FLIR / LLVIP")
    parser.add_argument(
        "--dataset",
        choices=["flir", "llvip"],
        default="llvip",
        help="Tên bộ dữ liệu (flir hoặc llvip)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Số lượng epoch huấn luyện (mặc định: 50)",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=4,
        help="Kích thước batch (mặc định: 4)",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=416,
        help="Kích thước ảnh đầu vào (mặc định: 416)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Số worker cho DataLoader (mặc định: 2; 0 nếu muốn giảm tải CPU)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help="Thiết bị huấn luyện ('cpu', '0', 'cuda', hoặc 'auto')",
    )
    parser.add_argument(
        "--fraction",
        type=float,
        default=1.0,
        help="Tỷ lệ tập dữ liệu sử dụng (1.0 = toàn bộ, 0.1 = 10%%)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Tên thư mục lưu kết quả trong runs/",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Tiếp tục huấn luyện từ checkpoint last.pt gần nhất",
    )
    args = parser.parse_args()

    # Xác định device
    if args.device == "auto":
        device = "0" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device

    device_tag = "gpu" if device in ("0", "cuda") or str(device).isdigit() else "cpu"
    run_name = args.name or f"{args.dataset}_yolov8n_{device_tag}"
    run_dir = ROOT / "runs" / run_name

    if args.resume:
        checkpoint = run_dir / "weights" / "last.pt"
        if not checkpoint.exists():
            raise FileNotFoundError(f"Không tìm thấy checkpoint: {checkpoint}")
        print(f"Tiếp tục huấn luyện từ: {checkpoint}")
        model = YOLO(str(checkpoint))
        model.train(resume=True)
        return

    data_yaml = ROOT / "prepared_dataset" / args.dataset / "data.yaml"
    if not data_yaml.exists():
        data_yaml = ROOT / "configs" / f"{args.dataset}.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError(f"Không tìm thấy file cấu hình: {data_yaml}")

    print("=" * 60)
    print("BẮT ĐẦU HUẤN LUYỆN YOLOv8")
    print(f"Dataset : {args.dataset} ({data_yaml})")
    print(f"Device  : {device} ({'GPU CUDA' if device != 'cpu' else 'CPU'})")
    print(f"Epochs  : {args.epochs}")
    print(f"Batch   : {args.batch}")
    print(f"Imgsz   : {args.imgsz}")
    print(f"Workers : {args.workers}")
    print(f"Fraction: {args.fraction}")
    print(f"Run name: {run_name}")
    print("=" * 60)

    model = YOLO("yolov8n.pt")
    model.train(
        data=str(data_yaml),
        device=device,
        imgsz=args.imgsz,
        batch=args.batch,
        epochs=args.epochs,
        patience=10,
        workers=args.workers,
        pretrained=True,
        save=True,
        save_period=5,
        plots=True,
        fraction=args.fraction,
        project=str(ROOT / "runs"),
        name=run_name,
        exist_ok=True,
    )


if __name__ == "__main__":
    main()

