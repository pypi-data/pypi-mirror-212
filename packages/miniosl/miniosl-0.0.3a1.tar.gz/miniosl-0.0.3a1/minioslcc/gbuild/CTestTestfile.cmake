# CMake generated Testfile for 
# Source directory: /home/kaneko/git-work/miniosl/minioslcc
# Build directory: /home/kaneko/git-work/miniosl/minioslcc/gbuild
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test([=[run_test_mini]=] "/home/kaneko/git-work/miniosl/minioslcc/gbuild/minitest")
set_tests_properties([=[run_test_mini]=] PROPERTIES  _BACKTRACE_TRIPLES "/home/kaneko/git-work/miniosl/minioslcc/CMakeLists.txt;37;add_test;/home/kaneko/git-work/miniosl/minioslcc/CMakeLists.txt;0;")
add_test([=[run_test_file]=] "/home/kaneko/git-work/miniosl/minioslcc/gbuild/minitest_file")
set_tests_properties([=[run_test_file]=] PROPERTIES  _BACKTRACE_TRIPLES "/home/kaneko/git-work/miniosl/minioslcc/CMakeLists.txt;44;add_test;/home/kaneko/git-work/miniosl/minioslcc/CMakeLists.txt;0;")
subdirs("pybind11")
