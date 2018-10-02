from typing import List, Callable
import os


class File:

    def __init__(self, path):
        self.__path = path

    def path(self) -> str:
        return self.__path

    def read(self):
        with open(self.__path) as file:
            return file.read()


class Files:

    def __init__(self, dir_path):
        if not os.path.isdir(dir_path):
            raise NotADirectoryError()
        self.__dir_path = dir_path

    def _join_path(self, path):
        return os.path.join(self.__dir_path, path)

    def get_files(self, file_filter: Callable = None) -> List[File]:
        result = list()
        for entity in os.listdir(self.__dir_path):
            entity_path = self._join_path(entity)
            if os.path.isfile(entity_path) and (file_filter and file_filter(entity_path)):
                result.append(File(entity_path))
        return result


class SearchResult:
    _files: List[File] = list()

    @property
    def files(self) -> List[File]:
        return self._files

    @property
    def count(self) -> int:
        return len(self.files)


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
        self.rest_search_result()

    def _get_files_for_search(self) -> List[File]:
        if self.__last_result:
            return self.__last_result.files
        return self.__files

    def search(self, search_string) -> SearchResult:
        result = SearchResultSetter()
        for file in self._get_files_for_search():
            if search_string in file.read():
                result.add_file(file)
        self.__last_result = result
        return self.__last_result

    def rest_search_result(self):
        self.__last_result = None


class Command:

    def __init__(self, files: List[File]):
        self.__searcher = Searcher(files)

    def _show_result(self, result: SearchResult):
        print('Нашли в:')
        for file in result.files:
            print(file.path())
        print("Всего:", result.count)

    def search_result(self, search_string):
        return self.__searcher.search(search_string)

    def start(self):
        search_string = input('Введите строку поиска:')
        result = self.search_result(search_string)
        if not result.count:
            print('Ничего не найдено, начните поиск заново')
            self.__searcher.rest_search_result()
        else:
            self._show_result(result)
        self.start()


path = os.path.abspath(os.path.dirname(__file__))
file_ser = Files(os.path.abspath(os.path.join(path, 'Migrations')))
command = Command(file_ser.get_files(lambda file_path: os.path.splitext(file_path)[1] == '.sql'))
command.start()
