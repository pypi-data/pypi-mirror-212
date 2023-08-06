from pyftdi.ftdi import Ftdi
from datetime import datetime
from typing import Union
import struct

CMD_READ_STATUS = 1
CMD_WRITE_REG = 2
CMD_READ_REG = 3
CMD_WRITE_MEM = 4
CMD_READ_MEM = 5

MLD1200_VID = 0x0403
MLD1200_PID = 0x6010

# This must match setting in FPGA, or be lower
FPGA_FIFO_SIZE = 8192

MAX_NUM_TRIES = 3

# Used internally to 'fix' bug in PyFTDI where sometimes after a command we get a NULL read response
def __read_clear(ftdi_dev: object) -> None:
    num_tries = 0
    while(num_tries < MAX_NUM_TRIES):
        try:
            ftdi_dev.purge_buffers()
            ftdi_dev.read_data(1)
            break
        except:
            num_tries = num_tries + 1


def init(dev_name: str) -> object:
    """Initialize FTDI device and returns a handle to it

    Args:
        dev_name (str): Name of FTDI device, typically the serial number

    Returns:
        FTDI Device object

    """

    url = "ftdi://ftdi:2232:" + dev_name + "/1"

    ftdi_dev = Ftdi()
    ftdi_dev.open_mpsse_from_url(url)
    ftdi_dev.set_bitmode(0, Ftdi.BitMode.SYNCFF)
    # Lowering the latency timer greatly speeds up the read requests,
    # But at lower values the USB is more prone to errors
    # ftdi_dev.set_latency_timer(2)

    # Two calls (of any type) are necessary on startup
    # In theory, if we could know ahead of time if we've
    # sent USB messages to the board (thus turning on the clock
    # and fixing alignment), we could skip these calls.

    # Note: Both calls *fail* if this is the first time
    # init has been called since board power-up

    # The first call turns on the clock on the FTDI
    val = read_status(ftdi_dev, 0)
    if(val == None):
        # Second call fixes the data alignment
        read_status(ftdi_dev, 0)

    return ftdi_dev


def list_devices() -> list[str]:
    """Get a list of available MLD1200 devices connected to host

    Args: None

    Returns:
        List containing serial number of each device found that matched the MLD1200 VID and PID

        Example: `[FT2S5LOX, FT2S5QOA]`

    """
    ftdi_dev = Ftdi()
    ret = []
    num_tries = 0
    while(num_tries < MAX_NUM_TRIES):
        try:
            res = ftdi_dev.find_all([(MLD1200_VID, MLD1200_PID)])
            for r in res:
                ret.append(r[0].sn)
            break
        except:
            num_tries = num_tries + 1

    return ret

def read_status(ftdi_dev: object, address: int) -> int:
    """Low-level function to read from status register

    Args:
        ftdi_dev (object): FTDI Device
        address (int): Status register address

    Returns:
        Value contained in status register at given address

    """
    __read_clear(ftdi_dev)

    payload = struct.pack("<I", (CMD_READ_STATUS << 24) | (address & 0xFF))

    num_tries = 0
    val = None
    while(num_tries < MAX_NUM_TRIES):
        try:
            ftdi_dev.write_data(payload)
            response = ftdi_dev.read_data(4)

            if(len(response) == 4):
                val, = struct.unpack("<I", response)
                break

            num_tries = num_tries + 1
        except:
            num_tries = num_tries + 1

    return val

def read_register(ftdi_dev: object, address: int) -> int:
    """Low-level function to read from control register

    Args:
        ftdi_dev (object): FTDI Device
        address (int): Control register address

    Returns:
        Value contained in control register at given address

    """

    __read_clear(ftdi_dev)

    payload = struct.pack("<I", (CMD_READ_REG << 24) | (address & 0xFF))

    num_tries = 0
    val = None
    while(num_tries < MAX_NUM_TRIES):
        try:
            ftdi_dev.write_data(payload)
            response = ftdi_dev.read_data(4)

            if(len(response) == 4):
                val, = struct.unpack("<I", response)
                break

            num_tries = num_tries + 1
        except:
            num_tries = num_tries + 1

    return val

