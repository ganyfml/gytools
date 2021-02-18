#!/usr/bin/python3

from time import sleep
from tqdm import tqdm

pbar = tqdm(total=5)
pbar.set_description(desc='test', refresh=True)
sleep(2)
for i in range(5):
    sleep(0.5)
    pbar.write(f'{i}')
    pbar.update(1)
