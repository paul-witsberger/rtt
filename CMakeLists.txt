cmake_minimum_required(VERSION 3.29)
project(rtt)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zc:__cplusplus")

add_subdirectory(src)