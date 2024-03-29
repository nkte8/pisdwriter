#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-
from PiSDWriter import global_vars as g
from PiSDWriter import jinja2_writter, sd_writer, downloader, system, notification
import pyudev, argparse, os

template_files={
    "network-config",
    "user-data"
}

os_info = {
    "ubuntu22" : {
        "url": "https://cdimage.ubuntu.com/releases/22.04.3/release/ubuntu-22.04.3-preinstalled-server-arm64+raspi.img.xz",
        "path":  g.os_dir + "/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz"
        }
}

cloudinit_info = {
    # "url": "https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/cloud-init/22.4.2-0ubuntu0~20.04.2/cloud-init_22.4.2.orig.tar.gz",
    "url": "https://launchpadlibrarian.net/638360245/cloud-init_22.4.2.orig.tar.gz",
    "path":  g.os_dir + "/cloudinit.tar.gz"
}

def daemon_run(img_path, cinit_path):
    if not os.path.exists(g.out_dir):
        print("Config file seems not ready: run 'pisdwriter --setup or --configure'")
        return
    if not os.path.exists(g.os_dir):
        print("OS Image seems not ready: run 'pisdwriter --setup or --download'")
        return

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

            print('start write {0} to {1}'.format(os.path.basename(img_path),device_node))
            notification.send_notification(
                setting_path = g.conf_dir + "/settings.json",
                message = "Start Process:)"
            )
            sd_writer.write_os_to_sdcard(img_path,write_device=device_node)
            print("device write completed!")

            print('start write configs to {0}'.format(device_node + "1"))
            sd_writer.write_configs_to_sdcard(
                device_node + "1",
                "/",
                [ g.app_dir + "/output/network-config",
                  g.app_dir + "/output/user-data"])
            print("new config write completed!")

            print('start restore newer cloud-init to {0}'.format(device_node + "2"))
            sd_writer.write_cloudinit_to_sdcard(
                device_node + "2",
                "/usr/lib/python3/dist-packages/",
                cinit_path,
                "**/cloudinit")
            print("new cloudinit restore completed!")
            print("New SD card initialized! you can remove media.")
            notification.send_notification(
                setting_path = g.conf_dir + "/settings.json",
                message = "SDcard initialize success;)"
            )

def download(os_name):
    os.makedirs(g.os_dir, exist_ok=True)

    print("download: " + os_info[os_name]["url"])
    downloader.download_file(
        os_info[os_name]["url"],
        os_info[os_name]["path"])

    print("download: " + cloudinit_info["url"])
    downloader.download_file(
        cloudinit_info["url"],
        cloudinit_info["path"])

def configure():
    config = jinja2_writter.load_vars()
    for template_file in template_files:
        jinja2_writter.write_config(template_file, g.out_dir, config)

def setup():
    system.setup_systemd()

def cleanup():
    system.remove(g.os_dir)
    system.remove(g.out_dir)
    system.remove_systemd()

def main():
    parser = argparse.ArgumentParser(description='write RaspberryPi SD easiry')
    parser.add_argument('-i','--install', action='store_true',
                        help='Run prepair startup(download & configure & setup)')
    parser.add_argument('--download', action='store_true',
                        help='Download os image and cloud-init.')  
    parser.add_argument('--configure', action='store_true',
                        help='Configure write data from config: ' + g.conf_dir)
    parser.add_argument('--setup', action='store_true',
                        help='Setup as systemd service.')
    parser.add_argument('--daemon', action='store_true',
                        help='Start process with configured data: ' + g.out_dir)
    parser.add_argument('--clean', action='store_true',
                        help='Cleanup downloaded images, output config and disable PiSDWriter.service')
    args = parser.parse_args()

    if os.geteuid() != 0 or os.getuid() != 0 :
        print("WARNING: This application needs root permision for write on device.")

    if args.install:
        download("ubuntu22")
        configure()
        setup()
    elif args.daemon:
        daemon_run(os_info["ubuntu22"]["path"],
                cloudinit_info["path"])
    elif args.download:
        download("ubuntu22")
    elif args.configure:
        configure()
    elif args.setup:
        setup()
    elif args.clean:
        cleanup()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
