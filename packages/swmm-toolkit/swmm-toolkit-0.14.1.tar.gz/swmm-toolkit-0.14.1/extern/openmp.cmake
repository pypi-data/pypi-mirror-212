#
# CMakeLists.txt - CMake configuration file for OpenMP Library on Darwin
#
# Created: Mar 17, 2021
# Updated: May 19, 2021
#
# Author: Michael E. Tryby
#         US EPA ORD/CESER
#
# Note:
#  Need to build libomp for binary compatibility with Python.
#
#  OpenMP library build fails for Xcode generator. Use Ninja or Unix Makefiles
#  instead.
#

################################################################################
#####################    CMAKELISTS FOR OPENMP LIBRARY    ######################
################################################################################

include(FetchContent)


FetchContent_Declare(OpenMP
    URL
        https://github.com/llvm/llvm-project/releases/download/llvmorg-11.1.0/openmp-11.1.0.src.tar.xz
    URL_HASH
        SHA256=d187483b75b39acb3ff8ea1b7d98524d95322e3cb148842957e9b0fbb866052e
)

set(OPENMP_STANDALONE_BUILD TRUE)
set(LIBOMP_INSTALL_ALIASES OFF)

FetchContent_MakeAvailable(OpenMP)
set(OpenMP_AVAILABLE TRUE)


target_link_directories(omp
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/_deps/openmp-build/runtime/src>
        $<INSTALL_INTERFACE:${LIBRARY_DIST}>
)

install(TARGETS omp
    LIBRARY
    DESTINATION
        "${LIBRARY_DIST}"
)
