cmake_minimum_required(VERSION 3.29)
project(rtt)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zc:__cplusplus")

find_package(Qt6 REQUIRED COMPONENTS Core Gui Test Widgets)

set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

enable_testing(true)

qt_add_executable(${PROJECT_NAME}
    src/main.cpp
)
add_test(NAME ${PROJECT_NAME} COMMAND ${PROJECT_NAME})

set_target_properties(${PROJECT_NAME} PROPERTIES
    WIN32_EXECUTABLE TRUE
)
target_link_libraries(${PROJECT_NAME} PRIVATE Qt::Test)

install(TARGETS ${PROJECT_NAME} DESTINATION ${CMAKE_INSTALL_BINDIR})
