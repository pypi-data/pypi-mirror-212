import struct
from simplejson import dumps

NUM_RUN_BITS = 13  # 13-bit maximum in run-length encoding 'run' field
MAX_RUN_ALLOWED_RLE = pow(2, NUM_RUN_BITS)

def convert_derived_absolute2rle(derived_file_name: str) -> list[list[bytearray]]:
     """Convert absolute timing derived file to RLE format suitable for upload to device

     Args:
         derived_file_name(str): File to convert to RLE format

     Returns:
         A list containing each section found in derived file. Each section is given as an array of bytes

     """
     initial = []
     final = []

     with open(derived_file_name, 'r') as fp:
         for num_lines, line in enumerate(fp):
             pass
     num_sections = int((num_lines) / 21)

     for n in range(num_sections):
         initial.append([])
         final.append(bytearray())

     with open(derived_file_name, "r") as f:

         # 1 Timing, 8 Tune, 1 Address per MLD, two MLDs
         for section in range(num_sections):
             section_bitstream = bytearray()
             section_word_count = 0

             # First line is discarded
             f.readline()
             for n in range(20):
                 # 0 - Tunebox 1 Timing
                 # 1 - Tunebox 1 Value
                 # 2 - Tunebox 2 Timing
                 # 3 - Tunebox 2 Value
                 # 4 - Tunebox 3 Timing
                 # 5 - Tunebox 3 Value
                 # 6 - Tunebox 4 Timing
                 # 7 - Tunebox 4 Value
                 # 8 - Tunebox 5 Timing
                 # 9 - Tunebox 5 Value
                 # 10 - Tunebox 6 Timing
                 # 11 - Tunebox 6 Value
                 # 12 - Tunebox 7 Timing
                 # 13 - Tunebox 7 Value
                 # 14 - Tunebox 8 Timing
                 # 15 - Tunebox 8 Value
                 # 16 - Address timing
                 # 17 - Left
                 # 18 - Right
                 # 19 - Output bits?
                 initial[section].append(f.readline().strip().split())

             tunebox_timing = []
             tunebox_value = []
             for n in range(8):
                 tunebox_timing.append(initial[section][n*2][0:-8])
                 tunebox_value.append(initial[section][(n*2)+1][0:-8])

             # Convert
             for n in range(len(tunebox_timing)):
                 for entry in tunebox_timing[n]:
                     entry = int(entry)

             address_timing = initial[section][16][0:-8]
             address_left = initial[section][17][0:-8]
             address_right = initial[section][18][0:-8]
             address_front = initial[section][19][0:-8]

             # Now we will run through in time, a given tunebox or address can get 'ahead' of this, if if when we parse it,
             # it has a steady-state that extends beyond our current time, we'll catch up to it later...
             current_time = 0
             time_length = int(tunebox_timing[0][-1])
             pos_time = [0, 0, 0, 0, 0, 0]
             pos_index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

             while(current_time <= time_length):
                 for n in range(6):
                     if(n < 4):
                         pos_index1 = pos_index[(n * 2)]
                         pos_index2 = pos_index[(n * 2)+1]

                         if(pos_time[n] <= current_time):
                             # Behind, so generate RLE word

                             # TODO: Check here if we are done with this tunebox

                             time_diff1 = MAX_RUN_ALLOWED_RLE if (time_diff1 > MAX_RUN_ALLOWED_RLE) else tunebox_timing[n][pos_index1] - pos_time[n]
                             time_diff2 = MAX_RUN_ALLOWED_RLE if (time_diff2 > MAX_RUN_ALLOWED_RLE) else tunebox_timing[n][pos_index2] - pos_time[n]

                             time_diff = time_diff1 if(time_diff1 < time_diff2) else time_diff2
                             value1 = tunebox_value[n][pos_index1]
                             value2 = tunebox_value[n][pos_index2]

                             pos_and_time = ((n & 0x7) << 13) | (time_diff & 0x1FFF)
                             value = (value1 << 16) | (value2)

                             # Write word to bitstream
                             section_bitstream.extend(struct.pack(">HH", pos_and_time, value))
                             section_word_count = section_word_count + 1

                             pos_time[n] = pos_time[n] + time_diff
                             pos_index1 = pos_index1 + 1 if(pos_time[n] == tunebox_timing[n][pos_index1]) else pos_index1
                             pos_index2 = pos_index2 + 1 if(pos_time[n] == tunebox_timing[n][pos_index2]) else pos_index2

                             pos_index[(n * 2)] = pos_index1
                             pos_index[(n * 2)+1] = pos_index2


                 # There is a better way to hop, but for now use this
                 current_time = current_time + 1


     for section in range(num_sections):

         # Technically its 8 tuneboxes, 1 address, but functionally it is the same for us here
         rle = []
         tunebox = []
         for n in range(6):
             rle.append([])




     # Now we iterate thru using the 'time' in the first array position
     for time_div in range(1, len(initial[section][0])):
         time_jump = int(initial[section][0][time_div])
         # For each Tune and Address line (9 lines total)
         for n in range(6):
             if(n<4):
                 pos_value = int(initial[section][1+(n*2)][time_div])
                 pos_value2 = int(initial[section][2+(n*2)][time_div])
             elif(n==4):
                 pos_value = (int(initial[section][1+(n*2)][time_div]) & 0x0000_0FFF) | ((int(initial[section][1+(n*2)][time_div]) & 0x0F00_0000) >> 12)
                 pos_value2 = 0
             elif(n==5):
                 pos_value = ((int(initial[section][1+((n-1)*2)][time_div]) & 0x00FF_F000) >> 12) | ((int(initial[section][1+((n-1)*2)][time_div]) & 0xF000_0000) >> 16)
                 pos_value2 = 0
             else:
                 raise Exception
             # Check if the value has changed for this position
             # This means we will write out its length and old value to the file
             # Then restart the 'run' count on the new value
             # If a count is greater than MAX_RUN_ALLOWED_RLE, may have to write multiple times
             if(tunebox[n][1] == pos_value) and (tunebox[n][2] == pos_value2):
                 tunebox[n][0] = tunebox[n][0] + time_jump
             else:
                 # Value changed, dump previous value to rle array
                 rle[tunebox[n][3]] = (n, tunebox[n][0] - 1 ,tunebox[n][1], tunebox[n][2])
                 rle.append([])
                 # Update to new values
                 tunebox[n][0] = time_jump
                 tunebox[n][1] = pos_value
                 tunebox[n][2] = pos_value2
                 tunebox[n][3] = len(rle)-1
         # Check to make sure no position will starve out before this time jump is over
         # Iterate thru so in a long jump we don't fill one FIFO before starting on the next
         check_overrun = True
         while(check_overrun):
             check_overrun = False
             for n in range(6):
                 if(tunebox[n][0] > MAX_RUN_ALLOWED_RLE):
                     rle[tunebox[n][3]] = (n, MAX_RUN_ALLOWED_RLE-1, tunebox[n][1], tunebox[n][2])
                     rle.append([])
                     tunebox[n][0] = tunebox[n][0] - MAX_RUN_ALLOWED_RLE
                     tunebox[n][3] = len(rle)-1
                     check_overrun = True
         # Write any outstanding final
         for n in range(6):
             if(time_div == len(initial[section][0]) - 1):
                 rle[tunebox[n][3]] = (n, tunebox[n][0] - 1, tunebox[n][1], tunebox[n][2])

         # Dump RLE to bitstream
         final[section].extend(struct.pack(">I", len(rle)))
         for pos in rle:
             pos_and_time = ((pos[0] & 0x7) << 13) | (pos[1] & 0x1FFF)

             if(pos[0] == 4) or (pos[0] == 5):
                 value = pos[2] & 0xFFFF
             else:
                 value = (pos[2] & 0xFF) << 8 | (pos[3] & 0xFF)

             final[section].extend(struct.pack(">HH", pos_and_time, value))

         time_required = 0
         for time_div in range(len(initial[section][0])):
             time_required = time_required + int(initial[section][0][time_div])

         # print("Time required for section " + str(section) + ":" + str(time_required * 10) + "ns (" + str(time_required * 10 / 1000000) + "ms)")

     return final

