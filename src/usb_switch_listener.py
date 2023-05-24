#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
import subprocess

def switch_callback(msg, path):
    switch_value = msg.data

    if switch_value == 0:
        script_argument = "off"
    elif switch_value == 1:
        script_argument = "on"
    else:
        rospy.logwarn("Invalid switch value: %d", switch_value)
        return

    script_path = path
    command = "sudo %s %s" % (script_path, script_argument)

    try:
        subprocess.check_output(command, shell=True)
        rospy.loginfo("Script executed with root privileges. Argument: %s", script_argument)
    except subprocess.CalledProcessError as e:
        rospy.logerr("Error executing script: %s", e)


if __name__ == '__main__':
    rospy.init_node('usb_switch_listener', anonymous=True)
    rate = rospy.Rate(5)  # hz
    commands_topic = rospy.get_param('~command_topic')
    command_topic_single = rospy.get_param('~command_topic_single')
    script_path = rospy.get_param('~script_path')

    command_handler = lambda msg: switch_callback(msg, script_path)
    rospy.Subscriber(commands_topic, Int32, command_handler)
    rospy.Subscriber(command_topic_single, Int32, command_handler)

    rospy.spin()