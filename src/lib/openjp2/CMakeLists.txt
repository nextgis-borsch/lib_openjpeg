### Modified for NextGIS Borsch

include_regular_expression("^.*$")

configure_file(opj_config.h.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/opj_config.h @ONLY)
configure_file(opj_config_private.h.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/opj_config_private.h @ONLY)

include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Defines the source code for the library
set(CSOURCES
    bio.c
    cio.c
    dwt.c
    event.c
    image.c
    invert.c
    j2k.c
    jp2.c
    mct.c
    mqc.c
    openjpeg.c
    opj_clock.c
    pi.c
    raw.c
    t1.c
    t2.c
    tcd.c
    tgt.c
    function_list.c
    opj_malloc.c
)

set(HEADERS_PRIV
    bio.h
    cio.h
    dwt.h
    event.h
    image.h
    invert.h
    j2k.h
    jp2.h
    mct.h
    mqc.h
    opj_clock.h
    pi.h
    raw.h
    t1.h
    t2.h
    tcd.h
    tgt.h
    function_list.h
    opj_codec.h
    opj_includes.h
    opj_intmath.h
    opj_malloc.h
)

set(HHEADERS
    openjpeg.h opj_stdint.h ${CMAKE_CURRENT_BINARY_DIR}/opj_config.h
)

###if(BUILD_JPIP)
###  add_definitions(-DUSE_JPIP)
###  set(OPENJPEG_SRCS
###    ${OPENJPEG_SRCS}
###    ${CMAKE_CURRENT_SOURCE_DIR}/cidx_manager.c
###    ${CMAKE_CURRENT_SOURCE_DIR}/phix_manager.c
###    ${CMAKE_CURRENT_SOURCE_DIR}/ppix_manager.c
###    ${CMAKE_CURRENT_SOURCE_DIR}/thix_manager.c
###    ${CMAKE_CURRENT_SOURCE_DIR}/tpix_manager.c
###  )
###endif()

if(BUILD_SHARED_LIBS)
    add_library(${OPENJPEG_LIBRARY_NAME} SHARED ${CSOURCES} ${HHEADERS} ${HEADERS_PRIV})
    set_target_properties (${OPENJPEG_LIBRARY_NAME} PROPERTIES
        VERSION ${VERSION}
        SOVERSION ${SOVERSION}
        DEFINE_SYMBOL OPJ_EXPORTS
    )
    if(MSVC)
        set_target_properties(${OPENJPEG_LIBRARY_NAME} PROPERTIES IMPORT_SUFFIX "_i.lib")
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${OPENJPEG_LIBRARY_NAME} SHARED ${CSOURCES} ${HHEADERS} ${HEADERS_PRIV})
    set_target_properties(${OPENJPEG_LIBRARY_NAME} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.openjpeg.openjpeg
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      PUBLIC_HEADER "${HHEADERS}"
      VERSION ${VERSION}
      SOVERSION ${SOVERSION}
      )
else()
    add_library(${OPENJPEG_LIBRARY_NAME} STATIC ${CSOURCES} ${HHEADERS} ${HEADERS_PRIV})
endif()

if(M_LIB)
    target_link_libraries(${OPENJPEG_LIBRARY_NAME} ${M_LIB})
endif()

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
    install(TARGETS ${OPENJPEG_LIBRARY_NAME}
        RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT libraries
        ARCHIVE DESTINATION ${INSTALL_LIB_DIR} COMPONENT libraries
        LIBRARY DESTINATION ${INSTALL_LIB_DIR} COMPONENT libraries
        FRAMEWORK DESTINATION ${INSTALL_LIB_DIR}
    )
endif()

if(NOT SKIP_INSTALL_FILES AND NOT SKIP_INSTALL_ALL)
    install(FILES openjpeg.h opj_stdint.h ${CMAKE_CURRENT_BINARY_DIR}/opj_config.h DESTINATION ${INSTALL_INC_DIR} COMPONENT headers)
endif()

# install man page of the library
###install(
###  FILES       ${OPENJPEG_SOURCE_DIR}/doc/man/man3/libopenjp2.3
###  DESTINATION ${OPENJPEG_INSTALL_MAN_DIR}/man3)

# internal utilities to generate t1_luts.h (part of the jp2 lib)
# no need to install:
###add_executable(t1_generate_luts t1_generate_luts.c)
###if(UNIX)
###  target_link_libraries(t1_generate_luts m)
###endif()

# Experimental option; let's how cppcheck performs
# Implementation details:
# I could not figure out how to easily upload a file to CDash. Instead simply
# pretend cppcheck is part of the Build step. Technically cppcheck can even
# output gcc formatted error/warning report
# Another implementation detail: I could not redirect error to the error
# catching mechanism something is busted in cmake 2.8.5, I had to use the
# warning regex to catch them.
if(OPENJPEG_CPPCHECK)
  find_package(CPPCHECK REQUIRED)
  foreach(f ${OPENJPEG_SRCS})
    # cppcheck complains about too many configuration, pretend to be WIN32:
    add_custom_command(TARGET ${OPENJPEG_LIBRARY_NAME}
      COMMAND ${CPPCHECK_EXECUTABLE} -DWIN32 ${f})
  endforeach()
endif()
