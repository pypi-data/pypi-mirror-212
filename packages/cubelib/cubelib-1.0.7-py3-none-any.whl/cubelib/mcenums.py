from .types import MCEnum, Byte, VarInt, UnsignedByte, BitMask

class PlayerDiggingStatusEnum(MCEnum):

    IntegerType: Byte

    StartedDigging = 0
    CancelledDigging = 1
    FinishedDigging = 2
    DropItemStack = 3
    DropItem = 4
    ShootArrow_FinishEating = 5

class FaceEnum(MCEnum):

    IntegerType: Byte

    YNEG = 0
    YPOS = 1
    ZNEG = 2
    ZPOS = 3
    XNEG = 4
    XPOS = 5

    SPECIAL = -1

class EntityActionActionIDEnum(MCEnum):

    IntegerType: VarInt

    StartSneaking = 0
    StopSneaking = 1
    LeaveBed = 2
    StartSprinting = 3
    StopSprinting = 4
    JumpWithHorse = 5
    OpenRiddenHorseInventory = 6

class UseEntityTypeEnum(MCEnum):

    IntegerType: VarInt

    Interact = 0
    Attack = 1
    InteractAt = 2

class UpdateBlockEntityActionEnum(MCEnum):

    IntegerType: UnsignedByte

    Spawner = 1
    CommandBlock = 2
    Beacon = 3 
    MobHead = 4
    FlowerPot = 5
    Banner = 6

class ScoreboardObjectiveModeEnum(MCEnum):

    IntegerType: Byte

    Create = 0
    Remove = 1
    Update = 2

class UpdateScoreActionEnum(MCEnum):

    IntegerType: Byte

    Update = 0
    Remove = 1

class ChatMessagePositionEnum(MCEnum):

    IntegerType: Byte

    Chat = 0
    System = 1
    Actionbar = 2

class ChangeGameStateReasonEnum(MCEnum):

    IntegerType: UnsignedByte

    InvalidBed = 0
    EndRaining = 1
    BeginRaining = 2
    ChangeGameMode = 3 # 0: Survival, 1: Creative, 2: Adventure, 3: Spectator
    EnterCredits = 4
    DemoMessage = 5
    ArrowHittingPlayer = 6
    FadeValue = 7
    FadeTime = 8
    PlayMobAppearance = 10


class ClientSettingsChatModeEnum(MCEnum):

    IntegerType: Byte

    Enabled = 0
    CommandsOnly = 1
    Hidden = 2

class JoinGameDimensionEnum(MCEnum):

    IntegerType: Byte

    Nether = -1
    Overworld = 0
    End = 1

class ClientSettingsSkinPartsBitmaskEnum(BitMask):

    Cape = 0x01
    Jacket = 0x02
    LeftSleeve = 0x04
    RightSleeve = 0x08
    LeftPantsLeg = 0x09
    RightPantsLeg = 0x20
    Hat = 0x40

    Reserved = 0x80
