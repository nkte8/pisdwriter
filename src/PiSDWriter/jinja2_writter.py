# -*- coding: utf-8 -*-
from PiSDWriter import global_vars as g
import jinja2, yaml, subprocess, os

def load_vars():
    main_config_path = g.conf_dir + '/main.yml'
    wifi_config_path = g.conf_dir + '/wifi.yml'
    config = yaml.safe_load(open(main_config_path))

    if os.path.isfile(wifi_config_path):
        wifi_config = yaml.safe_load(open(wifi_config_path))
        wifi_info = {
            "__wifi_setting_ssid": wifi_config["wifi_setting"]["ssid"],
            "__wifi_setting_psk": 
                get_wifi_passwd(
                    wifi_config["wifi_setting"]["ssid"],
                    wifi_config["wifi_setting"]["password"]),
            "use_wifi": True
        }
        config.update(wifi_info)

    return config

def get_wifi_passwd(ssid, password):
    wpa_output=subprocess.Popen([
        "wpa_passphrase", ssid, password
        ],stdout=subprocess.PIPE)

    grep_result=subprocess.Popen([
        "grep", "-e", "psk=[A-z,0-9]"
        ],stdin=wpa_output.stdout,stdout=subprocess.PIPE)

    awk_result=subprocess.Popen([
        "awk", "-F", "=", "{ print $2 }"
        ],stdin=grep_result.stdout,stdout=subprocess.PIPE)
    result = awk_result.communicate()[0].decode("utf-8")

    wpa_output.stdout.close()
    grep_result.stdout.close()
    awk_result.stdout.close()
    return result.replace("\n", " ")

def write_config(file_name):
    templates_path = g.app_dir + '/templates'
    outconf_path = g.out_dir
    os.makedirs(outconf_path, exist_ok=True)

    fileSystemLoader = jinja2.FileSystemLoader(searchpath=templates_path)
    env = jinja2.Environment(loader=fileSystemLoader)
    template = env.get_template(file_name+'.j2')

    template_vars = load_vars()

    with open(outconf_path + '/' + file_name, 'w') as file:
        file.write(template.render(template_vars))
