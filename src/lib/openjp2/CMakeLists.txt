### Modified for NextGIS Borsch

include_regular_expression("^.*$")

include_directories(
  ${${OPENJPEG_NAMESPACE}_BINARY_DIR}/src/lib/openjp2 # opj_config.h and opj_config_private.h
)
# Defines the source code for the library
set(OPENJPEG_SRCS
  ${CMAKE_CURRENT_SOURCE_DIR}/thread.c
  ${CMAKE_CURRENT_SOURCE_DIR}/thread.h
  ${CMAKE_CURRENT_SOURCE_DIR}/bio.c
  ${CMAKE_CURRENT_SOURCE_DIR}/bio.h
  ${CMAKE_CURRENT_SOURCE_DIR}/cio.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cio.h
  ${CMAKE_CURRENT_SOURCE_DIR}/dwt.c
  ${CMAKE_CURRENT_SOURCE_DIR}/dwt.h
  ${CMAKE_CURRENT_SOURCE_DIR}/event.c
  ${CMAKE_CURRENT_SOURCE_DIR}/event.h
  ${CMAKE_CURRENT_SOURCE_DIR}/image.c
  ${CMAKE_CURRENT_SOURCE_DIR}/image.h
  ${CMAKE_CURRENT_SOURCE_DIR}/invert.c
  ${CMAKE_CURRENT_SOURCE_DIR}/invert.h
  ${CMAKE_CURRENT_SOURCE_DIR}/j2k.c
  ${CMAKE_CURRENT_SOURCE_DIR}/j2k.h
  ${CMAKE_CURRENT_SOURCE_DIR}/jp2.c
  ${CMAKE_CURRENT_SOURCE_DIR}/jp2.h
  ${CMAKE_CURRENT_SOURCE_DIR}/mct.c
  ${CMAKE_CURRENT_SOURCE_DIR}/mct.h
  ${CMAKE_CURRENT_SOURCE_DIR}/mqc.c
  ${CMAKE_CURRENT_SOURCE_DIR}/mqc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/mqc_inl.h
  ${CMAKE_CURRENT_SOURCE_DIR}/openjpeg.c
  ${CMAKE_CURRENT_SOURCE_DIR}/openjpeg.h
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_clock.c
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_clock.h
  ${CMAKE_CURRENT_SOURCE_DIR}/pi.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pi.h
  ${CMAKE_CURRENT_SOURCE_DIR}/t1.c
  ${CMAKE_CURRENT_SOURCE_DIR}/t1.h
  ${CMAKE_CURRENT_SOURCE_DIR}/t2.c
  ${CMAKE_CURRENT_SOURCE_DIR}/t2.h
  ${CMAKE_CURRENT_SOURCE_DIR}/tcd.c
  ${CMAKE_CURRENT_SOURCE_DIR}/tcd.h
  ${CMAKE_CURRENT_SOURCE_DIR}/tgt.c
  ${CMAKE_CURRENT_SOURCE_DIR}/tgt.h
  ${CMAKE_CURRENT_SOURCE_DIR}/function_list.c
  ${CMAKE_CURRENT_SOURCE_DIR}/function_list.h
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_codec.h
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_includes.h
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_intmath.h
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_malloc.c
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_malloc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/opj_stdint.h
  ${CMAKE_CURRENT_SOURCE_DIR}/sparse_array.c
  ${CMAKE_CURRENT_SOURCE_DIR}/sparse_array.h
)
if(BUILD_JPIP)
  add_definitions(-DUSE_JPIP)
  set(OPENJPEG_SRCS
    ${OPENJPEG_SRCS}
    ${CMAKE_CURRENT_SOURCE_DIR}/cidx_manager.c
    ${CMAKE_CURRENT_SOURCE_DIR}/cidx_manager.h
    ${CMAKE_CURRENT_SOURCE_DIR}/phix_manager.c
    ${CMAKE_CURRENT_SOURCE_DIR}/ppix_manager.c
    ${CMAKE_CURRENT_SOURCE_DIR}/thix_manager.c
    ${CMAKE_CURRENT_SOURCE_DIR}/tpix_manager.c
    ${CMAKE_CURRENT_SOURCE_DIR}/indexbox_manager.h
  )
