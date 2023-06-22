from typing import NoReturn
from string import punctuation
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
        """очишает и разделяет текст по словам"""
        self.text = self.text.lower()
        self.punct = punctuation + "—"
        self.words_clean = re.findall(r"\b[\w-]+\b", self.text)

    def print_text(self) -> None:
        """выводит текст и его длинну"""
        print(self.words_clean)
        print(f"длинна текста: {len(self.words_clean)} слов.")


TextAnalyser("text.txt")
