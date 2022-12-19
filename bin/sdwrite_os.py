# -*- coding: utf-8 -*-
import requests, subprocess, os
from tqdm import tqdm


def download_os_image(os_url, os_path):
    file_url = os_url
    file_size = int(requests.head(file_url).headers["content-length"])

    res = requests.get(file_url, stream=True)
    pbar = tqdm(total=file_size, unit="B", unit_scale=True)

    with open(os_path ,mode='wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            f.write(chunk)
            pbar.update(len(chunk))
        pbar.close()

def write_to_sdcard(os_path, write_device="/dev/null"):
    if os.path.isfile(os_path):
        unxz_output=subprocess.Popen([
        "unxz", os_path, "-c"
        ],stdout=subprocess.PIPE)

        dd_result=subprocess.Popen([
            "dd", "of="+write_device, "bs=4M", "conv=fsync", "status=progress"
            ],stdin=unxz_output.stdout,stdout=subprocess.PIPE)

        dd_result.wait()

if __name__ == "__main__":
    download_os_image()
