cmake_minimum_required(VERSION 3.1.0)

project(example)

include(../cmake/resource_loader.cmake)

# Libs
add_subdirectory(liba/)
add_subdirectory(libb/)

# App
add_subdirectory(app/)
