#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include <sensor_msgs/msg/joint_state.hpp>

using namespace std::chrono_literals;
using std::placeholders::_1;


class getpo : public rclcpp::Node
{  
public:
  getpo() : Node("getpo")
  {
    auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(10));
    getpo_subscriber_ = this->create_subscription<std_msgs::msg::Float32MultiArray>(
      "/position",
      qos_profile,
      std::bind(&getpo::subscribe_topic_message, this, _1));
    pub_ = this->create_publisher<sensor_msgs::msg::JointState>("joint_states", qos_profile);
    timer_ = this->create_wall_timer(30ms, std::bind(&getpo::publish, this));
  }
  std::array<float, 2> position ={0.0f,0.0f};
  std::array<float, 2> velocity ={0.0f,0.0f};

private:
  void subscribe_topic_message(const std_msgs::msg::Float32MultiArray::SharedPtr pose)
  {
    RCLCPP_INFO(this->get_logger(), "Received message: '%f'", pose->data[0]);
    position[0]=pose->data[0];
    position[1]=pose->data[1];
    velocity[0]=pose->data[2];
    velocity[1]=pose->data[3];

  }
  void publish()
{

  auto msg = std::make_unique<sensor_msgs::msg::JointState>();


  msg->header.frame_id = "base_link";
  msg->header.stamp = rclcpp::Clock{}.now();

  msg->name.push_back("wheel_left_joint");
  msg->name.push_back("wheel_right_joint");

  msg->position.push_back(position[0]);
  msg->position.push_back(position[1]);

  msg->velocity.push_back(velocity[0]);
  msg->velocity.push_back(velocity[1]);

  pub_->publish(std::move(msg));
}
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Subscription<std_msgs::msg::Float32MultiArray>::SharedPtr getpo_subscriber_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr pub_;
};


int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<getpo>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}