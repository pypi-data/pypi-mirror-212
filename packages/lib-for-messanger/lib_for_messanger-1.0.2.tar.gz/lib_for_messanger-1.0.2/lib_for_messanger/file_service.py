import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class FileService:
    gauth = None
    drive = None

    def __init__(self, file_path, data_list, object_class):
        if FileService.gauth is None and FileService.drive is None:
            FileService.gauth = GoogleAuth()
            FileService.gauth.LocalWebserverAuth()
            FileService.drive = GoogleDrive(FileService.gauth)

        self.__file_name = file_path
        self.__data_list = data_list

        json_array = []
        file_list = FileService.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file["title"] == self.__file_name:
                json_array = json.loads(file.GetContentString())
                break

        for json_object in json_array:
            self.__data_list.append(object_class.from_json_object(json_object))

    def save_data(self):
        file = None
        file_list = FileService.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for _file in file_list:
            if _file["title"] == self.__file_name:
                file = _file
                break

        if file is None:
            return

        json_array = []
        for el in self.__data_list:
            json_array.append(el.to_json_object())
        file.SetContentString(json.dumps(json_array))
        file.Upload()

