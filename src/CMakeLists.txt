find_package(PythonLibs)
include_directories(${PYTHON_INCLUDE_DIRS})

add_executable(py_runner py_runner.cpp)
target_link_libraries(python_runner ${PYTHON_LIBRARIES})
