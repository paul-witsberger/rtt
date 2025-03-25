# Create a library for the dispay module
add_library(display Display.cpp)

# Include directories for the display module
target_include_directories(display PUBLIC ${CMAKE_SOURCE_DIR}/include)