cmake_minimum_required(VERSION 3.13)
project(Blackscholes)

set(CMAKE_CXX_STANDARD 17)

set(SMARTREDIS_INSTALL_PATH /home/bohan/smartredis/install)
find_library(SMARTREDIS_LIBRARY smartredis
             PATHS ${SMARTREDIS_INSTALL_PATH}/lib
             NO_DEFAULT_PATH REQUIRED
)

# Fortran-only:
#find_library(SMARTREDIS_FORTRAN_LIBRARY smartredis-fortran
#             PATHS SMARTREDIS_INSTALL_PATH/lib
#             NO_DEFAULT_PATH REQUIRED
#)

include_directories(SYSTEM
    /usr/local/include
    ${SMARTREDIS_INSTALL_PATH}/include
)

# Build executables

add_executable(Blackscholes
    blackscholes_outsourced_to_redis.cpp
)
target_link_libraries(Blackscholes
    ${SMARTREDIS_LIBRARY}
    # Fortran-only:
    #${SMARTREDIS_FORTRAN_LIBRARY}
)
