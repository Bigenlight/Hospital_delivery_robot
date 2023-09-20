// Copyright 2019 ROBOTIS CO., LTD.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Author: Darby Lim

#include <array>

#include <memory>
#include <string>
#include <utility>

#include "turtlebot3_node/sensors/joint_state.hpp"

using robotis::turtlebot3::sensors::JointState;

JointState::JointState(
  std::shared_ptr<rclcpp::Node> & nh,
  const std::string & topic_name,
  const std::string & frame_id)
: Sensors(nh, frame_id)
{
  pub_ = nh->create_publisher<sensor_msgs::msg::JointState>(topic_name, this->qos_);
  sub_ = nh->create_subscription<std_msgs::msg::Float32MultiArray>(
      "/position",
      this->qos_,
      std::bind(&JointState::subscribe, this, std::placeholders::_1));

  RCLCPP_INFO(nh_->get_logger(), "Succeeded to create joint state publisher");
}

static std::array<float, robotis::turtlebot3::sensors::JOINT_NUM> last_diff_position, last_position;

  std::array<float, robotis::turtlebot3::sensors::JOINT_NUM> position;

  std::array<float, robotis::turtlebot3::sensors::JOINT_NUM> velocity;
std::array<float,1> count={0};

void JointState::subscribe(const std_msgs::msg::Float32MultiArray::SharedPtr pose)
{
  position[0]=pose->data[0];
  position[1]=pose->data[1];
  velocity[0]=pose->data[2];
  velocity[1]=pose->data[3];
  count[0]=pose->data[4];
}

void JointState::publish(
  const rclcpp::Time & now,
  std::shared_ptr<DynamixelSDKWrapper> & dxl_sdk_wrapper)
{
  auto msg = std::make_unique<sensor_msgs::msg::JointState>();

  // std::array<int32_t, JOINT_NUM> current =
  //   {dxl_sdk_wrapper->get_data_from_device<int32_t>(
  //     extern_control_table.resent_current_left.addr,
  //     extern_control_table.resent_current_left.length),
  //   dxl_sdk_wrapper->get_data_from_device<int32_t>(
  //     extern_control_table.resent_current_right.addr,
  //     extern_control_table.resent_current_right.length)};

  msg->header.frame_id = this->frame_id_;
  msg->header.stamp = now;

  msg->name.push_back("wheel_left_joint");
  msg->name.push_back("wheel_right_joint");

  msg->position.push_back(last_diff_position[0]);
  msg->position.push_back(last_diff_position[1]);

  msg->velocity.push_back(velocity[0]);
  msg->velocity.push_back(velocity[1]);

  // msg->effort.push_back(current[0]);
  // msg->effort.push_back(current[1]);
if (count[0]<1){
  last_diff_position[0] = 0;
  last_diff_position[1] = 0;

  last_position = position;
}
else{
  last_diff_position[0] += (position[0] - last_position[0]);
  last_diff_position[1] += (position[1] - last_position[1]);

  last_position = position;
}
  pub_->publish(std::move(msg));
}
