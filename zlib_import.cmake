include(FetchContent)
FetchContent_Declare(
        zlib_git
        GIT_REPOSITORY https://github.com/madler/zlib.git
        GIT_TAG        51b7f2abdade71cd9bb0e7a373ef2610ec6f9daf # v1.3.1
)
FetchContent_Populate(zlib_git)

set(ZLIB_PATH ${zlib_git_SOURCE_DIR})

# Configure zconf.h
configure_file(
        ${ZLIB_PATH}/zconf.h.in
        ${CMAKE_CURRENT_BINARY_DIR}/zconf.h
        @ONLY
)

add_library(zlib STATIC
        ${ZLIB_PATH}/adler32.c
        ${ZLIB_PATH}/compress.c
        ${ZLIB_PATH}/crc32.c
        ${ZLIB_PATH}/deflate.c
        ${ZLIB_PATH}/inffast.c
        ${ZLIB_PATH}/inflate.c
        ${ZLIB_PATH}/inftrees.c
        ${ZLIB_PATH}/trees.c
        ${ZLIB_PATH}/uncompr.c
        ${ZLIB_PATH}/zutil.c
)

target_include_directories(zlib PUBLIC
        ${ZLIB_PATH}/
        ${CMAKE_CURRENT_BINARY_DIR}/
)