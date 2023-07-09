"""
allows  to specify a "NoReturn" return
"""
from typing import NoReturn
import re
import collections
import chardet
import pymorphy3
import wordcloud

class HighInaccuracyError(Exception):
    pass

class TextAnalyser:
    """
    analyses the text in Russian with the arguments received as input

    returns wordcloud and a report

    """

    def __init__(
        self,
        input_file=None,
        parts_of_speech=None,
        mwords=None,
        width=None,
        height=None,
        name=None,
        background=None
    ) -> None:
        """
        calls a chain of methods

        accepts argent to work on and passes it on

        :input_file: name of the input file
        :parts_of_speech: the parts to search for
        :mwords: maximum number of words 
        :width: the width of the output image
        :height: height of output image
        :name: name of output image
        :background: background of output image
        """
        self.check_file_name(input_file)
        self.set_default_arguments(
            name_input_file=input_file,
            parts_of_speech=parts_of_speech,
            max_words=mwords,
            wordcloud_width=width,
            wordcloud_height=height,
            wordcloud_background=background,
            name_image_file=name)
        self.check_encoding_and_avaibality()
        self.read_file()
        self.check_empty_file()
        self.make_words()
        self.make_analyzed_words()
        self.check_empty_analyzed()
        self.find_popular_words()
        self.create_object()
        self.generate_wordcloud()
        self.save_image_to_file()
        self.print_report()

    def check_file_name(self, input_file) -> None | NoReturn:
        """
        checks whether the name of the file to be analysed is specified 
        """
        if input_file is None:
            raise ValueError(
                "не указан файл для анализа")

    def set_default_arguments(
        self,
        name_input_file,
        parts_of_speech,
        max_words,
        wordcloud_width,
        wordcloud_height,
        wordcloud_background,
        name_image_file
    ) -> None:
        """create variables and set default values where needed"""
        self.input_file = name_input_file
        self.file = None
        self.text = None
        self.words_clean = None
        self.analyzed_words = []
        self.popular_words = None
        self.encoding = None
        self.wcl = None
        if not parts_of_speech:
            parts_of_speech = ["VERB", "NOUN"]
        self.parts_of_speech = parts_of_speech
        if not max_words:
            max_words = 200
        self.max_words = max_words
        if not wordcloud_width:
            wordcloud_width = 1920
        self.wordcloud_width = wordcloud_width
        if not wordcloud_height:
            wordcloud_height = 1080
        self.wordcloud_height = wordcloud_height
        if not wordcloud_background:
            wordcloud_background = "white"
        self.wordcloud_background = wordcloud_background
        if not name_image_file:
            name_image_file = "wordcloud.png"
        self.name_image_file = name_image_file

    def check_encoding_and_avaibality(self) -> None:
        """
        checks the encoding of the file, if the accuracy is below 51% it raises an error
        """
        try:
            with open(self.input_file, "rb") as file:
                data = file.read()
                result = chardet.detect(data)
                confidence = result['confidence']
                if confidence >= 0.51:
                    self.encoding = result["encoding"]
                else:
                    raise HighInaccuracyError("не удается точно определить кодировку")
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"файл{self.input_file} не найден!") from exc
    def read_file(self, mode="r") -> None | NoReturn:
        """file read attempt"""
        try:
            with open(self.input_file, mode, encoding=self.encoding) as file:
                self.file = file
                self.text = self.file.read()
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"файл {self.input_file} не найден!") from exc

    def check_empty_file(self) -> None | NoReturn:
        """checks if there is text"""
        if not self.text:
            raise ValueError(
                f"файл {self.input_file} пуст! используйте другой файл.")

    def make_words(self) -> None:
        """clears and divides text by words + converts to lower case"""
        self.text = self.text.lower()
        self.words_clean = re.findall(r"\b[а-яё-]+\b", self.text)

    def make_analyzed_words(self) -> None | NoReturn:
        """separates by parts of speech"""
        self.analyzed_words = []
        morph = pymorphy3.MorphAnalyzer()
        try:
            for word in self.words_clean:
                pars_word = morph.parse(word)[0]
                if pars_word.tag.POS in self.parts_of_speech:
                    self.analyzed_words.append(pars_word.normal_form)
        except Exception as exc:
            raise ValueError("неверная часть речи") from exc

    def check_empty_analyzed(self) -> None | NoReturn:
        """checks the words to be analysed for their presence"""
        if not self.analyzed_words:
            raise IndexError(
                "нет проанализированных слов")

    def find_popular_words(self) -> None:
        """popular word search"""
        words_counter = collections.Counter(self.analyzed_words)
        self.popular_words = words_counter.most_common(self.max_words)

    def create_object(self) -> None:
        """creates an object to work with the "wordcloud" library"""
        self.wcl = wordcloud.WordCloud(
            width=self.wordcloud_width,
            height=self.wordcloud_height,
            background_color=self.wordcloud_background,
            max_words=self.max_words
        )

    def generate_wordcloud(self) -> None:
        """picture creation"""
        words = collections.Counter(self.analyzed_words)
        self.wcl.generate_from_frequencies(dict(words))

    def save_image_to_file(self) -> None:
        """file creation"""
        try:
            self.wcl.to_file(self.name_image_file)
        except Exception as exc:
            raise PermissionError(
                'файл невозможно записать') from exc

    def print_report(self) -> None:
        """outputs a text report"""
        print("----------")
        print(
            fr"кодировка файла: * {self.encoding} *")
        print(
            f"----------\nвсего слов в тексте: [{len(self.words_clean)}]\n----------")
        print(
            f"найдено указанных частей речи: [{len(self.analyzed_words)}]\n---------")
        print(
            f"[{len(self.popular_words)}] наиболее популярных слов среди ваших частей речи: "
            f"\n\n{self.popular_words}")


TextAnalyser("text.txt", ["VERB", "NOUN"], 20, 800, 400, background="white")
