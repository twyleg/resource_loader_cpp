// Copyright (C) 2023 twyleg
#pragma once

#include <string>
#include <vector>
#include <filesystem>

namespace ResourceLoader {

void init();

std::string_view getResourceAsString(const std::string& resourceName);
const std::vector<unsigned char>& getResourceAsVector(const std::string& resourceName);
void saveResourceToFile(const std::string& resourceName, const std::filesystem::path& filePath);

}

