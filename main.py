from typing import NoReturn
import pymorphy3
import re

"""
скачать txt
берет из файла txt
топ 10/20 глаголов/сущ/прилагательных в этом тексте
создать картинку - облако слов
"""


class TextAnalyser:
    def __init__(self, file_name=None) -> None:
        """позвать цепочку методов"""
        if file_name is None:
            raise Exception("не указан файл для анализа")
        self.file_name = file_name
        self.read_file()
        self.check_empty_file()
        self.prepare_text()
        self.make_analyzed_words()
        self.print_text()

    def read_file(self, mode="r", enc="UTF-8") -> None | NoReturn:
        """попытка чтения файла"""
        try:
            with open(self.file_name, mode, encoding=enc) as file:
                self.file = file
                self.text = self.file.read()
        except FileNotFoundError:
            raise Exception(f"файл {self.file_name} не найден!")

    def check_empty_file(self) -> None | NoReturn:
        """проверяет есть ли текст"""
        if not self.text:
            raise Exception(
                f"файл {self.file_name} пуст! используйте другой файл.")

    def prepare_text(self) -> None:
        """очишает и разделяет текст по словам + переводит в нижний регистр"""
        self.text = self.text.lower()
        self.words_clean = re.findall(r"\b[а-яё-]+\b", self.text)

    def make_analyzed_words(self, inp=["VERB", "NOUN"]):
        self.analyzed_words = []
        morph = pymorphy3.MorphAnalyzer()
        try:
            for word in self.words_clean:
                pars_word = morph.parse(word)[0]
                if pars_word.tag.POS in inp:
                    self.analyzed_words.append(pars_word.normal_form)
        except:
            raise Exception("неверная часть речи")
        print(self.analyzed_words)

    def print_text(self) -> None:
        """выводит текст и его длинну"""
        print(f"длинна текста: {len(self.words_clean)} слов.")
        print(self.analyzed_words)
        print(
            f"слов после парса: {len(self.analyzed_words)} слов.")


TextAnalyser("text.txt")