endif()

set(HHEADERS
    openjpeg.h opj_stdint.h ${CMAKE_CURRENT_BINARY_DIR}/opj_config.h
)

option(OPJ_DISABLE_TPSOT_FIX "Disable TPsot==TNsot fix. See https://github.com/uclouvain/openjpeg/issues/254." OFF)
if(OPJ_DISABLE_TPSOT_FIX)
  add_definitions(-DOPJ_DISABLE_TPSOT_FIX)
endif()

# Special case for old i586-mingw32msvc-gcc cross compiler
if(NOT WIN32 AND CMAKE_COMPILER_IS_GNUCC AND CMAKE_C_COMPILER MATCHES ".*mingw32msvc.*" )
  set(WIN32 YES)
endif()

if(BUILD_SHARED_LIBS)
    add_library(${OPENJPEG_LIBRARY_NAME} SHARED ${OPENJPEG_SRCS} ${HHEADERS})
    set_target_properties (${OPENJPEG_LIBRARY_NAME} PROPERTIES
        VERSION ${VERSION}
        SOVERSION ${SOVERSION}
        DEFINE_SYMBOL OPJ_EXPORTS
    )
    if(MSVC)
        set_target_properties(${OPENJPEG_LIBRARY_NAME} PROPERTIES IMPORT_SUFFIX "_i.lib")
    endif()

    if(BUILD_SHARED_LIBS AND BUILD_STATIC_LIBS)
      # Builds both static and dynamic libs
      add_library(${OPENJPEG_LIBRARY_NAME} SHARED ${OPENJPEG_SRCS})
      add_library(openjp2_static STATIC ${OPENJPEG_SRCS})
      set_target_properties(openjp2_static PROPERTIES OUTPUT_NAME ${OPENJPEG_LIBRARY_NAME})
      set(INSTALL_LIBS ${OPENJPEG_LIBRARY_NAME} openjp2_static)
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${OPENJPEG_LIBRARY_NAME} SHARED ${OPENJPEG_SRCS} ${HHEADERS})
    set_property(SOURCE ${HHEADERS}
        PROPERTY MACOSX_PACKAGE_LOCATION "Headers/${OPENJPEG_INSTALL_SUBDIR}"
    )
    set_target_properties(${OPENJPEG_LIBRARY_NAME} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.openjpeg.openjpeg
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      # PUBLIC_HEADER "${HHEADERS}"
      VERSION ${VERSION}
      SOVERSION ${SOVERSION}
      )
else()
    add_definitions(-DOPJ_STATIC)
    add_library(${OPENJPEG_LIBRARY_NAME} STATIC ${CSOURCES} ${HHEADERS} ${HEADERS_PRIV})
endif()

set_target_properties(${OPENJPEG_LIBRARY_NAME} PROPERTIES LINKER_LANGUAGE CXX)

set(INSTALL_LIBS ${OPENJPEG_LIBRARY_NAME})
if(M_LIB)
    set(OPENJPEG_LINK_LIBRARIES ${M_LIB})
endif()

##############################################
# install
##############################################
if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL )
    install(TARGETS ${INSTALL_LIBS}
        EXPORT ${PACKAGE_UPPER_NAME}Targets
        RUNTIME DESTINATION ${INSTALL_BIN_DIR}
        LIBRARY DESTINATION ${INSTALL_LIB_DIR}
        ARCHIVE DESTINATION ${INSTALL_LIB_DIR}
        INCLUDES DESTINATION ${INSTALL_INC_DIR}/${OPENJPEG_INSTALL_SUBDIR}
        FRAMEWORK DESTINATION ${INSTALL_LIB_DIR}
    )
endif()

if(NOT SKIP_INSTALL_HEADERS AND NOT SKIP_INSTALL_ALL )
  install(FILES ${HHEADERS} DESTINATION ${INSTALL_INC_DIR}/${OPENJPEG_INSTALL_SUBDIR})
