from pprint import pprint
from typing import List
import os


class File:

    def __init__(self, path):
        self.__path = path

    def get_path(self) -> str:
        return self.__path


class Files:

    def __init__(self, dir_path):
        if not os.path.isdir(dir_path):
            raise NotADirectoryError()
        self.__dir_path = dir_path

    def __join_path(self, path):
        return os.path.join(self.__dir_path, path)

    def get_files(self) -> List[File]:
        result = list()
        for entity in os.listdir(self.__dir_path):
            entity_path = self.__join_path(entity)
            if os.path.isfile(entity_path):
                result.append(File(entity_path))
        return result


class SearchResult:
    _files: List[File] = list()

    def get_files(self) -> List[File]:
        return self._files

    def get_count(self) -> int:
        return int(len(self.get_files()))


class SearchResultSetter(SearchResult):

    def __init__(self):
        self._files = list()

    def add_file(self, file: File):
        self._files.append(file)


class Searcher:
    __files = list()
    __last_result: SearchResult = None

    def __init__(self, files):
        self.__files = files
        self.__last_result = None

    def __get_files_for_search(self) -> List[File]:
        if self.__last_result:
            return self.__last_result.get_files()
        return self.__files

    def search(self, search_string) -> SearchResult:
        result = SearchResultSetter()
        for file in self.__get_files_for_search():
            with open(file.get_path()) as search_file:
                if search_string in search_file.read():
                    result.add_file(file)
        self.__last_result = result
        return self.__last_result


class Command:

    def __init__(self, files: Files):
        self.__searcher = Searcher(files.get_files())

    def start(self):
        search_string = input('Введите строку поиска:')
        result = self.__searcher.search(search_string)
        if result.get_count() > 10:
            print('Много файлов ищите еще')
            self.start()
        print('Нашли в')
        print(result.get_files())


file_ser = Files('./Migrations/')
pprint(file_ser.get_files())


#command = Command()

# word = input('Введите строку поиска:')
# command = Command(FileForSearch())
# command.start()
# files = FileForSearch()
# searcher = Searcher(files.get_files()) # List[Files]
