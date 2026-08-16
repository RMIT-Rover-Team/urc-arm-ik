cmake_minimum_required(VERSION 3.16)
project(MyNode LANGUAGES CXX)

# Add DEFCOM library from local folder
add_subdirectory(external/DEFCOM)

# Your executable
add_executable(TagPoseCalculator
    src/main.cpp
)

# Link against DEFCOM
target_link_libraries(TagPoseCalculator
    PRIVATE
        DEFCOM
)

# Include DEFCOM headers
target_include_directories(TagPoseCalculator
    PRIVATE
        external/DEFCOM/include
)

# C++ standard
target_compile_features(TagPoseCalculator PUBLIC cxx_std_17)