def write_register(ftdi_dev: object, address: int, data: int) -> None:
    """Low-level function to write to control register

    Args:
        ftdi_dev (object): FTDI Device
        address (int): Control register address
        data (int): Integer value to write to address

    """

    payload = struct.pack("<II", (CMD_WRITE_REG << 24) | (address & 0xFF), data)

    num_tries = 0
    while(num_tries < MAX_NUM_TRIES):
        try:
            ftdi_dev.write_data(payload)
            break
        except:
            num_tries = num_tries + 1


def read_memory(ftdi_dev: object, address: int, num_words: int) -> list[int]:
    """Low-level function to read from DDR memory

    Args:
        ftdi_dev (object): FTDI Device
        address (int): Address to start reading from (32-bit word accesses)
        num_words (int): Number of 32-bit words to read

    Returns:
        List of 32-bit words read from memory, starting from address given. Empty list returned on error

    """

    __read_clear(ftdi_dev)

    ret = []

    if(num_words == 0):
        num_words = 1

    tlen = num_words
    offset = 0
    while(tlen > 0):
        if tlen > FPGA_FIFO_SIZE:
            tsize = FPGA_FIFO_SIZE
        else:
            tsize = tlen

        num_bytes = tsize * 4
        payload = struct.pack("<II", (CMD_READ_MEM << 24) | ((address + offset) & 0xFFFFFF), tsize - 1)

        num_tries = 0
        while(num_tries < MAX_NUM_TRIES):
            try:
                ftdi_dev.write_data(payload)
                response = ftdi_dev.read_data(num_bytes)
                if(len(response) == num_bytes):
                    for i in range(0, num_bytes, 4):
                        val, = struct.unpack_from("<I", response, i)
                        ret.append(val)
                    break
                num_tries = num_tries + 1
            except:
                num_tries = num_tries + 1

        if(num_tries == MAX_NUM_TRIES):
            return []

        offset = offset + tsize
        tlen = tlen - tsize

    return ret

def write_memory(ftdi_dev: object, address: int, data: Union[int, list[int]]) -> None:
    """Low-level function to write to DDR memory

    Args:
        ftdi_dev (object): FTDI Device
        address (int): Address to start writing to (32-bit word accesses)
        data (int/list): Either an integer value, or a list of integers to write

    """
    if(type(data) is int):
        data = [data]
    else:
        if(type(data[0]) is not int):
            return

    tlen = len(data)
    offset = 0
    while(tlen > 0):
        if tlen > FPGA_FIFO_SIZE:
            tsize = FPGA_FIFO_SIZE
        else:
            tsize = tlen

        payload = struct.pack("<II", (CMD_WRITE_MEM << 24) | ((address + offset) & 0xFFFFFF), tsize)
        for n in range(0, tsize):
            payload = payload + struct.pack("<I", data[offset+n])

        offset = offset + tsize
        tlen = tlen - tsize

        ftdi_dev.write_data(payload)

def gather_status_registers(ftdi_dev: object) -> dict[Union[int, bool, str, float]]:
    """Gather values from all status registers and place them in a dictionary

    Args:
        ftdi_dev (object): FTDI Device

    """
    resp = {}

    try:
        val = read_status(ftdi_dev, 0)
        resp['program_load'] = bool(val & 0x80000000)
        resp['program_active'] = bool(val & 0x40000000)
        resp['program_armed'] = bool(val & 0x20000000)
        resp['program_ddr_load'] = bool(val & 0x10000000)
        resp['program_ddr_lock'] = bool(val & 0x08000000)
        resp['program_done'] = bool(val & 0x040000000)
        resp['program_error'] = bool(val & 0x02000000)
        resp['fp_status'] = int(val & 0xFF)

        val = read_status(ftdi_dev, 5)
        resp['program_run_count'] = val
        val = read_status(ftdi_dev, 6)
        resp['program_error_count'] = val
        val = read_status(ftdi_dev, 1)
        resp['trigger_active'] = bool(val & 0x80000000)
        resp['trigger_counter'] = val & 0x7FFFFFFF
        val = read_status(ftdi_dev, 3)
        resp['external_clock_freq'] = val
        val = read_status(ftdi_dev, 4)
        resp['external_clock_active'] = bool(val & 0x80000000)
        resp['external_clock_counter'] = val & 0x7FFFFFFF
        val = read_status(ftdi_dev, 2)
        resp['buildtime'] = str(datetime.fromtimestamp(val))

        val = read_status(ftdi_dev, 7)
        resp['program_run_timer'] = int(val)

        val = read_status(ftdi_dev, 8)
        resp['uptime'] = int(val)
    except:
        return {}

    return resp

