# Copyright (C) 2023 twyleg
set(TARGET_NAME libb)


#
# find packages
#
find_package(fmt REQUIRED)


#
# Add resource to be embedded in binary
#
add_resources(RESOURCE_FILES example_resource_from_libb.txt)


#
# add source files to target
#
add_library(${TARGET_NAME}
	libb.cc
	libb.h
)


#
# set target properties
#
set_target_properties(${TARGET_NAME}
	PROPERTIES
	CXX_STANDARD 17
	INCLUDE_CURRENT_DIR ON
)


#
# link against libs
#
target_link_libraries(${TARGET_NAME}
	fmt::fmt
	resource_loader
)


#
# add parent folder to targets include directories
#
target_include_directories(${TARGET_NAME}
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..
)
