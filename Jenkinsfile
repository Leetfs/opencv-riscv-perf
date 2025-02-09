node('master') { // 指定 master 节点

    stage('Clean master Workspace') {
        // 清空工作区
        deleteDir()
    }

    stage('Clone OpenCV') {
        sh 'git clone https://github.mtftm.com/Leetfs/opencv.git ./opencv'
        sh 'git clone https://github.mtftm.com/Leetfs/opencv-riscv-perf.git ./perf'
    }

    stage('Build OpenCV for RISC-V Vector') {
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
    
    stage('Build OpenCV for RISC-V') {
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
    
    stage('stash buildFiles') {
        stash name: 'buildFiles-core', includes: 'opencv/build/bin/opencv_perf_core,opencv/build-vector/bin/opencv_perf_core'
        stash name: 'buildFiles-imgproc', includes: 'opencv/build/bin/opencv_perf_imgproc,opencv/build-vector/bin/opencv_perf_imgproc'
    }
}

node {
    
    stage('Perf Test') {
        parallel(
            "Core Perf Test": {
                node('RVV') {
                    // 清空工作区
                    stage('Clean Workspace') {
                        deleteDir()
                    }

                    // 下载构建文件
                    stage('unstash buildFiles-core') {
                        unstash 'buildFiles-core'
                    }

                    // RV Core Perf Test
                    stage('RV Core Perf Test') {
                        sh '''
                        mkdir -p output
                        cd ./opencv/build/bin/
                        chmod +x opencv_perf_core
                        ./opencv_perf_core --gtest_filter="*Abs*:*Mul*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RV_core_test_report.json
                        '''
                    }

                    // RVV Core Perf Test
                    stage('RVV Core Perf Test') {
                        sh '''
                        cd ./opencv/build-vector/bin/
                        chmod +x opencv_perf_core
                        ./opencv_perf_core --gtest_filter="*Abs*:*Mul*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RVV_core_test_report.json
                        '''
                    }

                    stage('stash core test report') {
                    stash name: 'core', includes: 'output/*'
                    }
                }
                
            },
            "Imgproc Perf Test": {
                node('RVV') {
                    // 清空工作区
                    stage('Clean Workspace') {
                        deleteDir()
                    }

                    // 下载构建文件
                    stage('unstash buildFiles-imgproc') {
                        unstash 'buildFiles-imgproc'
                    }

                    // RV Imgproc Perf Test
                    stage('RV Imgproc Perf Test') {
                        sh '''
                        mkdir -p output
                        cd ./opencv/build/bin/
                        chmod +x opencv_perf_imgproc
                        ./opencv_perf_imgproc --gtest_filter="*Resize*:*Bilateral*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RV_imgproc_test_report.json
                        '''
                    }

                    // RVV Imgproc Perf Test
                    stage('RVV Imgproc Perf Test') {
                        sh '''
                        cd ./opencv/build-vector/bin/
                        chmod +x opencv_perf_imgproc
                        ./opencv_perf_imgproc --gtest_filter="*Resize*:*Bilateral*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RVV_imgproc_test_report.json
                        '''
                    }

                    stage('stash imgproc test report') {
                    stash name: 'imgproc', includes: 'output/*'
                    }
                }
            }
        )
    }
}

node('master') { // 指定 master 节点

    stage('unstash output') {
        unstash 'core'
        unstash 'imgproc'
    }

    stage('Generate Test Report') {
        sh '''
            cd perf
            python3 test_report.py
        '''
        publishHTML (target : [allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: './',
        reportFiles: 'test_report.html',
        reportName: 'TestReport',
        reportTitles: '测试报告'])
        
    }
}