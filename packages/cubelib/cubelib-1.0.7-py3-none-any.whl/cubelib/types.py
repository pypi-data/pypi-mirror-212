"""
cubelib.types
=================================================================
Module that contains the minecraft protocol types implementation.
"""

from io import BytesIO
from enum import Enum
from struct import pack, unpack

from cubelib.errors import BufferExhaustedException
from cubelib.enums import state

from typing import Tuple
from uuid import UUID as UUIDD
from nbt import nbt  # NBT

class SafeBuff(BytesIO):
    """
    This class make BytesIO object safe for reading.
    It re-defines read() method and add returned bytes length comparison with requested,
    and raises BufferExhaustedException if it not equal.
    """

    def read(self, *a) -> bytes:

        if not a:
            return super().read()

        r = super().read(a[0])
        if len(r) != a[0]:
            raise BufferExhaustedException(f'Buffer returned {len(r)} instead of required {a[0]}')
        return r

    def close(self) -> None:
        """Don't close your eyes"""
        return None

class NBT(nbt.NBTFile):

    TAGS_TO_STR = {
        nbt.TAG_Short: 'short',
        nbt.TAG_Int: 'int',
        nbt.TAG_Long: 'long',
        nbt.TAG_Byte: 'byte',
        nbt.TAG_Float: 'float',
        nbt.TAG_Double: 'double',
        nbt.TAG_Byte_Array: 'bytearray',
        # TAG_Int_Array: 'bytearray',
        nbt.TAG_Compound: 'dict',
        nbt.TAG_String: 'str',
        nbt.TAG_List: 'list'
    }
    STRS_TO_TAG = {v: k for k, v in TAGS_TO_STR.items()}
    STRS_TO_STRS = {i.__name__: k for i, k in TAGS_TO_STR.items()}

    @staticmethod
    def __nbt_list_to_list(tag_list: nbt.TAG_List) -> list:
        output = []

        for tag in tag_list.tags:
            if isinstance(tag, nbt.TAG_List):
                type_ = NBT.STRS_TO_STRS[tag.tag_info().split(': [')[1][:-4].split(' ')[1]]
                value = (type_, NBT.__nbt_list_to_list(tag))

            elif isinstance(tag, nbt.TAG_Compound):
                value = NBT.__nbt_compound_to_dict(tag)

            elif isinstance(tag, nbt.TAG_String):
                value = tag.value

            else:
                value = (NBT.TAGS_TO_STR[tag.__class__], tag.value)

            output.append(value)

        #print(f"LIST->LIST {tag_list.name} -> {output}")
        return output

    @staticmethod
    def __nbt_compound_to_dict(tag_compound: nbt.TAG_Compound) -> dict:
        output = {}

        for tag in tag_compound.tags:
            if isinstance(tag, nbt.TAG_List):
                type_ = NBT.STRS_TO_STRS[tag.tag_info().split(': [')[1][:-4].split(' ')[1]]
                value = (type_, NBT.__nbt_list_to_list(tag))

            elif isinstance(tag, nbt.TAG_Compound):
                value = NBT.__nbt_compound_to_dict(tag)

            elif isinstance(tag, nbt.TAG_String):
                value = tag.value

            else:
                value = (NBT.TAGS_TO_STR[tag.__class__], tag.value)

            output[tag.name] = value

        #print(f"COMP->DICT {tag_compound.name} -> {output}")
        return output

    def to_dict(self: nbt.NBTFile) -> dict:
        return {self.name: NBT.__nbt_compound_to_dict(self)}

    @staticmethod
    def from_dict(data: dict) -> nbt.NBTFile:
        compound = list(data)[0]

        instance = NBT()
        instance.name = compound

        data = data[compound]

        for key, value in data.items():
            if isinstance(value, dict):
                instance.tags.append(NBT.__dict_to_nbt_compound(value, name=key))

            elif isinstance(value, tuple):
                if not isinstance(value[1], list):
                    vinstance = NBT.STRS_TO_TAG[value[0]](name=key)
                    vinstance.value = value[1]
                else:
                    vinstance = NBT.__list_to_nbt_list(*value, name=key)
                instance.tags.append(vinstance)

            elif isinstance(value, str):
                instance.tags.append(nbt.TAG_String(value, name=key))

        #print(f"DICT->NBTF '{compound}' -> {instance}")
        return instance

    @staticmethod
    def __dict_to_nbt_compound(data: dict, name='') -> nbt.TAG_Compound:
        instance = nbt.TAG_Compound(name=name)

        for key, value in data.items():
            if isinstance(value, dict):
                instance.tags.append(NBT.__dict_to_nbt_compound(value, name=key))

            elif isinstance(value, tuple):
                if not isinstance(value[1], list):
                    vinstance = NBT.STRS_TO_TAG[value[0]](name=key)
                    vinstance.value = value[1]
                else:
                    vinstance = NBT.__list_to_nbt_list(*value, name=key)
                instance.tags.append(vinstance)

            elif isinstance(value, str):
                instance.tags.append(nbt.TAG_String(value, name=key))

        #print(f"DICT->COMP {name} -> {instance}")
        return instance

    @staticmethod
    def __list_to_nbt_list(type_: str, data: list, name='') -> nbt.TAG_List:
        instance = nbt.TAG_List(NBT.STRS_TO_TAG[type_], name=name)

        for key in data:
            if isinstance(key, dict):
                instance.append(NBT.__dict_to_nbt_compound(key))

            elif isinstance(key, tuple):
                if not isinstance(key[1], list):
                    vinstance = NBT.STRS_TO_TAG[key[0]]()
                    vinstance.value = key[1]
                else:
                    vinstance = NBT.__list_to_nbt_list(*key)
                instance.tags.append(vinstance)

            elif isinstance(key, str):
                instance.tags.append(nbt.TAG_String(key))

            else:
                vinstance = NBT.STRS_TO_TAG[type_]()
                vinstance.value = key
                instance.tags.append(vinstance)

        #print(f"LIST->LIST {type_} -> {instance}")
        return instance

    def __eq__(self, other):
        if not isinstance(other, NBT):
            return False

        return self.to_dict() == other.to_dict()

    @staticmethod
    def destroy(buff: SafeBuff) -> nbt.NBTFile:
        return NBT(buffer=buff)

    def build(self) -> bytes:
        buff = SafeBuff()
        self.write_file(buffer=buff)
        return buff.getvalue()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:

        def unwrap_nbt_list(tag):
            out = []
            for tag in tag.tags:
                if isinstance(tag, nbt.TAG_List):
                    val = unwrap_nbt_list(tag)

                elif isinstance(tag, nbt.TAG_Compound):
                    val = unwrap_nbt_dict(tag)
                else:
                    val = tag.value

                out.append(val)

            return out

        def unwrap_nbt_dict(tag):
            out = {}

            for tag in tag.tags:
                if isinstance(tag, nbt.TAG_List):
                    val = unwrap_nbt_list(tag)

                elif isinstance(tag, nbt.TAG_Compound):
                    val = unwrap_nbt_dict(tag)

                else:
                    val = tag.value

                out[tag.name] = val

            return out
        # print(f"NBTEntry['{self.name}']({unwrap_nbt_dict(self)})")
        # print(f"NBTEntry['{self.name}']({NBT.__nbt_compound_to_dict(self)})")
        return f"NBTEntry['{self.name}']({unwrap_nbt_dict(self)})"  # not-annotated
        # return f"NBTEntry['{self.name}']({NBT.__nbt_compound_to_dict(self)})"

