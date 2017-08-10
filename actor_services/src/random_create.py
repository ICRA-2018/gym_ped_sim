#!/usr/bin/env python
# coding=utf-8

'''
Author:Tai Lei
Date:
Info:
'''

import random
import numpy as np
import rospkg
from lxml import etree
from lxml.etree import Element
from copy import deepcopy

#rospy.init_node('creat_world', anonymous=True)
rospack = rospkg.RosPack()
plugin_pkg_path = rospack.get_path("actor_plugin")
plugin_path = plugin_pkg_path + "/lib/libactorplugin_ros.so"
actor_pkg_path = rospack.get_path("actor_services")

tree_ = etree.parse(actor_pkg_path+'/worlds/empty.world')
world_ = tree_.getroot().getchildren()[0]

skin_list = ["moonwalk.dae",
        "run.dae",
        "sit_down.dae",
        "sitting.dae",
        "stand_up.dae",
        "stand.dae",
        "talk_a.dae",
        "talk_b.dae",
        "walk.dae"]


actor_list = []
for item in range(10):
    actor = Element("actor", name="actor"+str(item))

    pose = Element("pose")
    #randomly generate position to pose text
    x = str((np.random.rand()-0.5)*12)
    y = str((np.random.rand()-0.5)*12)
    pose.text = x+" "+y+" "+"1.02 0 0 0"
    actor.append(pose)

    skin = Element("skin")
    skin_fn = Element("filename")
    skin_fn.text=random.choice(skin_list)
    skin_scale = Element("scale")
    skin_scale.text = "1"
    skin.append(skin_fn)
    skin.append(skin_scale)
    actor.append(skin)

    animation = Element("animation", name="walking")
    animate_fn = Element("filename")
    animate_fn.text = "walk.dae"
    interpolate_x = Element("interpolate_x")
    interpolate_x.text = "true"
    animate_scale = Element("scale")
    animate_scale.text = "1"
    animation.append(animate_fn)
    animation.append(animate_scale)
    animation.append(interpolate_x)
    actor.append(animation)

    plugin = Element("plugin", name="None", filename=plugin_path)
    speed = Element("speed")
    speed.text = str(np.random.normal(1.34, 0.26, 1)[0])
    dodgingRight = Element("dodgingRight")
    dodgingRight.text = str(np.random.rand() < 0.5).lower()
    target = Element("target")
    x = str((np.random.rand()-0.5)*12)
    y = str((np.random.rand()-0.5)*12)
    target.text =  x+" "+y+" "+"1.02"
    target_weight = Element("target_weight")
    target_weight.text = "1.5"
    obstacle_weight = Element("obstacle_weight")
    obstacle_weight.text = "1.5"
    animation_factor = Element("animation_factor")
    speed_ = str((np.random.rand()*3)+5)
    animation_factor.text = speed_
    ignore_obstacle = Element("ignore_obstacles")
    model_cafe = Element("model")
    model_cafe.text = "caffe"
    model_ground_plane = Element("model")
    model_ground_plane.text = "ground_plane"
    ignore_obstacle.append(model_cafe)
    ignore_obstacle.append(model_ground_plane)
    plugin.append(speed)
    plugin.append(dodgingRight)
    plugin.append(target)
    plugin.append(target_weight)
    plugin.append(obstacle_weight)
    plugin.append(animation_factor)
    plugin.append(ignore_obstacle)
    actor.append(plugin)

    world_.append(actor)

tree_.write(actor_pkg_path+'/worlds/ped_world.world', pretty_print=True, xml_declaration=True, encoding="utf-8")