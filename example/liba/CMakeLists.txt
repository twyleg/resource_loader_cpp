# Copyright (C) 2023 twyleg
set(TARGET_NAME liba)


#
# find packages
#
find_package(fmt REQUIRED)


#
# add resource to be embedded in binary
#
add_resources(PREFIX liba
	example_resource_from_liba.txt
)



#
# add source files to target
#
add_library(${TARGET_NAME}
	liba.cc
	liba.h
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
