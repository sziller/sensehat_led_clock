from SenseHatLedClock import Class_SenseHatLedClock as SHLC

if __name__ == "__main__":
    clock = SHLC.LedClock(clock_style=0, duration=0, low_light=False)
    clock.run()
