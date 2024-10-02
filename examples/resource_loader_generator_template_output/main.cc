// Copyright (C) 2024 twyleg
#include "resource_loader.h"

#include <fmt/core.h>

#include <filesystem>

int main(int argc, char *argv[]) {


	fmt::print(ResourceLoader::getResourceAsString("example_resource_one.txt"));
	fmt::print(ResourceLoader::getResourceAsString("example_resource_two.txt"));

	fmt::print(ResourceLoader::getResourceAsString("prefix_a/example_resource_one.txt"));
	fmt::print(ResourceLoader::getResourceAsString("prefix_b/example_resource_two.txt"));

	ResourceLoader::saveResourceToFile("example_resource_one.txt", std::filesystem::current_path() / "example_resource_one.txt");

	return 0;
}
