import string
import random
from os.path import isfile


def read_txtFile(path: str, encoding_type: str = "utf-8") -> str:
    assert isfile(path), f"Not found {path}"
    assert isinstance(encoding_type, str), "Encoding must be of type str"
    # TODO : CHECK encoding_type
    File = open(path, 'r', encoding=encoding_type)
    txt = File.read()
    File.close()
    return txt.upper()


def new_substituion() -> dict:
    select_letter = [*string.ascii_lowercase]
    select_letter_2 = select_letter.copy()
    password_key = {}
    while len(select_letter) > 0:
        password_character = random.choice(select_letter)
        select_letter.remove(password_character)
        decoding_character = random.choice(select_letter_2)
        select_letter_2.remove(decoding_character)
        password_key[password_character.upper()] = decoding_character
    return password_key


def write_txt(file_name: str, text: str, encoding_type: str = "utf-8"):
    assert isinstance(file_name, str), "file_name must be of type str"
    assert isinstance(text, str), "txt must be of type str"
    assert isinstance(encoding_type, str), "Encoding must be of type str"
    # TODO : CHECK encoding_type
    File = open(file_name, 'w+', encoding=encoding_type)
    File.write(text)
    File.close()


def main():
    password_key = new_substituion()
    file = "acik_metin.txt"
    txt = read_txtFile(file)
    for key in password_key:
        txt = txt.replace(key, password_key[key])
    write_txt(file_name="sifreli_metin_2.txt", text=txt)


if __name__ == '__main__':
    main()
