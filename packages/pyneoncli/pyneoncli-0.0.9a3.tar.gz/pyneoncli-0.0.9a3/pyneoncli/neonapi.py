import json
import pprint
import sys
import time
from typing import Iterator

import requests

from pyneoncli.neon import NeonProject, NeonBranch, NeonOperations, NeonOperationsDetails
from pyneoncli.neonfunction import NeonFunction as nf

BASE_URL_V2 = "https://console.neon.tech/api/v2/"


class NeonAPIException(requests.exceptions.HTTPError):

    def __init__(self, *args, **kwargs):
        self._path = kwargs.pop("path", None)
        self._header = kwargs.pop("header", None)
        self._method = kwargs.pop("method", None)
        self._err = kwargs.pop("err", None)
        self._text = kwargs.pop("text", None)
        self._operation = kwargs.pop("operation", None)
        super().__init__(*args, **kwargs)

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        self._operation = value

    @property
    def path(self):
        return self._path

    @property
    def header(self):
        return self._header

    @property
    def method(self):
        return self._method

    @property
    def err(self):
        return self._err

    @property
    def text(self):
        return self._text

    @staticmethod
    def blank_if_none(label: str, value: str, end="\n") -> str:
        if value is None:
            return ""
        else:
            return f"{label}: {value}{end}"

    def __str__(self):
        if self._header is None:
            h = ""
        else:
            h = f"header: {pprint.pformat(self._header)}"
        m = self.blank_if_none("method", self._method)
        o = self.blank_if_none("operation", self._operation)
        p = self.blank_if_none("path", self._path)
        msg = self.blank_if_none("message", self._text)

        return f'{p}{h}{m}{o}{msg}'


class NeonTimeoutException(Exception):
    pass


class Requester:

    def __init__(self, base_url: str = BASE_URL_V2, key=None):
        self._key = key
        self._base_url = base_url
        self._headers = {'Authorization': f"Bearer {self._key}",
                         'Content-Type': "application/json"}

    def request(self, method: str, operation: str, **kwargs):
        try:
            # print(self._headers)
            # print(kwargs)
            path = f"{self._base_url}{operation}"
            r = requests.request(method, path, headers=self._headers, **kwargs)
            r.raise_for_status()
            return r.json()

        except requests.exceptions.HTTPError as err:
            raise NeonAPIException(path=path, method=method, err=err, text=r.text)

    def GET(self, operation: str, **kwargs):
        return self.request("GET", operation)

    def POST(self, operation: str, data: dict = None) -> dict:
        if data is None:
            data = dict()
        self._headers["Accept"] = "application/json"
        return self.request("POST", operation, data=json.dumps(data))

    def PUT(self, operation: str, **kwargs) -> dict:
        return self.request("PUT", operation, **kwargs)

    def DELETE(self, operation: str, **kwargs) -> dict:
        return self.request("DELETE", operation, **kwargs)

    def PATCH(self, operation: str, **kwargs) -> dict:
        return self.request("PATCH", operation, **kwargs)

    def HEAD(self, operation: str, **kwargs):
        return self.request("HEAD", operation, **kwargs)


