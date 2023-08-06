import os
import sys
import json
import argparse

from pyneoncli.neon import NeonBranch, NeonProject, NeonOperations, NeonOperationsDetails
from pyneoncli.neonapi import NeonAPI, NeonAPIException, NeonTimeoutException
from pyneoncli.printer import ColorText, Printer


def prompt(msg: str, expected: list[str] = None, yes:bool=False) -> str|None:
    if yes:
        return "y"
    response = input(msg)
    if expected is None:
        return response
    else:
        if response in expected:
            return response
        else:
            return None


class CLICommands:

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args
        self._api_key = args.apikey
        self._api = NeonAPI(args.apikey)
        if args is None:
            self._p = Printer()
            self._c = ColorText()
        else:
            self._p = Printer(nocolor=args.nocolor, filters=args.fieldfilter)
            self._c = ColorText(nocolor=args.nocolor)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self._p = Printer(nocolor=self._args.nocolor, filters=self._args.fieldfilter)
        self._c = ColorText(nocolor=self._args.nocolor)


class CLIList(CLICommands):

    def __init__(self, args: argparse.Namespace = None) -> None:
        super().__init__(args)

    def list_all(self):
        p = None
        for p in self._api.get_projects():
            print(f"{self._p.project_id(p)}")
            for branch in self._api.get_branches(p.id):
                print(f"  {self._p.branch_id(branch)}")
        if p is None:
            print("No projects found")

    def list_projects(self, project_ids: list[str] = None):
        if project_ids is None:
            for p in self._api.get_projects():
                print(f"{self._p.project_id(p)}")
        elif type(project_ids) is list:
            if len(project_ids) == 0:
                for p in self._api.get_projects():
                    self._p.print(p.data)
            else:
                for project_id in project_ids:
                    p = self._api.get_project_by_id(project_id)
                    self._p.print(p.data)
        else:
            print(f"Wrong argument type for list_projects: {type(project_ids)}")
            sys.exit(1)

    def list_branches_for_project(self, p: NeonProject):
        for b in self._api.get_branches(p.id):
            print(f"  {self._p.branch_id(b)}")

    def list_branches_for_projects(self, project_ids: list[str]):
        for i in project_ids:
            project = self._api.get_project_by_id(i)
            self.list_branches_for_project(project)

    def list_branches_for_branch_ids(self, branch_ids: list[str]):
        for i in branch_ids:
            this_pid, this_bid = i.strip().split(":")
            p = self._api.get_project_by_id(this_pid)
            print(f"{self._p.project_id(p)}")
            for b in self._api.get_branches(p.id):
                if this_bid == b.id:
                    print(f"  {self._p.branch_id(b)}")

    def list_operations(self, project_ids: list[str]):
        for id in project_ids:
            ops = self._api.get_list_of_operations(id)
            for op in ops:
                self._p.print(op.data)

    def list_operations_details(self, op_ids: list[str]):
        for op_id in op_ids:
            project_id, operation_id = op_id.strip().split(":")
            op = self._api.get_operation_details(project_id, operation_id)
            self._p.print(op.data)

    def list_projects_by_name(self, project_names:list[str]):
        for project in self._api.get_projects():
            if project.name in project_names:
                print(f"{self._p.project_id(project)}")
                for branch in self._api.get_branches(project.id):
                    print(f"  {self._p.branch_id(branch)}")


