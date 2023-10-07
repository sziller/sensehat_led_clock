"""
Object definition and related functions to display a customizable LED clock for RaspberryPi's SenseHat
This is open-source code, use it as is.
by Sziller @sziller.eu
"""

import time
from SenseHatLedClock import graphic_settings as gs
from SenseHatCustomExceptions import DisplayErrors as DiEr


LIVE = None
try:
    from sense_hat import SenseHat
    LIVE = True
except ImportError as e1:
    try:
        from sense_emu import SenseHat
        LIVE = False
    except ImportError as e2:
        raise DiEr.MissingDisplay()

print("===========================")
print("= using: {:^16} =".format({True: "SenseHat", False: "Emulator"}[LIVE]))
print("===========================")


class LedClock:
    """=== Class name: LedClock ========================================================================================
    Main Clock Object to display different clock styles
    on RaspberryPi's SenseHat 8x8 LED Display
    ============================================================================================== by Sziller ==="""
    def __init__(self, clock_style: int = 0, duration: int = 0, low_light: bool = True, heartbeat: int = 2,
                 numbers: dict = gs.NUMBERS_8x8,
                 perimeter: dict = gs.PERIMETER,
                 colortable: dict = gs.COLORTABLE,
                 **kwargs  # to make instantiation tolerant to undefined keyword arguments
                 ):
        self.sense = SenseHat()
        self.sense.low_light            = low_light
        self.duration: int              = duration   # seconds to display clock - 0 means forever
        self.heartbeat: int             = heartbeat  # seconds to wait between loops turns

        self.numbers                    = numbers
        self.perimeter                  = perimeter
        self.colortable                 = colortable

        self.delta_t_h = -2  # time as returned by time.time - your time
        self.delta_t_m = 0

        # 0: hour as integer in center 6x6, minutes as single dot on perimeter
        # 1: hour as integer in center 6x6, minutes as continuous line on perimeter
        # 2: minutes as integer in center 6x6, hours as 2 or 3 pixel bar on perimeter
        self.clock_style: int           = clock_style
        
        self.curr_time_string = ""

    def run(self):
        """=== Method name: run ========================================================================================
        Method actually runs instance.
        ========================================================================================== by Sziller ==="""
        time_now = time.time()
        time_at_end = time_now + self.duration
        while time_now <= time_at_end:
            if self.duration:
                time_now = time.time()  # if no duration defined, infinite loop
            cst = time.time() - 3600 * self.delta_t_h - 60 * self.delta_t_m  # Current System Time
            dst = time.gmtime(cst)  # Detailed System Time
            self.curr_time_string = time.strftime("%H:%M", dst)
            self.update()
            time.sleep(self.heartbeat)

    def update(self):
        """=== Method name: update =====================================================================================
        Method takes in an HH:MM syntax time-string and renders it using the LED matrix with a clock style.
        ========================================================================================== by Sziller ==="""
        time_as_list = self.curr_time_string.split(":")
        hour, minute = int(time_as_list[0]), int(time_as_list[1])

        bin_matrix_perim_comp = []

        if self.clock_style in [0, 1]:
            unit = 28.0 / 60  # 28 is the nr of perimeter cells
            min_unit = minute * unit + 1
            bin_matrix_hours = list_flatten(self.numbers[hour])

            for row in self.perimeter:
                bin_matrix_perim_comp.append(logical_list_entry_limit_substitute(row, min_unit, 0, 1, self.clock_style))
            bin_matrix_perim = list_flatten(bin_matrix_perim_comp)

            col_matrix_hours = logical_list_entry_substitute(bin_matrix_hours,
                                                             self.colortable['background'],
                                                             self.colortable['number'])
            col_matrix_perim = logical_list_entry_substitute(bin_matrix_perim,
                                                             self.colortable['background'],
                                                             self.colortable['perim'])
            image = logical_list_combine_adv(col_matrix_perim,
                                             col_matrix_hours,
                                             self.colortable['background'])
        elif self.clock_style == 2:
            hour_unit = hour % 12
            bin_matrix_mins = list_flatten(self.numbers[minute])

            for row in self.perimeter:
                bin_matrix_perim_comp.append(logical_list_entry_dict_substitute(row, hour_unit, 0, 1))
            bin_matrix_perim = list_flatten(bin_matrix_perim_comp)

            col_matrix_hours = logical_list_entry_substitute(bin_matrix_mins,
                                                             self.colortable['background'],
                                                             self.colortable['number'])
            col_matrix_perim = logical_list_entry_substitute(bin_matrix_perim,
                                                             self.colortable['background'],
                                                             self.colortable['perim'])
            image = logical_list_combine_adv(col_matrix_perim,
                                             col_matrix_hours,
                                             self.colortable['background'])
        else:
            print("ERROR: no image was defined")
            image = False

        if image:
            self.sense.set_pixels(image)
            
            
