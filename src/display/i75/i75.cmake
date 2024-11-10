add_library(display INTERFACE)

include(${PIMORONI_PICO_PATH}/drivers/hub75/hub75.cmake)
include(libraries/hershey_fonts/hershey_fonts)
include(libraries/bitmap_fonts/bitmap_fonts)
include(libraries/pico_graphics/pico_graphics)

target_sources(display INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/i75.cpp
)

target_include_directories(display INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(display INTERFACE
    hub75
    pico_graphics
    hershey_fonts
    bitmap_fonts

    pico_stdlib
    hardware_adc
    hardware_pio
    hardware_dma
)

set(DISPLAY_NAME "Interstate 75")