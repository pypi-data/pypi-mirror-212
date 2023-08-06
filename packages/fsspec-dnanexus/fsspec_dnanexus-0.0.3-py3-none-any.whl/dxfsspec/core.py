import os
import stat
import json
import logging
import dxpy
from typing import Tuple, Union

from dxpy import api, DXFile, DXError, new_dxfile
from dxpy.exceptions import ResourceNotFound, InvalidAuthentication, PermissionDenied

from fsspec.spec import AbstractFileSystem, AbstractBufferedFile

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', force=True)
log = logging.getLogger("dxfs")

PROTOCOL = "dnanexus"

FILE_REQUEST_TIMEOUT = 60
WRITE_PERMS = ["CONTRIBUTE", "ADMINISTER", "UPLOAD"]
READ_PERMS = ["VIEW", *WRITE_PERMS]

DIRECTORY_TYPE = "directory"
FILE_TYPE = "file"

KEEP_DETAILS = ["id", "name", "detail_name", "created", "modified", "type", "class"]

class DXFileSystemException(Exception):
    pass

class DXFileSystem(AbstractFileSystem):
    
    cachable = False # do not cache this instance
    default_block_size = 5 * 2**20
    protocol = ["dnanexus", "DNANEXUS"]
    api_host = "api.dnanexus.com"
    root_marker = "/"

    def __init__(
        self,
        block_size=None,
        cache_type="readahead",
        asynchronous=False,
        loop=None,
        **storage_options,
    ):
        """
        :param Dict[str, Any] storage_options: a dictionary including
            :token str:
                Set to authentication of dxpy
            :staging bool: default False
                Login to staging
            :overwrite bool: default False
                Write a new file if the filename already exists in folder
        """
        super().__init__(loop=loop, asynchronous=asynchronous, skip_instance_cache=True, **storage_options)

        self.block_size = block_size or self.default_block_size
        self.cache_type = cache_type
        self.dx_path_extractor = DXPathExtractor()
        self.storage_options = storage_options

        # prefer token to FSSPEC_DNANEXUS_TOKEN
        self.token = storage_options.get("token", None) or os.environ.get("FSSPEC_DNANEXUS_TOKEN")

        if storage_options.get("staging", False):
            self.api_host = "stagingapi.dnanexus.com"

        self.dx_login(token=self.token, api_host=self.api_host)

    def dx_login(self, token=None, api_host="api.dnanexus.com"):
        # if token is not provided, dxfsspec uses thes token of dxpy by default
        if not token:
            return
        
        try:
            dxpy.set_api_server_info(host=api_host, protocol='https')
            dxpy.set_security_context({'auth_token_type': 'Bearer', 'auth_token': token})
            dxpy.set_workspace_id(None)
            log.debug(f'Logged as: {dxpy.whoami()}')
        except InvalidAuthentication as e:
            raise DXFileSystemException(f'Login failed! {e}')
 
    def _open(self, path, mode="rb",
        block_size=None,
        autocommit=True,
        cache_type=None,
        cache_options=None,
        **kwargs):
        if block_size is None:
            block_size = self.block_size
        if cache_type is None:
            cache_type = self.cache_type

        return DXBufferedFile(
            fs=self,
            path=path,
            mode=mode,
            block_size=block_size,
            cache_type=cache_type,
            autocommit=autocommit,
            cache_options=cache_options
        )

    def info(self, path, **kwargs):
        path = self._strip_protocol(path)
        project_id, file_id, _ = self.dx_path_extractor.extract_path(path)

        if not project_id or not file_id:
            raise DXFileSystemException(f"ValueError: Unsupported format of this path {path}")

        try:
            dxfile = DXFile(file_id, project=project_id)
            return dxfile.describe()
        except ResourceNotFound as e:
            raise DXFileSystemException(f"FileNotFound: {e}")

    def exists(self, path, **kwargs):
        describe = self._file_describe(path, **kwargs)
        return describe is not None

    def isfile(self, path, **kwargs):
        describe = self._file_describe(path, **kwargs)
        if not describe:
            return False
        return describe['class'] == 'file'

    def _file_describe(self, path, **kwargs):
        path = self._strip_protocol(path)
        try:
            project_id, file_id, _ = self.dx_path_extractor.extract_path(path)
            if project_id and file_id:
                return api.file_describe(file_id, input_params={"project": project_id})
        except (ResourceNotFound, DXFileSystemException):
            return None
        return None

    def ls(self, path, detail=True, unique=False, fields=[], **kwargs):
        def filter_duplicated_filenames(files):
            res = {}
            for file in files:
                name = file["name"]
                # file name doest not exist
                if name not in res:
                    res[name] = file
                else: # already exists
                    # check the latest created time
                    if file["created"] > res[name]["created"]:
                        res[name] = file
            return list(res.values())

        path = self._strip_protocol(path)

        project_id, _, folder_path = self.dx_path_extractor.extract_path(path, mode=None)
        if not project_id:
            raise DXFileSystemException(f"ProjectNotFound: There is no project with path {path}")
        
        try:
            results = api.project_list_folder(object_id=project_id, 
                                    input_params={"folder": folder_path, "describe": True})
            
            contents = []
            # add type for folders
            for folder in results["folders"]:
                contents.append({"name": folder, "type": DIRECTORY_TYPE})
            
            # get object describe
            objects = [obj["describe"] for obj in results["objects"]]
            # filter the duplicated file names
            if unique:
                objects = filter_duplicated_filenames(objects)
            
            # add fullpath to name for file type
            # add type for objects
            for i, obj in enumerate(objects):
                obj["type"] = FILE_TYPE
                obj["name"] = os.path.join(obj["folder"], obj["name"])
                obj["detail_name"] = f"{PROTOCOL}://{obj['project']}:{obj['name']} : {obj['id']}"
                
                # keep details using a list of keys
                # ignore the key if it does not exist
                objects[i] = {key: obj[key] for key in KEEP_DETAILS + fields if key in obj}
                
            # append processed objects
            contents += objects
            
            # only return file id if detail is False
            if not detail:
                contents = [info["name"] for info in contents]
            
            return contents

        except ResourceNotFound as e:
            raise DXFileSystemException(f"ResourceNotFound: {e}")
        except DXError as e:
            raise DXFileSystemException(f"Unknown Error: {e}")


    def mkdir(self, path, create_parents=True, **kwargs):
        path = self._strip_protocol(path)

        project_id, _, folder_path = self.dx_path_extractor.extract_path(path, mode=None)

        if not project_id:
            raise DXFileSystemException(f"ProjectNotFound: There is no project with path {path}")

        try:
            return api.project_new_folder(object_id=project_id, input_params={
                                                            "folder": folder_path, 
                                                            "parents": create_parents})
        except ResourceNotFound as e:
            raise DXFileSystemException(f"ProjectNotFound: {e}")
        except DXError as e:
            raise DXFileSystemException(f"Unknown Error: {e}")

