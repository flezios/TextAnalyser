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
        self.prepare_text()
        self.print_text()

    def read_file(self, mode="r", enc="UTF-8"):
        try:
            with open(self.file_name, mode, encoding=enc) as file:
                self.file = file
                self.text = self.file.read()
        except FileNotFoundError:
            raise Exception(f"файл {self.file_name} не найден!")

    def prepare_text(self):
        self.text = self.text.lower()
        self.words_unclean = self.text.split()
        self.words_clean = []
        punct = punctuation + "—"
        for word in (self.words_unclean):
            out = re.sub(rf"[{punct}]", "", word)
            if out:
                self.words_clean.append(out)

    def print_text(self):
        """выводит текст"""
        print(self.words_clean)


TextAnalyser("text.txt")
