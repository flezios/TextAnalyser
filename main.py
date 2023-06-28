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
    def __init__(self, file_name=None, pos=["VERB", "NOUN"], mwords=200, w=1920, h=1080, background="white") -> None:
        """позвать цепочку методов"""
        if file_name is None:
            raise Exception("не указан файл для анализа")
        self.file_name = file_name
        self.read_file()
        self.check_empty_file()
        self.prepare_text()
        self.make_analyzed_words(pos)
        self.check_empty_analyzed()
        self.find_popular_words(mwords)
        self.create_object(w, h, background, mwords)
        self.generate_wordcloud()
        self.save_image_to_file()
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

    def make_analyzed_words(self, inp) -> None | NoReturn:
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

    def find_popular_words(self, num) -> None:
        """поиск популярных слов"""
        words_counter = collections.Counter(self.analyzed_words)
        self.popular_words = words_counter.most_common(num)

    def create_object(self, w, h, background, mwords) -> None:
        self.wcl = wordcloud.WordCloud(
            width=w, height=h, background_color=background, max_words=mwords)

    def generate_wordcloud(self) -> None:
        """создание картинки"""
        words = collections.Counter(self.analyzed_words)
        self.wcl.generate_from_frequencies(dict(words))

    def save_image_to_file(self, name="wordcloud.png") -> None:
        """создание файла"""
        try:
            self.wcl.to_file(name)
        except:
            raise Exception("файл невозможно записать")

    def print_text(self) -> None:
        """выводит отчет по тексту"""
        print(
            f"----------\nвсего слов в тексте: [{len(self.words_clean)}]\n----------")
        print(
            f"найдено указанных частей речи: [{len(self.analyzed_words)}]\n---------")
        print(
            f"[{len(self.popular_words)}] наиболее популярных слов среди ваших частей речи: \n\n{self.popular_words}")


TextAnalyser("text.txt", ["VERB", "NOUN"], 20, 800, 400, "white")
