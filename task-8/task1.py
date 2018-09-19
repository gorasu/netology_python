from typing import List


class File:

    def get_path(self) -> str:
        pass


class Files:

    def get_files(self) -> List[File]:
        pass


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

# word = input('Введите строку поиска:')
# command = Command(FileForSearch())
# command.start()
# files = FileForSearch()
# searcher = Searcher(files.get_files()) # List[Files]
