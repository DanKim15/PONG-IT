from time import sleep
import turret
import flywheels
import random


def routine1(m_turret, m_flywheels):
    m_turret.go_to_angle(-15)
    sleep(0.25)
    m_flywheels.fire(0, 0)
    sleep(0.7)
    m_turret.go_to_angle(15)
    sleep(0.25)
    m_flywheels.fire(0, 0)


def routine2(m_turret, m_flywheels):
    sleep(2)
    m_turret.go_to_angle(-15)
    sleep(0.25)
    m_flywheels.fire(0, 0)
    sleep(0.7)
    m_turret.go_to_angle(15)
    sleep(0.25)
    m_flywheels.fire(0, 0)
    sleep(0.7)
    m_turret.go_to_angle(0)
    sleep(0.25)
    m_flywheels.fire(0, 0)
    sleep(0.7)
    m_turret.go_to_angle(15)
    sleep(0.25)
    m_flywheels.fire(0, 0)
    sleep(0.7)
    m_turret.go_to_angle(-7)
    sleep(0.25)
    m_flywheels.fire(0, 0)
    sleep(0.7)


def routine3(m_turret, m_flywheels):
    m_turret.go_to_angle(-15)
    sleep(0.5)
    m_flywheels.fire(0, 0)
    sleep(1)
    m_turret.go_to_angle(15)
    sleep(0.5)
    m_flywheels.fire(0, 0)


def randshot(m_turret, m_flywheels):
    randangle = random.randint(-18, 16)
    m_turret.go_to_angle(randangle)
    sleep(0.5)
    m_flywheels.fire(0, 0)
    sleep(1)


# test_t = turret.turret()
# test_f = flywheels.flywheels()
# sleep(4)
# routine1(test_t, test_f)