def gather_control_registers(ftdi_dev: object) -> dict[Union[int, bool, str, float]]:
    """Gather values from all control registers and place them in a dictionary

    Args:
        ftdi_dev (object): FTDI Device

    """

    resp = {}
    try:
        val = read_register(ftdi_dev, 0)
        resp['program_load'] = bool(val & 0x00000001)

        val = read_register(ftdi_dev, 1)
        resp['program_numwords'] = val

        val = read_register(ftdi_dev, 2)
        resp['trigger_invert'] = bool(val & 0x40000000)
        resp['trigger_delay'] = int(val & 0x000000FF)

        val = read_register(ftdi_dev, 3)
        resp['enable_tunebox1'] = (val & 0x000000FF)
        resp['enable_tunebox2'] = (val & 0x0000FF00) >> 8
        resp['enable_tunebox3'] = (val & 0x00FF0000) >> 16
        resp['enable_tunebox4'] = (val & 0xFF000000) >> 24

        val = read_register(ftdi_dev, 4)
        resp['enable_tunebox5'] = (val & 0x000000FF)
        resp['enable_tunebox6'] = (val & 0x0000FF00) >> 8
        resp['enable_tunebox7'] = (val & 0x00FF0000) >> 16
        resp['enable_tunebox8'] = (val & 0xFF000000) >> 24

        val = read_register(ftdi_dev, 5)
        resp['enable_left_address']  = (val & 0x00000FFF)
        resp['enable_right_address'] = (val & 0x0FFF0000) >> 16
        resp['enable_frontpanel'] = ((val & 0xF0000000) >> 24) | ((val & 0x0000F000) >> 12)

        val = read_register(ftdi_dev, 6)
        resp['invert_tunebox1'] = (val & 0x000000FF)
        resp['invert_tunebox2'] = (val & 0x0000FF00) >> 8
        resp['invert_tunebox3'] = (val & 0x00FF0000) >> 16
        resp['invert_tunebox4'] = (val & 0xFF000000) >> 24

        val = read_register(ftdi_dev, 7)
        resp['invert_tunebox5'] = (val & 0x000000FF)
        resp['invert_tunebox6'] = (val & 0x0000FF00) >> 8
        resp['invert_tunebox7'] = (val & 0x00FF0000) >> 16
        resp['invert_tunebox8'] = (val & 0xFF000000) >> 24

        val = read_register(ftdi_dev, 8)
        resp['invert_left_address']  = (val & 0x00000FFF)
        resp['invert_right_address'] = (val & 0x0FFF0000) >> 16
        resp['invert_frontpanel'] = ((val & 0xF0000000) >> 24) | ((val & 0x0000F000) >> 12)
    except:
        return {}

    return resp