def convert_derived2rle(derived_file_name: str) -> list[list[bytearray]]:
    """Convert derived file to RLE format suitable for upload to device

    Args:
        derived_file_name(str): File to convert to RLE format

    Returns:
        A list containing each section found in derived file. Each section is given as an array of bytes

    """
    initial = []
    final = []

    with open(derived_file_name, 'r') as fp:
        for num_lines, line in enumerate(fp):
            pass
    num_sections = int((num_lines) / 10)

    for n in range(num_sections):
        initial.append([])
        final.append(bytearray())

    with open(derived_file_name, "r") as f:
        # First line is discarded
        f.readline()

        # 1 Timing, 8 Tune, 1 Address per MLD, two MLDs
        for section in range(num_sections):
            for n in range(10):
                initial[section].append(f.readline().strip().split())

    for section in range(num_sections):

        # Technically its 8 tuneboxes, 1 address, but functionally it is the same for us here
        rle = []
        tunebox = []
        for n in range(6):
            rle.append([])

            # Address line is... complicated, actually 12 bit Left Address, 12 bit Right Address, 8 bit diagnostic
            if(n<4):
                init_val = int(initial[section][1+(n*2)][0])
                init_val2 = int(initial[section][2+(n*2)][0])
            elif(n==4):
                init_val = (int(initial[section][9][0]) & 0x0000_0FFF) | ((int(initial[section][9][0]) & 0x0F00_0000) >> 12)
                init_val2 = 0
            elif(n==5):
                init_val = ((int(initial[section][9][0]) & 0x00FF_F000) >> 12) | ((int(initial[section][9][0]) & 0xF000_0000) >> 16)
                init_val2 = 0

            tunebox.append([int(initial[section][0][0]), init_val, init_val2, n])

        # Check to make sure no position will starve out before this time jump is over
        # Iterate thru so in a long jump we don't fill one FIFO before starting on the next
        check_overrun = True
        while(check_overrun):
            check_overrun = False
            for n in range(6):
                if(tunebox[n][0] > MAX_RUN_ALLOWED_RLE):
                    rle[tunebox[n][3]] = (n, MAX_RUN_ALLOWED_RLE-1, tunebox[n][1], tunebox[n][2])
                    rle.append([])
                    tunebox[n][0] = tunebox[n][0] - MAX_RUN_ALLOWED_RLE
                    tunebox[n][3] = len(rle)-1
                    check_overrun = True

        # Now we iterate thru using the 'time' in the first array position
        for time_div in range(1, len(initial[section][0])):
            time_jump = int(initial[section][0][time_div])

            # For each Tune and Address line (9 lines total)
            for n in range(6):

                if(n<4):
                    pos_value = int(initial[section][1+(n*2)][time_div])
                    pos_value2 = int(initial[section][2+(n*2)][time_div])
                elif(n==4):
                    pos_value = (int(initial[section][9][time_div]) & 0x0000_0FFF) | ((int(initial[section][9][time_div]) & 0x0F00_0000) >> 12)
                    pos_value2 = 0
                elif(n==5):
                    pos_value = ((int(initial[section][9][time_div]) & 0x00FF_F000) >> 12) | ((int(initial[section][9][time_div]) & 0xF000_0000) >> 16)
                    pos_value2 = 0

                # Check if the value has changed for this position
                # This means we will write out its length and old value to the file
                # Then restart the 'run' count on the new value
                # If a count is greater than MAX_RUN_ALLOWED_RLE, may have to write multiple times
                if(tunebox[n][1] == pos_value) and (tunebox[n][2] == pos_value2):
                    tunebox[n][0] = tunebox[n][0] + time_jump

                    if(tunebox[n][0] > MAX_RUN_ALLOWED_RLE):
                        rle[tunebox[n][3]] = (n, MAX_RUN_ALLOWED_RLE-1, tunebox[n][1], tunebox[n][2])
                        rle.append([])
                        tunebox[n][0] = tunebox[n][0] - MAX_RUN_ALLOWED_RLE
                        tunebox[n][3] = len(rle)-1
                else:
                    # Value changed, dump previous value to rle array
                    rle[tunebox[n][3]] = (n, tunebox[n][0] - 1 ,tunebox[n][1], tunebox[n][2])
                    rle.append([])

                    # Update to new values
                    tunebox[n][0] = time_jump
                    tunebox[n][1] = pos_value
                    tunebox[n][2] = pos_value2
                    tunebox[n][3] = len(rle)-1

            # Check to make sure no position will starve out before this time jump is over
            # Iterate thru so in a long jump we don't fill one FIFO before starting on the next
            check_overrun = True
            while(check_overrun):
                check_overrun = False
                for n in range(6):
                    if(tunebox[n][0] > MAX_RUN_ALLOWED_RLE):
                        rle[tunebox[n][3]] = (n, MAX_RUN_ALLOWED_RLE-1, tunebox[n][1], tunebox[n][2])
                        rle.append([])
                        tunebox[n][0] = tunebox[n][0] - MAX_RUN_ALLOWED_RLE
                        tunebox[n][3] = len(rle)-1
                        check_overrun = True

        # Write any outstanding final
        for n in range(6):
            # if(time_div == len(initial[section][0]) - 1):
            if(tunebox[n][0] > 0):
                rle[tunebox[n][3]] = (n, tunebox[n][0] - 1, tunebox[n][1], tunebox[n][2])

        # pprint.pprint(rle)
        # Generate bitstream for each section
        final[section].extend(struct.pack(">I", len(rle)))
        for pos in rle:
            pos_and_time = ((pos[0] & 0x7) << 13) | (pos[1] & 0x1FFF)

            if(pos[0] == 4) or (pos[0] == 5):
                value = pos[2] & 0xFFFF
            else:
                value = (pos[3] & 0xFF) << 8 | (pos[2] & 0xFF)

            final[section].extend(struct.pack(">HH", pos_and_time, value))

        time_required = 0
        for time_div in range(len(initial[section][0])):
            time_required = time_required + int(initial[section][0][time_div])

        # print("Time required for section " + str(section) + ":" + str(time_required * 10) + "ns (" + str(time_required * 10 / 1000000) + "ms)")

        # byte_count = 0
        # num_entries = len(rle)
        # byte_count = len(rle) * 4

        # print("Total entries: " + str(num_entries))
        # print(str(byte_count) + " bytes required (" + str(byte_count*8) + " bits)")
        # print()

    return final



