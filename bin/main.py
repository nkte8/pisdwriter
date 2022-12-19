#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-
import jinja2_writter, sdwrite_os
import time, os, sys, pyudev

template_files={
    "network-config",
    "user-data"
}

os_info = {
    "ubuntu22" : {
        "os_url": "https://cdimage.ubuntu.com/releases/22.04.1/release/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz",
        "dl_path": "/tmp/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz"
        }
}

def run(img_path):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    print("monitoring device is ready.")

    for device in iter(monitor.poll, None):
        if 'ID_FS_TYPE' in device and \
            str(device.device_type) == "disk" and \
            str(device.action) == "add":
            device_node = device.device_node
            print('device find: {0}'.format(device_node))

            sdwrite_os.write_to_sdcard(img_path,write_device=device_node)
            print("write completed!")

if __name__ == "__main__":

    for template_file in template_files:
        jinja2_writter.write_config(template_file)

    sdwrite_os.download_os_image(
        os_info["ubuntu22"]["os_url"],
        os_info["ubuntu22"]["dl_path"])

    run(os_info["ubuntu22"]["dl_path"])

