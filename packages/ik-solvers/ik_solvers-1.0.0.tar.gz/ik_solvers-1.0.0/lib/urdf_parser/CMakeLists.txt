
set (URDF_MAJOR_VERSION 3)
set (URDF_MINOR_VERSION 0)
set (URDF_PATCH_VERSION 2)
set (URDF_VERSION ${URDF_MAJOR_VERSION}.${URDF_MINOR_VERSION}.${URDF_PATCH_VERSION})
set (URDF_MAJOR_MINOR_VERSION ${URDF_MAJOR_VERSION}.${URDF_MINOR_VERSION})

find_package(TinyXML)
# bionic has not cmake module, workaround
if (NOT TinyXML_FOUND AND UNIX)
  include(FindPkgConfig)
  pkg_check_modules (TinyXML tinyxml)
else()
  # Make it fail in platforms without pkgconfig
  find_package(TinyXML REQUIRED) # bionic has not cmake module
endif()
find_package(console_bridge REQUIRED)

include_directories(
  include
  ${TinyXML_INCLUDE_DIRS}
)
SET(LIB_SOURCE_FILES
    src/pose.cpp
    src/model.cpp
    src/link.cpp
    src/joint.cpp
    src/world.cpp
    src/urdf_model_state.cpp
    src/twist.cpp)



add_library(urdf_parser STATIC
  ${LIB_SOURCE_FILES} 
)
set_target_properties(urdf_parser PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_link_libraries(urdf_parser PUBLIC
  ${TinyXML_LIBRARIES}
  ${console_bridge_LIBRARIES})
target_include_directories(urdf_parser SYSTEM PUBLIC
  ${TinyXML_INCLUDE_DIRS})
target_include_directories(urdf_parser PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/include
)

INSTALL(
  TARGETS
  urdf_parser
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)