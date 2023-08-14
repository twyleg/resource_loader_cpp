# Copyright (C) 2023 twyleg
cmake_minimum_required(VERSION 3.25.1)


project(resource_loader_example)

#
# Resource loader
# init_resource_loader() needs to be called from top level CMakeLists.txt before usage of the reosurce loader
#
add_subdirectory(external/resource_loader_cpp/)
init_resource_loader()


# Libs
add_subdirectory(liba/)
add_subdirectory(libb/)


# App
add_subdirectory(app/)
