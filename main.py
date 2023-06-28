from typing import NoReturn
import pymorphy3
import re
import collections
import wordcloud

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
        self.check_empty_analyzed()
        self.find_popular_words()
        self.generate_wordcloud()
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

    def make_analyzed_words(self, inp=["VERB", "NOUN"]) -> None | NoReturn:
        """разделяет по частям речи"""
        self.analyzed_words = []
        morph = pymorphy3.MorphAnalyzer()
        try:
            for word in self.words_clean:
                pars_word = morph.parse(word)[0]
                if pars_word.tag.POS in inp:
                    self.analyzed_words.append(pars_word.normal_form)
        except:
            raise Exception("неверная часть речи")

    def check_empty_analyzed(self) -> None | NoReturn:
        """проверяет есть ли проанализ. слова"""
        if not self.analyzed_words:
            raise Exception(
                "нет проанализированных слов")

    def find_popular_words(self, num=10) -> None:
        """поиск популярных слов"""
        words_counter = collections.Counter(self.analyzed_words)
        self.popular_words = words_counter.most_common(num)

    def generate_wordcloud(self, name="wordcloud.png") -> None:
        """создание картинки"""
        wcl = wordcloud.WordCloud(
            width=800, height=400, background_color='white')
        words = collections.Counter(self.analyzed_words)
        wcl.generate_from_frequencies(dict(words))
        wcl.to_file(name)

    def print_text(self) -> None:
        """выводит текст и его длинну"""
        print(self.popular_words)


TextAnalyser("text.txt")
