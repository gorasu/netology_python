from pprint import pprint
from src.parser import *

file_list = ['./file/newsafr.xml', './file/newsafr.json', './file/newsafr.txt']

for file in file_list:
    factory = ParserFactory(file)
    parser = factory.get_parser()
    parser.parse()
    top_word = TopNewsWord(parser.get_news())
    print('Парсер', type(parser))
    pprint(top_word.by_letter_count(6))
