# Copyright (C) 2024 twyleg
cmake_minimum_required(VERSION 3.16.3)


project(resource_loader_generator_cmake_example)

#
# Resource loader
# init_resource_loader() needs to be called from top level CMakeLists.txt before usage of the resource loader
#
add_subdirectory(external/resource_loader/)
resource_loader_init(TARGET resources)


# Libs
add_subdirectory(libs/liba/)
add_subdirectory(libs/libb/)

# App
add_subdirectory(app/)
