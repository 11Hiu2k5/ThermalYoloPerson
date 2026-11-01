from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
if ROOT.name == "scripts":
    ROOT = ROOT.parent

MODEL_PATH = ROOT / "models" / "flir_best.pt"
if not MODEL_PATH.exists():
    MODEL_PATH = ROOT / "runs" / "flir_yolov8n_cpu" / "weights" / "best.pt"

DATA_YAML = ROOT / "prepared_dataset" / "flir" / "data.yaml"
if not DATA_YAML.exists():
    DATA_YAML = ROOT / "configs" / "flir.yaml"

assert MODEL_PATH.exists(), f"Không tìm thấy model: {MODEL_PATH}"
assert DATA_YAML.exists(), f"Không tìm thấy file data.yaml: {DATA_YAML}"

model = YOLO(str(MODEL_PATH))

metrics = model.val(
    data=str(DATA_YAML),
    split="val",
    imgsz=416,
    conf=0.001,
    iou=0.6,
    plots=True,
    project=str(ROOT / "runs" / "evaluation"),
    name="flir_val"
)

print("\n========== KẾT QUẢ ĐÁNH GIÁ FLIR ==========")
print(f"Precision:  {metrics.box.mp:.4f}")
print(f"Recall:     {metrics.box.mr:.4f}")
print(f"mAP50:      {metrics.box.map50:.4f}")
print(f"mAP50-95:   {metrics.box.map:.4f}")
print("==========================================")