class Optional:
    """
    Special type, container for basic types that make them optional,
    decoder must read optional type only if other field, provided in field_name equals (or not quals if inv)
    to excepted_val.
    """

    def __init__(self, field_name, excepted_val, equals=True):

        self.field_name = field_name
        self.excepted_val = excepted_val
        self.equals = equals

    def __getitem__(self, type):

        self.type = type
        return self

    def build(self, value):

        return self.type.build(value)

    def is_legit(self, field_val):

        if self.equals:
            if isinstance(self.excepted_val, tuple):
                if field_val in self.excepted_val:
                    return True
                return False
            if field_val == self.excepted_val:
                return True
            return False
        else:
            if isinstance(self.excepted_val, tuple):
                if field_val in self.excepted_val:
                    return False
                return True
            if field_val == self.excepted_val:
                return False
            return True


class VarInt:
    """
    Most important Minecraft protocol datatype.
    Encodes integer value in range -2_147_483_648 <= val <= 2_147_483_647.
    """

    _max = 2_147_483_647
    _min = -2_147_483_648

    @staticmethod
    def cntd_destroy(buff: SafeBuff) -> Tuple[int, int]:
        """
        Returns number of bytes that occupied by the value and value
        """

        total = 0
        shift = 0
        val = 0x80
        while val & 0x80:
            val = unpack('B', buff.read(1))[0]
            total |= ((val & 0x7F) << shift)
            shift += 7
            if shift // 7 > 5:
                raise RuntimeError('VarInt is too big!')
        if total & (1 << 31):
            total = total - (1 << 32)
        return total, shift // 7

    @staticmethod
    def destroy(buff: SafeBuff) -> int:

        return VarInt.cntd_destroy(buff)[0]

    @staticmethod
    def build(val: int) -> bytes:

        if not VarInt._max >= val >= VarInt._min:
            raise ValueError(f'VarInt must be in range ({VarInt._max} >= value >= {VarInt._min})')

        total = b''
        if val < 0:
            val = (1 << 32) + val
        while val >= 0x80:
            bits = val & 0x7F
            val >>= 7
            total += pack('B', (0x80 | bits))
        bits = val & 0x7F
        total += pack('B', bits)
        return total

