find_package(Boost REQUIRED COMPONENTS unit_test_framework)

# Add test executable
add_executable(test_display test_display.cpp)

# Link Boost.Teest and the display library
target_link_libraries(test_display PRIVATE Boost::unit_test_framework display)

