# pyneoncli

A python package and command line tool for interaction with the [Neon](https://neon.tech) Serverless Postgres [API](https://api-docs.neon.tech/reference/getting-started-with-neon-api).

This is a work in progress and this version is incomplete. 

This version only supports the Neon V2 API. 

The program can read the NEON_API_KEY from the environment or it can he loaded from a .env field in the current working directory.

## Installation

You can install the package from PyPi using pip:
```commandline
pip install pyneoncli
```
This will install the package and the command line tool. You can invoke the command line tool using the command `neoncli`.
# Operation
```
usage: neoncli [-h] [--apikey APIKEY] [--version] [--nocolor] [--yes] [-f FIELDFILTER]
               {list,project,branch} ...

neoncli -  neon command line client

options:
  -h, --help            show this help message and exit
  --apikey APIKEY       Specify NEON API Key (env NEON_API_KEY)
  --version             show program's version number and exit
  --nocolor             Turn off Color output
  --yes                 Answer yes to all prompts
  -f FIELDFILTER, --fieldfilter FIELDFILTER
                        Enter field values to filter results on

subcommands:
  Invoke a specific neon command

  {list,project,branch}
                        e.g. neoncli list will list all projects
    list                List Neon objects
    project             Create and delete Neon projects
    branch              create and delete Neon branches

use neoncli list  -h for more information on the list command
use neoncli branch  -h for more information on the branch command
use neoncli project -h for more information on the project command

Version : 0.0.9a2
```