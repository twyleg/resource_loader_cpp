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

	return 0;
}
