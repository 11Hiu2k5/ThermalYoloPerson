
import json
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "prepared_dataset"
SEED = 42


def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def write_yolo_label(path, boxes):
    """boxes contains normalized (cx, cy, w, h), class id is always 0."""
    with path.open("w", encoding="utf-8") as f:
        for cx, cy, w, h in boxes:
            f.write(
                f"0 {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n"
            )


def normalize_box(x, y, w, h, image_w, image_h):
    # Clip the box to image boundaries.
    x1 = max(0.0, min(float(image_w), x))
    y1 = max(0.0, min(float(image_h), y))
    x2 = max(0.0, min(float(image_w), x + w))
    y2 = max(0.0, min(float(image_h), y + h))

    bw, bh = x2 - x1, y2 - y1
    if bw <= 0 or bh <= 0:
        return None

    cx = (x1 + x2) / 2 / image_w
    cy = (y1 + y2) / 2 / image_h
    return cx, cy, bw / image_w, bh / image_h


def copy_image(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def prepare_flir():
    source = ROOT / "FLIR_ADAS_v2"
    target = OUT / "flir"

    reset_dir(target)
    stats = []

    for split in ("train", "val"):
        source_split = source / (
            "images_thermal_train" if split == "train"
            else "images_thermal_val"
        )
        json_path = source_split / "coco.json"

        with json_path.open("r", encoding="utf-8-sig") as f:
            coco = json.load(f)

        # Find person by category name instead of assuming an ID.
        person_ids = {
            cat["id"] for cat in coco["categories"]
            if cat["name"].strip().lower() == "person"
        }
        if not person_ids:
            raise ValueError(f"FLIR: no person category in {json_path}")

        annotations = {}
        for ann in coco["annotations"]:
            if ann["category_id"] in person_ids:
                annotations.setdefault(ann["image_id"], []).append(
                    ann["bbox"]
                )

        image_dir = target / "images" / split
        label_dir = target / "labels" / split
        image_dir.mkdir(parents=True)
        label_dir.mkdir(parents=True)

        missing = 0
        total_boxes = 0

        for img in coco["images"]:
            src = source_split / img["file_name"]
            if not src.is_file():
                missing += 1
                continue

            # Preserve subdirectory information in the filename.
            safe_name = img["file_name"].replace("\\", "/").replace("/", "__")
            dst = image_dir / safe_name
            copy_image(src, dst)

            boxes = []
            iw, ih = float(img["width"]), float(img["height"])

            for bbox in annotations.get(img["id"], []):
                x, y, w, h = map(float, bbox)
                box = normalize_box(x, y, w, h, iw, ih)
                if box:
                    boxes.append(box)

            write_yolo_label(label_dir / f"{dst.stem}.txt", boxes)
            total_boxes += len(boxes)

        stats.append(
            (f"FLIR {split}", len(list(image_dir.iterdir())),
             total_boxes, missing)
        )

    (target / "data.yaml").write_text(
        f"path: {target.as_posix()}\n"
        "train: images/train\n"
        "val: images/val\n"
        "names:\n"
        "  0: person\n",
        encoding="utf-8"
    )
    return stats


def parse_voc_xml(xml_path):
    root = ET.parse(xml_path).getroot()
    size = root.find("size")
    if size is None:
        raise ValueError(f"Missing image size in {xml_path}")

    iw = float(size.findtext("width"))
    ih = float(size.findtext("height"))
    boxes = []

    for obj in root.findall("object"):
        name = (obj.findtext("name") or "").strip().lower()
        if name != "person":
            continue

        bnd = obj.find("bndbox")
        if bnd is None:
            continue

        xmin = float(bnd.findtext("xmin"))
        ymin = float(bnd.findtext("ymin"))
        xmax = float(bnd.findtext("xmax"))
        ymax = float(bnd.findtext("ymax"))

        box = normalize_box(
            xmin, ymin, xmax - xmin, ymax - ymin, iw, ih
        )
        if box:
            boxes.append(box)

    return boxes


def prepare_llvip():
    source = ROOT / "LLVIP"
    target = OUT / "llvip"

    reset_dir(target)

    image_sets = {
        "train": [],
        "val": [],
        "test": [],
    }

    # LLVIP train: make a reproducible 90/10 train/validation split.
    infrared_train = source / "infrared" / "train"
    train_images = sorted(
        p for p in infrared_train.rglob("*")
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
    )
    rng = random.Random(SEED)
    rng.shuffle(train_images)

    n_val = max(1, round(len(train_images) * 0.10)) if train_images else 0
    image_sets["val"] = train_images[:n_val]
    image_sets["train"] = train_images[n_val:]

    # Keep the official LLVIP test set unchanged.
    test_dir = source / "infrared" / "test"
    image_sets["test"] = sorted(
        p for p in test_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
    )

    annotation_dir = source / "Annotations"
    stats = []

    for split, images in image_sets.items():
        image_dir = target / "images" / split
        label_dir = target / "labels" / split
        image_dir.mkdir(parents=True)
        label_dir.mkdir(parents=True)

        missing_xml = 0
        total_boxes = 0

        for src in images:
            xml_path = annotation_dir / f"{src.stem}.xml"
            if not xml_path.is_file():
                missing_xml += 1
                continue

            # Prefix filename with split to prevent filename collisions.
            dst_name = f"{src.stem}{src.suffix.lower()}"
            dst = image_dir / dst_name
            copy_image(src, dst)

            boxes = parse_voc_xml(xml_path)
            write_yolo_label(label_dir / f"{dst.stem}.txt", boxes)
            total_boxes += len(boxes)

        stats.append(
            (f"LLVIP {split}", len(list(image_dir.iterdir())),
             total_boxes, missing_xml)
        )

    (target / "data.yaml").write_text(
        f"path: {target.as_posix()}\n"
        "train: images/train\n"
        "val: images/val\n"
        "test: images/test\n"
        "names:\n"
        "  0: person\n",
        encoding="utf-8"
    )
    return stats


def validate_dataset(dataset_dir):
    print(f"\nValidation: {dataset_dir.name}")
    for split in ("train", "val", "test"):
        images_dir = dataset_dir / "images" / split
        labels_dir = dataset_dir / "labels" / split
        if not images_dir.exists():
            continue

        images = [
            p for p in images_dir.iterdir()
            if p.is_file()
        ]
        missing_labels = [
            p.name for p in images
            if not (labels_dir / f"{p.stem}.txt").is_file()
        ]

        invalid_lines = []
        for label in labels_dir.glob("*.txt"):
            for line_no, line in enumerate(
                label.read_text(encoding="utf-8").splitlines(), 1
            ):
                parts = line.split()
                if len(parts) != 5:
                    invalid_lines.append(f"{label.name}:{line_no}")
                    continue
                try:
                    cls, *coords = map(float, parts)
                except ValueError:
                    invalid_lines.append(f"{label.name}:{line_no}")
                    continue
                if cls != 0 or any(v < 0 or v > 1 for v in coords):
                    invalid_lines.append(f"{label.name}:{line_no}")

        print(
            f"  {split}: images={len(images)}, "
            f"missing_labels={len(missing_labels)}, "
            f"invalid_lines={len(invalid_lines)}"
        )
        if missing_labels:
            print("    Missing label examples:", missing_labels[:5])
        if invalid_lines:
            print("    Invalid label examples:", invalid_lines[:5])


def main():
    if not (ROOT / "FLIR_ADAS_v2").is_dir():
        raise FileNotFoundError("Cannot find FLIR_ADAS_v2")
    if not (ROOT / "LLVIP").is_dir():
        raise FileNotFoundError("Cannot find LLVIP")

    print("Preparing datasets in:", OUT)
    print("\nFLIR stats:")
    for row in prepare_flir():
        print(f"  {row[0]}: images={row[1]}, person_boxes={row[2]}, "
              f"missing_source_images={row[3]}")

    print("\nLLVIP stats:")
    for row in prepare_llvip():
        print(f"  {row[0]}: images_copied={row[1]}, person_boxes={row[2]}, "
              f"missing_xml={row[3]}")

    validate_dataset(OUT / "flir")
    validate_dataset(OUT / "llvip")
    print("\nDone. Original datasets were not modified.")


if __name__ == "__main__":
    main()
