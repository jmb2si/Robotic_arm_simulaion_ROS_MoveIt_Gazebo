cmake_minimum_required(VERSION 2.8.3)
project(trex_gazebo)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  roscpp
  rospy
)

# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

catkin_package(
  CATKIN_DEPENDS
  gazebo_ros
  CATKIN_DEPENDS
  INCLUDE_DIRS
  LIBRARIES ${PROJECT_NAME}
) 

include_directories(include ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS} ${SDFormat_INCLUDE_DIRS} )

link_directories(
  ${GAZEBO_LIBRARY_DIRS}
  ${catkin_LIBRARY_DIRS}
)



install(DIRECTORY launch worlds plugins msg
DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(PROGRAMS
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)