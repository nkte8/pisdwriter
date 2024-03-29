# PiSDWriter
ラズベリーパイでラズベリーパイの初期設定済みSDカードを焼くアプリケーションです。
現在Ubuntu 22.04 LTSの書き込みにのみ対応しています。

# インストール方法

## パッケージのインストール
```sh
# raspberry piにあらかじめpipをインストール
# apt install -y python-pip
sudo pip install git+https://github.com/nkte8/pisdwriter
```

## 事前設定

### 1. 設定作成

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
ip_address: 192.168.3.100 # 初期設定したSDカードの初回アクセス先
```

`wifi.yml`（wifiでアクセスしたい場合作成・ない場合は有線設定が作成される）
```yml
---
wifi_setting:
  ssid: wifi_ssid
  password: wifi_password #平文でOK Raspberrt Piにはwpa_suppricantで難読化される。
```

必要であればLine Notification APIを用いて通知を送信することができます。  
https://notify-bot.line.me/ja/ にてtokenを取得後、`<pythonモジュールインストール先ディレクトリ>/dist-packages/PiSDWriter/configs/settings.json`を設定。

```json
{
    "line_notification": {
        "token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }
}
```
設定作成後、以下を実行します。
```
sudo systemctl restart pisdwriter
```

### 2. セットアップ

`pisdwriter -i`でOSイメージのダウンロードとtemplateの作成・systemdへ設定します。
```log
$ sudo pisdwriter -i
download: https://cdimage.ubuntu.com/releases/22.04.1/release/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz
100%|████████████████████████████████████████████████████████████████████████████████| 962M/962M [08:36<00:00, 1.86MB/s]download: https://launchpadlibrarian.net/638360245/cloud-init_22.4.2.orig.tar.gz
100%|███████████████████████████████████████████████████████████████████████████████| 1.50M/1.50M [00:01<00:00, 994kB/s]config: network-config is ready
config: user-data is ready
Created symlink /etc/systemd/system/multi-user.target.wants/PiSDWriter.service → /lib/systemd/system/PiSDWriter.service
```

# 使用方法

プログラムが実行されている間にUSBにデータデバイスが差し込まれると、デバイスを検知してSDカードへ書き込みを行います。
ログはjournalで確認してください。

```
$ journalctl -u pisdwriter
```

settings.jsonを設定している場合は、処理開始時と終了時にnotificationを送信します。


# アンインストール

クリーンアップコマンドの実行、手動作成した設定ファイルの削除を実施し、`pip uninstall`を実施します。
```log
root@ubuntu:~# pisdwriter --clean
Removed /etc/systemd/system/multi-user.target.wants/PiSDWriter.service.
root@ubuntu:~# rm -v /usr/local/lib/python3.10/dist-packages/PiSDWriter/configs/*.yml
root@ubuntu:~# pip uninstall pisdwriter
```