class DXBufferedFile(AbstractBufferedFile):

    part_min = 5 * 2**20
    part_max = 5 * 2**30

    def __init__(self, 
                 fs,
                 path: str,
                 mode: str = "rb",
                 block_size: int = 5 * 2**20,
                 cache_type: str ="readahead",
                 autocommit: bool = True,
                 cache_options: dict = None):
        
        self.project_id, file_id, self.file_path = DXPathExtractor().extract_path(path, mode=mode)

        # if self.project_id:
        #     self.check_permissions(project_id=self.project_id, mode=mode)

        self.dxfile: Union[DXFile, None] = DXFile(file_id, project=self.project_id) if file_id else None

        if "r" in mode:
            self.details = fs.info(path)
            self.size = self.details["size"]

        super().__init__(
            fs,
            path,
            mode,
            block_size,
            cache_type=cache_type,
            autocommit=autocommit,
            cache_options=cache_options,
        )

    def check_permissions(self, project_id: str, mode: str = "rb"):
        if "w" in mode and not project_id:
            raise DXFileSystemException(f"The project ID is required when writing the file.")

        proj_desc = api.project_describe(project_id, input_params={"fields": {"permissions": True}})

        permissions = proj_desc["permissions"]
        user_id = dxpy.whoami() # user id by token
        user_perm = permissions.get(user_id)

        # if current user does not have permission to access the project
        if not user_perm:
            raise DXFileSystemException(f"PermissionDenied: The user {user_id} does not have access to the project {project_id}.")

        # if current user does not have write permission
        if "w" in mode and user_perm not in WRITE_PERMS:
            raise DXFileSystemException(f"WritePermissionDenied: The user {user_id} does not have permission to write file to the project {project_id}.")

    def _upload_chunk(self, final=False):
        log.debug(
            f"Upload for {self}, final={final}, loc={self.loc}, buffer loc={self.buffer.tell()}"
        )
        self.buffer.seek(0)
        (data0, data1) = (None, self.buffer.read(self.blocksize))

        while data1:
            (data0, data1) = (data1, self.buffer.read(self.blocksize))
            data1_size = len(data1)

            if 0 < data1_size < self.blocksize:
                remainder = data0 + data1
                remainder_size = self.blocksize + data1_size

                if remainder_size <= self.part_max:
                    (data0, data1) = (remainder, None)
                else:
                    partition = remainder_size // 2
                    (data0, data1) = (remainder[:partition], remainder[partition:])

            try:
                self.dx_handler.write(data=data0)
            except PermissionDenied as e:
                raise DXFileSystemException(f"PermissionDenied: {e}")
            

        if final:
            self.dx_handler.flush()
            try:
                self.dx_handler.wait_until_parts_uploaded()
            except DXError:
                raise DXFileSystemException("File {} was not uploaded correctly!".format(self.dx_handler.name))
            self.dx_handler.close()
            self.dx_handler.wait_on_close()
            self.dx_handler = None

        return not final

    def _initiate_upload(self):
        """Create remote file/upload"""
        log.debug("Initiate upload for %s" % self)

        folder = os.path.dirname(self.file_path)
        filename = os.path.basename(self.file_path)

        if not self.fs.storage_options.get("overwrite"):
            file_existed = dxpy.find_one_data_object(name=filename, 
                                                    folder=folder, 
                                                    project=self.project_id, 
                                                    recurse=False,
                                                    zero_ok=True)
            if file_existed:
                raise DXFileSystemException(f"FileAlreadyExists: The filename '{filename}' already existed in the folder '{folder}'.")
        try:
            self.dx_handler = new_dxfile(name=filename,
                                     folder=folder,
                                     project=self.project_id,
                                     parents=True,
                                     mode="a")

            self.dx_handler._ensure_write_bufsize()
            self.dx_handler._num_bytes_transmitted = 0
        except PermissionDenied as e:
            raise DXFileSystemException(f"PermissionDenied: {e}")

    def _fetch_range(self, start, end):
        """Get the specified set of bytes from remote"""
        dl_url, dl_headers = self.dxfile.get_download_url()
        return dxpy._dxhttp_read_range(url=dl_url, 
                                       headers=dl_headers, 
                                       start_pos=start, 
                                       end_pos=end, 
                                       timeout=FILE_REQUEST_TIMEOUT)

