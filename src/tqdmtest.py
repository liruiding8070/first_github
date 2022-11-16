from tqdm import tqdm
import time

with tqdm(total = 100, desc = '前缀', postfix = '后缀', mininterval = 0.3, leave = False) as pbar:
    for i in range(100):
        time.sleep(0.1)
        pbar.update(1)
