find_package(PythonLibs)
include_directories(${PYTHON_INCLUDE_DIRS})

add_executable(polybench_runner polybench_runner.cpp)
target_link_libraries(polybench_runner pthread)

add_executable(py_runner py_runner.cpp)
target_link_libraries(py_runner ${PYTHON_LIBRARIES})
