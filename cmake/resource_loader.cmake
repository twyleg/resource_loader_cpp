# Copyright (C) 2023 twyleg
set(script ${CMAKE_CURRENT_LIST_DIR}/../python/resource_loader/resource_loader.py CACHE PATH "Resource loader python script location ")
set(resource_loader_src ${CMAKE_BINARY_DIR}/resource_loader_src CACHE PATH "Resource loader generated sources location")

function(init_resource_loader)

    message(STATUS "Creating resource_loader target")

    find_package(Python3 REQUIRED COMPONENTS Interpreter)

    if (NOT DEFINED Python3_FOUND)
            message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
    endif()

    file(MAKE_DIRECTORY ${resource_loader_src})

    add_library(resource_loader
    )

    target_include_directories(resource_loader
                    PUBLIC ${resource_loader_src}
    )



endFunction()

function(add_resources)

		message(STATUS "Adding resource")

                find_package(Python3 REQUIRED COMPONENTS Interpreter)

		set(oneValueArgs TARGET)
		set(multiValueArgs RESOURCE_FILES)
		#	cmake_parse_arguments(ADD_RESOURCES "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )
		cmake_parse_arguments(ADD_RESOURCES "" "" "${multiValueArgs}" ${ARGN} )

                set(run_resource_loader ${Python3_EXECUTABLE} ${script} -o ${resource_loader_src} ${resource_file})


		foreach(resource_file IN LISTS ADD_RESOURCES_RESOURCE_FILES)

				message(STATUS "Resource file: ${resource_file}")

				get_filename_component(OUTPUT_FILENAME ${resource_file} NAME)
                                set(output_filepath ${resource_loader_src}/resource_${OUTPUT_FILENAME}.cc)

				execute_process(
                                                COMMAND ${Python3_EXECUTABLE} ${script} -o ${resource_loader_src} ${resource_file}
						WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
				)

				add_custom_command(
						OUTPUT ${output_filepath}
                                                COMMAND ${Python3_EXECUTABLE} ${script} -o ${resource_loader_src} ${resource_file}
						WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
                                                DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}
						COMMENT "Generating resource: ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}"
				)

				target_sources(resource_loader PRIVATE ${output_filepath})
                                target_sources(resource_loader PRIVATE ${resource_loader_src}/resource_loader.cc)
                                target_sources(resource_loader PRIVATE ${resource_loader_src}/resource_loader.h)

		endforeach()


endfunction()
