import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class FileService:
    gauth = None
    drive = None

    def __init__(self, file_path, data_list, object_class):
        if FileService.gauth is None and FileService.drive is None:

            gauth = GoogleAuth()
            # Try to load saved client credentials
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
            else:
                # Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")

            # gauth = GoogleAuth()
            # gauth.LocalWebserverAuth()
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

        # with open(self.__file_name, "w") as file:
        #     json_array = []
        #     for el in self.__data_list:
        #         json_array.append(el.to_json_object())
        #     # print(json_array)
        #     json.dump(json_array, file)
