add_library(display INTERFACE)

include(libraries/hershey_fonts/hershey_fonts)
include(libraries/bitmap_fonts/bitmap_fonts)
include(libraries/pico_graphics/pico_graphics)
include(libraries/cosmic_unicorn/cosmic_unicorn)

target_sources(display INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/cosmic.cpp
)

target_include_directories(display INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(display INTERFACE
    cosmic_unicorn
    pico_graphics
    hershey_fonts
    bitmap_fonts

    pico_stdlib
    hardware_adc
    hardware_pio
    hardware_dma
)

set(DISPLAY_NAME "Cosmic Unicorn")