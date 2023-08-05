# import base64
import json
import requests
from requests.auth import HTTPBasicAuth

EP_API = '/api/v2.0'
EP_ME = '/me'
EP_FOLDERS = '/folders'
EP_DATASOURCES = '/datasources'
EP_REPORTS = '/reports'

class User:
    def __init__(self, Id: str, Username: str, DisplayName: str):
        self.Id = Id
        self.Username = Username
        self.DisplayName = DisplayName
        
    def __iter__(self):
        yield from {
            "Id": self.Id,
            "Username": self.Username,
            "DisplayName": self.DisplayName
        }.items()
        
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return self.__str__()
    
    def to_obj(self):
        obj = {
            'Username': self.Username,
            'DisplayName': self.DisplayName
        }
        if self.Id != None:
            obj.update({'Id': self.Id})
        return obj
    
    @staticmethod
    def from_json(json_dct):
        return User(
            json_dct['Id'],
            json_dct['Username'],
            json_dct['DisplayName']
        )

class Folder:
    def __init__(self, Id: str, Name: str, Description: str, Path: str, ParentFolderId: str):
        self.Id = Id
        self.Name = Name
        self.Description = Description
        self.Path = Path
        self.ParentFolderId = ParentFolderId
        
    def __iter__(self):
        yield from {
            "Id": self.Id,
            "Name": self.Name,
            "Description": self.Description,
            "Path": self.Path,
            "ParentFolderId": self.ParentFolderId
        }.items()
        
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return self.__str__()
        
    def to_obj(self):
        obj = {
            'Name': self.Name,
            'Description': self.Description,
            'Path': self.Path,
            'ParentFolderId': self.ParentFolderId
        }
        if self.Id != None:
            obj.update({'Id': self.Id})
        return obj
    
    @staticmethod
    def from_json(json_dct):
        return Folder(
            json_dct['Id'],
            json_dct['Name'],
            json_dct['Description'],
            json_dct['Path'],
            json_dct['ParentFolderId']
        )

class Datasource:
    def __init__(self, Id, Name: str, Description: str, Path: str, ParentFolderId: str, DataSourceType: str, ConnectionString: str, Content: str, ContentType: str = '', Size: int = 0):
        self.Id = Id
        self.Name = Name
        self.Description = Description
        self.Path = Path
        self.ParentFolderId = ParentFolderId
        self.DataSourceType = DataSourceType
        self.ConnectionString = ConnectionString
        self.Content = Content
        self.ContentType = ContentType
        self.Size = Size
        
    def __iter__(self):
        yield from {
            "Id": self.Id,
            "Name": self.Name,
            "Description": self.Description,
            "Path": self.Path,
            "ParentFolderId": self.ParentFolderId,
            "DataSourceType": self.DataSourceType,
            "ConnectionString": self.ConnectionString,
            "Content": self.Content,
            "ContentType": self.ContentType,
            "Size": self.Size
        }.items()
        
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return self.__str__()
    
    def to_obj(self):
        obj = {
            'Name': self.Name,
            'Description': self.Description,
            'Path': self.Path,
            'ParentFolderId': self.ParentFolderId,
            'DataSourceType': self.DataSourceType,
            'ConnectionString': self.ConnectionString,
            'Content': self.Content,
            'ContentType': self.ContentType,
            'Size': self.Size
        }
        if self.Id != None:
            obj.update({'Id': self.Id})
        return obj
    
    @staticmethod
    def from_json(json_dct):
        return Datasource(
            json_dct['Id'],
            json_dct['Name'],
            json_dct['Description'],
            json_dct['Path'],
            json_dct['ParentFolderId'],
            json_dct['DataSourceType'],
            json_dct['ConnectionString'],
            json_dct['Content'],
            json_dct['ContentType'],
            json_dct['Size']
        )

