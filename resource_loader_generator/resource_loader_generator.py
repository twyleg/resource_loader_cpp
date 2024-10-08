# Copyright (C) 2024 twyleg
import argparse
import hashlib
import json
import os

import jinja2
import shutil

from typing import List, Dict
from pathlib import Path


FILE_DIR = Path(__file__).parent


class Resource:
    def __init__(self, filepath: Path, name: str):
        self.filepath = filepath
        self.name = name
        self.name_hash = self._generate_short_hash(self.name)
        self.size = 0
        self.data_lines: List[str] = []

    def to_dict(self) -> dict:
        return {
            "file_path": str(self.filepath),
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, resource_as_dict: Dict[str, str]) -> "Resource":
        return Resource(Path(resource_as_dict["file_path"]), resource_as_dict["name"])

    @classmethod
    def _generate_short_hash(cls, input: str):
        return hashlib.sha1(input.encode("UTF-8")).hexdigest()[:10]

    @classmethod
    def _chunks(cls, lst, n):
        return [lst[i : i + n] for i in range(0, len(lst), n)]

    def load_data(self) -> None:
        values = []
        with open(self.filepath, "rb") as file:
            while True:
                c = file.read(1)
                self.size += 1
                if not c:
                    break
                values.append(ord(c))

        for chunk in self._chunks(values, 8):
            self.data_lines.append(" ".join(["{0:#0{1}x},".format(value, 4) for value in chunk]))


class Cache:

    def __init__(self, output_dir_path: Path, cache_filename="resource_loader_cache.json"):
        self._output_dir_path = output_dir_path
        self._cache_file_path = output_dir_path / cache_filename

        self.cached_resources: Dict[str, Resource] = self._read_cache()

    def __contains__(self, resource: Resource) -> bool:
        return resource.name_hash in self.cached_resources

    def __len__(self) -> int:
        return len(self.cached_resources)

    def _read_cache(self) -> Dict[str, Resource]:
        if self._cache_file_path.exists():
            with open(self._cache_file_path, "r") as cache_file:
                cache_file_data = cache_file.read()
                input_json = json.loads(cache_file_data)
                return {filename_hash: Resource.from_dict(resource_as_dict) for filename_hash, resource_as_dict in input_json["resources"].items()}
        else:
            return {}

    def add_resource(self, resource: Resource):
        self.cached_resources[resource.name_hash] = resource

    def flush(self):
        output_obj = {"resources": {filename_hash: cached_resource.to_dict() for filename_hash, cached_resource in self.cached_resources.items()}}
        with open(self._cache_file_path, "w") as cache_file:
            json.dump(output_obj, cache_file, indent=2)


class ResourceLoaderGenerator:

    def __init__(self, output_dir_path: Path):
        self.output_dir_path = output_dir_path
        self.cache = Cache(output_dir_path)
        self._environment = jinja2.Environment(loader=jinja2.FileSystemLoader(FILE_DIR / "resources/templates/"))

    def generate(self):
        self._generate_resource_loader_cpp_files()
        self._generate_resource_loader_header_files()
        for _, resource in self.cache.cached_resources.items():
            self._generate_resource_cpp_file(resource)
        self.cache.flush()

    def _generate_resource_loader_header_files(self):
        resource_loader_header_source_filepath = FILE_DIR / "resources/static/resource_loader.h"
        resource_loader_header_destination_filepath = self.output_dir_path / "resource_loader.h"
        if not resource_loader_header_destination_filepath.exists():
            shutil.copyfile(resource_loader_header_source_filepath, resource_loader_header_destination_filepath)

    def _generate_resource_loader_cpp_files(self):
        template = self._environment.get_template("resource_loader.cc.jinja")
        with open(self.output_dir_path / "resource_loader.cc", "w") as output_file:
            output_file.write(template.render(resources=self.cache.cached_resources.values()))

    def _generate_resource_cpp_file(self, resource: Resource) -> None:
        output_filename = f"resource_{resource.name_hash}.cc"
        output_filepath = self.output_dir_path / output_filename
        if not output_filepath.exists() or os.path.getmtime(resource.filepath) > os.path.getmtime(output_filepath):
            template = self._environment.get_template("resource.cc.jinja")
            with open(output_filepath, "w") as output_file:
                output_file.write(template.render(resource=resource))

    def add_resource(self, resource: Resource):
        if resource not in self.cache:
            resource.load_data()
            self.cache.add_resource(resource)
        else:
            self.cache.cached_resources[resource.name_hash].load_data()


def parse_cli_args(cli_args: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", dest="output_dir", default=Path.cwd(), help="Output directory")
    parser.add_argument("-p", "--prefix", dest="prefix", default=None, help="Resource prefix")
    parser.add_argument("resource_file", type=str, nargs="?", default=None, help="Resource file to add.")
    return parser.parse_args(cli_args)


def main():
    args = parse_cli_args()

    output_dir_path = Path(args.output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)
    resource_loader_generator = ResourceLoaderGenerator(output_dir_path)

    if args.resource_file:
        resource_file_path = Path(args.resource_file)
        resource_name = f"{args.prefix}/{resource_file_path.name}" if args.prefix else resource_file_path.name
        resource = Resource(resource_file_path.absolute(), resource_name)
        resource_loader_generator.add_resource(resource)
        print(resource.name_hash)

    resource_loader_generator.generate()


if __name__ == "__main__":
    main()
