# -*- coding: utf-8 -*-
import requests
import json, os

line_api_url = "https://notify-api.line.me/api/notify"

def send_notification(setting_path, message):

    if os.path.isfile(setting_path):
        json_file = open(setting_path, 'r')
        json_data = json.load(json_file)

        return send_line_notification(json_data["line_notification"], message)
    else:
        print(setting_path + "not found. skip notification...")

def send_line_notification(config, message):
    headers = {
        'Authorization': 'Bearer ' + config["token"]
        }
    data = {'message': message}
    return requests.post(line_api_url, data = data, headers=headers)