class RawNeonAPI:

    def __init__(self, api_key: str = None) -> None:
        self._api_key = api_key
        self._requester = Requester(key=self._api_key)

    def get_first_operation(self, project_id: str) -> NeonOperations:
        try:
            path = f"{nf.projects}/{project_id}/{nf.operations}"
            for item in self._requester.GET(path)[str(nf.operations)]:
                return NeonOperations(item)
        except NeonAPIException as err:
            err.operation = "get_first_operation"
            raise err

    def get_list_of_operations(self, project_id: str) -> Iterator[NeonOperations]:
        try:
            path = f"{nf.projects}/{project_id}/{nf.operations}"
            for item in self._requester.GET(path)[str(nf.operations)]:
                yield NeonOperations(item)
        except NeonAPIException as err:
            err.operation = "get_list_of_operations"
            raise err

    def get_operation_details(self, project_id:str, operation_id:str) -> NeonOperationsDetails:
        try:
            path = f"{nf.projects}/{project_id}/{nf.operations}/{operation_id}"
            return NeonOperationsDetails(self._requester.GET(path)["operation"])
        except NeonAPIException as err:
            err.operation = "get_operation_details"
            raise err

    def is_complete(self, project_id: str, sleep_time: float = 0.1, timeout: float = 30.0) -> bool:
        complete, _ = self.completion_time(project_id, sleep_time=sleep_time, timeout=timeout)
        return complete

    def completion_time(self, project_id: str, sleep_time: float = 0.1, timeout: float = 30.0) -> tuple[bool, float]:
        start = time.time()
        so_far = start
        while True:
            op = self.get_first_operation(project_id)
            if op.status == "finished":
                so_far = time.time() - start
                return True, so_far
            else:
                time.sleep(sleep_time)
                so_far = time.time() - start
                if so_far > timeout:
                    return False, so_far

    def create_project(self, project_name: str) -> NeonProject:
        payload = {"project": {"name": project_name}}
        try:
            data = self._requester.POST(str(nf.projects), data=payload)
        except NeonAPIException as err:
            err.operation = "create_project"
            raise err
        return NeonProject(data=data["project"])

    def delete_project(self, project_id: str) -> NeonProject:
        try:
            data = self._requester.DELETE(f"{nf.projects}/{project_id}")["project"]
            return NeonProject(data=data)
        except NeonAPIException as err:
            err.operation = "delete_projects"
            raise err

    def get_projects(self) -> Iterator[NeonProject]:
        try:
            return (NeonProject(item) for item in self._requester.GET(str(nf.projects))[str(nf.projects)])
        except NeonAPIException as err:
            err.operation = "get_projects"
            raise err

    def get_project_by_id(self, project_id: str) -> NeonProject:
        try:
            data = self._requester.GET(f"{nf.projects}/{project_id}")["project"]
            return NeonProject(data=data)
        except NeonAPIException as err:
            err.operation = "get_project_by_id"
            raise err

    def get_projects_by_id(self, project_ids: list[str] = None) -> Iterator[NeonProject]:
        try:
            if project_ids is None:
                yield from self.get_projects()
            elif not isinstance(project_ids, list):
                raise TypeError("project_ids must be a list")
            elif len(project_ids) == 0:
                yield from self.get_projects()
            else:
                for _id in project_ids:
                    yield self.get_project_by_id(_id)
        except NeonAPIException as err:
            err.operation = "get_projects_by_id"
            raise err

    def create_branch(self, project_id: str) -> NeonBranch:
        try:
            data = self._requester.POST(f"projects/{project_id}/{nf.branches}")["branch"]
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "create_branch"
            raise err

    def delete_branch(self, project_id: str, branch_id: str) -> NeonBranch:
        try:
            data = self._requester.DELETE(f"projects/{project_id}/{nf.branches}/{branch_id}")["branch"]
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "delete_branch"
            raise err

    def get_branch_by_id(self, project_id: str, branch_id: str) -> NeonBranch:
        try:
            data = self._requester.GET(f"{nf.projects}/{project_id}/{nf.branches}/{branch_id}")["branch"]
            return NeonBranch(data=data)
        except NeonAPIException as err:
            err.operation = "get_branch_by_id"
            raise err

    def get_branches(self, project_id: str) -> Iterator[NeonBranch]:
        try:
            return (NeonBranch(item) for item in
                    self._requester.GET(f"{nf.projects}/{project_id}/{nf.branches}")[str(nf.branches)])
        except NeonAPIException as err:
            err.operation = "get_branches"
            raise err


class NeonAPI(RawNeonAPI):
    TIMEOUT_DEFAULT = 30.0  # 30 seconds

    def __init__(self, api_key: str = None, sleep_time: float = 0.1, timeout: float = TIMEOUT_DEFAULT) -> None:
        self._api_key = api_key
        self._timeout = timeout
        self._sleep_time = sleep_time
        super().__init__(api_key=self._api_key)

    def create_project(self, project_name: str) -> NeonProject:
        p = super().create_project(project_name)
        if self.is_complete(project_id=p.id, sleep_time=self._sleep_time, timeout=self._timeout):
            return p
        else:
            raise NeonTimeoutException(f"Project creation for {project_name} timed out after {self._timeout} seconds")

    def delete_project(self, project_id: str) -> NeonProject:
        return super().delete_project(project_id)

    def get_project_by_id(self, project_id: str) -> NeonProject:
        p = super().get_project_by_id(project_id)
        if self.is_complete(project_id=p.id, sleep_time=self._sleep_time, timeout=self._timeout):
            return p
        else:
            raise NeonTimeoutException(f"get_project_by_id timed out after {self._timeout} seconds for {p.id}")

    def get_projects_by_id(self, project_ids: list[str] = None) -> Iterator[NeonProject]:
        for p in super().get_projects_by_id(project_ids=project_ids):
            if self.is_complete(project_id=p.id, sleep_time=self._sleep_time, timeout=self._timeout):
                yield p
            else:
                raise NeonTimeoutException(f"get_project_by_id timed out after {self._timeout} seconds for {p.id}")

    def create_branch(self, project_id: str) -> NeonBranch:
        b = super().create_branch(project_id)
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return b
        else:
            raise NeonTimeoutException(f"Branch creation for {project_id} timed out after {self._timeout} seconds")

    def get_branch_by_id(self, project_id: str, branch_id: str) -> NeonBranch:
        b = super().get_branch_by_id(project_id, branch_id)
        if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
            return b
        else:
            raise NeonTimeoutException(f"get_branch_by_id timed out after {self._timeout} seconds for {b.id}")

    def get_branches(self, project_id: str) -> Iterator[NeonBranch]:
        for b in super().get_branches(project_id):
            if self.is_complete(project_id=project_id, sleep_time=self._sleep_time, timeout=self._timeout):
                yield b
            else:
                raise NeonTimeoutException(f"get_branches timed out after {self._timeout} seconds for {b.id}")