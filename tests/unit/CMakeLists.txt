# UNIT TESTS

include_directories(
  ${OPENJPEG_BINARY_DIR}/src/lib/openjp2 # opj_config.h
  ${OPENJPEG_SOURCE_DIR}/src/lib/openjp2
)

set(unit_test
  testempty0
  testempty1
  testempty2
)
foreach(ut ${unit_test})
  add_executable(${ut} ${ut}.c)
  target_link_libraries(${ut} ${OPENJPEG_LIBRARY_NAME})
  add_test(NAME ${ut} COMMAND ${ut})
endforeach()

if(WIN32)
    add_custom_command(TARGET testempty2
                        POST_BUILD
                        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${OPENJPEG_LIBRARY_NAME}> $<TARGET_FILE_DIR:testempty2>
                        COMMENT "Copy ${OPENJPEG_LIBRARY_NAME} to tests"
                    )
endif()
