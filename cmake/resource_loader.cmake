set(script ${CMAKE_CURRENT_LIST_DIR}/../python/resource_loader/resource_loader.py)

function(add_resources)

        message(STATUS "Adding resource")

        find_package(Python3 REQUIRED COMPONENTS Interpreter)

        if (NOT DEFINED Python3_FOUND)
            message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
        endif()

        set(oneValueArgs TARGET)
        set(multiValueArgs RESOURCE_FILES)
#	cmake_parse_arguments(ADD_RESOURCES "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )
        cmake_parse_arguments(ADD_RESOURCES "" "" "${multiValueArgs}" ${ARGN} )


        if (NOT TARGET resource_loader)
            file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/resource_loader)
        endif()


        foreach(resource_file IN LISTS ADD_RESOURCES_RESOURCE_FILES)

                message(STATUS "Resource file: ${resource_file}")

                get_filename_component(OUTPUT_FILENAME ${resource_file} NAME)
                set(OUTPUT_FILEPATH ${CMAKE_BINARY_DIR}/resource_loader/resource_${OUTPUT_FILENAME}.cc)

                set(run_resource_loader COMMAND ${Python3_EXECUTABLE} ${script} -o ${CMAKE_BINARY_DIR}/resource_loader ${resource_file})

                message(STATUS ${run_resource_loader})

                execute_process(
                        ${run_resource_loader}
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
                )

                add_custom_command(
                        OUTPUT ${OUTPUT_FILEPATH}
                        ${run_resource_loader}
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
                        MAIN_DEPENDENCY ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}
                        COMMENT "Generating resource: ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}"
                )



                if (NOT TARGET resource_loader)

                        message(STATUS "Creating resource_loader target")

                        add_library(resource_loader
                                ${CMAKE_BINARY_DIR}/resource_loader/resource_loader.cc
                                ${CMAKE_BINARY_DIR}/resource_loader/resource_loader.h
                        )

                        target_include_directories(resource_loader
                                PUBLIC ${CMAKE_BINARY_DIR}/resource_loader/
                        )
                endif()

                target_sources(resource_loader PRIVATE ${OUTPUT_FILEPATH})

        endforeach()


endfunction()




#set(script ${CMAKE_CURRENT_LIST_DIR}/../resource_loader/resource_loader.py)

#function(init_resource_loader)

#	find_package(Python3 REQUIRED COMPONENTS Interpreter)

#	if (NOT DEFINED Python3_FOUND)
#			message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
#	endif()

#	if (NOT TARGET resource_loader)
#		message(STATUS "Creating resource_loader target")
#		file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/resource_loader)
#	endif()

#	execute_process(
#		COMMAND ${Python3_EXECUTABLE} ${script} -o ${CMAKE_BINARY_DIR}/resource_loader
#		WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
#	)

#	add_library(resource_loader
#		${CMAKE_BINARY_DIR}/resource_loader/resource_loader.cc
#		${CMAKE_BINARY_DIR}/resource_loader/resource_loader.h
#	)

##	add_custom_target(resource_loader
##		DEPENDS
##		${CMAKE_BINARY_DIR}/resource_loader/resource_loader.cc
##		${CMAKE_BINARY_DIR}/resource_loader/resource_loader.h
##	)

#	target_include_directories(resource_loader
#		PUBLIC ${CMAKE_BINARY_DIR}/resource_loader/
#	)

#endfunction()

#function(add_resources)

#	message(STATUS "Adding resource")

#	find_package(Python3 REQUIRED COMPONENTS Interpreter)

#	if (NOT DEFINED Python3_FOUND)
#			message(FATAL_ERROR "Python3 not found. Please check your installation and PATH variable.")
#	endif()

#	set(oneValueArgs TARGET)
#	set(multiValueArgs RESOURCE_FILES)
##	cmake_parse_arguments(ADD_RESOURCES "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )
#	cmake_parse_arguments(ADD_RESOURCES "" "" "${multiValueArgs}" ${ARGN} )

#	if (NOT TARGET resource_loader)

#		set(resource_files "" CACHE INTERNAL "resource_files")

#		message(STATUS "Creating resource_loader target")
#		file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/resource_loader)

#		add_library(resource_loader
#			${CMAKE_BINARY_DIR}/resource_loader/resource_loader.cc
#			${CMAKE_BINARY_DIR}/resource_loader/resource_loader.h
#		)

#		target_include_directories(resource_loader
#			PUBLIC ${CMAKE_BINARY_DIR}/resource_loader/
#		)
#	endif()


#	foreach(resource_file IN LISTS ADD_RESOURCES_RESOURCE_FILES)

#		message(STATUS "Resource file: ${resource_file}")


#		list(APPEND resource_files ${resource_file})
#		message(STATUS "Resource file: ${resource_files}")

#		get_filename_component(OUTPUT_FILENAME ${resource_file} NAME)
#		set(OUTPUT_FILEPATH ${CMAKE_BINARY_DIR}/resource_loader/resource_${OUTPUT_FILENAME}.cc)

#		add_custom_command(
#			OUTPUT ${OUTPUT_FILEPATH}
#			COMMAND ${Python3_EXECUTABLE} ${script} -o ${CMAKE_BINARY_DIR}/resource_loader ${resource_file}
#			WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
#			MAIN_DEPENDENCY ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}
#			COMMENT "Generating resource: ${CMAKE_CURRENT_SOURCE_DIR}/${resource_file}"
#		)

#		execute_process(
#			COMMAND ${Python3_EXECUTABLE} ${script} -o ${CMAKE_BINARY_DIR}/resource_loader ${resource_file}
#			WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
#		)

##		add_dependencies(resource_loader ${OUTPUT_FILEPATH})
#		target_sources(resource_loader PRIVATE ${OUTPUT_FILEPATH})


#	endforeach()


#endfunction()
