"""
Example and testcall to instantiate and run LEDClock included in this module
by Sziller @sziller.eu
"""
from SenseHatLedClock import Class_SenseHatLedClock as SHLC

if __name__ == "__main__":
    clock = SHLC.LedClock(clock_style=2, duration=0, low_light=False)
    clock.run()
