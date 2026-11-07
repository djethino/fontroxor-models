# FontRoxor models

Handwriting and text recognition models for [FontRoxor](https://github.com/djethino), the font editor. FontRoxor uses
them to read a photographed or scanned handwritten sheet and turn each letter into a glyph.

- **They run on the user's computer.** The sheet never leaves it: the models are executed locally on the CPU by
  [tract](https://github.com/sonos/tract), with nothing else to install.
- **Each model keeps its own licence and credits.** We redistribute models made by others, sometimes converted to ONNX.
  The authors, the licence, the original source and what we changed are written in each model's card and in the
  archive itself. Nothing here is endorsed by the original authors.
- **The catalogue** is [`models.json`](models.json): FontRoxor reads it to offer the models that fit a language, then
  downloads the archive, checks its SHA-256 and installs it.

| Model | Reads | Licence | Authors |
|---|---|---|---|
| [manu-mcfrench](manu-mcfrench/README.md) | French handwriting, 17th–21st century | CC-BY-4.0 | Simon Gabay, Thibault Clérice, Alix Chagué (Université de Genève, Inria) |
| [paddleocr-latin-v5](paddleocr-latin-v5/README.md) | Latin script, printed (34 languages) | Apache-2.0 | PaddlePaddle Authors (Baidu) |
| [paddleocr-chinese-v5](paddleocr-chinese-v5/README.md) | Chinese, Japanese, Latin | Apache-2.0 | PaddlePaddle Authors (Baidu) |
| [paddleocr-arabic-v3](paddleocr-arabic-v3/README.md) | Arabic, Urdu, Persian, printed | Apache-2.0 | PaddlePaddle Authors (Baidu) |

## Layout

- `<model>/README.md`: the model card (what it reads, credits, licence, source, changes).
- `LICENSES/`: the full licence texts.
- `models.json`: the catalogue (download address, size, SHA-256 of each archive).
- Releases: one per model and version, tagged `<model>-<version>`, carrying `<model>.zip` (the model files, its card
  and its licence).
- `tools/build.py`: builds the archives and the catalogue.
- `tools/convert_kraken.py`: converts a [kraken](https://kraken.re) model to the format above.

## Choosing models

FontRoxor is a commercial product. A model is only added if its licence allows commercial use **and** its training
data does too: a model under an open licence trained on non-commercial data (such as IAM or Muharaf) is left out.

Kraken models are converted with [`tools/convert_kraken.py`](tools/convert_kraken.py), and checked to read exactly as
kraken does.
