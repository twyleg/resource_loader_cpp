# Copyright (C) 2023 twyleg
import argparse
import hashlib
import json

import jinja2
import shutil

from typing import List, Dict, Union, Optional
from pathlib import Path

FILE_DIRPATH = Path(__file__).parent

DEFAULT_OUTPUT_DIRPATH = Path.cwd()


class Resource:
    def __init__(self, filepath: Path, load_data=True):
        self.filepath = filepath
        self.filepath_hash = self.generate_short_hash(str(filepath))
        if load_data:
            self.data_lines = self.load_data_lines_from_file(filepath)

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

            with open(self._cache_filepath, "r") as cache_file:
                cache_file_data = cache_file.read()
                self.cached_resources = json.loads(cache_file_data)
        else:
            self.cached_resources = {
                "files": []
            }

    def add_resource_file_to_cache(self, resource_filepath: Path):
        self.cached_resources["files"].append(str(resource_filepath))

    def get_cached_resources(self) -> List[Path]:
        return [Path(cached_resource) for cached_resource in self.cached_resources["files"]]

    def write_cache(self):
        with open(self._cache_filepath, "w") as cache_file:
            json.dump(self.cached_resources, cache_file)


def generate_resource_loader(resource_filepaths: List[Path], output_dir: Path):
    shutil.copyfile(FILE_DIRPATH / "static/resource_loader.h", output_dir / "resource_loader.h")
    # shutil.copyfile(FILE_DIRPATH / "static/resource_loader.cc", output_dir / "resource_loader.cc")

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(FILE_DIRPATH / "templates/"))
    template = environment.get_template("resource_loader.cc.jinja")

    resources = [Resource(resource_filepath, load_data=False) for resource_filepath in resource_filepaths]

    with open(output_dir / "resource_loader.cc", "w") as output_file:
        output_file.write(template.render(resources=resources))


def generate_resource(resource_filepath: Path, output_dir: Path):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(FILE_DIRPATH / "templates/"))
    template = environment.get_template("resource.cc.jinja")

    resource = Resource(resource_filepath)

    output_filename = f"resource_{resource_filepath.name}.cc"

    with open(output_dir / output_filename, "w") as output_file:
        output_file.write(template.render(resource=resource))


def generate_resources(resource_filepaths: List[Path], output_dir: Path):
    cache = Cache(output_dir)
    for resource_filepath in resource_filepaths:
        generate_resource(resource_filepath, output_dir)
        cache.add_resource_file_to_cache(resource_filepath)
    cache.write_cache()
    generate_resource_loader(cache.get_cached_resources(), output_dir)


def parse_cli_args(cli_args: List[str] = None) -> Dict[str, Union[str, bool, List]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", dest="output_dir", default=DEFAULT_OUTPUT_DIRPATH,
                        help="Output directory")
    parser.add_argument('resource_files', metavar='resource_files', type=str, nargs='*', help="Resource files to add.")
    return vars(parser.parse_args(cli_args))


def start():
    args = parse_cli_args()

    resource_filepaths = [Path(resource_file) for resource_file in args["resource_files"]]
    output_dir = Path(args["output_dir"])

    generate_resources(resource_filepaths, output_dir)



if __name__ == '__main__':
    start()