def write_control_registers(ftdi_dev: object, values: dict[str, int]) -> None:
    """Write an dictionary of values to control registers

    Example: write_control_registers(dev, {'trigger_invert': 1, 'trigger_delay': 3})

    Args:
        ftdi_dev (object): FTDI Device
        values (dict): A dictionary of values to write, using the key/pair

    """

    # DO NOT WRITE TO PROGRAM LOAD
    # write_register(ftdi_dev, 0, int(values['program_load']))

    # DO NOT WRITE TO PROGRAM NUMWORDS!!
    # write_register(ftdi_dev, 1, values['program_numwords'])
    value = 0
    if 'trigger_invert' in values.keys():
        value = value | ((int(values['trigger_invert'], 0) & 0x1) << 30)
    if 'trigger_delay' in values.keys():
        value = value | (int(values['trigger_delay'], 0) & 0xFF)
    if 'trigger_invert' in values.keys() or 'trigger_delay' in values.keys():
        write_register(ftdi_dev, 2, value)

    value = 0
    if 'enable_tunebox1' in values.keys():
        value = value | (int(values['enable_tunebox1'], 0) & 0xFF)
    if 'enable_tunebox2' in values.keys():
        value = value | ((int(values['enable_tunebox2'], 0) & 0xFF) << 8)
    if 'enable_tunebox3' in values.keys():
        value = value | ((int(values['enable_tunebox3'], 0) & 0xFF) << 16)
    if 'enable_tunebox4' in values.keys():
        value = value | ((int(values['enable_tunebox4'], 0) & 0xFF) << 24)
    if 'enable_tunebox1' in values.keys() or 'enable_tunebox2' in values.keys() or 'enable_tunebox3' in values.keys() or 'enable_tunebox4' in values.keys():
        write_register(ftdi_dev, 3, value)

    value = 0
    if 'enable_tunebox5' in values.keys():
        value = value | (int(values['enable_tunebox5'], 0) & 0xFF)
    if 'enable_tunebox6' in values.keys():
        value = value | ((int(values['enable_tunebox6'], 0) & 0xFF) << 8)
    if 'enable_tunebox7' in values.keys():
        value = value | ((int(values['enable_tunebox7'], 0) & 0xFF) << 16)
    if 'enable_tunebox8' in values.keys():
        value = value | ((int(values['enable_tunebox8'], 0) & 0xFF) << 24)
    if 'enable_tunebox5' in values.keys() or 'enable_tunebox6' in values.keys() or 'enable_tunebox7' in values.keys() or 'enable_tunebox8' in values.keys():
        write_register(ftdi_dev, 4, value)

    value = 0
    if 'enable_left_address' in values.keys():
        value = value | (int(values['enable_left_address'], 0) & 0x00000FFF)
    if 'enable_right_address' in values.keys():
        value = value | ((int(values['enable_right_address'], 0) & 0x00000FFF) << 16)
    if 'enable_frontpanel' in values.keys():
        value = value |  ((int(values['enable_frontpanel'], 0) & 0x0000000F) << 12) | ((int(values['enable_frontpanel'], 0) & 0x000000F0) << 24)
    if 'enable_left_address' in values.keys() or 'enable_right_address' in values.keys() or 'enable_frontpanel' in values.keys():
        write_register(ftdi_dev, 5, value)

    value = 0
    if 'invert_tunebox1' in values.keys():
        value = value | (int(values['invert_tunebox1'], 0) & 0xFF)
    if 'invert_tunebox2' in values.keys():
        value = value | ((int(values['invert_tunebox2'], 0) & 0xFF) << 8)
    if 'invert_tunebox3' in values.keys():
        value = value | ((int(values['invert_tunebox3'], 0) & 0xFF) << 16)
    if 'invert_tunebox4' in values.keys():
        value = value | ((int(values['invert_tunebox4'], 0) & 0xFF) << 24)
    if 'invert_tunebox1' in values.keys() or 'invert_tunebox2' in values.keys() or 'invert_tunebox3' in values.keys() or 'invert_tunebox4' in values.keys():
        write_register(ftdi_dev, 6, value)

    value = 0
    if 'invert_tunebox5' in values.keys():
        value = value | (int(values['invert_tunebox5'], 0) & 0xFF)
    if 'invert_tunebox6' in values.keys():
        value = value | ((int(values['invert_tunebox6'], 0) & 0xFF) << 8)
    if 'invert_tunebox7' in values.keys():
        value = value | ((int(values['invert_tunebox7'], 0) & 0xFF) << 16)
    if 'invert_tunebox8' in values.keys():
        value = value | ((int(values['invert_tunebox8'], 0) & 0xFF) << 24)
    if 'invert_tunebox5' in values.keys() or 'invert_tunebox6' in values.keys() or 'invert_tunebox7' in values.keys() or 'invert_tunebox8' in values.keys():
        write_register(ftdi_dev, 7, value)

    value = 0
    if 'invert_left_address' in values.keys():
        value = value | (int(values['invert_left_address'], 0) & 0x00000FFF)
    if 'invert_right_address' in values.keys():
        value = value | ((int(values['invert_right_address'], 0) & 0x00000FFF) << 16)
    if 'invert_frontpanel' in values.keys():
        value = value |  ((int(values['invert_frontpanel'], 0) & 0x0000000F) << 12) | ((int(values['invert_frontpanel'], 0) & 0x000000F0) << 24)
    if 'invert_left_address' in values.keys() or 'invert_right_address' in values.keys() or 'invert_frontpanel' in values.keys():
        write_register(ftdi_dev, 8, value)

