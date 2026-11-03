# Chinese, Japanese and Latin (PP-OCRv5 server)

A text recognition model from [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (`PP-OCRv5_server_rec`). FontRoxor uses it
to read a free handwritten or printed sheet line by line.

- **Reads**: Simplified and Traditional Chinese, Japanese, Pinyin and English. PaddleOCR trains this model on handwritten Chinese as well as print.
- **Note**: It is the largest model here (about 80 MB).
- **Authors**: PaddlePaddle Authors (Baidu). ONNX conversion by [monkt](https://huggingface.co/monkt/paddleocr-onnx).
- **Licence**: [Apache-2.0](../LICENSES/Apache-2.0.txt), the licence of PaddleOCR's models and of the ONNX conversion.

## What we changed

Nothing: `rec.onnx`, `dict.txt` and `config.json` are redistributed unchanged from https://huggingface.co/monkt/paddleocr-onnx,
so that FontRoxor does not depend on a repository it does not maintain. FontRoxor reads `config.json` as it is.

Not made or endorsed by the PaddleOCR authors.
