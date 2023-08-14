# Copyright (C) 2023 twyleg
import argparse
import hashlib
import json
import sys

import jinja2
import shutil

from typing import List, Dict, Union, Optional
from pathlib import Path

FILE_DIRPATH = Path(__file__).parent

DEFAULT_OUTPUT_DIRPATH = Path.cwd()


class Resource:
    def __init__(self, filepath: Path, prefix="", load_data=True):
        self.filepath = filepath
        self.prefix = prefix
        self.name = f"{prefix}/{filepath}" if prefix else str(filepath)
        self.name_hash = self.generate_short_hash(self.name)
        if load_data:
            self.data_lines = self.load_data_lines_from_file(filepath)

    def to_dict(self) -> dict:
        return {
            "filepath": str(self.filepath),
            "prefix": self.prefix,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, input: dict) -> "Resource":
        return Resource(Path(input["filepath"]), input["prefix"], load_data=False)

    @classmethod
    def generate_short_hash(cls, input: str):
        return hashlib.sha1(input.encode("UTF-8")).hexdigest()[:10]

    @classmethod
    def chunks(cls, lst, n):
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    @classmethod
    def load_data_lines_from_file(cls, filepath: Path) -> List[str]:

        values = []
        with open(filepath, "r") as file:
            while True:
                c = file.read(1)
                if not c:
                    break
                values.append(ord(c))

        data_lines = []
        for chunk in cls.chunks(values, 8):
            data_lines.append(" ".join(["{0:#0{1}x},".format(value, 4) for value in chunk]))

        return data_lines

class Cache:

    def __init__(self, output_dirpath: Path):
        self._output_dirpath = output_dirpath
        self._cache_filepath = output_dirpath / "resource_loader_cache.json"

        if self._cache_filepath.exists():
            self.cached_resources = self.read_cache()
        else:
            self.cached_resources: List[Resource] = []

    def read_cache(self) -> List[Resource]:
        with open(self._cache_filepath, "r") as cache_file:
            cache_file_data = cache_file.read()
            input_json = json.loads(cache_file_data)
            return [Resource.from_dict(resource_as_dict) for resource_as_dict in input_json["resources"]]

    def add_resource_file_to_cache(self, resource: Resource):
        self.cached_resources.append(resource)

    def get_cached_resources(self) -> List[Resource]:
        return self.cached_resources

    def write_cache(self):
        output_obj = {
            "resources": [cached_resource.to_dict() for cached_resource in self.cached_resources]
        }
        with open(self._cache_filepath, "w") as cache_file:
            json.dump(output_obj, cache_file)


def generate_resource_loader(resources: List[Resource], output_dir: Path):

    resource_loader_header_destination_filepath = output_dir / "resource_loader.h"
    if not resource_loader_header_destination_filepath.exists():
        shutil.copyfile(FILE_DIRPATH / "static/resource_loader.h", resource_loader_header_destination_filepath)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(FILE_DIRPATH / "templates/"))
    template = environment.get_template("resource_loader.cc.jinja")

    # resources = [Resource(resource_filepath, load_data=False) for resource_filepath in resource_filepaths]

    with open(output_dir / "resource_loader.cc", "w") as output_file:
        output_file.write(template.render(resources=resources))


def generate_resource(resource: Resource, output_dir: Path):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(FILE_DIRPATH / "templates/"))
    template = environment.get_template("resource.cc.jinja")

    output_filename = f"resource_{resource.filepath.name}.cc"

    with open(output_dir / output_filename, "w") as output_file:
        output_file.write(template.render(resource=resource))


def generate_resources(resource_filepaths: List[Path], output_dir: Path, prefix: str = ""):
    cache = Cache(output_dir)
    for resource_filepath in resource_filepaths:
        resource = Resource(resource_filepath, prefix)
        generate_resource(resource, output_dir)
        cache.add_resource_file_to_cache(resource)
    cache.write_cache()
    generate_resource_loader(cache.get_cached_resources(), output_dir)


def parse_cli_args(cli_args: List[str] = None) -> Dict[str, Union[str, bool, List]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", dest="output_dir", default=DEFAULT_OUTPUT_DIRPATH,
                        help="Output directory")
    parser.add_argument("-p", "--prefix", dest="prefix", default="",
                        help="Output directory")
    parser.add_argument('resource_files', metavar='resource_files', type=str, nargs='*', help="Resource files to add.")
    return vars(parser.parse_args(cli_args))


def start():
    args = parse_cli_args()

    resource_filepaths = [Path(resource_file) for resource_file in args["resource_files"]]
    output_dir = Path(args["output_dir"])
    prefix = args["prefix"]

    generate_resources(resource_filepaths, output_dir, prefix)



if __name__ == '__main__':
    start()