class DXPathExtractor():
    root_marker = "/"

    def __init__(self) -> None:
        pass

    def get_project_id(self, id_or_path: str) -> str:
        if self.is_dx_project_id(id_or_path):
            try:
                api.project_describe(id_or_path)
                return id_or_path
            except ResourceNotFound as e:
                raise DXFileSystemException(f"ProjectNotFound: {e}")
            except DXError as e:
                raise DXFileSystemException(f"Unknown Error: {e}")

        dx_proj = dxpy.find_one_project(name=id_or_path, zero_ok=True, level="VIEW")
        if dx_proj is None:
            raise DXFileSystemException(f"ProjectNotFound: There is no project with {id_or_path} name")

        return dx_proj["id"]

    def is_dx_project_id(self, file_id: str) -> bool:
        try:
            dxpy.verify_string_dxid(file_id, expected_classes="project")
            return True
        except DXError as e:
            log.debug(e)
            return False

    def is_dx_file_id(self, file_id: str) -> bool:
        try:
            dxpy.verify_string_dxid(file_id, expected_classes="file")
            return True
        except DXError as e:
            log.debug(e)
            return False

    def get_file_id(self, id_or_path: str, project_id: str = None) -> str:
        if self.is_dx_file_id(id_or_path):
            try:
                # check if dxfile exists
                api.file_describe(id_or_path, input_params={"project": project_id})
                return id_or_path
            except ResourceNotFound as e:
                raise DXFileSystemException(f"FileNotFound: {e}")
            except DXError as e:
                raise DXFileSystemException(f"Unknown Error: {e}")

        folder = os.path.dirname(id_or_path)
        filename = os.path.basename(id_or_path)
        # check if dxfile exists by name and project
        dxfile_desc = None
        dxfiles = dxpy.find_data_objects(classname="file", 
                                            name=filename, 
                                            folder=folder, 
                                            project=project_id, 
                                            describe=True,
                                            recurse=False)
        for file in dxfiles:
            file_desc = file["describe"]
            if dxfile_desc is None or file_desc["created"] > dxfile_desc["created"]:
                dxfile_desc = file_desc
        
        if dxfile_desc is None:
            raise DXFileSystemException("FileNotFound: Cannot find any file matching { name: '%s', folder: '%s', project: '%s' }" \
                                    % (filename, folder, project_id ))
        
        return dxfile_desc["id"]

    def extract_path(self, path: str, mode: Union[str, None] = "rb") -> Tuple[str, str, str]:
        project_id = None
        file_id = None
        file_path = None # used for write case

        file_info = path.split(":")
        # DX id format
        # project-xxx:file-yyyy
        file_id_or_path = None
        if len(file_info) == 2:
            project_id_or_name, file_id_or_path = file_info
            
            project_id = self.get_project_id(id_or_path=project_id_or_name)
            
            if mode != None and "r" in mode:
                file_id = self.get_file_id(id_or_path=file_id_or_path, project_id=project_id)
            else:
                file_path = file_id_or_path
        else:
            file_id_or_path = file_info[0]
            if self.is_dx_file_id(file_id=file_id_or_path):
                file_id = file_id_or_path
                
                # find dx project based on dx file id
                dxfile = DXFile(file_id)
                dxfile_desc = dxfile.describe()
                project_id = dxfile_desc["project"]

        return project_id, file_id, file_path or self.root_marker
