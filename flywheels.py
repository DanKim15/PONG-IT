import RPi.GPIO as GPIO
from time import sleep

TOP_PIN = 19
BOTTOM_PIN = 37

SERVO_IN1 = 26
SERVO_IN2 = 24
SERVO_IN3 = 22
SERVO_IN4 = 18
STEP_SLEEP = 0.001
STEP_COUNT = 1600
STEP_DIRECTION = True

STEP_SEQUENCE = [[1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 0, 1]]

MOTOR_PINS = [SERVO_IN1, SERVO_IN2, SERVO_IN3, SERVO_IN4]


top_speed = 0
bottom_speed = 0


class flywheels():
    def __init__(self):
        self.LOW_DUTY_CYCLE = 8
        self.MED_DUTY_CYCLE = 7.75
        self.HIGH_DUTY_CYCLE = 9
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TOP_PIN, GPIO.OUT)
        GPIO.setup(BOTTOM_PIN, GPIO.OUT)

        GPIO.setup(SERVO_IN1, GPIO.OUT)
        GPIO.setup(SERVO_IN2, GPIO.OUT)
        GPIO.setup(SERVO_IN3, GPIO.OUT)
        GPIO.setup(SERVO_IN4, GPIO.OUT)
        GPIO.output(SERVO_IN1, GPIO.LOW)
        GPIO.output(SERVO_IN2, GPIO.LOW)
        GPIO.output(SERVO_IN3, GPIO.LOW)
        GPIO.output(SERVO_IN4, GPIO.LOW)

        self.pwm_top = GPIO.PWM(TOP_PIN, 50)
        self.pwm_bottom = GPIO.PWM(BOTTOM_PIN, 50)
        self.top_speed = 0
        self.bottom_speed = 0
        self.pwm_top.start(0)
        self.pwm_bottom.start(0)

    def set_top(self, speed):
        self.top_speed = speed

    def set_bottom(self, speed):
        self.bottom_speed = speed

    def stop_wheels(self):
        self.pwm_top.ChangeDutyCycle(0)
        self.pwm_bottom.ChangeDutyCycle(0)
        self.top_speed = 0
        self.bottom_speed = 0

    def get_top(self):
        return self.top_speed

    def get_bottom(self):
        return self.bottom_speed

    def feed(self):
        i = 0
        motor_step_counter = 0
        for i in range(STEP_COUNT):
            for pin in range(0, len(MOTOR_PINS)):
                GPIO.output(MOTOR_PINS[pin],
                            STEP_SEQUENCE[motor_step_counter][pin])
            motor_step_counter = (motor_step_counter - 1) % 8
            sleep(STEP_SLEEP)

    def fire(self, firespin, firespeed):
        if firespin == 0:
            if firespeed == 0:
                self.set_top(self.LOW_DUTY_CYCLE)
                self.set_bottom(self.MED_DUTY_CYCLE)
            else:
                self.set_top(self.LOW_DUTY_CYCLE)
                self.set_bottom(self.LOW_DUTY_CYCLE)
        elif firespin == -1:
            if firespeed == 0:
                self.set_top(self.LOW_DUTY_CYCLE)
                self.set_bottom(self.LOW_DUTY_CYCLE)
            else:
                self.set_top(self.LOW_DUTY_CYCLE)
                self.set_bottom(self.LOW_DUTY_CYCLE)
        else:
            if firespeed == 0:
                self.set_top(self.LOW_DUTY_CYCLE)
                self.set_bottom(self.LOW_DUTY_CYCLE)
            else:
                self.set_top(self.LOW_DUTY_CYCLE)
                self.set_bottom(self.LOW_DUTY_CYCLE)

        self.pwm_top.ChangeDutyCycle(self.top_speed)
        self.pwm_bottom.ChangeDutyCycle(self.bottom_speed)
        sleep(0.05)
        self.feed()
        sleep(0.75)
        self.stop_wheels()


# test = flywheels()

# sleep(0.5)
# test.set_top(LOW_DUTY_CYCLE)
# test.set_bottom(LOW_DUTY_CYCLE)
# test.fire()
