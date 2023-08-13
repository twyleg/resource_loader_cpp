# Copyright (C) 2023 twyleg
cmake_minimum_required(VERSION 3.26.4)


project(resource_loader_example)


# Resource loader
add_subdirectory(external/resource_loader_cpp/)


# Libs
add_subdirectory(liba/)
add_subdirectory(libb/)


# App
add_subdirectory(app/)
