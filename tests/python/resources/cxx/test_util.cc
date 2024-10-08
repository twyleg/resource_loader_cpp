// Copyright (C) 2023 twyleg
#include "resource_loader.h"

#include <iostream>


int main(int argc, char *argv[]) {

	if(argc != 2) {
		std::cerr << "Error: wrong number of args!\n\r";
		return -1;
	}


	std::cout << ResourceLoader::getResourceAsString(argv[1]);
	return 0;
}
