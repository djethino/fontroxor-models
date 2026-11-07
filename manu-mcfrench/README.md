# Manu McFrench — French manuscripts, 17th–21st century

A handwritten text recognition model for French, trained on openly licensed manuscripts from the 17th to the 21st
century gathered by [HTR-United](https://htr-united.github.io/). FontRoxor uses it to read a free handwritten sheet
(cursive included) line by line.

- **Authors**: Simon Gabay, Thibault Clérice, Alix Chagué (Université de Genève, Inria)
- **Original model**: `ManuMcFondue.mlmodel` for [kraken](https://kraken.re), https://doi.org/10.5281/zenodo.10886224
- **Licence**: [CC-BY-4.0](../LICENSES/CC-BY-4.0.txt), the licence of the original model. This converted model is
  distributed under the same licence.
- **Reported accuracy**: character error rate 8.8 % on its test set (from the original model's metadata).
- **Characters**: 258 (Latin with French and other accented letters, digits, punctuation, some Greek).

## What we changed

The network was converted from the kraken format to ONNX by [`tools/convert_kraken.py`](../tools/convert_kraken.py) of this repository:

- a softmax is added at the end, and the output is laid out as `[1, columns, classes]`;
- the character set is written to `dict.txt` (line *k* is class *k* + 1; class 0 is the CTC blank);
- `fontroxor-model.json` records what the network expects: lines 120 pixels high, one grey channel, light ink on a
  dark ground (`mean` 1, `std` −1), 16 pixels of paper on each side.

The weights and the character set are unchanged. On the same line image, the converted model reads exactly what the
original reads in kraken.

This conversion is not made or endorsed by the original authors.
