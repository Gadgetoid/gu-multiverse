add_library(display INTERFACE)

include(${PIMORONI_PICO_PATH}/drivers/hub75_legacy/hub75.cmake)

target_sources(display INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/i75.cpp
)

target_include_directories(display INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(display INTERFACE
    hub75_legacy

    pico_stdlib
    hardware_adc
    hardware_pio
    hardware_dma
)

set(DISPLAY_NAME "Interstate 75")