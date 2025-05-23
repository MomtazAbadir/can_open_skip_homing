cmake_minimum_required(VERSION 3.8)
project(crawlr_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)
find_package(canopen REQUIRED)
find_package(lely_core_libraries REQUIRED)


# install launch file
install(DIRECTORY
   urdf meshes 
  DESTINATION share/${PROJECT_NAME})
  
  # install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(FILES urdf/crawlr.xacro
  DESTINATION share/${PROJECT_NAME}/urdf)
install(FILES urdf/crawlr_ros2_control.xacro
  DESTINATION share/${PROJECT_NAME}/urdf)
  install(FILES urdf/initial_positions.yaml
  DESTINATION share/${PROJECT_NAME}/urdf)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
