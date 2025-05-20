cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED MULTIVERSE_BOARD)
set(MULTIVERSE_BOARD galactic)
message(WARNING "No \"MULTIVERSE_BOARD\" specified. Defaulting to \"galactic\"")
else()
message("\"MULTIVERSE_BOARD\" is set to \"${MULTIVERSE_BOARD}\".")
endif()

set(NAME ${MULTIVERSE_BOARD}-multiverse)
set(DISPLAY_PATH ${CMAKE_CURRENT_LIST_DIR}/src/display/${MULTIVERSE_BOARD}/${MULTIVERSE_BOARD}.cmake)

include(pimoroni_pico_import.cmake)
include(pico_sdk_import.cmake)

# Gooey boilerplate
project(${NAME} C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the SDK
pico_sdk_init()

# Tiny USB
set(FAMILY rp2040)
set(BOARD pico_sdk)

set(SRC_DIR ${CMAKE_CURRENT_LIST_DIR}/src)

# Add your source files
add_executable(${NAME}
    ${SRC_DIR}/main.cpp
    ${SRC_DIR}/cdc_uart.cpp
    ${SRC_DIR}/get_serial.cpp
    ${SRC_DIR}/usb_descriptors.cpp
)

target_include_directories(
    ${NAME} PRIVATE
    ${SRC_DIR}
)

target_compile_definitions(
    ${NAME} PRIVATE
    MULTIVERSE_BOARD="${MULTIVERSE_BOARD}"
)

include(${DISPLAY_PATH})

# Don't forget to link the libraries you need!
target_link_libraries(${NAME}
    display

    pico_stdlib
    pico_unique_id
    hardware_pio
    hardware_watchdog

    tinyusb_device
    tinyusb_board
)

# create map/bin/hex file etc.
pico_add_extra_outputs(${NAME})

# Set up files for the release packages
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/${NAME}.uf2
    ${CMAKE_CURRENT_LIST_DIR}/README.md
    ${CMAKE_CURRENT_LIST_DIR}/LICENSE
    ${CMAKE_CURRENT_LIST_DIR}/99-fire.rules
    ${CMAKE_CURRENT_LIST_DIR}/examples/life.py
    ${CMAKE_CURRENT_LIST_DIR}/examples/multi_fire.py
    ${CMAKE_CURRENT_LIST_DIR}/examples/multi_matrix.py
    ${CMAKE_CURRENT_LIST_DIR}/examples/multi_synth.py
    DESTINATION .
)

set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY OFF)
set(CPACK_GENERATOR "ZIP" "TGZ")
include(CPack)
