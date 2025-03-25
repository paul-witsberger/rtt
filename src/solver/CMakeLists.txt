# Create a library for the solver module
add_library(solver Solver.cpp)

# Include directoriers for the solver module
target_include_directories(solver PUBLIC ${CMAKE_SOURCE_DIR}/include)