# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm

def download_file(file_url, save_path):
    file_size = int(requests.head(file_url).headers["content-length"])

    res = requests.get(file_url, stream=True)
    pbar = tqdm(total=file_size, unit="B", unit_scale=True)

    with open(save_path ,mode='wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            f.write(chunk)
            pbar.update(len(chunk))
        pbar.close()