endif()

# Add path to includes to build-tree export
target_include_directories(${OPENJPEG_LIBRARY_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)

# Add all targets to the build-tree export set
export(TARGETS ${INSTALL_LIBS}
    FILE ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Targets.cmake)

# Create the <Package>Config.cmake file
configure_file(${PROJECT_SOURCE_DIR}/cmake/PackageConfig.cmake.in
    ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake @ONLY)

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
    # Install the <Package>Config.cmake
    install(FILES
      ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake
      DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)

    # Install the export set for use with the install-tree
    install(EXPORT ${PACKAGE_UPPER_NAME}Targets DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)
endif()

if(BUILD_DOC)
# install man page of the library
install(
  FILES       ${OPENJPEG_SOURCE_DIR}/doc/man/man3/libopenjp2.3
  DESTINATION ${INSTALL_MAN_DIR}/man3)
endif()

if(BUILD_LUTS_GENERATOR)
# internal utility to generate t1_luts.h (part of the jp2 lib)
# no need to install:
  add_executable(t1_generate_luts t1_generate_luts.c)
  if(UNIX)
    target_link_libraries(t1_generate_luts m)
  endif()
endif()

# Experimental option; let's how cppcheck performs
# Implementation details:
# I could not figure out how to easily upload a file to CDash. Instead simply
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

if(OPJ_USE_DSYMUTIL)
  if(BUILD_SHARED_LIBS)
    add_custom_command(TARGET ${OPENJPEG_LIBRARY_NAME} POST_BUILD
    COMMAND "dsymutil" "$<TARGET_SONAME_FILE:${OPENJPEG_LIBRARY_NAME}>"
    COMMENT "dsymutil $<TARGET_SONAME_FILE:${OPENJPEG_LIBRARY_NAME}>"
    DEPENDS ${OPENJPEG_LIBRARY_NAME})
  endif()
endif()

#################################################################################
# threading configuration
#################################################################################
set(CMAKE_THREAD_PREFER_PTHREAD TRUE)

option(OPJ_USE_THREAD "Build with thread/mutex support " ON)
if(NOT OPJ_USE_THREAD)
   add_definitions( -DMUTEX_stub)
endif(NOT OPJ_USE_THREAD)

find_package(Threads QUIET)

if(OPJ_USE_THREAD AND WIN32 AND NOT Threads_FOUND )
    add_definitions( -DMUTEX_win32)
    set(Threads_FOUND YES)
endif()

if(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_WIN32_THREADS_INIT )
   add_definitions( -DMUTEX_win32)
endif(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_WIN32_THREADS_INIT )

if(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT )
   add_definitions( -DMUTEX_pthread)
endif(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT )

if(OPJ_USE_THREAD AND NOT Threads_FOUND)
  message(FATAL_ERROR "No thread library found and thread/mutex support is required by OPJ_USE_THREAD option")
endif(OPJ_USE_THREAD AND NOT Threads_FOUND)

if(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)
   set(OPENJPEG_LINK_LIBRARIES ${OPENJPEG_LINK_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT})
endif(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)

if(OPENJPEG_LINK_LIBRARIES)
    target_link_libraries(${OPENJPEG_LIBRARY_NAME} PRIVATE ${OPENJPEG_LINK_LIBRARIES})
endif()

if(BUILD_UNIT_TESTS)
    add_executable(bench_dwt bench_dwt.c)
    if(UNIX)
        target_link_libraries(bench_dwt m ${OPENJPEG_LIBRARY_NAME})
    endif()
    if(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)
        target_link_libraries(bench_dwt ${CMAKE_THREAD_LIBS_INIT})
    endif(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)

    add_executable(test_sparse_array test_sparse_array.c)
    if(UNIX)
        target_link_libraries(test_sparse_array m ${OPENJPEG_LIBRARY_NAME})
    endif()
    if(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)
        target_link_libraries(test_sparse_array ${CMAKE_THREAD_LIBS_INIT})
    endif(OPJ_USE_THREAD AND Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)
endif(BUILD_UNIT_TESTS)
