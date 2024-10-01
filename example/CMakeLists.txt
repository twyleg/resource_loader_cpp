# Copyright (C) 2023 twyleg
cmake_minimum_required(VERSION 3.25.1)


project(resource_loader_example)

#
# Resource loader
# init_resource_loader() needs to be called from top level CMakeLists.txt before usage of the reosurce loader
#
add_subdirectory(external/resource_loader_cpp/)
resource_loader_init(TARGET resources)


# Libs
add_subdirectory(libs/liba/)
add_subdirectory(libs/libb/)

# App
add_subdirectory(app/)
