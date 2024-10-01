// Copyright (C) 2024 twyleg
#include <liba/liba.h>
#include <libb/libb.h>

#include <resource_loader.h>

#include <fmt/core.h>

#include <filesystem>

int main(int argc, char *argv[]) {

	liba::printResourceFromLibA();
	libb::printResourceFromLibB();

	fmt::print(ResourceLoader::getResourceAsString("example_resource_one.txt"));
	fmt::print(ResourceLoader::getResourceAsString("example_resource_two.txt"));

	fmt::print(ResourceLoader::getResourceAsString("liba/example_resource_from_liba.txt"));
	fmt::print(ResourceLoader::getResourceAsString("liba/example_resource_from_lib.txt"));

	fmt::print(ResourceLoader::getResourceAsString("libb/example_resource_from_libb.txt"));
	fmt::print(ResourceLoader::getResourceAsString("libb/example_resource_from_lib.txt"));


	ResourceLoader::saveResourceToFile("STS-129_Atlantis_Ready_to_Fly.jpg", std::filesystem::current_path() / "test_image.jpg");

	return 0;
}