class CLIProject(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_one_project(self, project_name: str):
        project = self._api.create_project(project_name)
        self._p.print(project.data)
        return project

    def create_project(self, project_names: list[str]) -> list[str]:
        project_ids = []
        if project_names is not None and type(project_names) is list:
            for project_name in project_names:
                try:
                    p = self.create_one_project(project_name)
                    project_ids.append(p.id)
                except NeonAPIException as e:
                    print(f"{self._c.red(msg='Error creating project: ')} {e.path}")
                    print(f"  Status Code : {e.err.response.status_code}")
                    print(f"  Reason      : {e.err.response.reason}")
                    print(f"  Text        : {e.err.response.text}")
        return project_ids

    def delete_one_project(self, project_id: str, check=True):
        if check:
            resp = prompt(msg=f"Are you sure you want to delete project {project_id}? (y/n): ",
                          expected=["y", "Y", "yes", "Yes", "YES"],
                          yes=self._args.yes)
            if resp:
                project = self._api.delete_project(project_id)
                self._p.print(project.data)
                return project
            else:
                print("Aborted project deletion")
                return None
        else:
            project = self._api.delete_project(project_id)
            self._p.print(project.data)
            return project

    def delete_projects(self, project_ids: list[str], check=True) -> list[str]:
        deleted_project_ids = []
        if project_ids is not None and type(project_ids) is list:
            for project_id in project_ids:
                try:
                    p = self.delete_one_project(project_id, check=check)
                    if p is not None:
                        deleted_project_ids.append(p.id)
                except NeonAPIException as e:
                    print(f"{self._c.red(msg='Error deleting project: ')} {e.path}")
                    print(f"  Status Code : {e.err.response.status_code}")
                    print(f"  Reason      : {e.err.response.reason}")
                    print(f"  Text        : {e.err.response.text}")
        else:
            print("You must specify a project id with --project_id for delete project")
            sys.exit(1)
        return deleted_project_ids

    def delete_all_projects(self):
        project_ids = []
        any_ids = False
        resp = prompt(msg=f"Are you sure you want to delete all projects? (y/n): ",
                      expected=["y", "Y", "yes", "Yes", "YES"],
                      yes=self._args.yes)
        if resp is not None:
            for project in self._api.get_projects():
                self._api.delete_project(project.id)
                project_ids.append(project.id)
                print(f"{project.id} deleted")
                any_ids = True
            if not any_ids:
                print("No projects to delete")
            return project_ids
        else:
            print("Aborting delete all projects")
            return None


class CLIBranch(CLICommands):

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)

    def create_one_branch(self, project_id: str):
        project = self._api.get_project_by_id(project_id)
        branch = self._api.create_branch(project.id)
        self._p.print(branch.data)
        return branch

    def create_branch(self, project_ids: list[str]):
        branches = []
        for project_id in project_ids:
            branch = self.create_one_branch(project_id)
            branches.append(branch)
        return branches

    def delete_branch(self, branch_ids: list[str]):
        if branch_ids is not None and type(branch_ids) is list:
            for id in branch_ids:
                pid, bid = id.strip().split(":")
                b = self._api.delete_branch(pid, bid)
                self._p.print(b.data)
        else:
            print("You must specify a branch id with --branch_id for delete branch")
            sys.exit(1)


class CLIDispatcher:

    def __init__(self) -> None:
        self._printer = Printer()

    @staticmethod
    def dispatch_list(args: argparse.Namespace):
        try:
            any_args = False
            l = CLIList(args)
            if args.all:
                l.list_all()
                any_args = True
            elif args.branch_ids:
                l.list_branches_for_branch_ids(args.branch_ids)
                any_args = True
            elif args.project_ids:
                l.list_projects(args.project_ids)
                any_args = True
            elif args.project_names:
                l.list_projects_by_name(args.project_names)
                any_args = True
            elif args.projects:
                l.list_projects()
                any_args = True
            elif args.branch_ids:
                l.list_branches_for_branch_ids(args.branch_ids)
                any_args = True
            elif args.op_project_ids:
                l.list_operations(args.op_project_ids)
                any_args = True
            elif args.op_ids:
                l.list_operations_details(args.op_ids)
                any_args = True

            if not any_args:
                l.list_all()

        except NeonAPIException as api_error:
            print(api_error)
            sys.exit(1)

        except NeonTimeoutException as timeout_error:
            print(timeout_error)
            sys.exit(1)

    @staticmethod
    def dispatch_main(args: argparse.Namespace):
        pass

    @staticmethod
    def dispatch_project(args: argparse.Namespace):
        p = CLIProject(args)
        if args.create_names:
            p.create_project(args.create_names)
        if args.delete_ids:
            p.delete_projects(args.delete_ids)
        if args.delete_all:
            p.delete_all_projects()

    @staticmethod
    def dispatch_branch(args: argparse.Namespace):
        b = CLIBranch(args=args)
        if args.project_ids:
            b.create_branch(args.project_ids)
        if args.delete_ids:
            b.delete_branch(args.delete_ids)

