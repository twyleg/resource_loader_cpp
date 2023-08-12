set(script ${CMAKE_CURRENT_LIST_DIR}/../resource_loader/resource_loader.py)

function(add_resources)

	message(STATUS "Adding resource")

	find_package(Python3 REQUIRED COMPONENTS Interpreter)

	if (NOT DEFINED Python3_FOUND)
			message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
	endif()

	set(oneValueArgs TARGET)
	set(multiValueArgs RESOURCE_FILES)
	cmake_parse_arguments(ADD_RESOURCES "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

	if (NOT TARGET resource_loader)
		message(STATUS "Creating resource_loader target")

#		add_custom_target(
#				resource_loader
#				ALL
#		)

#		add_library(resource_loader
#		)

		file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/resource_loader)
	endif()


	foreach(resource_file IN LISTS ADD_RESOURCES_RESOURCE_FILES)

		message(STATUS ${ADD_RESOURCES_RESOURCE_FILES})

		add_custom_target(
				${resource_file}
				${Python3_EXECUTABLE} ${script} -t ${ADD_RESOURCES_TARGET} -o ${CMAKE_BINARY_DIR}/resource_loader ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}
				DEPENDS
				${resource_file}
		)


		execute_process(
			COMMAND ${Python3_EXECUTABLE} ${script} -t ${ADD_RESOURCES_TARGET} -o ${CMAKE_BINARY_DIR}/resource_loader ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}
		)


	endforeach()

	if (NOT TARGET resource_loader)

		add_library(resource_loader
			${CMAKE_BINARY_DIR}/resource_loader/resource_loader.cc
			${CMAKE_BINARY_DIR}/resource_loader/resource_loader.h
			${CMAKE_BINARY_DIR}/resource_loader/resource_${ADD_RESOURCES_TARGET}.cc
		)

	else()

		target_sources(resource_loader PUBLIC ${CMAKE_BINARY_DIR}/resource_loader/resource_${ADD_RESOURCES_TARGET}.cc)

	endif()




endfunction()
