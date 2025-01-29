pipeline {
    agent none  // 不指定全局 agent
    stages {
        stage('Clean Workspace') {
            agent {
                label 'master'
            }
            steps {
                script {
                    // 清空工作区
                    deleteDir()
                }
            }
        }
        stage('Clone OpenCV') {
            agent {
                label 'master'
            }
            steps {
                script {
                    sh 'git clone https://github.mtftm.com/opencv/opencv.git ./opencv'
                    sh 'git clone https://github.mtftm.com/Leetfs/opencv-riscv-perf.git ./perf'
                }
            }
        }

        stage('Build OpenCV for RISC-V Vector') {
            agent {
                label 'master'
            }
            steps {
                script {
                    // 配置交叉编译工具链并开始构建
                    sh '''
                        cd ./opencv && mkdir build-Vector && cd build-Vector
                        cmake -D CMAKE_BUILD_TYPE=Release \
                        -D CMAKE_CXX_FLAGS="-static -O3 -march=rv64imafdcv" \
                        -D CMAKE_C_FLAGS="-static -O3 -march=rv64imafdcv" \
                        -D ENABLE_PERF_TESTS=ON \
                        -D WITH_EIGEN=ON \
                        -D CMAKE_INSTALL_PREFIX=./install \
                        -D CMAKE_TOOLCHAIN_FILE=../../perf/toolchain-riscv64.cmake \
                        -D BUILD_TESTS=ON \
                        -D BUILD_EXAMPLES=OFF \
                        -D BUILD_DOCS=OFF \
                        -D BUILD_opencv_core=ON \
                        -D BUILD_opencv_imgproc=ON ..
                        make opencv_perf_core opencv_perf_imgproc -j $(nproc)
                    '''
                }
            }
        }
        
        stage('Build OpenCV for RISC-V') {
            agent {
                label 'master'
            }
            steps {
                script {
                    // 配置交叉编译工具链并开始构建
                    sh '''
                        cd ./opencv && mkdir build && cd build
                        cmake -D CMAKE_BUILD_TYPE=Release \
                        -D CMAKE_CXX_FLAGS="-static -O3 -march=rv64imafdc" \
                        -D CMAKE_C_FLAGS="-static -O3 -march=rv64imafdc" \
                        -D ENABLE_PERF_TESTS=ON \
                        -D WITH_EIGEN=ON \
                        -D CMAKE_INSTALL_PREFIX=./install \
                        -D CMAKE_TOOLCHAIN_FILE=../../perf/toolchain-riscv64.cmake \
                        -D BUILD_TESTS=ON \
                        -D BUILD_EXAMPLES=OFF \
                        -D BUILD_DOCS=OFF \
                        -D BUILD_opencv_core=ON \
                        -D BUILD_opencv_imgproc=ON ..
                        make opencv_perf_core opencv_perf_imgproc -j $(nproc)
                    '''
                }
            }
        }

        // stage('Run Performance Tests') {
        //     agent {
        //         label 'RVV'  // 在 RVV 节点上运行
        //     }
        //     steps {
        //         script {
        //             // 运行性能测试
        //             sh 'opencv_perf_core'  // 运行 Core 模块性能测试
        //             sh 'opencv_perf_imgproc'  // 运行 ImgProc 模块性能测试
        //         }
        //     }
        // }

        // stage('Clean Up') {
        //     agent {
        //         label 'master'  // 在 master 节点上运行清理工作
        //     }
        //     steps {
        //         script {
        //             // 清理克隆的源代码
        //             // sh 'rm -rf /opencv'
        //         }
        //     }
        // }
    }
}