def convert_rle2raw(rle_file_name: str) -> list[list[int]]:
    """Convert RLE file to raw format. Typical use for allowing comparisons between different formats

    Args:
        rle_file_name(str): File to convert to 'raw' format

    Returns:
        List containing each section, inside of which is an array of the 8 tuneboxes, and the address (Left + Right + Front Panel)

    """

    byte_offset = 0
    section = 0
    final = []
    with open(rle_file_name, "rb") as f:

        data = f.read()
        while(byte_offset < len(data)):
            final.append([])
            for n in range(10):
                final[section].append([])

            entries = struct.unpack_from(">I", data, byte_offset)[0]

            for n in range(entries):
                pos_time, value = struct.unpack_from(">HH", data, byte_offset + 4 + (n*4))
                pos = pos_time >> 13
                time = pos_time & 0x1FFF
                for t in range(time+1):
                    try:
                        if pos == 4:
                            final[section][8].append(value)
                        elif pos == 5:
                            final[section][9].append(value)
                        else:
                            final[section][(pos*2)].append(value & 0xFF)
                            final[section][(pos*2)+1].append(value >> 8)
                    except Exception as e:
                        print(e)

            byte_offset = byte_offset + 4 + (entries * 4)

            #for n in range(len(final[section])):
            #    print("Total entries in section " + str(section) + ": " + str(n) + ": " + str(len(final[section][n])))
            #    val = 0
            #    for i in range(len(final[section][n])):
            #        val = val + final[section][n][i]
            #    print("Sum per line: " + str(val))

            #print()
            section = section + 1

    return final

