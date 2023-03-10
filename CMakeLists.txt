cmake_minimum_required(VERSION 3.12)

set(NAME gu-multiverse) 

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

# Include required libraries
# This assumes `pimoroni-pico` is stored alongside your project
include(libraries/hershey_fonts/hershey_fonts)
include(libraries/bitmap_fonts/bitmap_fonts)
include(libraries/pico_graphics/pico_graphics)
include(libraries/galactic_unicorn/galactic_unicorn)

# Don't forget to link the libraries you need!
target_link_libraries(${NAME}
    pico_stdlib pico_unique_id tinyusb_device tinyusb_board hardware_pio pico_graphics galactic_unicorn hershey_fonts bitmap_fonts
)

# create map/bin/hex file etc.
pico_add_extra_outputs(${NAME})

# Set up files for the release packages
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/${NAME}.uf2
    ${CMAKE_CURRENT_LIST_DIR}/README.md
    ${CMAKE_CURRENT_LIST_DIR}/LICENSE
    ${CMAKE_CURRENT_LIST_DIR}/99-fire.rules
    ${CMAKE_CURRENT_LIST_DIR}/examples/multiverse.py
    ${CMAKE_CURRENT_LIST_DIR}/examples/multi_matrix.py
    ${CMAKE_CURRENT_LIST_DIR}/examples/multi_fire.py
    DESTINATION .
)

set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY OFF)
set(CPACK_GENERATOR "ZIP" "TGZ")
include(CPack)
