CMAKE_MINIMUM_REQUIRED(VERSION 2.4)

PROJECT(humotion-hai16)

INCLUDE(FindPkgConfig)
PKG_SEARCH_MODULE(VDEMO REQUIRED vdemo)

SET(PROGNAME vdemo_scripts)

# these are somehow used in configured files
SET(vdemo_prefix ${VDEMO_PREFIX})
SET(vdemo_demoroot "${CMAKE_INSTALL_PREFIX}/etc/vdemo_scripts")
SET(prefix ${CMAKE_INSTALL_PREFIX})
SET(bindir "${CMAKE_INSTALL_PREFIX}/bin")

FILE(GLOB files "*.sh.in")

# Remove all generated scripts from file list in case of in source builds
FOREACH(item ${files})
    IF(${item} MATCHES "/vdemo_[^/]*$")
        LIST(REMOVE_ITEM files ${item})
    ENDIF()
ENDFOREACH(item)

# configure demo files to inject variables
SET(demofiles)
FOREACH(file ${files})
    STRING(REGEX REPLACE "^(.*)\\.in$" "\\1" demofile ${file})
    LIST(APPEND demofiles ${demofile})
    CONFIGURE_FILE(${file} "${CMAKE_CURRENT_BINARY_DIR}/${demofile}" @ONLY)
    INSTALL(FILES "${CMAKE_CURRENT_BINARY_DIR}/${demofile}" DESTINATION "etc/vdemo_scripts")
ENDFOREACH()

FILE(GLOB demos "demo/*.py")
LIST(REMOVE_ITEM demos "*~")
INSTALL(FILES ${demos}
        DESTINATION "share/hai16-demo"
        PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ OWNER_EXECUTE GROUP_EXECUTE WORLD_EXECUTE)


FILE(GLOB components "component_scripts/component_*")
LIST(REMOVE_ITEM components "*~")
INSTALL(FILES ${components}
        DESTINATION "etc/vdemo_scripts/component_scripts"
        PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ OWNER_EXECUTE GROUP_EXECUTE WORLD_EXECUTE)

INSTALL(FILES "vdemo_aux_functions.sh"
        DESTINATION "etc/vdemo_scripts"
        PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ GROUP_EXECUTE WORLD_EXECUTE)

# configure starter script for each demo configuration
FOREACH(demofile ${demofiles})
    MESSAGE( STATUS "file = ${demofile}" )
    GET_FILENAME_COMPONENT(demoname ${demofile} NAME_WE)
    SET(VDEMO_demofile "${vdemo_demoroot}/${demoname}.sh")
    SET(vdemo_starter "vdemo_${demoname}.sh")
    CONFIGURE_FILE(vdemo_start.in ${vdemo_starter})
    INSTALL(FILES "${PROJECT_BINARY_DIR}/${vdemo_starter}"
        DESTINATION bin
        PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ GROUP_WRITE WORLD_READ OWNER_EXECUTE GROUP_EXECUTE WORLD_EXECUTE
    )
ENDFOREACH()
