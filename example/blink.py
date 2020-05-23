if __name__ == '__main__':
    from pino.ino import Arduino, Comport, PinMode, PinState
    from pino.config import Config
    # from pino.ui.clap import PinoCli
    from time import sleep

    # com = Comport().set_baudrate(115200) \
    #     .set_port("/dev/ttyACM0") \
    #     .set_inofile("$HOME/Experimental/pino/example/proto.ino") \
    #     .deploy() \
    #     .connect(1.15)

    # loop = 10
    # interval = 0.5

    config = Config("./example/config.yml")
    # config = PinoCli().get_config()
    com = Comport() \
        .apply_settings(config.get_comport()) \
        .deploy() \
        .connect()

    arduino = Arduino(com)
    arduino.set_pinmode(13, PinMode.OUTPUT)

    variables = config.get_experimental()
    loop = variables.get("loop", 10)
    interval = variables.get("interval", 0.5)

    for _ in range(loop):
        arduino.digital_write(13, PinState.HIGH)
        sleep(interval)
        arduino.digital_write(13, PinState.LOW)
        sleep(interval)
