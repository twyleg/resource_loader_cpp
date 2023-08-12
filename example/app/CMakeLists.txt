set(TARGET_NAME app)


#
# set cmake settings
#
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

add_resources(TARGET app RESOURCE_FILES example_resource_one.txt example_resource_two.txt)


#
# add source files to target
#
add_executable(${TARGET_NAME}
	main.cc
)


#
# link against libs
#
target_link_libraries(${TARGET_NAME}
	resource_loader
	liba
	libb
)
