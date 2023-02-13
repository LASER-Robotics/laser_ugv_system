# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_ugv_robots_descriptions_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED ugv_robots_descriptions_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(ugv_robots_descriptions_FOUND FALSE)
  elseif(NOT ugv_robots_descriptions_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(ugv_robots_descriptions_FOUND FALSE)
  endif()
  return()
endif()
set(_ugv_robots_descriptions_CONFIG_INCLUDED TRUE)

# output package information
if(NOT ugv_robots_descriptions_FIND_QUIETLY)
  message(STATUS "Found ugv_robots_descriptions: 0.0.0 (${ugv_robots_descriptions_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'ugv_robots_descriptions' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${ugv_robots_descriptions_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(ugv_robots_descriptions_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${ugv_robots_descriptions_DIR}/${_extra}")
endforeach()
