---------------------------
**Structuring the project**
---------------------------
The Qt project can be structured as follows:
root/
|-- CMakeLists.txt
|-- src/
|   |-- CMakeLists.txt
|   |-- main.cpp
|   |-- widget/
|       |-- widget.h
|       |-- widget.cpp
|       |-- widget.ui
The root CMakeLists.txt file sets up the project and includes the src folder.
The src folder contains the main application code and its CMakeLists.txt file.
The widget folder contains the widget class implementation files.

---------------------------
**Building the project**
---------------------------
To build the project, follow these steps:
1. Create a build directory in the root of the project.
2. Change into the build directory.
3. Run `cmake ..` to generate the build system.
4. Run `cmake --build .` to build the project.
