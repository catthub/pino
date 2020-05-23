if __name__ == '__main__':
    from pino.ino import Arduino, Comport, PinMode
    from pino.config import Config
    from time import sleep

    # com = Comport().set_baudrate(115200) \
    #     .set_port("/dev/ttyACM0") \
    #     .set_inofile("$HOME/Experimental/pino/example/proto.ino") \
    #     .deploy() \
    #     .connect(1.15)

    # loop = 10
    # interval = 0.5

    config = Config("./example/config.yml")
    com = Comport() \
        .apply_settings(config.get_comport()) \
        .deploy() \
        .connect()

    arduino = Arduino(com)
    arduino.set_pinmode(9, PinMode.SERVO)

    variables = config.get_experimental()
    loop = variables.get("loop", 10)
    interval = variables.get("interval", 0.5)

    for _ in range(loop):
        arduino.servo_rotate(9, 0)
        sleep(interval)
        arduino.servo_rotate(9, 90)
        sleep(interval)
