"""
скачать txt
берет из файла txt
топ 10/20 глаголов/сущ/прилагательных в этом тексте
создать картинку - облако слов
"""
"""
content = open("text.txt", "r", encoding="UTF-8")
# открытие файла
text = content.read()
# прочтение файла
print(text)
"""


class TextAnalyser:
    def __init__(self, file="text.txt", mode="r", encoding="UTF-8") -> None:
        """позвать цепочку методов"""
        self.open_file(file, mode, encoding)
        self.make_text()
        self.print_text()

    def open_file(self, file, mode, enc):
        """создает контент из файла"""
        self.content = open(file, mode, encoding=enc)

    def make_text(self):
        """создает текст"""
        self.text = self.content.read()

    def print_text(self):
        """выводит текст"""
        print(self.text)


TextAnalyser()
