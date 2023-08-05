# -*- coding: utf-8 -*-
# @FileName  :checkin_class.py
# @Time      :2023/4/7 22:46
# @Author    :yaoys
# @Desc      :

from ablesci_checkin.ableSci_checkin import ableSci
from cloud_189_checkin.cloud189_checkin import cloud189
from bilibili_checkin.bilibili_alive_auto_checkin import bilibili_alive
from bilibili_checkin.bilibili_auto_checkin import bilibili_coin
from glados_checkin.glados import glados
from gufenxueshu_checkin.gufen_checkin import gufenxueshu
from aliyunpan_checkin.aliyunpan_checkin import aliyunpan
from push_message.push_message import pushPlus, server
from wps_checkin.wps_cloud_checkin import wps_cloud
from wps_checkin.wps_vip_checkin import wps_vip

checkin_class = {
    "able_sci": {
        "cookie_name": "able_sci",
        "task_class_name": ableSci,
        "time_sleep": 0,
        "desc": "科研通平台相关配置"
    },
    "bilibili_live": {
        "cookie_name": "bilibili_live",
        "task_class_name": bilibili_alive,
        "time_sleep": 30,
        "desc": "B站直播签到平台相关配置"
    },
    "bilibili_icon": {
        "cookie_name": "bilibili_icon",
        "task_class_name": bilibili_coin,
        "time_sleep": 30,
        "desc": "B站获取硬币相关配置"
    },
    "cloud189": {
        "cookie_name": "cloud189",
        "task_class_name": cloud189,
        "time_sleep": 0,
        "desc": "天翼云盘相关配置"
    },
    "glados": {
        "cookie_name": "glados",
        "task_class_name": glados,
        "time_sleep": 0,
        "desc": "glados平台相关配置"
    },
    "gu_fen_xue_shu": {
        "cookie_name": "gu_fen_xue_shu",
        "task_class_name": gufenxueshu,
        "time_sleep": 0,
        "desc": "谷粉学术平台相关配置"
    },
    "aliyunpan": {
        "cookie_name": "aliyunpan",
        "task_class_name": aliyunpan,
        "time_sleep": 0,
        "desc": "阿里云盘相关配置"
    },
    "wps_vip": {
        "cookie_name": "wps_vip",
        "task_class_name": wps_vip,
        "time_sleep": 60,
        "desc": "Wps Vip相关配置"
    },
    "wps_cloud": {
        "cookie_name": "wps_cloud",
        "task_class_name": wps_cloud,
        "time_sleep": 60,
        "desc": "Wps云空间相关配置"
    }

}

message_class = {
    'pushPlus': ['pushPlus', pushPlus],
    'server': ['server', server]
}
