# -*- coding: utf-8 -*-
from PiSDWriter import global_vars as g
from PiSDWriter import jinja2_writter
import subprocess, os, shutil

def remove(dirpath):
    shutil.rmtree(dirpath,ignore_errors=True)

def setup_systemd():
    # shutil.copy(g.template_dir + "/PiSDWriter.service", "/usr/lib/systemd/system/")
    config = { "app_execstart_command": "/usr/local/bin/pisdwriter --daemon" }
    jinja2_writter.write_config(file_name = "pisdwriter.service",
        outconf_path = "/usr/lib/systemd/system",
        template_vars = config)

    _ = subprocess.Popen([
        "systemctl", "enable", "--now", "pisdwriter"
        ],stdout=subprocess.PIPE)
    _.wait()

def remove_systemd():
    _ = subprocess.Popen([
        "systemctl", "disable", "--now", "pisdwriter"
        ],stdout=subprocess.PIPE)
    _.wait()
    os.remove("/usr/lib/systemd/system/pisdwriter.service")
