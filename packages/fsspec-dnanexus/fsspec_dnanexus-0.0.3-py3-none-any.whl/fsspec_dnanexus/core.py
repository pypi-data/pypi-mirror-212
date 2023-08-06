import os
import stat
import json
import logging
import dxpy
from typing import Tuple, Union
from threading import Thread

from dxpy import api, DXFile, DXError, new_dxfile
from dxpy.exceptions import ResourceNotFound, InvalidAuthentication, PermissionDenied

from fsspec.spec import AbstractFileSystem, AbstractBufferedFile
from fsspec.utils import setup_logging

logger = logging.getLogger("dxfs")

if "FSSPEC_DNANEXUS_LOGGING_LEVEL" in os.environ:
    setup_logging(logger=logger, level=os.environ["FSSPEC_DNANEXUS_LOGGING_LEVEL"])

PROTOCOL = "dnanexus"

FILE_REQUEST_TIMEOUT = 60
WRITE_PERMS = ["CONTRIBUTE", "ADMINISTER", "UPLOAD"]
READ_PERMS = ["VIEW", *WRITE_PERMS]

DIRECTORY_TYPE = "directory"
FILE_TYPE = "file"

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
            :allow_duplicate_filenames bool: default False
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
            logger.debug(f'Logged as: {dxpy.whoami()}')
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

        logger.debug(f"Get info of '{file_id}' in '{project_id}'")
        try:
            desc = DXFile(file_id, project=project_id).describe()
            desc["type"] = desc["class"]
            return desc
        except ResourceNotFound as e:
            raise DXFileSystemException(f"FileNotFound: {e}")

    def exists(self, path, **kwargs):
        logger.debug(f"Check if {path} exists")
        describe = self._file_describe(path, **kwargs)
        return describe is not None

    def isfile(self, path, **kwargs):
        logger.debug(f"Check if {path} is file")
        describe = self._file_describe(path, **kwargs)
        if not describe:
            return False
        return describe['class'] == 'file'

    def _file_describe(self, path, **kwargs):
        path = self._strip_protocol(path)
        try:
            project_id, file_id, _ = self.dx_path_extractor.extract_path(path)
            logger.debug(f"Describe {file_id} in {project_id}")
            if project_id and file_id:
                return api.file_describe(file_id, input_params={"project": project_id})
        except (ResourceNotFound, DXFileSystemException):
            return None
        return None

    def ls(self, path, detail=False, unique=False, **kwargs):
        def filter_duplicated_filenames(files):
            logger.debug(f"Filter duplicate filenames")
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
        logger.debug(f"List information about files and directories in folder '{folder_path}' of {project_id}")
        if not project_id:
            raise DXFileSystemException(f"ProjectNotFound: There is no project with path {path}")
        
        try:
            results = api.project_list_folder(object_id=project_id, 
                                    input_params={"folder": folder_path,
                                                  "includeHidden": True,
                                                  "describe": dict(fields={"id": True,
                                                                           "project": True,
                                                                           "name": True,
                                                                           "class": True,
                                                                           "folder": True,
                                                                           "created": True,
                                                                           "createdBy": True,
                                                                           "modified": True,
                                                                           "hidden": True,
                                                                           "tags": True,
                                                                           "media": True,
                                                                           "archivalState": True,
                                                                           "cloudAccount": True,
                                                                           "size": True,
                                                                           "state": True})})
            folders = results["folders"]
            # get object describe
            # filter files that are not in closed state
            logger.debug(f"Filter files that are not in 'closed' state.")
            objects = [obj["describe"] for obj in results["objects"] if obj["describe"]["state"] == "closed"]
            # only return filename if detail is False
            if not detail:
                logger.debug(f"Return objects without detail.")
                objects = [os.path.join(obj["folder"], obj["name"]) for obj in objects]
                if unique:
                    logger.debug(f"Filter duplicate filenames")
                    objects = list(set(objects))
                return folders + objects

            logger.debug(f"Return folders and objects with detail.")
            # add type for folders
            folders = [{"name": folder, "type": DIRECTORY_TYPE} for folder in folders]

            # filter the duplicated file names
            if unique:
                objects = filter_duplicated_filenames(objects)

            logger.debug(f"Add more info including type, name, full_url.")
            for obj in objects:
                obj["type"] = obj["class"]
                obj["name"] = os.path.join(folder_path, obj["name"])
                obj["full_url"] = f"{PROTOCOL}://{obj['project']}:{obj['name']} : {obj['id']}"

            return folders + objects

        except ResourceNotFound as e:
            raise DXFileSystemException(f"ResourceNotFound: {e}")
        except DXError as e:
            raise DXFileSystemException(f"Unknown Error: {e}")


    def mkdir(self, path, create_parents=True, **kwargs):
        path = self._strip_protocol(path)

        project_id, _, folder_path = self.dx_path_extractor.extract_path(path, mode=None)
        logger.debug(f"Create new folder '{folder_path}' in {project_id}.")

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
            if self.dxfile and self.dxfile._get_state() != "closed":
                raise DXFileSystemException("NotSupportedError: Reading an open file is not supported.")
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
        logger.debug(
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
                logger.debug(f"Upload chunk with length {len(data0)}")
                self.dx_handler.write(data=data0)
            except PermissionDenied as e:
                raise DXFileSystemException(f"PermissionDenied: {e}")
            

        if final:
            logger.debug(f"Complete upload for {self}")
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
        logger.debug("Initiate upload for %s" % self.file_path)

        folder = os.path.dirname(self.file_path)
        filename = os.path.basename(self.file_path)

        try:
            self.dx_handler = new_dxfile(name=filename,
                                     folder=folder,
                                     project=self.project_id,
                                     parents=True,
                                     mode="a")

            self.dx_handler._ensure_write_bufsize()
            self.dx_handler._num_bytes_transmitted = 0

            if not self.fs.storage_options.get("allow_duplicate_filenames"):
                t = Thread(target=self.remove_duplicate_filenames, args=(filename,
                                                                         folder,
                                                                         self.project_id,
                                                                         self.dx_handler.get_id()))
                t.start()
        except PermissionDenied as e:
            raise DXFileSystemException(f"PermissionDenied: {e}")

    def _fetch_range(self, start, end):
        """Get the specified set of bytes from remote"""
        logger.debug(f"Fetch data in range: {start}-{end}")
        dl_url, dl_headers = self.dxfile.get_download_url()
        logger.debug(f"Get the specified set of bytes from {start} to {end}")
        return dxpy._dxhttp_read_range(url=dl_url, 
                                       headers=dl_headers, 
                                       start_pos=start, 
                                       end_pos=end, 
                                       timeout=FILE_REQUEST_TIMEOUT)
    def remove_duplicate_filenames(self, filename: str, folder: str, project_id: str, exclude_dxid: str):
        logger.debug(f"Remove the duplicate filenames {filename} in {folder} excluding {exclude_dxid}")
        objects = dxpy.find_data_objects(classname="file",
                                        name=filename,
                                        folder=folder, 
                                        project=project_id)
        
        # to make sure that do not remove the writing file
        file_ids = [obj["id"] for obj in objects if obj["id"] != exclude_dxid]
        if len(file_ids) > 0:
            try:
                api.project_remove_objects(project_id, input_params={"objects": file_ids, "force": True})
                logger.debug(f"Removed: {file_ids}")
            except Exception as e:
                logger.debug(f"DXFileSystemException: {e}")

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

        logger.debug(f"{id_or_path} is not DXProject ID. Try to find DXProject with name '{id_or_path}'")
        
        dx_proj = dxpy.find_one_project(name=id_or_path, zero_ok=True, level="VIEW")
        if dx_proj is None:
            raise DXFileSystemException(f"ProjectNotFound: There is no project with {id_or_path} name")

        return dx_proj["id"]

    def is_dx_project_id(self, project_id: str) -> bool:
        try:
            dxpy.verify_string_dxid(project_id, expected_classes="project")
            return True
        except DXError as e:
            logger.debug(f"{project_id} is not a DXProject ID")
            return False

    def is_dx_file_id(self, file_id: str) -> bool:
        try:
            dxpy.verify_string_dxid(file_id, expected_classes="file")
            return True
        except DXError as e:
            logger.debug(f"{file_id} is not a DXFile ID")
            return False

    def get_file_id(self, id_or_path: str, project_id: str = None) -> str:
        if self.is_dx_file_id(id_or_path):
            try:
                # check if dxfile exists
                # describe id to prevent dxpy takes so long when describing a file 
                api.file_describe(id_or_path, input_params={"project": project_id, "fields": {"id": True}})
                return id_or_path
            except ResourceNotFound as e:
                raise DXFileSystemException(f"FileNotFound: {e}")
            except DXError as e:
                raise DXFileSystemException(f"Unknown Error: {e}")

        logger.debug(f"{id_or_path} is not DXProject ID. Try to find DXFile with name '{id_or_path}' in {project_id}")
        folder = os.path.dirname(id_or_path)
        if not folder:
            raise DXFileSystemException("ValueError: The folder path should start with '/'")
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
        logger.debug(f"Extract info from {path}")
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