class MCEnum(Enum):

    """
        Most enums stored here (in types.py) and alliased from concrete packets that implements them.
        Why stored here? Idk but we need to separate it from packet for cross-version inheritance.
    """

    IntegerType: type

    @classmethod
    def destroy(class_, buff: SafeBuff):
        return class_(class_.__annotations__['IntegerType'].destroy(buff))

    def build(self) -> bytes:
        return self.__annotations__['IntegerType'].build(self.value)

    def __str__(self) -> str:
        return self.name

class FiniteLengthArray:

    def __init__(self, itype: type):
        self.ITYPE = itype

    def __getitem__(self, val):

        self.TYPE = val
        return self

    def destroy(self, buff: SafeBuff) -> list:

        count = self.ITYPE.destroy(buff)
        out = []
        for x in range(0, count):
            try:
                out.append(self.TYPE.destroy(buff))
            except BufferExhaustedException as e:
                raise RuntimeError(f"Buffer exhauseted on {x}/{count} iteration of decoding array of {self.TYPE}") from e
        return out

    def build(self, val: list) -> bytes:

        out = self.ITYPE.build(len(val))
        for i in val:
            out += self.TYPE.build(i)
        return out

class UnsignedShort:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!H', buff.read(2))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!H', val)

class NextState:

    Status = state.Status  # deprecated. removal release: 1.1.x. use cubelib.state instead!
    Login = state.Login  # deprecated. removal release: 1.1.x. use cubelib.state instead!

    @staticmethod
    def destroy(buff: SafeBuff):
        return state(int.from_bytes(buff.read(1), 'little'))

    @staticmethod
    def build(NextState: state) -> bytes:
        if NextState not in [state.Status, state.Login]:
            raise ValueError(f"NextState can be only Status or Login!")
        return bytes([NextState.value])

