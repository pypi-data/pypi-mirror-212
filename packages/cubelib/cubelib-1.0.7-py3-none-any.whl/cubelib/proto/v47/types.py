from ...types import *
from .enums import Material
import typing

class Position(Position):

    @staticmethod
    def destroy(buff: SafeBuff) -> Tuple[int, int, int]:
        #pre1.14 version        
        b = buff.read(8)
        #print(b)
        val = unpack('!q', b)[0]        
        x, y, z = (val >> 38, val >> 26 & 0xFFF, val & 0x3FFFFFF)
        if z >= 1 << 25: z -= 1 << 26
        if y >= 1 << 11: y -= 1 << 12
        return x, y, z

    @staticmethod
    def build(val: tuple) -> bytes:
        #pre1.14 version
        return pack('!Q', ((val[0] & 0x3FFFFFF) << 38) | ((val[1] & 0xFFF) << 26) | (val[2] & 0x3FFFFFF))

class BlockID(BlockID):

    def __init__(self, Type: Material, Meta: int):
        self.Type = Type
        self.Meta = Meta
    
    def __repr__(self):
        return f"BlockID(Type={self.Type}, Meta={self.Meta})"

    @classmethod
    def destroy(cls, buff: SafeBuff):
        BlockID = VarInt.destroy(buff)
        Type = BlockID >> 4
        Meta = BlockID & 15
        return cls(Material(Type), Meta)

    def build(self) -> bytes:
        return VarInt.build(self.Type.value << 4 | (self.Meta & 15))

class Slot(Slot):
    
    @staticmethod
    def destroy(buff: SafeBuff) -> dict:
        id_ = Short.destroy(buff)
        if id_ == -1:
            return None
        
        count = Byte.destroy(buff)
        damage = Short.destroy(buff)
        data = buff.read(1)

        material = Material(id_) if id_ in Material._value2member_map_ else id_
        if data == b"\x00":
            return {"id": material, "count": count, "damage": damage}
        else:
            buff.seek(buff.tell() - 1)                
            return {"id": material, "count": count, "damage": damage, "nbt": NBT.destroy(buff)}

    @staticmethod
    def build(val: typing.Union[dict, None]) -> bytes:
        if not val:        
            return b"\xff\xff"
                
        out = Short.build(val['id'].value if isinstance(val['id'], Material) else val['id'])
        out += Byte.build(val['count'])
        out += Short.build(val['damage'])

        if 'nbt' in val:
            out += val['nbt'].build()
        else:
            out += b"\x00"
        return out

class Metadata:

    @staticmethod
    def destroy(buff: SafeBuff) -> list:
        out = []
        while 7:
            key = int.from_bytes(buff.read(1), 'big')            
            if key == 0x7f: break
            index = key & 0x1f
            type = key >> 5

            if type == 0:
                v = Byte.destroy(buff)
            elif type == 1:
                v = Short.destroy(buff)
            elif type == 2:
                v = Int.destroy(buff)
            elif type == 3:
                v = Float.destroy(buff)
            elif type == 4:
                v = String.destroy(buff)
            elif type == 5:                
                v = Slot.destroy(buff)
            elif type == 6:
                raise NotImplementedError("Reserved. Metadata: type=6 as Int, Int, Int (x, y, z)")
            elif type == 7:
                v = (Float.destroy(buff), Float.destroy(buff), Float.destroy(buff))
            
            out.append({"index": index, "type": type, "value": v})
        return out
    
    @staticmethod
    def build(data: list) -> bytes:
        out = b""
        for meta in data:
            out += UnsignedByte.build((int(meta["type"]) << 5 | int(meta["index"]) & 0x1F) & 0xFF)
            if meta["type"] == 0:
                out += Byte.build(int(meta["value"]))

            elif meta["type"] == 1:
                out += Short.build(int(meta["value"]))
            
            elif meta["type"] == 2:
                out += Int.build(int(meta["value"]))
            
            elif meta["type"] == 3:
                out += Float.build(float(meta["value"]))
            
            elif meta["type"] == 4:
                out += String.build(meta["value"])
            
            elif meta["type"] == 5:
                out += Slot.build(meta["value"])

            elif meta["type"] == 6:
                raise NotImplementedError("Reserved. Metadata: type=6 as Int, Int, Int (x, y, z)")
            
            elif meta["type"] == 7:
                out += Float.build(float(meta["value"][0]))
                out += Float.build(float(meta["value"][1]))
                out += Float.build(float(meta["value"][2]))

        return out + b"\x7f"
