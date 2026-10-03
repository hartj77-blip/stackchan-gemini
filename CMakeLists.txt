cmake_minimum_required(VERSION 3.22)
# The shared Stack-chan core (git submodule): board, face, Gemini, themes...
set(EXTRA_COMPONENT_DIRS ${CMAKE_CURRENT_LIST_DIR}/core/components)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(stackchan_gemini)

# NFC (core/components/M5Unit-NFC on M5UnitUnified): UnitUnified can drive a unit
# over M5Unified's own I2C bus (M5.In_I2C, where the base's ST25R3916 sits),
# but only when it can see M5Unified's headers. Give it that, instead of
# letting it install a second I2C driver on the same port.
if(TARGET __idf_M5UnitUnified AND TARGET __idf_M5Unified)
    target_link_libraries(__idf_M5UnitUnified PRIVATE __idf_M5Unified)
endif()