class Bool:

    @staticmethod
    def destroy(buff: SafeBuff) -> bool:
        return unpack('!?', buff.read(1))[0]

    @staticmethod
    def build(val: bool) -> bytes:
        return pack('!?', val)

class Byte:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!b', buff.read(1))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!b', val)

class UnsignedByte:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!B', buff.read(1))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!B', val)

class Short:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!h', buff.read(2))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!h', val)

class Int:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!i', buff.read(4))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!i', val)

class Long:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!q', buff.read(8))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!q', val)

class Float:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!f', buff.read(4))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!f', val)

class Double:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!d', buff.read(8))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!d', val)

class String:

    @staticmethod
    def build(val: str) -> bytes:

        o = b""
        i = val.encode()
        o += VarInt.build(len(i))
        o += i
        return o

    @staticmethod
    def destroy(buff: SafeBuff) -> str:

        l = VarInt.destroy(buff)
        return buff.read(l).decode()

    def __class_getitem__(class_, val):

        obj = class_()

        # Type[int] set max length\max value
        if isinstance(val, int):
            obj.max = val

        # Type[[int]] set excepted length\value
        elif isinstance(val, list) and len(val) == 1:

            obj.min = val[0]
            obj.max = val[0]

        # Type[int, int] set range of excepted values\len
        elif isinstance(val, tuple) and len(val) == 2:

            obj.min = val[0]
            obj.max = val[1]

        else:
            raise Exception('какой далбаеб писал анатацию?!?!')

        return obj

class ByteArray(bytes):

    @staticmethod
    def destroy(buff: SafeBuff):
        return ByteArray(buff.read())

    @staticmethod
    def build(val) -> bytes:
        return val

    def __str__(self) -> str:
        return f"ByteArray[{len(self)}]"

class Position:

    def destroy(buff: SafeBuff) -> Tuple[int, int, int]:
        """Ver-dependent type"""
        ...

    def build(val: tuple) -> bytes:
        """Ver-dependent type"""
        ...

class Angle:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!B', buff.read(1))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!B', val)

class FiniteLengthByteArray(ByteArray):

    @staticmethod
    def destroy(buff: SafeBuff) -> bytes:
        return buff.read(VarInt.destroy(buff))

    @staticmethod
    def build(val: bytes) -> bytes:
        out = VarInt.build(len(val))
        out += val
        return out

class UUID:

    @staticmethod
    def destroy(buff: SafeBuff) -> UUIDD:
        return UUIDD(bytes=buff.read(16))

    @staticmethod
    def build(val: UUIDD) -> bytes:
        return val.bytes


