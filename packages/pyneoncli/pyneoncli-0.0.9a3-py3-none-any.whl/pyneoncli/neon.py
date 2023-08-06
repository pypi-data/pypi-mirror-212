import pprint


class NeonObject:

    def __init__(self, data: dict) -> None:
        self._data = data
        self._type = self.__class__.__name__

    @property
    def data(self):
        return self._data

    def obj_type(self):
        return self._type

    @property
    def id(self):
        return self._data["id"]

    @property
    def name(self):
        return self._data["name"]

    def __str__(self) -> str:
        return pprint.pformat(self._data)

    def __repr__(self) -> str:
        return f"NeonObject(data={self._data})"


class NeonOperations(NeonObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data=data)
        self._type = "operation"

    @property
    def project_id(self):
        return self._data["project_id"]

    @property
    def status(self):
        return self._data["status"]

    @property
    def action(self):
        return self._data["action"]


class NeonOperationsDetails(NeonObject):
    def __init__(self, data: dict) -> None:
        super().__init__(data=data)
        self._type = "operation_details"

    @property
    def status(self):
        return self._data["status"]

    def action(self):
        return self._data["action"]


class NeonProject(NeonObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data=data)
        self._type = "project"

    @property
    def project(self):
        return self._data

    @property
    def project_id(self):
        return self._data["id"]



class NeonBranch(NeonObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data=data)
        self._type = "branch"

    @property
    def project_id(self):
        return self._data["project_id"]

    def branch(self):
        return self._data
