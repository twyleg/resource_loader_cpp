// Copyright (C) 2023 twyleg
#include <resource_loader.h>

#include <fmt/core.h>


namespace libb {

void printResourceFromLibB() {
	fmt::print(ResourceLoader::getResource("libb/example_resource_from_libb.txt"));
}

}
