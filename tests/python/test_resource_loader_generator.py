# Copyright (C) 2024 twyleg
# fmt: off
import pytest
import shutil
import glob

from subprocess import check_output, run
from pathlib import Path

from resource_loader_generator.resource_loader_generator import Cache, Resource, ResourceLoaderGenerator

FILE_DIR = Path(__file__).parent

#
# General naming convention for unit tests:
#               test_INITIALSTATE_ACTION_EXPECTATION
#

@pytest.fixture
def txt_test_resource_a():
    return Resource(FILE_DIR / "resources/test_data/test_resource_a.txt", "test_resource_a.txt")

@pytest.fixture
def txt_test_resource_b():
    return Resource(FILE_DIR / "resources/test_data/test_resource_b.txt", "test_resource_b.txt")

@pytest.fixture
def empty_cache(tmp_path):
    return Cache(tmp_path)

@pytest.fixture
def cache_with_entry(tmp_path, txt_test_resource_a):
    cache = Cache(tmp_path)
    cache.add_resource(txt_test_resource_a)
    return cache

class TestCache:
    def test_EmptyCache_AddResourceToCache_ResourceAddedToChacheSuccessfully(
            self,
            empty_cache,
            txt_test_resource_a,
            txt_test_resource_b
    ):
        empty_cache.add_resource(txt_test_resource_a)

        assert txt_test_resource_a in empty_cache
        assert txt_test_resource_b not in empty_cache

    def test_CacheWithEntries_CheckForEntries_CorrectResultsRetunedSuccessfully(
            self,
            tmp_path,
            cache_with_entry,
            txt_test_resource_a,
            txt_test_resource_b
    ):
        cache_with_entry.flush()

        new_cache = Cache(tmp_path)

        assert txt_test_resource_a in new_cache
        assert txt_test_resource_b not in new_cache

        new_cache.add_resource(txt_test_resource_b)
        new_cache.flush()

        new_cache = Cache(tmp_path)

        assert txt_test_resource_a in new_cache
        assert txt_test_resource_b in new_cache

class TestResourceLoader:

    def compile_test_app(self, tmp_path: Path):
        shutil.copyfile(FILE_DIR / "resources/cxx/test_util.cc", tmp_path / "test_util.cc")
        cc_files = glob.glob(str(tmp_path / "*.cc"))
        command = ["g++", "-o", str(tmp_path / "test_util")]
        command.extend(cc_files)
        run(command)

    def run_test_app(self, tmp_path: Path, resource_name: str) -> str:
        return check_output([tmp_path / "test_util", resource_name]).decode("utf-8")

    def test_ResourceLoaderGeneratorWithEmptyCache_AddResources_ResourcesLoadedSuccessfully(
            self,
            tmp_path,
            txt_test_resource_a,
            txt_test_resource_b
    ):
        resource_loader_generator = ResourceLoaderGenerator(tmp_path)
        resource_loader_generator.add_resource(txt_test_resource_a)
        resource_loader_generator.add_resource(txt_test_resource_b)
        resource_loader_generator.generate()

        self.compile_test_app(tmp_path)
        assert self.run_test_app(tmp_path, "test_resource_a.txt") == "Example text file for target a.\n"
        assert self.run_test_app(tmp_path, "test_resource_b.txt") == "Example text file for target b.\n"

    def test_ResourceLoaderGeneratorWithCacheEntries_AddResources_ResourcesLoadedSuccessfully(
            self,
            tmp_path,
            txt_test_resource_a,
            txt_test_resource_b
    ):
        resource_loader_generator = ResourceLoaderGenerator(tmp_path)
        assert len(resource_loader_generator.cache) == 0
        resource_loader_generator.add_resource(txt_test_resource_a)
        resource_loader_generator.add_resource(txt_test_resource_b)
        resource_loader_generator.generate()

        resource_loader_generator = ResourceLoaderGenerator(tmp_path)
        assert len(resource_loader_generator.cache) == 2
        resource_loader_generator.add_resource(txt_test_resource_a)
        resource_loader_generator.add_resource(txt_test_resource_b)
        assert len(resource_loader_generator.cache) == 2
        resource_loader_generator.generate()

        self.compile_test_app(tmp_path)
        assert self.run_test_app(tmp_path, "test_resource_a.txt") == "Example text file for target a.\n"
        assert self.run_test_app(tmp_path, "test_resource_b.txt") == "Example text file for target b.\n"
