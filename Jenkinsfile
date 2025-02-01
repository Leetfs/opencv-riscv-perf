node('master') { // 指定 master 节点

    stage('Clean master Workspace') {
        // 清空工作区
        deleteDir()
    }

    stage('Clone OpenCV') {
        sh 'git clone https://github.com/opencv/opencv.git ./opencv'
        // sh 'git clone https://github.com/Leetfs/opencv-riscv-perf.git ./perf'
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
                -D CMAKE_TOOLCHAIN_FILE=../../toolchain-riscv64.cmake \
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
                -D CMAKE_TOOLCHAIN_FILE=../../toolchain-riscv64.cmake \
                -D BUILD_TESTS=ON \
                -D BUILD_EXAMPLES=OFF \
                -D BUILD_DOCS=OFF \
                -D BUILD_opencv_core=ON \
                -D BUILD_opencv_imgproc=ON ..
                make opencv_perf_core opencv_perf_imgproc -j $(nproc)
            '''
    }
    
    stage('stash buildFiles') {
        stash name: 'buildFiles', includes: 'opencv/build/bin/*,opencv/build-vector/bin/*'
    }
}

node('RVV') { // 指定 RVV 节点

    stage('Clean RVV Workspace') {
        // 清空工作区
        deleteDir()
    }
    
    stage('unstash buildFiles') {
        unstash 'buildFiles'
    }
    
    stage('RV Perf Test') {
        sh '''
                mkdir output
                cd ./opencv/build/bin/
                
                chmod +x opencv_perf_core
                ./opencv_perf_core --gtest_filter="*Abs*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RV_core_Abs_test_report.json
                ./opencv_perf_core --gtest_filter="*Mul*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RV_core_Mul_test_report.json
                
                chmod +x opencv_perf_imgproc
                ./opencv_perf_imgproc --gtest_filter="*Resize*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RV_imgproc_Resize_test_report.json
                ./opencv_perf_imgproc --gtest_filter="*Bilateral*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RV_imgproc_Bilateral_test_report.json
            '''
    }
    
    stage('RVV Perf Test') {
        sh '''
                cd ./opencv/build-vector/bin/
                
                chmod +x opencv_perf_core
                ./opencv_perf_core --gtest_filter="*Abs*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RVV_core_Abs_test_report.json
                ./opencv_perf_core --gtest_filter="*Mul*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RVV_core_Mul_test_report.json
                
                chmod +x opencv_perf_imgproc
                ./opencv_perf_imgproc --gtest_filter="*Resize*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RVV_imgproc_Resize_test_report.json
                ./opencv_perf_imgproc --gtest_filter="*Bilateral*" --perf_min_samples=50 --perf_force_samples=50 --gtest_output=json:../../../output/RVV_imgproc_Bilateral_test_report.json
            '''
    }

    stage('stash output') {
        stash name: 'output', includes: 'output/*'
    }
}

node('master') { // 指定 master 节点

    stage('unstash output') {
        unstash 'output'
    }

    stage('Generate Test Report') {
        sh 'python3 test_report.py'
        publishHTML (target : [allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: './',
        reportFiles: 'test_report.html',
        reportName: 'TestReport',
        reportTitles: '测试报告'])
    }
}