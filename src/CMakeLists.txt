# Add subdirectories for each module
add_subdirectory(display)
add_subdirectory(solver)

# Add the main executable
add_executable(rtt main.cpp)

# Link the modules to the main executable
target_link_libraries(rtt PRIVATE display solver)
