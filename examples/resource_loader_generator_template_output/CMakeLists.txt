# Copyright (C) 2023 twyleg
set(TARGET_NAME resource_loader_generator_template_output)

project(${TARGET_NAME})

#
# find packages
#
find_package(fmt REQUIRED)


#
# add source files to target
#
add_executable(${TARGET_NAME}
    main.cc
    resource_loader.cc
    resource_loader.h
    resource_8c0c4a5e43.cc
    resource_10d7e13243.cc
    resource_89f94aa0c0.cc
    resource_fd341f148f.cc
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
)
