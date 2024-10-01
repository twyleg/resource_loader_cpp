// Copyright (C) 2023 twyleg
#pragma once

#include <string>
#include <vector>

namespace ResourceLoader {

//class Resource {

//private:

//public:

//	Resource(const std::string& resourceName, const std::vector<char>& resourceData);

//};

void init();

std::string_view getResource(const std::string& resourceName);

}

