# Copyright (C) 2023 twyleg
set(TARGET_NAME app)


#
# add resources to be embedded in binary
#
resource_loader_add_resources(
    TARGET resources
    resources/txt/example_resource_one.txt
    resources/txt/example_resource_two.txt
    resources/img/STS-129_Atlantis_Ready_to_Fly.jpg
)


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
    resources
    liba
    libb
)
