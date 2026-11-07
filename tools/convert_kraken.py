"""Convert a kraken recognition model (.mlmodel: a VGSL network with a CTC output) into a folder FontRoxor reads:
`rec.onnx` (the network, softmax included, output [1, columns, classes]), `dict.txt` (one character per line, line k is
class k + 1; class 0 is the CTC blank) and `fontroxor-model.json` (its card: line height, normalisation, licence,
authors).

Environment (once):
    uv venv -p 3.12 .venv
    uv pip install -p .venv kraken onnx

Usage:
    .venv/Scripts/python -I convert_kraken.py <model.mlmodel> <output folder> --name "…" --license CC-BY-4.0 \
        --source https://doi.org/… --languages fr --scripts Latn --authors "…"

Find a model with `kraken list --recognition -l fra`, read its card (licence, authors, training data) with
`kraken show <doi>`, download it with `kraken get <doi>`. Check the licence of the model AND of its training data.
"""

import argparse
import json
import pathlib

import torch
from kraken.lib import models


class Exported(torch.nn.Module):
    """The kraken network, from the image [1, 1, H, W] (light ink on a dark ground, from 0 to 1) to the probabilities
    [1, columns, classes]."""

    def __init__(self, nn):
        super().__init__()
        self.nn = nn

    def forward(self, x):
        logits, _ = self.nn(x, None)  # [1, classes, 1, columns]
        # No `squeeze`: the export turns it into an `If` node (its size is checked), which some ONNX runtimes refuse.
        return logits[:, :, 0, :].softmax(1).permute(0, 2, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("out")
    ap.add_argument("--name", required=True)
    ap.add_argument("--license", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--languages", default="")
    ap.add_argument("--scripts", default="")
    ap.add_argument("--authors", default="")
    args = ap.parse_args()

    rec = models.load_any(args.model)
    vgsl = rec.nn
    batch, channels, height, width = vgsl.input
    if channels != 1 or height <= 1 or width != 0:
        raise SystemExit(f"unsupported input: {vgsl.input} (needs a fixed height, a free width, one channel)")
    net = vgsl.nn.eval()
    exported = Exported(net).eval()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    sample = torch.rand(1, 1, height, 400)
    torch.onnx.export(
        exported,
        (sample,),
        str(out / "rec.onnx"),
        input_names=["x"],
        output_names=["probs"],
        dynamic_axes={"x": {3: "W"}, "probs": {1: "T"}},
        opset_version=17,
        dynamo=False,
    )

    # Class k + 1 is line k of dict.txt; kraken numbers its classes from 1 to C - 1 (0: the blank).
    l2c = rec.codec.l2c
    classes = net(sample, None)[0].shape[1]
    lines = []
    for label in range(1, classes):
        text = l2c.get((label,), None) if isinstance(next(iter(l2c)), tuple) else l2c.get(label, None)
        if text is None:
            raise SystemExit(f"class {label} has no character")
        lines.append(text if isinstance(text, str) else "".join(text))
    (out / "dict.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # The reader normalises a pixel as (v/255 − mean)/std: mean 1, std −1 gives 1 − v/255, kraken's light ink.
    # `pad`: pixels of paper added on each side of a line (without it the first letter is lost).
    manifest = {
        "name": args.name,
        "languages": [s for s in args.languages.split(",") if s],
        "scripts": [s for s in args.scripts.split(",") if s],
        "license": args.license,
        "source": args.source,
        "authors": args.authors,
        "height": height,
        "blankLast": False,
        "space": False,
        "mean": 1.0,
        "std": -1.0,
        "channels": 1,
        "pad": 16,
    }
    (out / "fontroxor-model.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Check: the ONNX model is valid.
    import onnx

    onnx.checker.check_model(str(out / "rec.onnx"))
    with torch.no_grad():
        ref = exported(sample)
    print(f"{out}: {classes - 1} characters, height {height}, output {tuple(ref.shape)}")


if __name__ == "__main__":
    main()
