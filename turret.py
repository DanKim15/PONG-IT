import RPi.GPIO as GPIO
import pigpio
from time import sleep

PIG = pigpio.pi()

TURRETOUT_PIN = 13
TURRETIN_PIN_GPIO = 22

KP = 0.0875
KI = 0
KD = 0

PERIOD = 0.02
ENCODER_TO_ANGLE = 360 * 44 / 79
ANGLE_TOLERANCE = 1.5
MIN_DUTY_CYCLE = 6.7
MAX_DUTY_CYCLE = 7.65
CENTER_DUTY_CYCLE = 7.2
MAX_ANGLE = 30
MIN_ANGLE = -65
ENCODER_ZERO = 109
MAX_PULSE_WIDTH = 4096

LEFT_TURNING_SPEED = 7.7
RIGHT_TURNING_SPEED = 6.5

pulse_width = 0
high_tick = None


class turret():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TURRETOUT_PIN, GPIO.OUT)
        self.pwm_out = GPIO.PWM(TURRETOUT_PIN, 50)
        self.pwm_out.start(0)

    def pwm_callback(gpio, level, tick):
        global pulse_width, high_tick

        if level == 1:
            high_tick = tick
        elif level == 0:
            if high_tick is not None:
                pulse_width = pigpio.tickDiff(high_tick, tick)
                high_tick = None

    PIG.set_mode(TURRETIN_PIN_GPIO, pigpio.INPUT)
    PIG.callback(TURRETIN_PIN_GPIO, pigpio.EITHER_EDGE, pwm_callback)

    def get_angle(self):
        return (pulse_width - 1) / (MAX_PULSE_WIDTH - 1) * 180 - ENCODER_ZERO

    def go_to_angle(self, target_angle):
        if target_angle > MAX_ANGLE:
            target_angle = MAX_ANGLE
        if target_angle < MIN_ANGLE:
            target_angle = MIN_ANGLE
        current_angle = self.get_angle()
        prev_error = 0
        error = 0
        while (not self.close_enough(current_angle, target_angle, ANGLE_TOLERANCE)):
            current_angle = self.get_angle()
            error = target_angle - current_angle
            error_sum = error * PERIOD
            if prev_error != 0:
                error_rate = (error - prev_error) / PERIOD
            else:
                error_rate = 0
            prev_error = error
            pid = (KP * error + KI * error_sum + KD *
                   error_rate) * -1 + CENTER_DUTY_CYCLE
            clamped_pid = max(min(MAX_DUTY_CYCLE, pid), MIN_DUTY_CYCLE)
            self.pwm_out.ChangeDutyCycle(clamped_pid)
            sleep(PERIOD)
        self.stop_turning()

    def turn_left(self):
        self.pwm_out.ChangeDutyCycle(LEFT_TURNING_SPEED)

    def turn_right(self):
        self.pwm_out.ChangeDutyCycle(RIGHT_TURNING_SPEED)

    def chill_angle(self):
        return self.get_angle() > MIN_ANGLE and self.get_angle() < MAX_ANGLE

    def stop_turning(self):
        self.pwm_out.ChangeDutyCycle(0)

    def close_enough(self, first, second, tolerance):
        return first >= (second - tolerance) and first <= (second + tolerance)

# test = turret()
# sleep(1)

# test.go_to_angle(0)
# sleep(0.5)
# test.go_to_angle(15)
# print("done turn 1")
# sleep(0.5)
# print(test.get_angle())
# sleep(1)
# test.go_to_angle(-40)
# print("done turn 2")
# sleep(0.5)
# print(test.get_angle())
# sleep(1)
# test.go_to_angle(15)
# print("done turn 3")
# sleep(0.5)
# print(test.get_angle())
# sleep(1)
# test.go_to_angle(0)
# print("done turn 4")
# sleep(0.5)
# print(test.get_angle())
