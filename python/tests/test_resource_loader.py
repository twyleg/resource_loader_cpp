# Copyright (C) 2023 twyleg
import unittest
import tempfile
import shutil
import glob

from subprocess import check_output, run
from pathlib import Path
from resource_loader.resource_loader import generate_resources, _generate_resource_loader

FILE_DIR = Path(__file__).parent

#
# General naming convention for unit tests:
#               test_INITIALSTATE_ACTION_EXPECTATION
#


class ImageTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir_path = Path(tempfile.mkdtemp())
        print(self.tmp_dir_path)

    def compile_test_app(self):
        shutil.copyfile(FILE_DIR / "cxx/test_util.cc", self.tmp_dir_path / "test_util.cc")
        cc_files = glob.glob(str(self.tmp_dir_path / "*.cc"))
        command = ["g++", "-o", self.tmp_dir_path / "test_util"]
        command.extend(cc_files)
        print(command)
        run(command)

    def assert_resource(self, expected_content: str, resource_filepath: str):
        self.assertEqual(expected_content.encode(), check_output([self.tmp_dir_path / "test_util", resource_filepath]))


    def test_CleanEnvironment_GenerateResources_ResourcesAvailable(self):
        generate_resources([Path("resources/example_a.txt"), Path("resources/example_a.xsd")], self.tmp_dir_path)
        generate_resources([Path("resources/example_b.txt"), Path("resources/example_b.xsd")], self.tmp_dir_path)
        self.compile_test_app()
        self.assert_resource("Example text file for target a.\n", "resources/example_a.txt")
        self.assert_resource("Example text file for target b.\n", "resources/example_b.txt")
