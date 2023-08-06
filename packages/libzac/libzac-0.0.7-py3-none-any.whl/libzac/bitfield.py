import numpy as np
from .e import eread, ewrite

########## used for debug without actually read/wrtie memory #############
eread = lambda addr,length: np.random.randint(0,255,length,dtype="u1")
ewrite = lambda addr,value: None
##########################################################################

class bitfield():
    _fields_ = {}
    addr = ""
    __ENDIANESS = 'little'
    def __init__(self, data:int=0):
        self._data = data
        shift = 0
        for field,bit in self._fields_.items():
            mask = ((1<<bit)-1) << shift
            def getter(self, mask=mask, shift=shift): # `mask=mask` will remember current value of mask
                return (self.data & mask) >> shift
            def setter(self, value, mask=mask, shift=shift):
                self._data = ((value << shift) & mask) | (self.data & ~mask)
            setattr(type(self),field,property(getter, setter))
            shift += bit

    def __str__(self): # print(bitfield) will print all info about it
        s = f"{self.__class__.__name__} @ {self.addr} = {self.hex}\n"
        start = 0
        for field,bit in self._fields_.items():
            width = f"[{start+bit-1:2d}:{start:2d}]" if bit > 1 else f"[{start}]"
            s += f"  {field}{width} = {hex(getattr(self,field))}\n"
            start += bit
        return s
    
    @property
    def data(self):
        return self._data
    @property
    def hex(self):
        return hex(self.data)[2:]
    @property
    def bytes(self):
        return self.data.to_bytes(self.size, self.__ENDIANESS)   
    @classmethod
    @property
    def size(cls):
        return (sum(cls._fields_.values())-1)//8 + 1
    @classmethod
    def get(cls, field): 
        """get a signle bit field"""
        bf = cls()
        bf.read()
        return getattr(bf, field)
    @classmethod
    def set(cls, field, value):
        """set a single bit field while keep others untouched"""
        bf = cls()
        bf.read()
        setattr(bf, field, value)
        bf.write()
    @classmethod
    def from_bytes(cls, byte:bytes):
        return cls(int.from_bytes(byte, cls.__ENDIANESS))
    @classmethod
    def from_np(cls, np_array:np.ndarray):
        return cls.from_bytes(np_array.tobytes())

    def to_np(self, dtype:np.dtype="u1"):
        return np.frombuffer(self.bytes, dtype=dtype)

    def read(self):
        r = eread(self.addr, self.size) # read `self.size` bytes from memory at address `self.addr`
        print(f"read {r} @ {self.addr}")
        self._data = int.from_bytes(r.tobytes(), self.__ENDIANESS)

    def write(self):
        print(f"write {self.hex} @ {self.addr}")
        ewrite(self.addr, self.hex) # write `self.size` bytes to memory at address `self.addr`

if __name__ == "__main__":
    # following C bitfield struct `Example` has total 24 bits, which is 3 bytes
    # GCC's `__attribute__((packed))` minimize memory usage, no padding between members
    # ```c
    # typedef struct
    # {
    # 	volatile unsigned short A	    :8;
    # 	volatile unsigned short B	    :14;
    # 	volatile unsigned short C	    :2;
    # }__attribute__((packed)) Example;
    # sizeof(Example) == 3
    # ```

    # but ctypes.Structure with `_pack_=1` works like `#pragma pack(1)` in MSVC, 
    # align member at 1 byte boundary. not same as GCC's `__attribute__((packed))`
    from ctypes import Structure, sizeof, c_ubyte, c_uint16
    class Example_ctypes(Structure):
        addr = '8000'
        _pack_ = 1
        _fields_ = [
            ("A", c_uint16, 8),
            ("B", c_uint16, 14),
            ("C", c_uint16, 2),
        ]
    e = Example_ctypes()
    e.A = 0x00
    e.B = 0x3fff # set all 14 bit to 1
    e.C = 0x3
    print(bin(int.from_bytes(bytes(e),'little'))) 
    # >>> 0b11001111111111111100000000 
    #       CCPPBBBBBBBBBBBBBBAAAAAAAA  note 2 zero bit padded between B and C
    print(sizeof(Example_ctypes)) # >>> 4, because of padding/alignment

    # class `bitfield` mimic GCC's `__attribute__((packed))` behavior, no padding between members
    # it use bit-wise mask/shift to manipulate bitfield, does not rely on any memory layout 
    class Example_bitfield(bitfield):
        addr = '8000' # address of reading/writing via memory
        _fields_ = {
            "A" : 8,
            "B" : 14,
            "C" : 2,
        }
    x = Example_bitfield()
    x.A = 0x00
    x.B = 0x3fff # set all 14 bit to 1
    x.C = 0x3
    print(bin(int.from_bytes(x.bytes,'little'))) 
    # >>> 0b111111111111111100000000 
    #       CCBBBBBBBBBBBBBBAAAAAAAA  note B is NOT padded, still 14 bit
    print(x.size) # >>> 3, bitfield.size is calculated by sum all bitfield in cls._fields_