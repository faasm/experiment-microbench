# CMake setup
cmake_minimum_required (VERSION 3.11)

SET(CMAKE_EXE_LINKER_FLAGS "${FAASM_EXE_LINKER_FLAGS} \
    -Xlinker --export=_faasm_zygote \
    -Xlinker --export=__heap_base \
    -Xlinker --export=__data_end \
    -Xlinker --export=__wasm_call_ctors \
    -Xlinker --max-memory=4294901760 \
    -Wl,-z,stack-size=4194304 -Wl, \
")

SET(CMAKE_EXECUTABLE_SUFFIX ".wasm")

include_directories(${CMAKE_CURRENT_LIST_DIR}/utilities)

# NOTE - at the time of writing this switch greatly improved performance.
# BUT - we can't compile everything with it as it'll break other stuff that
# tries to use the unimplemented functionality
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -munimplemented-simd128")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -munimplemented-simd128")

# Define the polybench data type here
# We want to use 32-bit floats to work well with wasm
add_definitions(-DDATA_TYPE_IS_FLOAT=1)

set(FAASM_FUNC_LIBS faasm c-printscan-long-double)

function(polybench_func exec_name dir_path)
    add_executable(poly_${exec_name}
            ${dir_path}/${exec_name}/${exec_name}.c
            ${dir_path}/${exec_name}/${exec_name}.h
            utilities/polybench.c
            utilities/polybench.h
            )

        target_link_libraries(poly_${exec_name} ${FAASM_FUNC_LIBS})

    # Add this func to the list of all functions
    set(ALL_POLY_FUNCS ${ALL_POLY_FUNCS} poly_${exec_name} PARENT_SCOPE)

endfunction(polybench_func)

polybench_func(covariance datamining)
polybench_func(correlation datamining)

polybench_func(2mm linear-algebra/kernels)
polybench_func(3mm linear-algebra/kernels)
polybench_func(atax linear-algebra/kernels)
polybench_func(bicg linear-algebra/kernels)
polybench_func(doitgen linear-algebra/kernels)
polybench_func(mvt linear-algebra/kernels)

polybench_func(cholesky linear-algebra/solvers)
polybench_func(durbin linear-algebra/solvers)
polybench_func(gramschmidt linear-algebra/solvers)
polybench_func(lu linear-algebra/solvers)
polybench_func(ludcmp linear-algebra/solvers)
polybench_func(trisolv linear-algebra/solvers)

polybench_func(deriche medley)
polybench_func(floyd-warshall medley)
polybench_func(nussinov medley)

polybench_func(adi stencils)
polybench_func(fdtd-2d stencils)
polybench_func(heat-3d stencils)
polybench_func(jacobi-1d stencils)
polybench_func(jacobi-2d stencils)
polybench_func(seidel-2d stencils)

# Custom target to group all the poly functions
add_custom_target(polybench_all DEPENDS ${ALL_POLY_FUNCS})

