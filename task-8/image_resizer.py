# convert input.jpg -resize 200 output.jpg
# sips --resampleWidth 200 input.jpg
import os
import shutil
import subprocess
from sys import platform


class ExceptionIsNotImage(Exception):
    __file = ''

    def set_file(self, file):
        self.__file = file

    def get_file(self):
        return self.__file


class ResizeSettings:

    def __init__(self, source_file, result_dir=None):
        self.__width = None
        self.__result_dir = result_dir
        self.__source_file = source_file

    def is_image(self):
        return os.path.splitext(self.source_file)[1].lower().strip('.') in ['jpg', 'png', 'gif']

    @property
    def width(self):
        if not self.__width or self.__width <= 0:
            raise ValueError('width must be int and > 0')
        return self.__width

    @width.setter
    def width(self, value: int):
        self.__width = value

    @property
    def source_file(self):
        return self.__source_file

    @property
    def result_file(self):
        dir_result = self.__get_result_dir()
        file_name = os.path.basename(self.source_file)
        if self.__is_path_same():
            file_name = 'new_' + file_name
        return os.path.join(dir_result, file_name)

    def __get_result_dir(self):
        result_dir = self.__result_dir

        if self.__result_dir is None:
            result_dir = os.path.dirname(self.source_file)

        if not os.path.exists(result_dir):
            os.mkdir(os.path.abspath(result_dir))

        return result_dir

    def __is_path_same(self):
        return self.__get_result_dir() == os.path.dirname(self.source_file)


class Resizer:

    def resize(self, resize_settings: ResizeSettings):
        if not os.path.isfile(resize_settings.source_file):
            raise FileNotFoundError()
        if not resize_settings.is_image():
            exception = ExceptionIsNotImage()
            exception.set_file(resize_settings.source_file)
            raise exception
        self._resize_command(resize_settings)

    def _resize_command(self, resize_settings: ResizeSettings):
        raise NotImplementedError('Command "_resize_command" is not implemented')


class ResizerMac(Resizer):

    def _resize_command(self, resize_settings: ResizeSettings):
        shutil.copyfile(resize_settings.source_file, resize_settings.result_file)
        subprocess.run('sips --resampleWidth {width} {result} '.format(width=resize_settings.width
                                                                       , result=resize_settings.result_file),
                       shell=True)


class ResizerLinux(Resizer):

    def _resize_command(self, resize_settings: ResizeSettings):
        subprocess.run(
            'convert {source} -resize {width} {result} '.format(
                source=resize_settings.source_file
                , width=resize_settings.width
                , result=resize_settings.result_file)
            , shell=True)


class ResizerWindows(Resizer):

    def __get_command(self):
        return os.path.abspath(os.path.join('.', 'task-8.4-files', 'convert.exe'))

    def _resize_command(self, resize_settings: ResizeSettings):
        command = '{command} {source_file} {width} -resize {result_file}'.format(self.__get_command()
                                                                       , resize_settings.source_file
                                                                       , resize_settings.width
                                                                       , resize_settings.result_file )
        subprocess.run(command, shell=True)


def get_resizer() -> Resizer:
    if platform == "linux" or platform == "linux2":
        return ResizerLinux()
    elif platform == "darwin":
        return ResizerMac()
    elif platform == "win32":
        return ResizerWindows()


resizer = get_resizer()
source_folder = os.path.join('.', 'task-8.4-files', 'Source')
result_folder = os.path.join('.', 'task-8.4-files', 'Result')
error_list = []
for file in os.listdir(source_folder):
    try:
        resizer_config = ResizeSettings(os.path.join(source_folder, file), result_folder)
        resizer_config.width = 200
        resizer.resize(resizer_config)
    except ExceptionIsNotImage as e:
        error_list.append(e)
        continue

for e in error_list:
    error_str = '\n ERROR: {} не изображение, трансформация не удалась'.format(e.get_file())
    print(error_str)
