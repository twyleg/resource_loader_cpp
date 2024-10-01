// Copyright (C) 2023 twyleg
#include <resource_loader.h>

#include <fmt/core.h>


namespace liba {

void printResourceFromLibA() {
	fmt::print(ResourceLoader::getResource("liba/example_resource_from_liba.txt"));
}

}