def logical_list_entry_limit_substitute(list_in, threshold, false, true, is_line=1):
    """=== Function name: logical_list_entry_limit_substitute ==========================================================
    converts logical lists entries into entries represented by "false" or "true"
    WARNING! 'false' and 'true' are not capitalized. These are agrumens, not boolean values!!!
    ============================================================================================== by Sziller ==="""
    if is_line:
        return [true if 0 < _ <= int(threshold) else false for _ in list_in]
    else:
        return [true if _ == int(threshold) else false for _ in list_in]


def logical_list_entry_substitute(list_in, false, true):
    """=== Function name: logical_list_entry_substitute ================================================================
    converts logical lists entries into entries represented by "false" or "true"
    WARNING! 'false' and 'true' are not capitalized. These are agrumens, not boolean values!!!
    ============================================================================================== by Sziller ==="""
    return [false if _ == 0 else true for _ in list_in]


def logical_list_entry_dict_substitute(list_in, item, false, true, dict_in: dict or None = None):
    """=== Function name: logical_list_entry_substitute ================================================================
    converts logical lists entries into entries represented by "false" or "true"
    WARNING! 'false' and 'true' are not capitalized. These are agrumens, not boolean values!!!
    ============================================================================================== by Sziller ==="""
    if dict_in is not None:
        data = dict_in
    else:
        data = {0: [28, 1], 1: [2, 3, 4], 2: [4, 5, 6], 3: [7, 8], 4: [9, 10, 11], 5: [11, 12, 13],
                6: [14, 15], 7: [16, 17, 18], 8: [18, 19, 20], 9: [21, 22], 10: [23, 24, 25], 11: [25, 26, 27]}
    return [true if _ in data[item] else false for _ in list_in]


def list_display_dundle(list_in: list, sequence_length: int):
    """=== Method name: list_display_dundle ============================================================================
    ============================================================================================== by Sziller ==="""
    counter = 0
    times = len(list_in)
    while counter < times:
        line = ""
        sec_times = sequence_length
        loc_counter = 0
        while loc_counter < sec_times:
            if counter + loc_counter < times:
                line += " " + str(list_in[counter + loc_counter])
            loc_counter += 1
        counter += loc_counter


def data_leading_zero(integer: int, digits: int):
    """=== Method name: data_leading_zero ==============================================================================
    ============================================================================================== by Sziller ==="""
    str_integer = str(int(integer))
    act_digits = len(str_integer)
    lead = ""
    for _ in range(digits - act_digits):
        lead += '0'
    return lead + str_integer


def fifo_list(list_in: list, data_in, max_length: int = 0):
    """=== Method name: fifo_list ======================================================================================
        ============================================================================================== by Sziller ==="""
    answer = list(list_in)
    if not max_length:
        max_length = len(answer)
    answer.append(data_in)
    while len(answer) > max_length:
        del answer[0]
    return answer


def list_dict_fifo_extend_w_dist(listdict: dict, dict_in: dict, max_length=10):
    """=== Method name: list_dict_fifo_extend_w_dist ===================================================================
        ============================================================================================== by Sziller ==="""
    answer = {}
    for k, v in list(listdict.items()):
        answer[k] = fifo_list(list_in=v, data_in=dict_in[k], max_length=max_length)
    return answer


def logical_list_combine(list_base, list_add):
    """=== Method name: logical_list_combine ===========================================================================
        ============================================================================================== by Sziller ==="""
    counter = 0
    total = len(list_base)
    answer = []
    while counter < total:
        list_base_i = list_base[counter]
        if list_base_i:
            answer.append(list_base_i)
        else:
            answer.append(list_add[counter])
        counter += 1
    return answer


def logical_list_combine_adv(list_base, list_add, neutral):
    """=== Method name: logical_list_combine_adv =======================================================================
    ============================================================================================== by Sziller ==="""
    counter = 0
    total = len(list_base)
    answer = []
    while counter < total:
        list_base_i = list_base[counter]
        if list_base_i and list_base_i != neutral:
            answer.append(list_base_i)
        else:
            answer.append(list_add[counter])
        counter += 1
    return answer


def list_flatten(list_in):
    """=== Method name: list_flatten ===================================================================================
    ============================================================================================== by Sziller ==="""
    answer = []
    for x in list_in:
        for y in x:
            answer.append(y)
    return answer


if __name__ == "__main__":
    clock = LedClock(clock_style=1, duration=0, low_light=False)
    clock.run()
