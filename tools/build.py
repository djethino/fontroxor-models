"""Build the release archives and the catalogue (models.json) from model folders.

Usage:  python -I tools/build.py <folder with one subfolder per model> dist/

Each model's metadata lives in MODELS below; its folder must hold the files listed there. For every model the script
writes dist/<id>.zip (the model files, the model card README.md and its LICENSE at the archive root) and records the
archive's size and SHA-256 in models.json. Upload each dist/<id>.zip to the release tagged <id>-<version>.
"""

import hashlib
import json
import pathlib
import shutil
import sys
import zipfile

REPO = "djethino/fontroxor-models"
ROOT = pathlib.Path(__file__).resolve().parent.parent

LATIN = ["en", "fr", "de", "af", "it", "es", "bs", "pt", "cs", "cy", "da", "et", "ga", "hr", "uz", "hu", "sr", "id", "oc",
         "is", "lt", "mi", "ms", "nl", "no", "pl", "sk", "sl", "sq", "sv", "sw", "tl", "tr", "la"]

MODELS = [
    {
        "id": "manu-mcfrench",
        "version": 1,
        "name": "French manuscripts, 17th–21st century (Manu McFrench)",
        "kind": "handwriting",
        "languages": ["fr"],
        "scripts": ["Latn"],
        "license": "CC-BY-4.0",
        "authors": "Simon Gabay, Thibault Clérice, Alix Chagué (Université de Genève, Inria)",
        "source": "https://doi.org/10.5281/zenodo.10886224",
        "changes": "Converted from the kraken .mlmodel format to ONNX (softmax added, output [1, columns, classes]); network and character set unchanged.",
        "files": ["rec.onnx", "dict.txt", "fontroxor-model.json"],
    },
    {
        "id": "paddleocr-latin-v5",
        "version": 1,
        "name": "Latin script, printed (PP-OCRv5 mobile)",
        "kind": "print",
        "languages": LATIN,
        "scripts": ["Latn"],
        "license": "Apache-2.0",
        "authors": "PaddlePaddle Authors (Baidu); ONNX conversion by monkt",
        "source": "https://github.com/PaddlePaddle/PaddleOCR",
        "changes": "Redistributed unchanged from the ONNX conversion at https://huggingface.co/monkt/paddleocr-onnx (Apache-2.0).",
        "files": ["rec.onnx", "dict.txt", "config.json"],
    },
    {
        "id": "paddleocr-chinese-v5",
        "version": 1,
        "name": "Chinese, Japanese and Latin, printed and handwritten Chinese (PP-OCRv5 server)",
        "kind": "print",
        "languages": ["zh", "ja", "en"],
        "scripts": ["Hans", "Hant", "Jpan", "Latn"],
        "license": "Apache-2.0",
        "authors": "PaddlePaddle Authors (Baidu); ONNX conversion by monkt",
        "source": "https://github.com/PaddlePaddle/PaddleOCR",
        "changes": "Redistributed unchanged from the ONNX conversion at https://huggingface.co/monkt/paddleocr-onnx (Apache-2.0).",
        "files": ["rec.onnx", "dict.txt", "config.json"],
    },
    {
        "id": "paddleocr-arabic-v3",
        "version": 1,
        "name": "Arabic script, printed (PP-OCRv3 mobile)",
        "kind": "print",
        "languages": ["ar", "ur", "fa"],
        "scripts": ["Arab"],
        "license": "Apache-2.0",
        "authors": "PaddlePaddle Authors (Baidu); ONNX conversion by monkt",
        "source": "https://github.com/PaddlePaddle/PaddleOCR",
        "changes": "Redistributed unchanged from the ONNX conversion at https://huggingface.co/monkt/paddleocr-onnx (Apache-2.0).",
        "files": ["rec.onnx", "dict.txt", "config.json"],
    },
]


def main():
    source, dist = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    dist.mkdir(parents=True, exist_ok=True)
    catalogue = []
    for m in MODELS:
        folder = source / m["id"]
        archive = dist / f"{m['id']}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for name in m["files"]:
                z.write(folder / name, name)
            z.write(ROOT / m["id"] / "README.md", "README.md")
            z.write(ROOT / "LICENSES" / f"{m['license']}.txt", "LICENSE")
        data = archive.read_bytes()
        entry = {k: m[k] for k in ("id", "version", "name", "kind", "languages", "scripts", "license", "authors", "source", "changes")}
        entry["licenseUrl"] = f"https://github.com/{REPO}/blob/main/LICENSES/{m['license']}.txt"
        entry["card"] = f"https://github.com/{REPO}/blob/main/{m['id']}/README.md"
        entry["url"] = f"https://github.com/{REPO}/releases/download/{m['id']}-{m['version']}/{m['id']}.zip"
        entry["size"] = len(data)
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        catalogue.append(entry)
        print(f"{archive}: {len(data) / 1e6:.1f} MB")
    (ROOT / "models.json").write_text(json.dumps({"format": 1, "models": catalogue}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
