# Main CMakeLists.txt to build the OpenJPEG project using CMake (www.cmake.org)
# Written by Mathieu Malaterre

# Modified for NextGIS Borsch project (marked with ###)
#  Copyright (c) 2017 NextGIS, <info@nextgis.com>

# This CMake project will by default create a library called openjpeg
# But if you want to use this project within your own (CMake) project
# you will eventually like to prefix the library to avoid linking confusion
# For this purpose you can define a CMake var: OPENJPEG_NAMESPACE to whatever you like
# e.g.:
# set(OPENJPEG_NAMESPACE "GDCMOPENJPEG")

cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)

### for Borsch
project(openjpeg)
# Some init settings
set(CMAKE_COLOR_MAKEFILE ON)
# Set path to additional CMake modules
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

if(OSX_FRAMEWORK AND (BUILD_SHARED_LIBS OR BUILD_STATIC_LIBS))
  message(FATAL_ERROR "Only OSX_FRAMEWORK key or any or both BUILD_SHARED_LIBS
                       and BUILD_STATIC_LIBS keys are permitted")
endif()

if(OSX_FRAMEWORK)
  set(INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}/bin" CACHE INTERNAL "Installation directory for executables" FORCE)
  set(INSTALL_LIB_DIR "${CMAKE_INSTALL_PREFIX}/Library/Frameworks" CACHE INTERNAL "Installation directory for libraries" FORCE)
  set(SKIP_INSTALL_EXECUTABLES OFF)
  set(SKIP_INSTALL_EXPORT ON)
  set(SKIP_INSTALL_FILES OFF)
  set(SKIP_INSTALL_DOCS OFF)
  set(CMAKE_MACOSX_RPATH ON)
else()
    include(GNUInstallDirs)
    set(INSTALL_BIN_DIR ${CMAKE_INSTALL_BINDIR} CACHE INTERNAL "Installation directory for executables" FORCE)
    set(INSTALL_LIB_DIR ${CMAKE_INSTALL_LIBDIR} CACHE INTERNAL "Installation directory for libraries" FORCE)
    set(INSTALL_DOC_DIR ${CMAKE_INSTALL_DOCDIR} CACHE INTERNAL "Installation directory for doc pages" FORCE)
endif()

include(util)
check_version(OPENJPEG_VERSION_MAJOR OPENJPEG_VERSION_MINOR OPENJPEG_VERSION_BUILD)
set(VERSION ${OPENJPEG_VERSION_MAJOR}.${OPENJPEG_VERSION_MINOR}.${OPENJPEG_VERSION_BUILD})
set(OPENJPEG_INSTALL_SUBDIR "openjpeg-${OPENJPEG_VERSION_MAJOR}.${OPENJPEG_VERSION_MINOR}")

if(OSX_FRAMEWORK)
    set(FRAMEWORK_VERSION "${OPENJPEG_VERSION_MAJOR}")
    set(INSTALL_INC_DIR "${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Versions/${FRAMEWORK_VERSION}/Headers/${OPENJPEG_INSTALL_SUBDIR}" CACHE INTERNAL "Installation directory for headers" FORCE)
    set(INSTALL_DOC_DIR "${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Versions/${FRAMEWORK_VERSION}/Resources/docs")
    set(INSTALL_INC_DIR_PACKAGE "${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Versions/${FRAMEWORK_VERSION}/Headers" CACHE INTERNAL "Installation directory for headers in package" FORCE)
else()
    set(INSTALL_INC_DIR ${CMAKE_INSTALL_INCLUDEDIR}/${OPENJPEG_INSTALL_SUBDIR} CACHE INTERNAL "Installation directory for headers" FORCE)
    set(INSTALL_SHARE_DIR ${CMAKE_INSTALL_DATADIR}/${OPENJPEG_INSTALL_SUBDIR} CACHE INTERNAL "Installation directory for share data" FORCE)
    set(INSTALL_INC_DIR_PACKAGE ${CMAKE_INSTALL_FULL_INCLUDEDIR} CACHE INTERNAL "Installation directory for headers in package" FORCE)
endif()

report_version(${PROJECT_NAME} ${VERSION})

### Question: where these variables should be set (there are a lot of ${OPENJPEG_NAMESPACE}... variables in  the code)?
set(OPENJPEG_SOURCE_DIR ${CMAKE_SOURCE_DIR})
set(OPENJPEG_BINARY_DIR ${CMAKE_BINARY_DIR})

if(COMMAND CMAKE_POLICY)
  cmake_policy(SET CMP0003 NEW)
endif()

if(NOT OPENJPEG_NAMESPACE)
  set(OPENJPEG_NAMESPACE "OPENJPEG")
  set(OPENJPEG_STANDALONE 1)
endif()
# In all cases:
#string(TOLOWER ${OPENJPEG_NAMESPACE} OPENJPEG_LIBRARY_NAME)
###set(OPENJPEG_LIBRARY_NAME openjp2)
set(OPENJPEG_LIBRARY_NAME ${PROJECT_NAME})

###project(${OPENJPEG_NAMESPACE} C)

# Do full dependency headers.
include_regular_expression("^.*$")

#-----------------------------------------------------------------------------
# OPENJPEG version number, useful for packaging and doxygen doc:
set(OPENJPEG_VERSION
  "${OPENJPEG_VERSION_MAJOR}.${OPENJPEG_VERSION_MINOR}.${OPENJPEG_VERSION_BUILD}")
set(PACKAGE_VERSION
  "${OPENJPEG_VERSION_MAJOR}.${OPENJPEG_VERSION_MINOR}.${OPENJPEG_VERSION_BUILD}")

# Because autotools does not support X.Y notation for SOVERSION, we have to use
# two numbering, one for the openjpeg version and one for openjpeg soversion
# version | soversion
#   1.0   |  0
#   1.1   |  1
#   1.2   |  2
#   1.3   |  3
#   1.4   |  4
#   1.5   |  5
#   1.5.1 |  5
#   2.0   |  6
#   2.0.1 |  6
#   2.1   |  7
#   2.1.1 |  7
#   2.1.2 |  7
# above is the recommendation by the OPJ team. If you really need to override this default,
# you can specify your own OPENJPEG_SOVERSION at cmake configuration time:
# cmake -DOPENJPEG_SOVERSION:STRING=42 /path/to/openjpeg
if(NOT OPENJPEG_SOVERSION)
  set(OPENJPEG_SOVERSION 7)
endif(NOT OPENJPEG_SOVERSION)

set(SOVERSION ${OPENJPEG_SOVERSION})

# --------------------------------------------------------------------------
# On Visual Studio 8 MS deprecated C. This removes all 1.276E1265 security
# warnings
if(WIN32)
    if(NOT ITK_ENABLE_VISUAL_STUDIO_DEPRECATED_C_WARNINGS)
      add_definitions(
        -D_CRT_FAR_MAPPINGS_NO_DEPRECATE
        -D_CRT_IS_WCTYPE_NO_DEPRECATE
        -D_CRT_MANAGED_FP_NO_DEPRECATE
        -D_CRT_NONSTDC_NO_DEPRECATE
        -D_CRT_SECURE_NO_DEPRECATE
        -D_CRT_SECURE_NO_DEPRECATE_GLOBALS
        -D_CRT_SETERRORMODE_BEEP_SLEEP_NO_DEPRECATE
        -D_CRT_TIME_FUNCTIONS_NO_DEPRECATE
        -D_CRT_VCCLRIT_NO_DEPRECATE
        -D_SCL_SECURE_NO_DEPRECATE
        )
    endif()
endif()

include (configure)

#-----------------------------------------------------------------------------
# Build Library
add_subdirectory(src)

#-----------------------------------------------------------------------------
# Build Applications
###option(BUILD_CODEC "Build the CODEC executables" ON)
###option(BUILD_MJ2 "Build the MJ2 executables." OFF)
###option(BUILD_JPWL "Build the JPWL library and executables" OFF)
###option(BUILD_JPIP "Build the JPIP library and executables." OFF)
###if(BUILD_JPIP)
###  option(BUILD_JPIP_SERVER "Build the JPIP server." OFF)
###endif()
###option(BUILD_VIEWER "Build the OPJViewer executable (C++)" OFF)
###option(BUILD_JAVA "Build the openjpeg jar (Java)" OFF)
###option(BUILD_JP3D "Build the JP3D comp" OFF)
###mark_as_advanced(BUILD_VIEWER)
###mark_as_advanced(BUILD_JAVA)
###mark_as_advanced(BUILD_JP3D)

###if(BUILD_CODEC OR BUILD_MJ2)
  # OFF: It will only build 3rd party libs if they are not found on the system
  # ON: 3rd party libs will ALWAYS be build, and used
###  option(BUILD_THIRDPARTY "Build the thirdparty executables if it is needed" OFF)
###  add_subdirectory(thirdparty)
###  add_subdirectory(src/bin)
###endif ()
###add_subdirectory(wrapping)

#-----------------------------------------------------------------------------
# Build DOCUMENTATION (not in ALL target and only if Doxygen is found)

### Removed for Borsch

#-----------------------------------------------------------------------------
# Buld Testing

### Removed for Borsch

#-----------------------------------------------------------------------------
# install all targets referenced as OPENJPEGTargets
###install(EXPORT OpenJPEGTargets DESTINATION ${OPENJPEG_INSTALL_PACKAGE_DIR})
###configure_file( ${OPENJPEG_SOURCE_DIR}/cmake/OpenJPEGConfig.cmake.in
###  ${OPENJPEG_BINARY_DIR}/OpenJPEGConfig.cmake
###  @ONLY
###)
###install( FILES ${OPENJPEG_BINARY_DIR}/OpenJPEGConfig.cmake
###  DESTINATION ${OPENJPEG_INSTALL_PACKAGE_DIR}
###)

#-----------------------------------------------------------------------------
# install CHANGES and LICENSE
if(NOT SKIP_INSTALL_DOCS AND NOT SKIP_INSTALL_ALL)
    if(EXISTS ${OPENJPEG_SOURCE_DIR}/CHANGES)
      install(FILES CHANGES DESTINATION ${INSTALL_DOC_DIR})
    endif()
    install(FILES LICENSE DESTINATION ${INSTALL_DOC_DIR})
endif()

###include (cmake/OpenJPEGCPack.cmake)

#-----------------------------------------------------------------------------

### Borsch export.
if (REGISTER_PACKAGE)
    # Replace the path so not to modify a "template" PackageConfig.cmake.in file.
    set(INSTALL_INC_DIR ${CMAKE_INSTALL_FULL_INCLUDEDIR})

    export(TARGETS ${PROJECT_NAME} FILE ${PROJECT_NAME}-exports.cmake)

    set(EXPORT_PACKAGE_NAME OpenJPEG)
    string(TOUPPER ${EXPORT_PACKAGE_NAME} EXPORT_PACKAGE_NAME_UPPER)
    set(EXPORT_PACKAGE_LIB_NAME ${PROJECT_NAME})
    math(EXPR VERSION_NUM "${OPENJPEG_VERSION_MAJOR} * 10000 + ${OPENJPEG_VERSION_MINOR} * 100 + ${OPENJPEG_VERSION_BUILD}")

    export(PACKAGE ${EXPORT_PACKAGE_NAME})

    include(CMakePackageConfigHelpers)
    configure_package_config_file(
        ${CMAKE_SOURCE_DIR}/cmake/PackageConfig.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/${EXPORT_PACKAGE_NAME}Config.cmake
        INSTALL_DESTINATION ${CMAKE_CURRENT_BINARY_DIR} )
    write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/${EXPORT_PACKAGE_NAME}ConfigVersion.cmake
        VERSION ${VERSION}
        COMPATIBILITY AnyNewerVersion )
else()
    export(TARGETS ${PROJECT_NAME} FILE ${PROJECT_NAME}-exports.cmake EXPORT_LINK_INTERFACE_LIBRARIES)
endif()

# uninstall
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)
