# PiSDWriter
ラズベリーパイでラズベリーパイの初期設定済みSDカードを焼くプロダクト

# インストール方法
```sh
# raspberry piにあらかじめpipをインストール
# apt install -y python-pip
pip install git+https://github.com/nkte8/pisdwriter
```

# 使用方法

プログラムが実行されている間にUSBにデータデバイスが差し込まれると、問答無用でRaspberryPiを実行できるよう、書き込みを行います。

以下はヘルプメッセージです。
```log
ubuntu@ubuntu:~$ pisdwriter
INFO: This application needs root permision for write on device.
usage: pisdwriter [-h] [-d] [-i] [--download] [--configure] [--clean]

write RaspberryPi SD easiry

options:
  -h, --help    show this help message and exit
  -d, --daemon  Start process with created data: /usr/local/lib/python3.10/dist-packages/PiSDWriter/output
  -i, --setup   Run prepair startup(download & configure)
  --download    Download os image and cloud-init.
  --configure   Configure write data from config: /usr/local/lib/python3.10/dist-packages/PiSDWriter/configs
  --clean       Cleanup downloaded images
```

# 事前設定

## 1. 設定作成

`<pythonモジュールインストール先ディレクトリ>/dist-packages/PiSDWriter/configs`内の`main.yml.template`および`wifi.yml.template`を参考に設定を作成します。  

`main.yml`（必須）
```yml
---
gateway_addr: 192.168.3.1 #デフォルトゲートウェイ
nameserver_addrs: #DNSサーバ 2台まで設定可能
  - 8.8.8.8
  - 8.8.4.4
authorized_keys: #初期設定ユーザの公開鍵を直接記載
  - ssh-XXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

`wifi.yml`（wifiでアクセスしたい場合作成・ない場合は有線設定が作成される）
```yml
---
wifi_setting:
  ssid: wifi_ssid
  password: wifi_password #平文でOK Raspberrt Piにはwpa_suppricantで難読化される。
```

## 2. コンフィグ作成

`pisdwriter -i`でOSイメージのダウンロードとtemplateの作成を実施
```log
root@ubuntu:~# pisdwriter -i
download: https://cdimage.ubuntu.com/releases/22.04.1/release/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz
100%|████████████████████████████████████████████████████████████████████████████████| 962M/962M [07:47<00:00, 2.06MB/s]
download: https://launchpadlibrarian.net/638360245/cloud-init_22.4.2.orig.tar.gz
100%|██████████████████████████████████████████████████████████████████████████████| 1.50M/1.50M [00:01<00:00, 1.07MB/s]
root@ubuntu:~# ll /usr/local/lib/python3.10/dist-packages/PiSDWriter/output/
total 16
drwxr-xr-x 2 root root 4096 12月 29 03:02 ./
drwxr-xr-x 7 root root 4096  1月  1 14:51 ../
-rw-r--r-- 1 root root 1552  1月  1 14:59 network-config
-rw-r--r-- 1 root root 1469  1月  1 14:59 user-data
```

## 3. 実行

systemdでデーモン化し、完了です。
```sh
root@ubuntu:~# cat /usr/lib/systemd/system/PiSDWriter.service
[Unit]
Description=write RaspberryPi SD easiry
After=local-fs.target

[Service]
Type=simple
ExecStart=/usr/local/bin/pisdwriter --daemon
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
root@ubuntu:~# systemctl enable --now PiSDWriter
root@ubuntu:~# systemctl status PiSDWriter
● PiSDWriter.service - write RaspberryPi SD easiry
     Loaded: loaded (/lib/systemd/system/PiSDWriter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2022-12-31 21:14:09 JST; 18h ago
   Main PID: 591 (pisdwriter)
      Tasks: 1 (limit: 366)
     Memory: 23.8M
        CPU: 1.643s
     CGroup: /system.slice/PiSDWriter.service
             └─591 /usr/bin/python3 /usr/local/bin/pisdwriter --daemon

12月 31 21:14:09 ubuntu systemd[1]: Started write RaspberryPi SD easiry.
12月 31 21:14:13 ubuntu pisdwriter[591]: monitoring device is ready.
```

# アンインストール

クリーンアップコマンドの実行、作成した設定ファイルの削除を実施し、`pip uninstall`を実施します。
```sh
pisdwriter --clean
rm /usr/local/lib/python3.10/dist-packages/PiSDWriter/configs/*.yml
pip uninstall pisdwriter
```