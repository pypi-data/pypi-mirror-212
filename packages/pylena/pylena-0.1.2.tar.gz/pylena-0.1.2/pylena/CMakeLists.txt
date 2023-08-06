pybind11_add_module(pylena_cxx module.cpp)
target_link_libraries(pylena_cxx PRIVATE pylene-numpy pylene::scribo)
target_link_libraries(pylena_cxx PRIVATE -static-libstdc++)

add_subdirectory(morpho)
add_subdirectory(scribo)