def convert_derived2raw(derived_file_name: str) -> list[list[int]]:
    """Convert derived file to raw format. Typical use for allowing comparisons between different formats

    Args:
        derived_file_name(str): File to convert to 'raw' format

    Returns:
        List containing each section, inside of which is an array of the 8 tuneboxes, and the address (Left + Right + Front Panel)

    """
    initial = []
    final = []

    with open(derived_file_name, 'r') as fp:
        for num_lines, line in enumerate(fp):
            pass
    num_sections = int((num_lines) / 10)

    with open(derived_file_name, "r") as f:
        # First line is discarded
        f.readline()

        # 8 Tune, 1 Address per MLD, two MLDs
        for section in range(num_sections):
            initial.append([])
            final.append([])
            for n in range(10):
                initial[section].append(f.readline().split())

            for n in range(10):
                final[section].append([])

    for section in range(num_sections):
        # print("Estimated binary size: " + str(len(initial[section][0]) * 96) + " bits per section")
        # Now we iterate thru using the 'time' in the first array position
        for time_div in range(len(initial[section][0])):
            time_jump = int(initial[section][0][time_div])

            # For each Tune and Address line (9 lines total)
            for n in range(9):
                pos_value = int(initial[section][n+1][time_div])
                if(n == 8):
                    value =  ((pos_value & 0x0F000000) >> 12) |  (pos_value & 0x00000FFF)
                    value2 = ((pos_value & 0xF0000000) >> 16) | ((pos_value & 0x00FFF000) >> 12)
                    for j in range(time_jump):
                        final[section][n].append(value)
                        final[section][n+1].append(value2)
                else:
                    value = pos_value & 0xFF
                    for j in range(time_jump):
                        final[section][n].append(value)


        #for n in range(len(final[section])):
        #    print("Total entries in section " + str(section) + ": " + str(n) + ": " + str(len(final[section][n])))
        #    val = 0
        #    for i in range(len(final[section][n])):
        #        val = val + final[section][n][i]
        #    print("Sum per line: " + str(val))

        #print()

    return final

