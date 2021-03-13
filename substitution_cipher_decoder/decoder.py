#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 19:59:37 2020

@author: ademoguzhanozdemir
"""

import string
import pickle
from os.path import isfile

class WordDictionary:
    def __init__(self, en_dictionary="en_dictionary.dat"):
        self.__en_dic_words = {}
        self.__dic_path = en_dictionary
        self._dictionary()

    def __str__(self):
        return_txt = f" Sözlükte {len(self.__en_dic_words)}  ingilizce kelimele harf grubu mevcuttur."
        return return_txt

    def _check_file(func):
        def wrapper(self, *args, **kwargs):
            assert isfile(self.__dic_path), f"Not Found {self.__dic_path}"
            func(self, *args, **kwargs)
        return wrapper

    @_check_file
    def _dictionary(self):
        handle = open(self.__dic_path, "rb")
        self.__en_dic_words = pickle.load(handle)
        handle.close()

        return None

    def check(self, search_txt: str):
        """

        :search_txt: search_txt = searching a dictionary:
        :return: is check word in the dictionary
        """

        assert isinstance(search_txt, str)
        return_value = False
        if search_txt.strip() != "":
            size_search_txt = len(search_txt)
            if search_txt in self.__en_dic_words[size_search_txt]:
                return_value = True

        return return_value

    def most_popular_word(self, character_size: int):
        """

        :param character_size:  character count of the word
        :return most popular word:
        """
        assert isinstance(character_size, int)
        return_list = []
        two_character_word = """be to of in it on he as do at by we 
           or an my so up if go me no us"""
        two_character_words = two_character_word.split(" ")
        two_character_words = [x.strip().replace('\n', '') for x in two_character_words
                               if x.strip().replace('\n', '')]

        three_character_word = """the and for not you but his say her she 
           one all out who get can him see now its use two how our way new any day"""
        three_character_words = three_character_word.split(" ")
        three_character_words = [x.strip().replace('\n', '') for x in three_character_words
                                 if x.strip().replace('\n', '')]

        four_character_word = """that have with this from they will what
           when make like time just know take into year your good some them than 
           then look only come over also back work well even want give most next"""
        four_character_words = four_character_word.split(" ")
        four_character_words = [x.strip().replace('\n', '') for x in four_character_words
                                if x.strip().replace('\n', '')]

        five_character_word = """there which their other about these first water"""
        five_character_words = five_character_word.split(" ")
        five_character_words = [x.strip().replace('\n', '') for x in five_character_words
                                if x.strip().replace('\n', '')]

        if character_size == 2:
            return_list = two_character_words.copy()
        elif character_size == 3:
            return_list = three_character_words.copy()
        elif character_size == 4:
            return_list = four_character_words.copy()
        elif character_size == 5:
            return_list = five_character_words.copy()
        elif character_size in self.__en_dic_words:
            return_list = self.__en_dic_words[character_size]

        return return_list

    @_check_file
    def add_word(self, word):
        """

        :param word: add word
        :return:
        """
        assert isinstance(word, str)
        return_boolean = False
        word_size = len(word)
        if word not in self.__en_dic_words[word_size]:
            dic_words = self.__en_dic_words[word_size]
            dic_words.append(word)
            self.__en_dic_words[word_size] = dic_words
            handle = open(self.__dic_path, "wb")
            pickle.dump(self.__en_dic_words, handle)
            handle.close()
            return_boolean = True

        return return_boolean

    @_check_file
    def dell_word(self, word):
        """

               :param word: dell word
               :return:
               """
        assert isinstance(word, str)
        return_boolean = False
        word_size = len(word)
        if word in self.__en_dic_words[word_size]:
            dic_words = self.__en_dic_words[word_size]
            dic_words.remove(word)
            self.__en_dic_words[word_size] = dic_words
            handle = open(self.__dic_path, "wb")
            pickle.dump(self.__en_dic_words, handle)
            handle.close()
            return_boolean = True

        return return_boolean

    def get_words(self, word_size):
        """

        :param word_size: word length
        :return: words list
        """
        assert isinstance(word_size, int)
        if word_size in self.__en_dic_words:
            return self.__en_dic_words[word_size]

        return None

    @staticmethod
    def get_character_frequency():
        """

        :return: character_frequency list
        """
        most_character_frequency = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
                                    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
                                    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
                                    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
                                    'Z': 0.07}
        return most_character_frequency


class DecodingText:
    def __init__(self):
        self.__dictionary = WordDictionary()

    def __get_txt(self):
        assert isfile(self.__file_path), f"Not Found {self.__file_path}"

        file = open(self.__file_path, 'r', encoding='utf-8')
        md_raw_txt = file.read()
        file.close()

        return md_raw_txt

    def __clear_txt(self, md_raw_txt):
        punctuation_char = string.punctuation
        for c_punctuation in punctuation_char:
            md_raw_txt = md_raw_txt.replace(c_punctuation, ' ')
        md_raw_txt = md_raw_txt.upper()
        md_raw_txt = md_raw_txt.replace('\n', ' ')
        md_raw_txt = md_raw_txt.split(' ')
        md_raw_txt = [x.strip() for x in md_raw_txt if x.strip()]
        md_raw_txt = " ".join(md_raw_txt)
        return md_raw_txt

    def __get_character(self, get_list: list, get_encrypted: str):
        return_value = {}
        f_undefined_character = []
        len_txt = 100 / len(get_encrypted.replace(' ', ''))
        md_character = string.ascii_uppercase
        for word in get_list:
            for character in word:
                if character in md_character:
                    if character not in return_value:
                        return_value[character] = 0
                    return_value[character] += 1
                else:
                    f_undefined_character.append(character)
        for key in return_value:
            return_value[key] = round(return_value[key] * len_txt, 2)

        return return_value, f_undefined_character

    def __lower_index(self, txt: str):
        l_index = []
        for index_txt in range(len(txt)):
            if txt[index_txt].islower():
                l_index.append(index_txt)
        return l_index

    def __string_to_group(self, get_list: list, list_count: int):
        """

        :param get_list: gel list
        :param list_count: list count
        :return: return list value
        """
        assert isinstance(list_count, int)

        list_count += 1
        most_char_word = {}
        i: int
        for i in range(2, list_count):
            most_char_word[i] = self.__dictionary.most_popular_word(i)

        char_words = {}
        min_char_size = list_count
        for word in get_list:
            word_size = len(word)
            if 1 < word_size <= list_count:
                if word_size < min_char_size:
                    min_char_size = word_size
                if word_size not in char_words:
                    char_words[word_size] = [word]
                elif word not in char_words[word_size]:
                    char_words[word_size] += [word]

        return_list = []
        i: int
        for i in range(min_char_size, list_count):
            return_list.append([char_words[i], most_char_word[i]])

        return return_list

    def __list_match(self, l_matchers: list, most_used: list):
        """

        :param l_matchers: word group
        :param most_used:  most_used word
        :return:
        """
        return_list = {}
        if l_matchers and most_used:
            for l_match in l_matchers:
                l_index = self.__lower_index(l_match)
                if len(l_index) == 1:
                    return_list[l_match] = [x for x in most_used
                                            if x[l_index[0]] == l_match[l_index[0]]]
                elif len(l_index) == 2:
                    return_list[l_match] = [x for x in most_used
                                            if x[l_index[0]] == l_match[l_index[0]] and
                                            x[l_index[1]] == l_match[l_index[1]]]
                elif len(l_index) == 3:
                    return_list[l_match] = [x for x in most_used
                                            if x[l_index[0]] == l_match[l_index[0]] and
                                            x[l_index[1]] == l_match[l_index[1]] and
                                            x[l_index[2]] == l_match[l_index[2]]]
                elif len(l_index) == 4:
                    return_list[l_match] = [x for x in most_used
                                            if x[l_index[0]] == l_match[l_index[0]] and
                                            x[l_index[1]] == l_match[l_index[1]] and
                                            x[l_index[2]] == l_match[l_index[2]] and
                                            x[l_index[3]] == l_match[l_index[3]]]
                elif len(l_index) == 5:
                    return_list[l_match] = [x for x in most_used
                                            if x[l_index[0]] == l_match[l_index[0]] and
                                            x[l_index[1]] == l_match[l_index[1]] and
                                            x[l_index[2]] == l_match[l_index[2]] and
                                            x[l_index[3]] == l_match[l_index[3]] and
                                            x[l_index[4]] == l_match[l_index[4]]]
        return return_list

    def __txt_to_list(self, get_list):
        to_list = get_list.split(' ')
        to_list = [x.strip() for x in to_list if x.strip() and not x.islower()]
        return to_list

    def __upper_index(self, txt):
        f_u_index = []
        for index_txt in range(len(txt)):
            if txt[index_txt].isupper():
                f_u_index.append(index_txt)
        return f_u_index

    def __intersection_list(self, f_u_index, f_key, f_character_tolerance, f_uygun):
        tolerance_char = f_character_tolerance[f_key[f_u_index[0]]]
        list_txt = [x[f_u_index[0]] for x in f_uygun[f_key]]
        f_matched = set(tolerance_char) & set(list_txt)
        return f_matched

    def __write_password(self, encrypted_char, s_list, g_list):
        f_u_index = self.__upper_index(s_list)
        for encrypted_index in f_u_index:
            encrypted_char[s_list[encrypted_index]] = g_list[encrypted_index]
        return encrypted_char

    def __check_grammar(self, group: list, old_c: str, new_c: str):
        grammar_check: bool = False
        grammar_checker = []
        for item in group:
            enc = item[0]
            control = [self.__dictionary.check(search_txt=x.replace(old_c, new_c)) for x in enc
                       if x.replace(old_c, new_c).islower() and old_c in x]
            grammar_checker += control
            if False in control:
                break

        if False not in grammar_checker:
            grammar_check = True

        return grammar_check

    def writeFile(self):
        if self.__raw_encrypted_txt is not None:
            raw_encrypted_txt = self.__raw_encrypted_txt
            raw_encrypted_txt = raw_encrypted_txt.upper()
            for p_key in self.__password_key:
                decoding_char = self.__password_key[p_key]
                encryp_char = p_key
                raw_encrypted_txt = raw_encrypted_txt.replace(encryp_char, decoding_char)

            for un_char in self.__undefined_character:
                raw_encrypted_txt = raw_encrypted_txt.replace(un_char, un_char.lower())

            file = open('acik_metin.txt', 'w', encoding='utf-8')
            file.write(raw_encrypted_txt)
            file.close()

    def decoding_txt(self, file_path):
        self.__file_path = file_path
        most_character_frequency = self.__dictionary.get_character_frequency()
        most_frequency = [x for x in most_character_frequency]
        index_character = [*string.ascii_lowercase]
        lower_character = index_character.copy()

        password_index_map = []
        self.__password_key = {}
        self.__undefined_character = []

        try:
            self.__raw_encrypted_txt = self.__get_txt()
        except FileNotFoundError as error_txt:
            self.__raw_encrypted_txt = None
            return error_txt

        if self.__raw_encrypted_txt:
            clear_raw_encrypted_txt = self.__clear_txt(self.__raw_encrypted_txt)
            raw_encrypted_array = self.__txt_to_list(clear_raw_encrypted_txt)

            frequency_tolerance = 1.5
            increased_tolerance = 1.5

            list_group_size = 6
            character_tolerance = {}

            character_frequency_tolerance = dict([(c.upper(), frequency_tolerance) for c in lower_character])

            character_frequency, self.__undefined_character = self.__get_character(raw_encrypted_array,
                                                                                   clear_raw_encrypted_txt)

            clear_array = []

            for undefined in self.__undefined_character:
                clear_array = [x for x in raw_encrypted_array if undefined not in x]

            decoding_txt = " ".join(clear_array)

            for character in most_frequency:
                if character not in character_tolerance:
                    min_frequency = character_frequency[character] - character_frequency_tolerance[character]
                    min_frequency = round(min_frequency, 2)
                    if min_frequency < 0:
                        min_frequency = 0
                    max_frequency = character_frequency[character] + character_frequency_tolerance[character]
                    max_frequency = round(max_frequency, 2)
                    character_tolerance[character] = [x.lower() for x in most_character_frequency
                                                      if min_frequency <= most_character_frequency[x] <= max_frequency]
                    if len(character_tolerance[character]) == 1:
                        new_char = character_tolerance[character][0].lower()
                        self.__password_key[character] = new_char

                        pass_index = index_character.index(character.lower())
                        new_index = index_character.index(new_char)
                        password_index_map.append([pass_index, new_index])

                        lower_character.remove(new_char)
                        most_character_frequency.pop(character_tolerance[character][0].upper())

            for index_password in self.__password_key:
                remove_character = self.__password_key[index_password]
                for char_tolerance in character_tolerance:
                    cc_tolerance = character_tolerance[char_tolerance]
                    if remove_character in cc_tolerance:
                        cc_tolerance.remove(remove_character)
                        character_tolerance[char_tolerance] = cc_tolerance

            failed_decoding = 0

            while len(self.__password_key) < 26:
                for p_key in self.__password_key:
                    decoding_txt = decoding_txt.replace(p_key.strip(), self.__password_key[p_key])

                decoding_array = self.__txt_to_list(decoding_txt)
                group_words = self.__string_to_group(decoding_array, list_group_size)

                keys_count = len(self.__password_key)

                for group_word in group_words:

                    ff_pass_word = group_word[0]
                    ff_en_cok = group_word[1]

                    if ff_pass_word:
                        uygun = self.__list_match(ff_pass_word, ff_en_cok)

                        for key in uygun:
                            u_index = self.__upper_index(key)
                            if len(u_index) == 1:
                                s_matches = self.__intersection_list(u_index, key, character_tolerance, uygun)

                                if len(s_matches) == 1:

                                    password_character = key[u_index[0]]
                                    new_character = "".join(s_matches).lower()

                                    grammar = self.__check_grammar(group_words, password_character, new_character)

                                    if grammar:
                                        self.__password_key[password_character] = new_character
                                        lower_character.remove(new_character)
                                        pass_index = index_character.index(password_character.lower())
                                        new_index = index_character.index(new_character)
                                        password_index_map.append([pass_index, new_index])
                                        character_tolerance[password_character] = []

                                        if new_character.upper() in most_character_frequency:
                                            most_character_frequency.pop(new_character.upper())

                                        for char_tolerance in character_tolerance:
                                            cc_tolerance = character_tolerance[char_tolerance]
                                            if new_character in cc_tolerance:
                                                cc_tolerance.remove(new_character)
                                                character_tolerance[char_tolerance] = cc_tolerance

                                    else:
                                        new_tolerance = character_tolerance[password_character].copy()
                                        if new_tolerance:
                                            new_tolerance.remove(new_character)
                                        character_tolerance[password_character] = new_tolerance

                for char_x in character_tolerance:
                    if not character_tolerance[char_x] or keys_count == len(self.__password_key):
                        if char_x not in self.__password_key:
                            character_frequency_tolerance[char_x] += increased_tolerance
                            char_freq = character_frequency[char_x]
                            char_freq_tol = character_frequency_tolerance[char_x]
                            min_frequency = char_freq - char_freq_tol
                            min_frequency = round(min_frequency, 2)
                            if min_frequency < 0:
                                min_frequency = 0
                            max_frequency = character_frequency[char_x] + character_frequency_tolerance[char_x]
                            max_frequency = round(max_frequency, 2)

                            character_tolerance[char_x] = [x.lower() for x in most_character_frequency
                                                           if min_frequency <= most_character_frequency[
                                                               x] <= max_frequency]

                if len(lower_character) == 1:
                    last_pas_character = [x for x in character_tolerance if character_tolerance[x] == lower_character]
                    self.__password_key[last_pas_character[0]] = lower_character[0]

                if (keys_count == len(self.__password_key)):
                    failed_decoding += 1

                if failed_decoding == 26:
                    break

            if len(self.__password_key) == 26:
                return self.__password_key
            else:
                return 'Decoding failed'


def main():
    decode = DecodingText()
    decode.decoding_txt("sifreli_metin.txt")
    decode.writeFile()

if __name__ == '__main__':
    main()
