import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class FileService:
    gauth = None

    def __init__(self, file_path, data_list, object_class):
        if FileService.gauth is None:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()

        self.__file_name = file_path
        self.__data_list = data_list

        drive = GoogleDrive(FileService.gauth)
        file = drive.CreateFile({"title": f"{self.__file_name}"})

        json_array = json.loads(file.GetContentString())
        for json_object in json_array:
            self.__data_list.append(object_class.from_json_object(json_object))

        # path = os.path.join(file_path)
        #
        #
        #
        #
        # if not os.path.isfile(path):
        #     my_file = open(file_path, "w")
        #     my_file.write("[]")
        #     my_file.close()
        # else:
        #     with open(self.__file_name, "r") as file:
        #         json_array = json.load(file)
        #         for json_object in json_array:
        #             self.__data_list.append(object_class.from_json_object(json_object))
        #
        #         print(self.__data_list)

    def save_data(self):
        drive = GoogleDrive(FileService.gauth)
        file = drive.CreateFile({"title": f"{self.__file_name}"})

        json_array = []
        for el in self.__data_list:
            json_array.append(el.to_json_object())
        file.SetContentString(json.dumps(json_array))
        file.upload()


        # with open(self.__file_name, "w") as file:
        #     json_array = []
        #     for el in self.__data_list:
        #         json_array.append(el.to_json_object())
        #     # print(json_array)
        #     json.dump(json_array, file)