class Api:
    def __init__(self, url: str, user: str, password: str):
        self.url = url + EP_API
        self.basic_auth = HTTPBasicAuth(user, password)
        self.headers = {'Content-type': 'application/json;charset=UTF-8'}
        
    # REQUESTS
    def __getEndpointClass(self, endpoint: str):
        if endpoint == EP_ME:
            return User
        elif endpoint == EP_FOLDERS:
            return Folder
        elif endpoint == EP_DATASOURCES:
            return Datasource

    def __get(self, endpoint: str, args: str = ''):
        response = requests.get(self.url + endpoint + args, auth=self.basic_auth, headers=self.headers)
        object_hook = self.__getEndpointClass(endpoint=endpoint).from_json
        if response.status_code == 200:
            response_obj = json.loads(response.content)
            if 'value' in response_obj:
                value = json.loads(response.content)['value']
                return json.loads(json.dumps(value), object_hook=object_hook)
            else:
                return json.loads(response.content, object_hook=object_hook)
        return False
    
    def __post(self, endpoint: str, data: Folder|Datasource, args: str = ''):
        response = requests.post(self.url + endpoint + args, json=data.to_obj(), auth=self.basic_auth, headers=self.headers)
        object_hook = self.__getEndpointClass(endpoint=endpoint).from_json
        if response.status_code == 201:
            return json.loads(response.content, object_hook=object_hook)
        return False
    
    # USER
    def getUser(self):
        return self.__get(endpoint=EP_ME)
    
    # FOLDER
    def getFolders(self):
        return self.__get(endpoint=EP_FOLDERS)
    
    def getFolderById(self, id: str):
        return self.__get(endpoint=EP_FOLDERS, args='(' + id + ')')
    
    def getFolderByName(self, name: str):
        folders = self.getFolders()
        for f in folders:
            if f.Name == name:
                return f
        return False
    
    def getFolderByPath(self, path: str):
        return self.__get(endpoint=EP_FOLDERS, args="(Path='" + path + "')")
    
    def getRootFolder(self):
        return self.getFolderByPath(path = '/')
    
    def addFolder(self, folder: Folder):
        return self.__post(endpoint=EP_FOLDERS, data=folder)
    
    # def editFolder(self, id: str, folder: Folder):
    #     response = requests.patch(self.url + EP_FOLDERS + '(' + id + ')', json=folder, auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 204:
    #         return self.getFolderById(id = id)
    #     return False

    # def deleteFolder(self, id: str):
    #     response = requests.delete(self.url + EP_FOLDERS + '(' + id + ')', auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 204:
    #         return True
    #     return False
    
    # # DATASOURCE
    # def getDatasources(self):
    #     response = requests.get(self.url + EP_DATASOURCES, auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 200:
    #         value = json.loads(response.content)['value']
    #         return json.loads(json.dumps(value), object_hook=Datasource.from_json)
    #     return False

    # def getDatasourceById(self, id: str):
    #     response = requests.get(self.url + EP_DATASOURCES + '(' + id + ')', auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 200:
    #         return json.loads(response.content, object_hook=Datasource.from_json)
    #     return False

    # def getDatasourceByPath(self, path: str):
    #     response = requests.get(self.url + EP_DATASOURCES + "(Path='" + path + "')", auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 200:
    #         return json.loads(response.content, object_hook=Datasource.from_json)
    #     return False
    
    # def addDatasource(self, datasource: Datasource):
    #     response = requests.post(self.url + EP_DATASOURCES, json=datasource, auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 201:
    #         return json.loads(response.text, object_hook=Datasource.from_json)
    #     return False
    
    # def deleteDatasource(self, id: str):
    #     response = requests.delete(self.url + EP_DATASOURCES + '(' + id + ')', auth=self.basic_auth, headers=self.headers)
    #     if response.status_code == 204:
    #         return True
    #     return False
    
    # # REPORT
    
# def getB64EncodedFile(path):
#     with open(path, 'rb') as f:
#         byte_content = f.read()
#     base64_bytes = base64.b64encode(byte_content)
#     return base64_bytes.decode('utf-8')