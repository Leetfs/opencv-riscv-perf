## imgproc

./opencv_perf_core --gtest_list_tests \
./opencv_perf_imgproc --gtest_filter="*Resize*" \
./opencv_perf_imgproc --gtest_filter="*Bilateral*"

### Resize

- 348 tests from 8 test cases ran. (186705 ms total)
- 348 tests from 8 test cases ran. (177232 ms total)
- 348 tests from 8 test cases ran. (183280 ms total)
- 348 tests from 8 test cases ran. (178461 ms total)
- 348 tests from 8 test cases ran. (182093 ms total)

### Resize-Vector

- 348 tests from 8 test cases ran. (132436 ms total)
- 348 tests from 8 test cases ran. (133433 ms total)
- 348 tests from 8 test cases ran. (132340 ms total)
- 348 tests from 8 test cases ran. (133563 ms total)
- 348 tests from 8 test cases ran. (132189 ms total)

### Bilateral

- 44 tests from 3 test cases ran. (72405 ms total)
- 44 tests from 3 test cases ran. (72366 ms total)
- 44 tests from 3 test cases ran. (72550 ms total)
- 44 tests from 3 test cases ran. (72351 ms total)
- 44 tests from 3 test cases ran. (71934 ms total)

### Bilateral-Vector

- 44 tests from 3 test cases ran. (29017 ms total)
- 44 tests from 3 test cases ran. (29172 ms total)
- 44 tests from 3 test cases ran. (29250 ms total)
- 44 tests from 3 test cases ran. (29315 ms total)
- 44 tests from 3 test cases ran. (29016 ms total)

## Core

./opencv_perf_core --gtest_filter="*Abs*" --gtest_repeat=5 \
./opencv_perf_core --gtest_filter="*Mul*"

### Mul

- 30 tests from 2 test cases ran. (18867 ms total)
- 30 tests from 2 test cases ran. (18856 ms total)
- 30 tests from 2 test cases ran. (18894 ms total)
- 30 tests from 2 test cases ran. (18831 ms total)
- 30 tests from 2 test cases ran. (18890 ms total)

### Mul-Vector

- 30 tests from 2 test cases ran. (11101 ms total)
- 30 tests from 2 test cases ran. (11143 ms total)
- 30 tests from 2 test cases ran. (11036 ms total)
- 30 tests from 2 test cases ran. (11034 ms total)
- 30 tests from 2 test cases ran. (11055 ms total)

### Abs

- 40 tests from 2 test cases ran. (37899 ms total)
- 40 tests from 2 test cases ran. (37874 ms total)
- 40 tests from 2 test cases ran. (37857 ms total)
- 40 tests from 2 test cases ran. (37836 ms total)
- 40 tests from 2 test cases ran. (37882 ms total)

### Ads-Vector

- 40 tests from 2 test cases ran. (16298 ms total)
- 40 tests from 2 test cases ran. (17071 ms total)
- 40 tests from 2 test cases ran. (17153 ms total)
- 40 tests from 2 test cases ran. (14339 ms total)
- 40 tests from 2 test cases ran. (16981 ms total)
