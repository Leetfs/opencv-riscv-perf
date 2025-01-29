# 设置交叉编译的目标架构
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR riscv64)

# 设置交叉编译工具链路径
set(tools /opt/riscv)

# 设置 C 和 C++ 编译器
set(CMAKE_C_COMPILER ${tools}/bin/riscv64-unknown-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER ${tools}/bin/riscv64-unknown-linux-gnu-g++)

# 设置 sysroot（如果有）
set(CMAKE_SYSROOT /opt/riscv/sysroot)

# 配置查找路径
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# 使用静态链接
set(CMAKE_EXE_LINKER_FLAGS "-static")
# set(CMAKE_CXX_FLAGS "-static -O3") #启用优化
# set(CMAKE_C_FLAGS "-static -O3")
set(BUILD_SHARED_LIBS OFF)