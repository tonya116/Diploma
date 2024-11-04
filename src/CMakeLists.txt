add_library(calculations SHARED calculations.cpp)

# Указываем, где находятся заголовочные файлы
target_include_directories(calculations PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../include)
