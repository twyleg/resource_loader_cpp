// Copyright (C) 2024 twyleg
#include "resource_loader.h"

#include <vector>
#include <unordered_map>
#include <string>
#include <fstream>

namespace ResourceLoader {

extern const std::vector<unsigned char> data_8c0c4a5e43;
extern const std::vector<unsigned char> data_fd341f148f;
extern const std::vector<unsigned char> data_89f94aa0c0;
extern const std::vector<unsigned char> data_10d7e13243;

}

namespace {

std::unordered_map<std::string, const std::vector<unsigned char>&>& getResourcesMap();

void init(){
    getResourcesMap().emplace("example_resource_one.txt", ResourceLoader::data_8c0c4a5e43);
    getResourcesMap().emplace("example_resource_two.txt", ResourceLoader::data_fd341f148f);
    getResourcesMap().emplace("prefix_a/example_resource_one.txt", ResourceLoader::data_89f94aa0c0);
    getResourcesMap().emplace("prefix_b/example_resource_two.txt", ResourceLoader::data_10d7e13243);
}

std::unordered_map<std::string, const std::vector<unsigned char>&>& getResourcesMap() {
    static std::unordered_map<std::string, const std::vector<unsigned char>&> resourceMap;

    static bool isInitialized = false;
    if (!isInitialized) {
        isInitialized = true;
        init();
    }

    return resourceMap;
}

}

namespace ResourceLoader {


std::string_view getResourceAsString(const std::string& resourceName){
	auto& resource = getResourcesMap().find(resourceName)->second;
	return std::string_view(reinterpret_cast<const char*>(resource.data()), resource.size());
}

const std::vector<unsigned char>& getResourceAsVector(const std::string& resourceName){
    auto& resource = getResourcesMap().find(resourceName)->second;
    return resource;
}

void saveResourceToFile(const std::string& resourceName, const std::filesystem::path& filePath){
    const auto& resource = getResourceAsVector(resourceName);
    std::ofstream outputStream(filePath, std::ios::binary);
    outputStream.write(reinterpret_cast<const char*>(resource.data()), resource.size());
}


}
