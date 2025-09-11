cmake_minimum_required(VERSION 3.10)
project(MyGame LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Incluir diretórios de headers
include_directories(
    ${PROJECT_SOURCE_DIR}/model
    ${PROJECT_SOURCE_DIR}/view
)

# Pega todos os .cpp dentro de controller/, model/ e view/
file(GLOB CONTROLLER_SOURCES ${PROJECT_SOURCE_DIR}/controller/*.cpp)
file(GLOB MODEL_SOURCES ${PROJECT_SOURCE_DIR}/model/*.cpp)
file(GLOB VIEW_SOURCES ${PROJECT_SOURCE_DIR}/view/*.cpp)

# Cria o executável
add_executable(MyGame
    ${CONTROLLER_SOURCES}
    ${MODEL_SOURCES}
    ${VIEW_SOURCES}
)

# --- SFML ---
# Procura a SFML instalada no sistema
find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

# Linka SFML com o executável
target_link_libraries(MyGame PRIVATE sfml-graphics sfml-window sfml-system)
