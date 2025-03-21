# Set up
cmake_minimum_required(VERSION 3.29)
project(pyrtt)

# Specify relevant paths
set(PYTHON_VERSION 312)
set(BOOST_ROOT "C:/Users/paul/Documents/codes/boost_1_86_0")
set(PYTHON_ROOT "C:/Python312")
set(BIN_ROOT "C:/Users/paul/Documents/codes/rtt/bin")
set(LOCAL_PYTHON_ENV "C:/Users/paul/Documents/codes/rtt/venv_py_rtt/Lib/site-packages/${PROJECT_NAME}")
set(SOURCE_DIR "C:/Users/paul/Documents/codes/rtt/src")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zc:__cplusplus")

# Define Include and Link directories
set(BOOST_INCLUDE_DIR "${BOOST_ROOT}")
file(GLOB BOOST_LIBRARIES "${BOOST_ROOT}/stage/lib/*.lib")
set(PYTHON_INCLUDE_DIR "${PYTHON_ROOT}/include")
file(GLOB PYTHON_LIBRARIES "${PYTHON_ROOT}/libs/python*[^d].lib")

# Create the main shared library
add_library(${PROJECT_NAME} SHARED ${SOURCE_DIR}/main.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC ${BOOST_INCLUDE_DIR} ${PYTHON_INCLUDE_DIR})
target_link_libraries(${PROJECT_NAME} ${BOOST_LIBRARIES} ${PYTHON_LIBRARIES} "C:/Users/paul/Documents/codes/boost_1_86_0/stage/lib/boost_python312-vc143-mt-x64-1_86.lib")
set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".pyd")

# Copy relevant files to a convinient location
install(TARGETS ${PROJECT_NAME} DESTINATION ${BIN_ROOT})
install(DIRECTORY "${BOOST_ROOT}/stage/lib/" DESTINATION ${BIN_ROOT} FILES_MATCHING PATTERN "*.dll")
install(DIRECTORY "${BOOST_ROOT}/stage/lib/" DESTINATION ${BIN_ROOT} FILES_MATCHING PATTERN "*.lib")

# Copy relevant files to the Python virtual environment
install(TARGETS ${PROJECT_NAME} DESTINATION ${LOCAL_PYTHON_ENV})
install(DIRECTORY "${BOOST_ROOT}/stage/lib/" DESTINATION ${LOCAL_PYTHON_ENV} FILES_MATCHING PATTERN "*.dll")
install(DIRECTORY "${BOOST_ROOT}/stage/lib/" DESTINATION ${LOCAL_PYTHON_ENV} FILES_MATCHING PATTERN "*.lib")
