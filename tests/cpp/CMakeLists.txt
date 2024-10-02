# Copyright (C) 2024 twyleg
cmake_minimum_required(VERSION 3.16.3)

set(TARGET_NAME unit_tests)

project(cpp_unit_tests)

add_subdirectory(../../external/googletest googletest/)
add_subdirectory(../../ resource_loader/)
resource_loader_init(TARGET resources)

#
# add resources to be embedded in binary
#
resource_loader_add_resources(
    TARGET resources
    resources/example_resource_one.txt
    resources/example_resource_two.txt
)

resource_loader_add_resources(
    TARGET resources
    PREFIX prefix_a
    resources/example_resource_one.txt
)

resource_loader_add_resources(
    TARGET resources
    PREFIX prefix_b
    resources/example_resource_two.txt
)


#
# add source files to target
#
add_executable(${TARGET_NAME}
    main.cc
    resource_loader_test.cc
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
	resources
	GTest::gmock
	GTest::gtest
	GTest::gmock_main
	GTest::gtest_main
)