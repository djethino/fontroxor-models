# Arabic script, printed (PP-OCRv3 mobile)

A text recognition model from [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (`arabic_PP-OCRv3_mobile_rec`). FontRoxor uses it
to read a free handwritten or printed sheet line by line.

- **Reads**: Printed text in the Arabic script: Arabic, Urdu, Persian.
- **Note**: It is trained for print; handwriting is read less reliably.
- **Authors**: PaddlePaddle Authors (Baidu). ONNX conversion by [monkt](https://huggingface.co/monkt/paddleocr-onnx).
- **Licence**: [Apache-2.0](../LICENSES/Apache-2.0.txt), the licence of PaddleOCR's models and of the ONNX conversion.

## What we changed

Nothing: `rec.onnx`, `dict.txt` and `config.json` are redistributed unchanged from https://huggingface.co/monkt/paddleocr-onnx,
so that FontRoxor does not depend on a repository it does not maintain. FontRoxor reads `config.json` as it is.

Not made or endorsed by the PaddleOCR authors.
