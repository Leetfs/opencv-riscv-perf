pipeline {
    agent none  // 不指定全局 agent
    stages {
        stage('Clean master Workspace') {
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
                        cd ./opencv && mkdir build-vector && cd build-vector
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
        
        stage('stash') {
            agent {
                label 'master'
            }
            steps {
                script {
                    stash name: 'buildFiles', includes: 'opencv/build/bin/*,opencv/build-vector/bin/*'
                }
            }
        }
        
        stage('Clean RVV Workspace') {
            agent {
                label 'RVV'
            }
            steps {
                script {
                    // 清空工作区
                    deleteDir()
                }
            }
        }
        
        stage('unstash') {
            agent {
                label 'RVV'
            }
            steps {
                script {
                    unstash 'buildFiles'
                }
            }
        }
        
        stage('RV Perf Test') {
            agent {
                label 'RVV'
            }
            steps {
                script {
                    sh '''
                        cd ./opencv/build/bin/
                        
                        chmod +x opencv_perf_core
                        ./opencv_perf_core --gtest_filter="*Abs*"
                        ./opencv_perf_core --gtest_filter="*Mul*"
                        
                        chmod +x opencv_perf_imgproc
                        ./opencv_perf_imgproc --gtest_filter="*Resize*"
                        ./opencv_perf_imgproc --gtest_filter="*Bilateral*"
                    '''
                }
            }
        }
        
        stage('RVV Perf Test') {
            agent {
                label 'RVV'
            }
            steps {
                script {
                    sh '''
                        cd ./opencv/build-vector/bin/
                        
                        chmod +x opencv_perf_core
                        ./opencv_perf_core --gtest_filter="*Abs*"
                        ./opencv_perf_core --gtest_filter="*Mul*"
                        
                        chmod +x opencv_perf_imgproc
                        ./opencv_perf_imgproc --gtest_filter="*Resize*"
                        ./opencv_perf_imgproc --gtest_filter="*Bilateral*"
                    '''
                }
            }
        }
    }
}