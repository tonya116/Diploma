cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Установка стандарта C++
set(CMAKE_CXX_STANDARD 17)

# Добавление подпроекта C++ библиотеки
add_subdirectory(src)

file(GLOB_RECURSE SRC_FILES "${CMAKE_SOURCE_DIR}/src/*.cpp")
file(GLOB_RECURSE HDR_FILES "*.h")

add_executable(main main.cpp ${SRC_FILES} ${HDR_FILES})

# target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_SOURCE_DIR}/include )
# Линкуем библиотеки SFML, OpenGL и GLU
target_link_libraries(main calculations)
