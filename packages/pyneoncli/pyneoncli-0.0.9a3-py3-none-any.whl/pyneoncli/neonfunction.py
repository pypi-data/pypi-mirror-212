from enum import Enum


class NeonFunction(Enum):
    projects = "projects"
    branches = "branches"
    operations = "operations"

    def __str__(self) -> str:
        return self.value

