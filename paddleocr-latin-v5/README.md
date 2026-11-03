# Latin script, printed (PP-OCRv5 mobile)

A text recognition model from [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (`latin_PP-OCRv5_mobile_rec`). FontRoxor uses it
to read a free handwritten or printed sheet line by line.

- **Reads**: Printed text in the Latin script: English, French, German, Afrikaans, Italian, Spanish, Bosnian, Portuguese, Czech, Welsh, Danish, Estonian, Irish, Croatian, Uzbek, Hungarian, Serbian (Latin), Indonesian, Occitan, Icelandic, Lithuanian, Maori, Malay, Dutch, Norwegian, Polish, Slovak, Slovenian, Albanian, Swedish, Swahili, Tagalog, Turkish, Latin.
- **Note**: It is trained for print: on cursive handwriting it often misreads letters. For French handwriting, prefer [manu-mcfrench](../manu-mcfrench/README.md).
- **Authors**: PaddlePaddle Authors (Baidu). ONNX conversion by [monkt](https://huggingface.co/monkt/paddleocr-onnx).
- **Licence**: [Apache-2.0](../LICENSES/Apache-2.0.txt), the licence of PaddleOCR's models and of the ONNX conversion.

## What we changed

Nothing: `rec.onnx`, `dict.txt` and `config.json` are redistributed unchanged from https://huggingface.co/monkt/paddleocr-onnx,
so that FontRoxor does not depend on a repository it does not maintain. FontRoxor reads `config.json` as it is.

Not made or endorsed by the PaddleOCR authors.
