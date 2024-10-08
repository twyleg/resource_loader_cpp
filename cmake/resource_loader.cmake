# Copyright (C) 2024 twyleg
set(resource_loader_generator_python_script ${CMAKE_CURRENT_LIST_DIR}/../resource_loader_generator/resource_loader_generator.py CACHE PATH "Resource loader python resource_generator_python_script location ")
set(resource_loader_generated_src ${CMAKE_BINARY_DIR}/resource_loader_generated CACHE PATH "Resource loader generated sources location")


function(resource_loader_init)

        message(STATUS "Creating resource_loader target")

        find_package(Python3 REQUIRED COMPONENTS Interpreter)
        if (NOT DEFINED Python3_FOUND)
                message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
        endif()

        set(oneValueArgs TARGET)
        cmake_parse_arguments(ARGS "" "${oneValueArgs}" "" ${ARGN} )

        file(MAKE_DIRECTORY ${resource_loader_generated_src})

        execute_process(
                COMMAND ${Python3_EXECUTABLE} ${resource_loader_generator_python_script} -o ${resource_loader_generated_src}
                WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/
        )

        add_library(${ARGS_TARGET}
                "${resource_loader_generated_src}/resource_loader.cc"
                "${resource_loader_generated_src}/resource_loader.h"
        )

        target_include_directories(${ARGS_TARGET}
                PUBLIC ${resource_loader_generated_src}
        )

endFunction()


function(resource_loader_add_resources)

	message(STATUS "Adding resource(s):")

        find_package(Python3 REQUIRED COMPONENTS Interpreter)
        if (NOT DEFINED Python3_FOUND)
                message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
        endif()

        set(oneValueArgs TARGET PREFIX)
	set(multiValueArgs RESOURCE_FILES)
        cmake_parse_arguments(ARGS "" "${oneValueArgs}" "" ${ARGN} )

        if (NOT TARGET ${ARGS_TARGET})
            message(FATAL_ERROR "Missing requested target \"${ARGS_TARGET}\". Run \"resource_loader_init(TARGET ${ARGS_TARGET}\" before!")
        endif()

        if (DEFINED ARGS_PREFIX)
                set(prefix -p ${ARGS_PREFIX})
        endif()

        foreach(resource_file IN LISTS ARGS_UNPARSED_ARGUMENTS)

                set(resource_loader_generate_command ${Python3_EXECUTABLE} ${resource_loader_generator_python_script} -o ${resource_loader_generated_src} ${prefix} ${resource_file})

                execute_process(
                        COMMAND ${resource_loader_generate_command}
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                        OUTPUT_VARIABLE resource_name_hash
                        OUTPUT_STRIP_TRAILING_WHITESPACE
                        COMMAND_ECHO "NONE"
                )

                set(output_target_name "resource_${resource_name_hash}")
                set(output_filepath ${resource_loader_generated_src}/${output_target_name}.cc)
                get_filename_component(output_filename ${resource_file} NAME)

                if (DEFINED ARGS_PREFIX)
                    set(identifier ${ARGS_PREFIX}/${output_filename})
                else()
                    set(identifier ${output_filename})
                endif()

                message(STATUS "  - File: \"${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}\", Identifier: \"${identifier}\", Hash: \"${resource_name_hash}\"")

                # Command to generate C++ resource file from resource file
		add_custom_command(
			OUTPUT ${output_filepath}
                        COMMAND ${resource_loader_generate_command}
			WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}
                        COMMENT "Generating resource: ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file} -> ${output_filepath}"
		)

                # Target that represents the generated C++ resource file and
                # is depending on the generated C++ resource file.
                # The custom command will provide the dependency.
                add_custom_target(${output_target_name} DEPENDS ${output_filepath})

                # Add the generated C++ resource file to the given targets name
                target_sources(${ARGS_TARGET} PRIVATE ${output_filepath})
                # Add the custom target from two steps earlier as a dependency of the target
                # to regenerate the C++ resource file when the original resource file is cchanged.
                add_dependencies(${ARGS_TARGET} ${output_target_name})

	endforeach()


endfunction()
