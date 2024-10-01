// Copyright (C) 2024 twyleg
#include "resource_loader.h"

#include <vector>
#include <unordered_map>
#include <string>
#include <iostream>

namespace ResourceLoader {


extern const std::vector<char> data_8a838e60fb;

}

namespace {

std::unordered_map<std::string, const std::vector<char>&>& getResourcesMap();

void init(){
    getResourcesMap().emplace("liba/example_resource_from_liba.txt", ResourceLoader::data_8a838e60fb);
}

std::unordered_map<std::string, const std::vector<char>&>& getResourcesMap() {
    static std::unordered_map<std::string, const std::vector<char>&> resourceMap;

    static bool isInitialized = false;
    if (!isInitialized) {
        isInitialized = true;
        init();
    }

    return resourceMap;
}

}

namespace ResourceLoader {


std::string_view getResource(const std::string& resourceName){
	auto& resource = getResourcesMap().find(resourceName)->second;
	return std::string_view(resource.data(), resource.size());
}




}