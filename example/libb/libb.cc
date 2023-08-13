// Copyright (C) 2023 twyleg
#include <resource_loader.h>

#include <fmt/core.h>


namespace liba {

void printResourceFromLibB() {
	fmt::print(ResourceLoader::getResource("example_resource_from_libb.txt"));
}

}
