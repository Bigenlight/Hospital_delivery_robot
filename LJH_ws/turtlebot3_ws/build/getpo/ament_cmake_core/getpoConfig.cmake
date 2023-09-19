# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_getpo_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED getpo_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(getpo_FOUND FALSE)
  elseif(NOT getpo_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(getpo_FOUND FALSE)
  endif()
  return()
endif()
set(_getpo_CONFIG_INCLUDED TRUE)

# output package information
if(NOT getpo_FIND_QUIETLY)
  message(STATUS "Found getpo: 0.0.0 (${getpo_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'getpo' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${getpo_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(getpo_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${getpo_DIR}/${_extra}")
endforeach()
