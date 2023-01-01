# -*- coding: utf-8 -*-
from PiSDWriter import jinja2_writter
import subprocess, os, shutil

def remove(dirpath):
    shutil.rmtree(dirpath,ignore_errors=True)

def setup_systemd():
    jinja2_writter.write_config("PiSDWriter.service", "/usr/lib/systemd/system/")

    _ = subprocess.Popen([
        "systemctl", "enable", "--now", "PiSDWriter"
        ],stdout=subprocess.PIPE)
    _.wait()

def remove_systemd():
    _ = subprocess.Popen([
        "systemctl", "disable", "--now", "PiSDWriter"
        ],stdout=subprocess.PIPE)
    _.wait()
    os.remove("/usr/lib/systemd/system/PiSDWriter.service")
