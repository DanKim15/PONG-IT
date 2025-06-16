# Ping Pong Ball Shooter

A 3D-printed, Raspberry Pi–controlled ping pong ball shooter with flywheel spin, magnetic-encoder aiming, and a custom Tkinter GUI. See the demonstration video on YouTube: https://youtu.be/6qED_lX59yo?si=dJPwoOmIh94nCSA-

![|Picture of Device](https://github.com/DanKim15/PONG-IT/blob/main/Picture%20of%20Device.jpg)



## Description

This project implements a self-aiming ping pong ball shooter using:

1. **Flywheel Shooter**  
   Two independent 12 V DC motors drive upper and lower flywheels via belt-and-pulley. PWM control with a feedforward sets spin direction (topspin/backspin) and speed (low/medium/high).

2. **Aiming Turret**  
   A third 12 V DC motor with planetary gearbox rotates the shooter assembly on bearing stacks. A magnetic PWM-output encoder provides angle feedback. A PID loop in `turret.py` adjusts duty cycle to hold target angles (–65° to +30°).

3. **Ball Feeder**  
   A 28BYJ-48 stepper motor drives a TPU roller to feed one ball at a time from a hopper. Controlled by the `flywheels.feed()` routine.

4. **Control Application**  
   A full-screen Python/Tkinter GUI (`main.py`) offers:
   - Manual controls for turret left/right, spin type, and strength  
   - Preprogrammed auto-routines (`auto.py`) and random-shot mode  
   - Real-time readouts of turret angle and wheel RPM  

## Links

- **YouTube Demo:** [https://youtu.be/6qED_lX59yo?si=-5KMxGFBELn92zxb]  
- **OnShape CAD Model:** https://cad.onshape.com/documents/6284113ff0cfee7787d51cfc/w/e9bffdcc590bac75b9c03533/e/c320a9cfb7af32c09532333c?renderMode=0&uiState=685062f9a8103e3bf1df482c
  
  ![|Picture of CAD](https://github.com/DanKim15/PONG-IT/blob/main/Screenshot%20of%20CAD.png)


## How It Works

- **Turret PID Control**  
  - `turret.py` reads encoder pulse width using pigpio callback, and converts to degrees.  
  - `go_to_angle(target)` loops until error ≤1.5°, computing `PID = KP·error + KI·∑error + KD·Δerror/Δt`.  
  - Maps PID output to the motor controller duty cycle (6.7–7.65%) to rotate turret.

- **Flywheel & Feeder Logic**  
  - `flywheels.py` initializes two GPIO PWMs (flywheels) plus four GPIO outputs for stepper phases.  
  - `fire(spin, speed)` sets duty cycles, spins flywheels for 50 ms, then advances feeder one ball (1 600 steps), then stops.

- **GUI & Event Loop**  
  - `main.py` builds a `customtkinter` window in fullscreen.  
  - Frames: Readings, Auto Routines, Manual Control.  
  - Uses `root.after()` for periodic sensor updates and random routine scheduling.  
  - Buttons are tied to `turret.turn_left()`, `turret.turn_right()`, `flywheels.fire()`, or `auto.routineX()`.

## Skills & Tools Used

- **Languages:** Python 3.8  
- **Libraries:** RPi.GPIO, pigpio, customtkinter, time, random  
- **Hardware:** Raspberry Pi (≥3B), 12 V DC motors + controllers, 28BYJ-48 stepper, magnetic encoder, 3D-printed PLA/ABS parts, bearings, belts  
- **Concepts:** PWM motor control, PID feedback, stepper sequencing, Tkinter GUI, 3D CAD & 3D printing  