class PlayerListItemData:

    class Action(Enum):
        AddPlayer = 0
        UpdateGamemode = 1
        UpdateLatency = 2
        UpdateDisplayName = 3
        RemovePlayer = 4

    @staticmethod
    def destroy(buff: SafeBuff) -> dict:
        action = VarInt.destroy(buff)
        num_of_players = VarInt.destroy(buff)

        players = []
        for _ in range(num_of_players):
            uuid = UUID.destroy(buff)
            if action == 0:
                name = String.destroy(buff)
                properties_len = VarInt.destroy(buff)
                properties = []
                for i in range(properties_len):
                    pname = String.destroy(buff)
                    value = String.destroy(buff)
                    signed = Bool.destroy(buff)
                    signature = String.destroy(buff) if signed else None

                    property_ = {
                        "name": pname,
                        "value": value,
                        "signed": signed,
                        "signature": signature
                    }
                    properties.append(property_)

                gamemode = VarInt.destroy(buff)
                ping = VarInt.destroy(buff)
                has_display_name = Bool.destroy(buff)
                display_name = String.destroy(buff) if has_display_name else None
                players.append({
                    "uuid": uuid,
                    "name": name,
                    "properties": properties,
                    "gamemode": gamemode,
                    "ping": ping,
                    "display_name": display_name
                })

            elif action == 1:
                players.append({"uuid": uuid, "gamemode": VarInt.destroy(buff)})

            elif action == 2:
                players.append({"uuid": uuid, "ping": VarInt.destroy(buff)})

            elif action == 3:
                has_display_name = Bool.destroy(buff)
                display_name = String.destroy(buff) if has_display_name else None
                players.append({"uuid": uuid, "display_name": display_name})

            elif action == 4:
                players.append({"uuid": uuid})

        return {"action": PlayerListItemData.Action(action), "players": players}

    @staticmethod
    def build(val: dict):
        action = val["action"]
        out = VarInt.build(action.value)
        out += VarInt.build(len(val["players"]))

        for player in val["players"]:
            out += UUID.build(player["uuid"])
            if action == PlayerListItemData.Action.AddPlayer:
                out += String.build(player["name"])
                out += VarInt.build(len(player["properties"]))

                for property_ in player["properties"]:
                    out += String.build(property_["name"])
                    out += String.build(property_["value"])
                    out += Bool.build("signature" in property_)
                    if "signature" in property_:
                        out += String.build(property_["signature"])

                out += VarInt.build(player["gamemode"])
                out += VarInt.build(player["ping"])
                out += Bool.build(player["display_name"])
                if player["display_name"]:
                    out += String.build(player["display_name"])

            elif action == PlayerListItemData.Action.UpdateGamemode:
                out += VarInt.build(player["gamemode"])

            elif action == PlayerListItemData.Action.UpdateLatency:
                out += VarInt.build(player["ping"])

            elif action == PlayerListItemData.Action.UpdateDisplayName:
                out += Bool.build("display_name" in player)
                if "display_name" in player:
                    out += String.build(player["display_name"])

            elif action == PlayerListItemData.Action.RemovePlayer:
                pass

        return out

class Property:

    @staticmethod
    def destroy(buff: SafeBuff):
        key = String.destroy(buff)
        value = Double.destroy(buff)
        num_of_modifiers = VarInt.destroy(buff)
        modifiers = []
        for _ in range(num_of_modifiers):
            modifiers.append({
                "uuid": UUID.destroy(buff),
                "amount": Double.destroy(buff),
                "operation": Byte.destroy(buff)
            })
        return {"key": key, "value": value, "modifiers": modifiers}

    @staticmethod
    def build(val: dict):
        # undone
        print(val)
        return b"\x41" * 5

class BlockID:
    # ver-dependent
    ...

class Slot:
    # ver-dependent
    ...

class Metadata:
    # ver-dependent
    ...

class ChunkMeta:

    @staticmethod
    def destroy(buff: SafeBuff) -> (int, int, int):
        ChunkX = Int.destroy(buff)
        ChunkZ = Int.destroy(buff)
        PrimaryBitMask = UnsignedShort.destroy(buff)
        return ChunkX, ChunkZ, PrimaryBitMask

    @staticmethod
    def build(val: tuple) -> bytes:
        out = Int.build(val[0])
        out += Int.build(val[1])
        out = UnsignedShort.build(val[2])
        return out

class StatisticsElement:

    @staticmethod
    def destroy(buff: SafeBuff) -> dict:
        name = String.destroy(buff)
        value = VarInt.destroy(buff)
        return {"name": name, "value": value}

    @staticmethod
    def build(val: dict) -> bytes:
        out = String.build(val["name"])
        out += VarInt.build(val["value"])
        return out

class BitMask:
        
    Active: list
    
    @classmethod
    def destroy(cls, buff: SafeBuff):
        integer = UnsignedByte.destroy(buff)
        instance = cls()
        instance.Active = []

        for k, v in cls.__dict__.items():
            if not k.startswith("__"):
                if integer & v == v:
                    instance.Active.append(k)

        return instance
    
    def build(cls, val: int):
        return UnsignedByte.build(val)

    def __str__(self):        
        return f"BitMask({'|'.join(self.Active)})"
