# Copyright (C) 2023 twyleg
import argparse
import hashlib
import jinja2
import shutil

from typing import List, Dict, Union, Optional
from pathlib import Path

FILE_DIRPATH = Path(__file__).parent

DEFAULT_OUTPUT_DIRPATH = Path.cwd()


class Resource:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.filepath_hash = self.generate_short_hash(str(filepath))
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


def generate_resource_loader(output_dir: Path):
    shutil.copyfile(FILE_DIRPATH / "static/resource_loader.h", output_dir / "resource_loader.h")
    shutil.copyfile(FILE_DIRPATH / "static/resource_loader.cc", output_dir / "resource_loader.cc")


def generate_resource(resource_files: List[Path], output_dir: Path, target_name: Optional[str] = None):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(FILE_DIRPATH / "templates/"))
    template = environment.get_template("resource_target.cc.jinja")

    resources = [Resource(Path(resource_filepath)) for resource_filepath in resource_files]

    output_filename = f"resource_{target_name}.cc" if target_name else "resource.cc"

    with open(output_dir / output_filename, "w") as output_file:
        output_file.write(template.render(resources=resources))


def parse_cli_args(cli_args: List[str] = None) -> Dict[str, Union[str, bool, List]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", dest="output_dir", default=DEFAULT_OUTPUT_DIRPATH,
                        help="Output directory")
    parser.add_argument("-t", "--target", dest="target", default=None,
                        help="Target name")
    parser.add_argument('resource_files', metavar='resource_files', type=str, nargs='+', help="Resource files to add.")
    return vars(parser.parse_args(cli_args))


def start():
    args = parse_cli_args()

    resource_files = args["resource_files"]
    output_dir = Path(args["output_dir"])
    target_name = args["target"]

    generate_resource(resource_files, output_dir, target_name)
    generate_resource_loader(output_dir)


if __name__ == '__main__':
    start()
