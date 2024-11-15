import datetime
import os
import pathlib
import threading
import traceback
import subprocess
import re
import subprocess
import stat
from exif import Image
from win32_setctime import setctime
from PyQt5.QtCore import QThread, pyqtSignal


def change_date(path_folder: pathlib.Path, time: str) -> None:
    if '.' in time:
        result_time = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S.%f').timestamp()
    else:
        result_time = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S').timestamp()
    # result_time = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S.%f').timestamp()
    setctime(path_folder, result_time)
    os.utime(path_folder, times=(result_time, result_time))  # Изменен, открыт


class RedateDirAndFile(QThread):
    progress = pyqtSignal(int)  # Сигнал для progressBar
    status = pyqtSignal(str)  # Сигнал для статус бара
    messageChanged = pyqtSignal(str, str)
    errors = pyqtSignal()

    def __init__(self, incoming_data):  # Список переданных элементов.
        QThread.__init__(self)
        self.folder = incoming_data['folder']
        self.start_date = incoming_data['start_date']
        self.device_count = incoming_data['device_count']
        self.button = incoming_data['button']
        self.logging = incoming_data['logging']
        self.queue = incoming_data['queue']
        self.default_path = incoming_data['default_path']
        self.event = threading.Event()
        self.count = 0
        self.percent = 0
        self.progress_val = 0
        self.error_text = []

    def get_date(self, path: pathlib.Path) -> str:
        time = datetime.datetime.fromtimestamp(os.path.getctime(path)).time()
        return str(self.start_date) + ' ' + str(time)

    def folder_tree(self, path: pathlib.Path) -> dict:
        for obj in os.listdir(path):
            if os.path.isdir(pathlib.Path(path, obj)):
                info = os.stat(pathlib.Path(path, obj))                
                if info.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
                    continue
                date = self.get_date(path)
                answer = self.folder_tree(pathlib.Path(path, obj))
                if answer['error']:
                    return {'error': True, 'message': 'abort'}
                change_date(pathlib.Path(path, obj), date)
            else:
                format_file = obj.rpartition('.')[2]
                if format_file.lower() not in ['tif', 'tiff', 'jpeg', 'jpg', 'png']:
                    self.logging.info(f'Формат файла {obj} не подходит под указанные, пропускаем')
                    continue
                try:
                    answer = self.change_file(pathlib.Path(path, obj))
                    if answer['error']:
                        return {'error': True, 'message': 'abort'}
                except BaseException as exc:
                    self.logging.error(f"Не удалось изменить время у файла {pathlib.Path(path, obj)}")
                    self.logging.error(f"Ошибка: {exc}")
                    self.logging.info('-------------------------------------------')
        return {'error': False, 'message': 'continue'}

    def change_file(self, path: pathlib.Path) -> dict:
        if self.pause_threading():
            self.logging.warning('Прервано пользователем')
            self.progress.emit(0)
            os.chdir(self.default_path)
            self.button.setText('Старт')
            self.logging.info('----------------Прервано redate_file_and_photo----------------')
            return {'error': True, 'message': 'abort'}
        self.logging.info(f"Изменяем время в файле {path.name} (папка {path})")
        self.status.emit(f"Изменяем время в файле {path.name} (папка {os.path.basename(path.parent)})")
        time_file = []
        time = '08:10:15'
        sum_time = str(self.start_date) + ' ' + str(time)
        old_name = path.name
        name = path.name
        if ' ' in path.name:
            name = path.name.replace(' ', '_')
            os.rename(path, pathlib.Path(path.parent, name))
        redate_file = pathlib.Path(path.parent, name)
        exif = f"{str(pathlib.Path(self.default_path, 'exiftool', 'exiftool.exe'))} {str(redate_file)}"
        if redate_file.name.endswith('.tif') or redate_file.name.endswith('.tiff'):
            self.logging.info(f"Файл типа tif")
            file = subprocess.run(exif, capture_output=True, text=True)
            for property in file.stdout.split('\n'):
                if re.findall(r'\d{4}:\d{2}:\d{2}\s\d{2}:\d{2}:\d{2}', property.partition(':')[2]):
                    str_time = property.partition(':')[2].strip()
                    if '+' in str_time:
                        str_time = str(datetime.datetime.strptime(str_time, '%Y:%m:%d %H:%M:%S%z').time())
                        time_file.append(str_time)
                    else:
                        if '.' in str_time:
                            str_time = str_time.rpartition('.')[0]
                        time_file.append(str(datetime.datetime.strptime(str_time, '%Y:%m:%d %H:%M:%S').time()))
            if time_file:
                time = min(time_file)
            sum_time = str(self.start_date) + ' ' + str(time)
            self.logging.info(f"Меняем время, если есть. Time - {sum_time}")
            exif = str(pathlib.Path(self.default_path, 'exiftool', 'exiftool.exe')) + ' -ModifyDate="' + sum_time + '" -DateTimeOriginal="' + sum_time + '" -CreateDate="' + sum_time + '" ' + str(redate_file)
            subprocess.run(exif)
            del_file = [file for file in os.listdir(path.parent) if file.endswith('_original')]
            if del_file:
                for file in del_file:
                    os.remove(pathlib.Path(path.parent, file))
        else:
            self.logging.info(f"Файл другого типа")
            with open(redate_file, 'rb') as read_file:
                image = Image(read_file)
                if image.has_exif:
                    time_file.append(str(datetime.datetime.strptime(image.datetime_original, '%Y:%m:%d %H:%M:%S').time()))
                    time_file.append(str(datetime.datetime.strptime(image.datetime_digitized, '%Y:%m:%d %H:%M:%S').time()))
                    time_file.append(str(datetime.datetime.strptime(image.datetime, '%Y:%m:%d %H:%M:%S').time()))
                    if time_file:
                        time = min(time_file)
                    sum_time = str(self.start_date) + ' ' + str(time)
                    self.logging.info(f"Меняем время, если есть. Time - {sum_time}")
                    image.datetime_original = sum_time
                    image.datetime_digitized = sum_time
                    image.datetime = sum_time
                    with open(path, 'wb') as write_file:
                        write_file.write(image.get_file())
                else:
                    self.error_text.append(f"У файла {path.name} ({os.path.basename(path.parent)}) нет exif данных")
        # date = self.get_date(path)
        if name != old_name:
            os.rename(redate_file, pathlib.Path(path.parent, old_name))
        change_date(path, sum_time)
        self.progress_val += self.percent
        self.progress.emit(self.progress_val)
        self.logging.info(f"Закончили менять время")
        return {'error': False, 'message': 'continue'}

    def run(self):
        try:
            self.logging.info('Начинаем редактировать фото')
            self.status.emit('Старт')
            self.progress.emit(self.progress_val)
            for folder in os.listdir(pathlib.Path(self.folder)):
                self.percent += len(os.listdir(pathlib.Path(self.folder, folder))) \
                    if os.path.isdir(pathlib.Path(self.folder, folder)) else 1
            self.percent = 100 / self.percent
            for folder in os.listdir(pathlib.Path(self.folder)):
                if self.pause_threading():
                    self.logging.warning('Прервано пользователем')
                    self.progress.emit(0)
                    os.chdir(self.default_path)
                    self.button.setText('Старт')
                    self.logging.info('----------------Прервано redate_file_and_photo----------------')
                    return
                if folder.startswith('.'):
                    continue
                if os.path.isdir(pathlib.Path(self.folder, folder)):
                    info = os.stat(pathlib.Path(self.folder, folder))                
                    if info.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
                        self.progress_val += self.percent
                        self.progress.emit(self.progress_val)
                        continue
                    date = self.get_date(pathlib.Path(self.folder, folder))
                    answer = self.folder_tree(pathlib.Path(self.folder, folder))
                    if answer['error']:
                        return
                    change_date(pathlib.Path(self.folder, folder), date)
                    self.count += 1
                    if self.count == self.device_count:
                        self.count = 0
                        self.start_date = datetime.date.strftime(
                            (datetime.datetime.strptime(self.start_date, '%Y:%m:%d')
                             + datetime.timedelta(days=1)).date(), '%Y:%m:%d')
                else:
                    try:
                        format_file = folder.rpartition('.')[2]
                        if format_file.lower() not in ['tif', 'tiff', 'jpeg', 'jpg', 'png']:
                            self.logging.info(f'Формат файла {folder} не подходит под указанные, пропускаем')
                            continue
                        answer = self.change_file(pathlib.Path(self.folder, folder))
                        if answer['error']:
                            return
                    except BaseException as exc:
                        self.logging.error(f"Не удалось изменить время у файла {pathlib.Path(self.folder, folder)}")
                        self.logging.error(f"Ошибка: {exc}")
                        self.logging.info('-------------------------------------------')
            if self.error_text:
                self.logging.info("Выводим ошибки")
                self.logging.warning(self.error_text)
                self.status.emit('Готово с ошибками')
                self.queue.put({'errors': ['У некоторых файлов не было exif данных']})
                self.errors.emit()
            else:
                self.logging.info("----------------Конец работы программы----------------")
                self.status.emit('Готово')
            os.chdir(self.default_path)
            self.progress.emit(100)
            self.button.setText('Старт')
            return
        except BaseException as es:
            self.logging.error(es)
            self.logging.error(traceback.format_exc())
            self.progress.emit(0)
            self.status.emit('Ошибка!')
            os.chdir(self.default_path)
            self.button.setText('Старт')
            self.logging.error('----------------Ошибка redate_file_and_photo----------------')
            return

    def pause_threading(self) -> bool:
        question = False if self.queue.empty() else self.queue.get_nowait()
        if question:
            self.messageChanged.emit('Вопрос?', 'Редактирование фото остановлено пользователем.'
                                                ' Нажмите «Да» для продолжения или «Нет» для прерывания')
            self.event.wait()
            self.event.clear()
            if self.queue.get_nowait():
                self.status.emit('Прервано пользователем')
                self.progress.emit(0)
                return True
        return False
