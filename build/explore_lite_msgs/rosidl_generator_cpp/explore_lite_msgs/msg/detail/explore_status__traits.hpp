// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from explore_lite_msgs:msg/ExploreStatus.idl
// generated code does not contain a copyright notice

#ifndef EXPLORE_LITE_MSGS__MSG__DETAIL__EXPLORE_STATUS__TRAITS_HPP_
#define EXPLORE_LITE_MSGS__MSG__DETAIL__EXPLORE_STATUS__TRAITS_HPP_

#include "explore_lite_msgs/msg/detail/explore_status__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<explore_lite_msgs::msg::ExploreStatus>()
{
  return "explore_lite_msgs::msg::ExploreStatus";
}

template<>
inline const char * name<explore_lite_msgs::msg::ExploreStatus>()
{
  return "explore_lite_msgs/msg/ExploreStatus";
}

template<>
struct has_fixed_size<explore_lite_msgs::msg::ExploreStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<explore_lite_msgs::msg::ExploreStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<explore_lite_msgs::msg::ExploreStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // EXPLORE_LITE_MSGS__MSG__DETAIL__EXPLORE_STATUS__TRAITS_HPP_