def load_rle_from_file(rle_file_name: str) -> list[list[int]]:
    """Load an RLE file from disk into memory. Each section is loaded as an array of 32-bit integer values

    Args:
        rle_file_name(str): Path to RLE file to load

    Returns:
        List of sections, each containing an array of integer values

    """
    final = []
    section = 0
    with open(rle_file_name, "rb") as f:
        chunk = f.read(4)
        while(chunk):
            final.append([])
            section_numwords, = struct.unpack(">I", chunk)
            for n in range(section_numwords):
                section_data, = struct.unpack(">I", f.read(4))
                final[section].append(section_data)

            section = section + 1
            chunk = f.read(4)

    return final

def match(derived_file: str, rle_file: str) -> bool:
    """Checks if a derived file and and RLE file match output when converted to the same 'raw' format

    Args:
        derived_file(str): Path to derived file

        rle_file(str): Path to RLE file

    Returns:
        True if matched, False otherwise


    """

    derived_binary = convert_derived2raw(derived_file)
    bin_json = dumps(derived_binary)

    rle_binary = convert_rle2raw(rle_file)
    rle_json = dumps(rle_binary)

    return True if rle_json == bin_json else False

# import csv
# import pprint

# def convert_sum_to_obj(sum_file):
#     sum_obj = {}
#     sum_obj['data'] = []
#     with(open(sum_file, "rt")) as f:
#         reader = csv.reader(f)
#         for n, row in enumerate(reader):
#             if(n == 0):
#                 sum_obj['ventry'] = float(row[1]) # VEntry m/s
#                 sum_obj['vbender'] = float(row[3]) # VBender m/s
#                 sum_obj['vexit'] = float(row[5]) # Vexit m/s
#                 sum_obj['stage1_count'] = int(row[7]) # Stage 1 Traps
#                 sum_obj['stage2_count'] = int(row[9]) # Stage 2 Traps
#
#             if(n == 1):
#                 sum_obj['nozzle_pulse_width'] = float(row[2])
#                 sum_obj['nozzle_to_tw'] = float(row[4])
#
#             if(n == 2):
#                 sum_obj['ion_discharge_start'] = float(row[2])
#
#                 i = 4
#                 sum_obj['ion_on_off'] = []
#                 for i in range(4, len(row)):
#                     sum_obj['ion_on_off'].append(float(row[i]))
#
#             if(n == 3):
#                 sum_obj['bender_to_nozzle'] = float(row[2])
#                 sum_obj['bender_pulse_width'] = float(row[4])
#
#             if(n == 4):
#                 sum_obj['first_trap_to_nozzle'] = float(row[2])
#                 sum_obj['first_trap_pulse_width'] = float(row[4])
#
#             if(n == 5):
#                 sum_obj['rear_trap_to_nozzle'] = float(row[2])
#                 sum_obj['rear_trap_pulse_width'] = float(row[4])
#
#             # Row 6 is name values
#             if(n > 6):
#                 data_row = {}
#                 data_row['trap_num'] = int(row[0])
#                 data_row['cap_val'] = int(row[1])
#                 data_row['added_val'] = int(row[2])
#                 data_row['pulse_width'] = float(row[3])
#                 data_row['discharge_instant'] = float(row[4])
#                 data_row['enable'] = bool(row[5])
#                 data_row['botsw_on'] = float(row[6])
#                 data_row['botsw_off'] = float(row[7])
#                 data_row['charge_on_off'] = []
#                 for i in range(8, len(row)-1, 2):
#                     data_row['charge_on_off'].append([float(row[i]),float(row[i+1])])
#                 sum_obj['data'].append(data_row)
#
#     pprint.pprint(sum_obj, width=320)
#     return sum_obj
