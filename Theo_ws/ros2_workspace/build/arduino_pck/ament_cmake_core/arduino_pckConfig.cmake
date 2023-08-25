# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_arduino_pck_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED arduino_pck_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(arduino_pck_FOUND FALSE)
  elseif(NOT arduino_pck_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(arduino_pck_FOUND FALSE)
  endif()
  return()
endif()
set(_arduino_pck_CONFIG_INCLUDED TRUE)

# output package information
if(NOT arduino_pck_FIND_QUIETLY)
  message(STATUS "Found arduino_pck: 0.0.0 (${arduino_pck_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'arduino_pck' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${arduino_pck_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(arduino_pck_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${arduino_pck_DIR}/${_extra}")
endforeach()
