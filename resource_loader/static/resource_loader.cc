// Copyright (C) 2023 twyleg
#include "resource_loader.h"

#include <vector>
#include <unordered_map>
#include <string>

namespace {

std::unordered_map<std::string, const std::vector<char>&> resources;

}


namespace ResourceLoader {


std::string_view getResource(const std::string& resourceName){
	auto& resource = resources.find(resourceName)->second;
	return std::string_view(resource.data(), resource.size());
}


Resource::Resource(const std::string& resourceName, const std::vector<char>& resourceData) {
	resources.emplace(resourceName, resourceData);
}

}
