class BufferExhaustedException(Exception):
    """
        Raised when buffer read() returned less than need
        RATE on L1: Placebo (automatic skipping and waiting for further bytes)
        RATE on L2: Normal (raised in packets and prevents further analyzing)
    """
    pass

class BadPacketException(Exception):
    """
        Raised when bad packet passed to one of read() functions
        RATE: Fatal
        DESC: After broken L1 packet we losing ability to analyze byte stream
        and cannot find next packets' begin.
    """
    pass

class DecoderException(Exception):
    """
        Raised when error occured in Night.destroy (Decoder)
        RATE: Normal
        DESC: After broken L2 packet commonly we can proceed with further packets analyzing
        but if it was vital for protocol state changing it may prevent further 
        comminications
    """
    pass
