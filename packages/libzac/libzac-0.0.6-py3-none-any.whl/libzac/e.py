import os
import re
import numpy as np
import matplotlib.pyplot as plt
from .math import byte2int
import subprocess

def eread(addr, length=1, dtype="u1", ch=0):
    raw = subprocess.run(f"e {addr}l{length}", capture_output=True, env={"ch":f"{ch}"}).stdout.decode("utf8")
    return e2int(raw, dtype=dtype)[0]

def ewrite(addr, value, ch=0):
    subprocess.run(f"e {addr} {value}", env={"ch":f"{ch}"})

def ewrite_block(addr, u1_data):
    data_length = len(u1_data)
    addr = addr if isinstance(addr, int) else int(addr,16)
    
    for i in range(0,data_length,8):
        block = u1_data[i:min(i+8,data_length)]
        data = "".join([f"{b:02x}" if isinstance(b,(int,np.integer)) else b for b in block][::-1])
        start_address = f"{addr + i:x}"
        ewrite(start_address, data)

def e2byte(input, skip_row=1):
    if os.path.isfile(input):
        with open(input,"r") as f:
            raw = f.read()
    else:
        raw = input
    raw = raw.split("\n")[skip_row:]
    data = []
    addr = []
    start_addr = int(re.search(r"[0-9a-f]+(?= : )", raw[0]).group(), 16)
    start_addr += (re.search(r" [0-9a-f]{2} ", raw[0]).span()[0] - 8)//3
    for r in raw:
        row = re.split(r"(\W*[0-9a-f]+ : )", r)
        if len(row) > 2:
            for d in row[2].split(" "):
                if (len(d)==2):
                    data.append(int(d, 16))
                    addr.append(start_addr)
                    start_addr += 1
    byte = np.asarray(data, dtype=np.uint8).tobytes()
    addr = np.asarray(addr)
    return byte, addr

def e2int(input, dtype="<i4", skip_row=1):
    byte, addr = e2byte(input, skip_row=skip_row)
    itemsize = 1
    if isinstance(dtype, str):
        itemsize = int(dtype[-1])
    else:
        itemsize = np.dtype(dtype).itemsize
    return byte2int(byte, dtype), addr[::itemsize]

def e2plt(input, dtype="<i4", skip_row=1, x_hex=True, y_int=True):
    data, addr = e2int(input, dtype=dtype, skip_row=skip_row)
    fig, ax = plt.subplots()
    ax.plot(addr,data)
    if x_hex:
        ax.get_xaxis().set_major_formatter(lambda x, pos: hex(int(x)))
    if y_int:
        ax.get_yaxis().set_major_formatter(lambda x, pos: int(x))
    fig.show()

def ewrite_block(input, skip_row=1):
    u1_data, addr = e2int(input, "u1", skip_row=skip_row)
    ewrite_block(addr[0], u1_data)

