cmake_minimum_required(VERSION 2.8.3)
project(ik_solvers)

## Compile as C++11
add_compile_options(-std=c++11)

set(ADDITIONAL_COMPILE_OPTIONS -Wall -Wextra -Wpedantic -Wno-unused-parameter)

add_compile_options(${ADDITIONAL_COMPILE_OPTIONS})

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

# Get pybind11 with FetchContent
include(FetchContent)

FetchContent_Declare(
    pybind11-src
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.10.1
)
FetchContent_Declare(
  orocos_kinematics_dynamics
    GIT_REPOSITORY https://github.com/jongyaoY/orocos_kinematics_dynamics.git
    GIT_TAG        363bb879f723e34826787b266c97b06bfda6630a
)
if(${CMAKE_VERSION} VERSION_LESS 3.14)
  macro(FetchContent_MakeAvailable NAME)
    FetchContent_GetProperties(${NAME})
    if(NOT ${NAME}_POPULATED)
      FetchContent_Populate(${NAME})
      add_subdirectory(${${NAME}_SOURCE_DIR} ${${NAME}_BINARY_DIR})
    endif()
  endmacro()
endif()
FetchContent_MakeAvailable(pybind11-src orocos_kinematics_dynamics)
###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${EIGEN3_INCLUDE_DIR}
  # ${orocos_kdl_INCLUDE_DIRS}
)
set(LIB_SOURCE_FILES
  src/IKSolver.cpp
  src/ForwardDynamicsSolver.cpp
)
set(LIB_HEADER_FILES
  include/Utility.h
  include/IKSolver.h
  include/ForwardDynamicsSolver.h
  include/kdl_parser.hpp
)
add_subdirectory(lib/urdf_parser)
pybind11_add_module(PyIKSolver
  ${LIB_SOURCE_FILES} 
  ${LIB_HEADER_FILES}
  src/pybindings.cpp
)
target_include_directories(PyIKSolver PRIVATE 
${PYBIND11_INCLUDE_DIR} 
# ${orocos_kdl_INCLUDE_DIRS}
)

message(orocos_kdl_LIBRARIES="${orocos_kdl_LIBRARIES}")

target_link_libraries(PyIKSolver PRIVATE
  ${orocos_kdl_LIBRARIES}
  urdf_parser
  orocos-kdl
)
# install(
#   TARGETS
#     PyIKSolver
#   LIBRARY
#     DESTINATION PyIKSolver
# )


