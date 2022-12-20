#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-
from PiSDWriter import jinja2_writter, sd_writer, downloader 
import pyudev

template_files={
    "network-config",
    "user-data"
}

os_info = {
    "ubuntu22" : {
        "url": "https://cdimage.ubuntu.com/releases/22.04.1/release/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz",
        "path": "/tmp/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz"
        }
}

cloudinit_info = {
    # "url": "https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/cloud-init/22.4.2-0ubuntu0~20.04.2/cloud-init_22.4.2.orig.tar.gz",
    "url": "https://launchpadlibrarian.net/638360245/cloud-init_22.4.2.orig.tar.gz",
    "path": "/tmp/cloudinit.tar.gz"
}

def daemon_run(img_path, cinit_path):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    print("monitoring device is ready.")

    for device in iter(monitor.poll, None):
        if 'ID_FS_TYPE' in device and \
            str(device.device_type) == "disk" and \
            str(device.action) == "add":
            device_node = device.device_node
            print('device new connection at {0}'.format(device_node))

            sd_writer.write_os_to_sdcard(img_path,write_device=device_node)
            print("device write completed!")

            sd_writer.write_configs_to_sdcard(
                device_node + "1",
                "/",
                ["out/network-config","out/user-data"])
            print("new config write completed!")

            sd_writer.write_cloudinit_to_sdcard(
                device_node + "2",
                "/usr/lib/python3/dist-packages/",
                cinit_path,
                "**/cloudinit")
            print("new cloudinit write completed!")

def main():
    for template_file in template_files:
        jinja2_writter.write_config(template_file)

    print("download: " + os_info["ubuntu22"]["url"])
    downloader.download_file(
        os_info["ubuntu22"]["url"],
        os_info["ubuntu22"]["path"])

    print("download: " + cloudinit_info["url"])
    downloader.download_file(
        cloudinit_info["url"],
        cloudinit_info["path"])

    daemon_run(os_info["ubuntu22"]["path"],
                cloudinit_info["path"])

if __name__ == "__main__":
    main()
