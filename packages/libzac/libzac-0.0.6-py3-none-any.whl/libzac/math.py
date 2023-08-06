import numpy as np

def i4_to_i3u1(i4):
    """unpack a int32 array, turn lower 3 bytes into a uint8 array (endianness matters)"""
    offset = 1 if i4.dtype.byteorder == ">" else 0    
    return i4.view("u1").reshape(-1,4)[:, 0+offset:3+offset].ravel()

def i3u1_to_i4(i3u1, endian="<"):
    """pack every 3 items of a uint8 array as lower 3 bytes of int32 array (endianness matters)"""
    i4 = np.zeros(i3u1.size//3, dtype="i4")
    i4.view("u1").reshape(-1,4)[:,:3] = i3u1.reshape(-1,3)[:,::-1 if endian == ">" else 1]
    return u2i(i4, 24)

def u2i(x, width, overflow_warning=True):
    y = np.copy(x)
    overflow = (y >> width).astype(bool)
    if overflow_warning and overflow.any():
        print("Overflow")
    y[x >= (1<<(width-1))] -= (1<<width)
    y[overflow] = -1
    return y.astype(f"i{y.dtype.itemsize}")

def i2u(x, width, overflow_warning=True):
    y = np.copy(x)
    upper = y >  (1<<(width-1))-1
    lower = y < -(1<<(width-1))
    if overflow_warning and (upper.any() or lower.any()):
        print("Overflow")
    y[upper] =   (1<<(width-1))-1
    y[lower] =  -(1<<(width-1))
    y[y < 0] +=  (1<<(width))
    return y.astype(f"u{y.dtype.itemsize}")
    
def byte2int(byte, dtype="<i4"):
    if isinstance(dtype, str) and dtype[-1]=='3':
        i3u1 = np.frombuffer(byte,"u1").copy()
        endianness = ">" if dtype[0]==">" else "<"
        return i3u1_to_i4(i3u1, endianness)
    else:
        return np.frombuffer(byte,dtype=dtype).copy()