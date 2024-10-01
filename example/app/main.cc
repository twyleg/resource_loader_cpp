// Copyright (C) 2020 twyleg
#include <liba/liba.h>
#include <libb/libb.h>

#include <resource_loader.h>

#include <fmt/core.h>

int main(int argc, char *argv[]) {

	liba::printResourceFromLibA();
	libb::printResourceFromLibB();

	fmt::print(ResourceLoader::getResource("example_resource_one.txt"));
	fmt::print(ResourceLoader::getResource("example_resource_two.txt"));

	fmt::print(ResourceLoader::getResource("liba/example_resource_from_liba.txt"));
	fmt::print(ResourceLoader::getResource("libb/example_resource_from_libb.txt"));

	return 0;
}
