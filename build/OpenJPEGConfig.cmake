set(OPENJPEG_VERSION 2.1.2)

if(NOT TARGET openjpeg)
    file (READ "${CMAKE_CURRENT_LIST_DIR}/openjpeg-exports.cmake" _file_content)
    string (REPLACE "IMPORTED)" "IMPORTED GLOBAL)" _file_content "${_file_content}")
    file(WRITE "${CMAKE_CURRENT_LIST_DIR}/openjpeg-exports.cmake" "${_file_content}")

    include("${CMAKE_CURRENT_LIST_DIR}/openjpeg-exports.cmake")
    set_target_properties(openjpeg PROPERTIES INTERFACE_LINK_LIBRARIES "")
endif()


set(OPENJPEG_INCLUDE_DIR "/Users/Bishop/work/projects/borsch/lib_openjpeg/inst/Library/Frameworks/openjpeg.framework/Versions/2/Headers")
set(OPENJPEG_LIBRARY openjpeg)
set(OPENJPEG_LIBRARIES ${OPENJPEG_LIBRARY})
set(OPENJPEG_INCLUDE_DIRS ${OPENJPEG_INCLUDE_DIR})
set(OPENJPEG_VERSION_NUM "20102" CACHE INTERNAL "OpenJPEG version number")

set(OPENJPEG_FOUND TRUE)
