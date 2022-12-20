# -*- coding: utf-8 -*-
import subprocess, os, tempfile, re, pathlib
from tqdm import tqdm

def write_os_to_sdcard(os_path, write_device="/dev/null"):
    if os.path.isfile(os_path):
        unxz_output=subprocess.Popen([
        "unxz", os_path, "-c"
        ],stdout=subprocess.PIPE)

        dd_result=subprocess.Popen([
            "dd", "of="+write_device, "bs=4M", "conv=fsync", "status=progress"
            ],stdin=unxz_output.stdout,stdout=subprocess.PIPE)

        dd_result.wait()

def __mount_and_write_sdcard(device_node, function, *args):
    with tempfile.TemporaryDirectory(prefix="tmp_", dir=".") as dirpath:
        _ = subprocess.Popen([
            "mount", device_node, dirpath
            ],stdout=subprocess.PIPE)
        _.wait()
        
        function(dirpath, *args)

        _ = subprocess.Popen([
            "umount", dirpath
            ],stdout=subprocess.PIPE)
        _.wait()

def __open_gz_copy_to_sdcard(mntdir, dest, src, pattern):
    with tempfile.TemporaryDirectory(prefix="tmp_", dir=".") as dirpath:
        tar_output=subprocess.Popen([
            "tar", "xzf", src, "-C", dirpath
            ],stdout=subprocess.PIPE)
        tar_output.wait()

        find_first = [k for k in pathlib.Path(dirpath).glob(pattern)][0]

        cp_output=subprocess.Popen([
            "cp", "-f", find_first, mntdir + dest
            ],stdout=subprocess.PIPE)
        print("copy successed: " + find_first)
        cp_output.wait()

def write_cloudinit_to_sdcard(device_node, dest, src, pattern):
    if os.path.isfile(src):
        callback = __open_gz_copy_to_sdcard
        __mount_and_write_sdcard(device_node,callback,dest,src,pattern)


def __open_conf_copy_to_sdcard(mntdir, dest, src):
    for f in src:
        cp_output=subprocess.Popen([
            "cp", "-f", f, mntdir + dest
            ],stdout=subprocess.PIPE)
        print("copy successed: " + f)
        cp_output.wait()

def write_configs_to_sdcard(device_node,dest,*src):
    callback = __open_conf_copy_to_sdcard
    __mount_and_write_sdcard(device_node,callback,dest,*src)
