# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pedro/CSLP/data-compression-and-video-coding/src/c++

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pedro/CSLP/data-compression-and-video-coding/src/c++

# Include any dependencies generated for this target.
include CMakeFiles/VideoCodec.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/VideoCodec.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/VideoCodec.dir/flags.make

CMakeFiles/VideoCodec.dir/VideoCodec.cpp.o: CMakeFiles/VideoCodec.dir/flags.make
CMakeFiles/VideoCodec.dir/VideoCodec.cpp.o: VideoCodec.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pedro/CSLP/data-compression-and-video-coding/src/c++/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/VideoCodec.dir/VideoCodec.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/VideoCodec.dir/VideoCodec.cpp.o -c /home/pedro/CSLP/data-compression-and-video-coding/src/c++/VideoCodec.cpp

CMakeFiles/VideoCodec.dir/VideoCodec.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/VideoCodec.dir/VideoCodec.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pedro/CSLP/data-compression-and-video-coding/src/c++/VideoCodec.cpp > CMakeFiles/VideoCodec.dir/VideoCodec.cpp.i

CMakeFiles/VideoCodec.dir/VideoCodec.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/VideoCodec.dir/VideoCodec.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pedro/CSLP/data-compression-and-video-coding/src/c++/VideoCodec.cpp -o CMakeFiles/VideoCodec.dir/VideoCodec.cpp.s

# Object files for target VideoCodec
VideoCodec_OBJECTS = \
"CMakeFiles/VideoCodec.dir/VideoCodec.cpp.o"

# External object files for target VideoCodec
VideoCodec_EXTERNAL_OBJECTS =

VideoCodec: CMakeFiles/VideoCodec.dir/VideoCodec.cpp.o
VideoCodec: CMakeFiles/VideoCodec.dir/build.make
VideoCodec: /usr/local/lib/libopencv_dnn.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_gapi.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_highgui.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_ml.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_objdetect.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_photo.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_stitching.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_video.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_videoio.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_imgcodecs.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_calib3d.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_features2d.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_flann.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_imgproc.so.4.2.0
VideoCodec: /usr/local/lib/libopencv_core.so.4.2.0
VideoCodec: CMakeFiles/VideoCodec.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pedro/CSLP/data-compression-and-video-coding/src/c++/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable VideoCodec"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/VideoCodec.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/VideoCodec.dir/build: VideoCodec

.PHONY : CMakeFiles/VideoCodec.dir/build

CMakeFiles/VideoCodec.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/VideoCodec.dir/cmake_clean.cmake
.PHONY : CMakeFiles/VideoCodec.dir/clean

CMakeFiles/VideoCodec.dir/depend:
	cd /home/pedro/CSLP/data-compression-and-video-coding/src/c++ && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pedro/CSLP/data-compression-and-video-coding/src/c++ /home/pedro/CSLP/data-compression-and-video-coding/src/c++ /home/pedro/CSLP/data-compression-and-video-coding/src/c++ /home/pedro/CSLP/data-compression-and-video-coding/src/c++ /home/pedro/CSLP/data-compression-and-video-coding/src/c++/CMakeFiles/VideoCodec.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/VideoCodec.dir/depend

