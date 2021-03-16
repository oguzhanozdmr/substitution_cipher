# -*- coding: utf-8 -*-

import pickle
from os.path import isfile

"""
Sözlükte veriler karakter sayısına indexli dic olarak tutulmaktadır.
"""


class WordDictionary:
    def __init__(self):
        self.__words = {}
        self.__path = r"word_list/en_dictionary.dat"
        self.__read_dictionary()

    def __check_file(func):
        def wrapper(self, *args):
            assert isfile(self.__path), f"Not found {self.__path}"
            return_value = func(self, *args)
            return return_value

        return wrapper

    @__check_file
    def __read_dictionary(self) -> None:
        with open(self.__path, "rb") as handle:
            self.__words = pickle.load(handle)
            handle.close()

    @__check_file
    def __write_pickle(self):
        return_value = False
        try:
            with open(self.__path, "wb") as handle:
                pickle.dump(self.__words, handle)
                handle.close()
                return_value = True
        except Exception as e:
            raise Exception("Sorry, Word could not be added", e.__class__)
        return return_value

    def find_word(self, word: str) -> bool:
        word_found = False
        word = str(word).strip()
        if word:
            word_size = len(word)
            if word in self.__words[word_size]:
                word_found = True
        return word_found

    def get_most_popular_words(self, character_size: int):
        """

        :param character_size:  character count of the word
        :return most popular word:
        """
        assert isinstance(character_size, int)
        return_list = []
        most_used_words = """
        be to of in it on he as do at by we or an my so up if go me no us the and for not you but his say her she 
        one all out who get can him see now its use two how our way new any day  that have with this from they will
        what when make like time just know take into year your good some them than then look only come over also 
        back work well even want give most next there which their other about these first water 
        """
        if character_size < 5:
            return_list = [word.strip().replace("\n", "") for word in most_used_words.split(" ")
                           if len(word.strip()) == character_size]
        else:
            return_list = self.get_words(character_size)
        return return_list

    def get_words(self, character_size: int):
        assert isinstance(character_size, int)
        if character_size in self.__words:
            return self.__words[character_size]
        return []

    @staticmethod
    def get_character_frequency():
        most_character_frequency = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
                                    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
                                    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
                                    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
                                    'Q': 0.10, 'Z': 0.07}
        return most_character_frequency
