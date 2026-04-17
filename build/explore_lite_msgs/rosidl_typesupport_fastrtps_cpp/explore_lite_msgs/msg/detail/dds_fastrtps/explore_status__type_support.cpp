// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from explore_lite_msgs:msg/ExploreStatus.idl
// generated code does not contain a copyright notice
#include "explore_lite_msgs/msg/detail/explore_status__rosidl_typesupport_fastrtps_cpp.hpp"
#include "explore_lite_msgs/msg/detail/explore_status__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace explore_lite_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_explore_lite_msgs
cdr_serialize(
  const explore_lite_msgs::msg::ExploreStatus & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: status
  cdr << ros_message.status;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_explore_lite_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  explore_lite_msgs::msg::ExploreStatus & ros_message)
{
  // Member: status
  cdr >> ros_message.status;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_explore_lite_msgs
get_serialized_size(
  const explore_lite_msgs::msg::ExploreStatus & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: status
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.status.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_explore_lite_msgs
max_serialized_size_ExploreStatus(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: status
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  return current_alignment - initial_alignment;
}

static bool _ExploreStatus__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const explore_lite_msgs::msg::ExploreStatus *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ExploreStatus__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<explore_lite_msgs::msg::ExploreStatus *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ExploreStatus__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const explore_lite_msgs::msg::ExploreStatus *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ExploreStatus__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_ExploreStatus(full_bounded, 0);
}

static message_type_support_callbacks_t _ExploreStatus__callbacks = {
  "explore_lite_msgs::msg",
  "ExploreStatus",
  _ExploreStatus__cdr_serialize,
  _ExploreStatus__cdr_deserialize,
  _ExploreStatus__get_serialized_size,
  _ExploreStatus__max_serialized_size
};

static rosidl_message_type_support_t _ExploreStatus__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ExploreStatus__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace explore_lite_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_explore_lite_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<explore_lite_msgs::msg::ExploreStatus>()
{
  return &explore_lite_msgs::msg::typesupport_fastrtps_cpp::_ExploreStatus__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, explore_lite_msgs, msg, ExploreStatus)() {
  return &explore_lite_msgs::msg::typesupport_fastrtps_cpp::_ExploreStatus__handle;
}

#ifdef __cplusplus
}
#endif
