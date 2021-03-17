# -*- coding: utf-8 -*-
"""
@author: Oguzhan Ozdemir
"""
# pylint: disable=C0116
# pylint: disable=R0201
import string
from dictionary_layer import WordDictionary


class DecoderText:
    def __init__(self):
        self.__dictionary = WordDictionary()
        self.__get_char_freq_tolerance()
        self._crypto_key = {}
        self.__undefined_character = {}
        self._character_frequency = {}
        self._character_frequency_tolerance = self.__get_char_freq_tolerance()
        self.most_character_frequency = self.__dictionary.get_character_frequency()

    def _clear_txt(self, raw_txt: str):
        punctuation_char = string.punctuation
        raw_txt = raw_txt.replace('\n', ' ')
        for c_punctuation in punctuation_char:
            raw_txt = raw_txt.replace(c_punctuation, ' ')
        raw_txt = raw_txt.replace("i", "I")
        raw_txt = raw_txt.upper()
        raw_txt = [txt.strip() for txt in raw_txt.split(' ') if txt.strip()]
        return " ".join(raw_txt)

    def __txt_to_list(self, get_list):
        return get_list.strip().split(' ')

    def __get_character_frequency(self, word_list: list, word_size: int):
        assert isinstance(word_size, int)
        return_value = {}
        f_undefined_character = []
        len_txt = 100 / word_size
        md_character = string.ascii_uppercase
        for word in word_list:
            for character in word:
                if character in md_character:
                    if character not in return_value:
                        return_value[character] = 0
                    return_value[character] += 1
                else:
                    f_undefined_character.append(character)
        for key in return_value:
            return_value[key] = round(return_value[key] * len_txt, 2)
        self._character_frequency = return_value
        return return_value, f_undefined_character

    def _delete_undefined_character(self, word_list: list):
        clear_array = []
        for word in word_list:
            found_undefined = False
            for letter in word:
                if letter.lower() not in string.ascii_lowercase:
                    found_undefined = True
                    break
            if not found_undefined:
                clear_array.append(word)
        return clear_array

    def __return_txt(self, txt: str) -> str:
        if txt:
            txt = txt.upper()
            for key in self._crypto_key:
                txt = txt.replace(key, str(self._crypto_key[key]))
        return txt

    def __get_char_freq_tolerance(self, frequency_tolerance: int = 1.5):
        return dict([(char, frequency_tolerance) for char in string.ascii_uppercase])

    def _get_char_map(self, char_frequency: dict) -> dict:
        key_map = {}
        for character in char_frequency:
            tolerance = self._character_frequency_tolerance[character]
            min_frequency = self._character_frequency[character] - tolerance
            min_frequency = round(min_frequency, 2)
            if min_frequency < 0:
                min_frequency = 0
            max_frequency = self._character_frequency[character] + tolerance
            max_frequency = round(max_frequency, 2)
            key_map[character] = [_char.lower() for _char in self.most_character_frequency
                                  if min_frequency <= self.most_character_frequency[_char] <= max_frequency]
        return key_map

    def __match_char(self, chars_map: dict) -> dict:
        for character in chars_map:
            if len(chars_map[character]) == 1:
                self._crypto_key[character] = chars_map[character][0].lower()
                self.most_character_frequency.pop(chars_map[character][0].upper())
        for decoder_char in self._crypto_key:
            _char = self._crypto_key[decoder_char]
            for char_index in chars_map:
                chars_map[char_index] = [char for char in chars_map[char_index] if char != _char]
            if decoder_char in chars_map:
                chars_map.pop(decoder_char)
        return chars_map

    def _solve_txt(self, txt_list: list) -> list:
        for crypto_key in self._crypto_key:
            key = self._crypto_key[crypto_key]
            txt_list = [txt.replace(crypto_key, key) for txt in txt_list]
        return txt_list

    def __is_solve(self, text_array) -> list:
        resoled_list = set()
        for text in text_array:
            not_resolved = 0
            txt_set = set(text)
            if len(txt_set) > 1:
                for char in txt_set:
                    if char.isupper():
                        not_resolved += 1
                if not_resolved == 1:
                    resoled_list.add(text)
        return list(resoled_list)

    def _get_word(self, word_map: dict, word_size: int):
        most_used_word = self.__dictionary.get_most_popular_words(word_size)
        word_list = []
        for word in most_used_word:
            is_suitable = True
            for i in word_map:
                if word[i] != word_map[i]:
                    is_suitable = False
                    break
            if is_suitable:
                word_list.append(word)
        return word_list

    def create_word_map(self, word: str):
        unknown_letter = {}
        known_letter = {}
        for i in range(len(word)):
            if word[i].islower():
                known_letter[i] = word[i]
            else:
                unknown_letter[i] = word[i]
        return known_letter, unknown_letter

    def _remove_letter(self, words: list, know_character: dict) -> set:
        for i in range(len(words)):
            for know_index in know_character:
                word = words[i].replace(know_character[know_index], "")
                words[i] = word
        return set(words)

    def __first_value(self, dic_list: dict):
        first_value = ""
        if dic_list:
            for index in dic_list:
                first_value = str(dic_list[index]).upper()
        return first_value

    def __just_one_unknown(self, character: str, txt_array: list):
        grammar_words = set()
        for word in txt_array:
            if character in word:
                letters = [letter for letter in word if letter.isupper()]
                if len(letters) == 1:
                    grammar_words.add(word)
        return list(grammar_words)

    def __remove_map_char(self, char_map: dict, unknown_char: str, new_char: str):
        if unknown_char in char_map:
            char_map.pop(unknown_char)
        for char in char_map:
            if new_char in char_map[char]:
                new_map = char_map[char]
                new_map.remove(new_char)
                if new_map:
                    char_map[char] = new_map
            if not char_map[char]:
                char_map[char] = self.__update_map_tolerance(char)
        return char_map

    def __update_map_tolerance(self, char: dict):
        self._character_frequency_tolerance[char] += 1.5
        tolerance = self._character_frequency_tolerance[char]
        min_frequency = self._character_frequency[char] - tolerance
        min_frequency = round(min_frequency, 2)
        if min_frequency < 0:
            min_frequency = 0
        max_frequency = self._character_frequency[char] + tolerance
        max_frequency = round(max_frequency, 2)
        key_value = list(self._crypto_key.values())
        key_map = [_letter.lower() for _letter in self.most_character_frequency
                   if min_frequency <= self.most_character_frequency[_letter] <= max_frequency and
                   _letter.lower() not in key_value]
        return key_map

    def decoding_text(self, text: str) -> str:
        text = str(text)
        if text.strip():
            raw_txt = text
            clean_txt = self._clear_txt(text)

            if clean_txt:
                charter_size = len(clean_txt.replace(' ', ''))
                text_array = self.__txt_to_list(clean_txt)

                character_frequency, self.__undefined_character = self.__get_character_frequency(text_array,
                                                                                                 charter_size)

                if len(self.__undefined_character) > 0:
                    text_array = self._delete_undefined_character(text_array)

                char_map = self._get_char_map(character_frequency)
                char_map = self.__match_char(char_map)
                text_array = self._solve_txt(text_array)

                while len(character_frequency) > len(self._crypto_key):
                    resoled_list = self.__is_solve(text_array)
                    for txt in resoled_list:
                        know_character, unknown_character = self.create_word_map(txt)
                        dictionary_word = self._get_word(know_character, len(txt))
                        unk_char = self.__first_value(unknown_character)

                        if unk_char not in char_map:
                            continue
                        character_prediction = char_map[unk_char]
                        if not character_prediction:
                            continue
                        unknown_word = self._remove_letter(dictionary_word, know_character)
                        intersection_char = set(character_prediction) & unknown_word

                        if len(intersection_char) == 1:
                            new_char = "".join(intersection_char)
                            test_words = self.__just_one_unknown(unk_char, text_array)
                            if test_words:
                                is_not_wrong = True
                                for word in test_words:
                                    word = word.replace(unk_char, new_char)

                                    if not self.__dictionary.find_word(word):
                                        is_not_wrong = False
                                if is_not_wrong:
                                    self._crypto_key[unk_char] = new_char
                                    char_map = self.__remove_map_char(char_map, unk_char, new_char)
                    text_array = self._solve_txt(text_array)

                    if len(char_map) == 1:
                        for index in char_map:
                            self._crypto_key[index] = char_map[index][0]
                        break
        else:
            return ""
        new_txt = self.__return_txt(raw_txt)
        return new_txt
