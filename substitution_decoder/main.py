# -*- coding: utf-8 -*-

from os.path import isfile
import decoder_text

__version__ = "0.1.0"
__author__ = 'Oguzhan OZDEMIR <ademoguzhanozdmr@gmail.com>'


def read_txt(path: str = r'example/sifreli_metin.txt', encoding: str = "utf-8"):
    txt = ""
    if isfile(path):
        with open(path, 'r', encoding=encoding) as file:
            txt = file.read()
    return txt


def write_txt(txt: str, path: str = r"example/acik_metin.txt", encoding = "utf-8"):
    if txt:
        with open(path, 'w+', encoding=encoding) as file:
            file.write(txt)
        print("Done")


def main():
    # TODO  will be added to argparse
    txt = read_txt()
    decoder = decoder_text.DecoderText()
    new_txt = decoder.decoding_text(txt)
    write_txt(new_txt)


if __name__ == "__main__":
    main()
