# Copyright (C) 2023 twyleg
set(TARGET_NAME app)


#
# add resources to be embedded in binary
#
add_resources(RESOURCE_FILES example_resource_one.txt example_resource_two.txt)


#
# add source files to target
#
add_executable(${TARGET_NAME}
	main.cc
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
	resource_loader
	liba
	libb
)
