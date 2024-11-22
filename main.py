import customtkinter as ctk
import sys
import turret
import flywheels
import auto

ctk.set_appearance_mode("Dark")
main_turret = turret.turret()
main_flywheels = flywheels.flywheels()
root = ctk.CTk()
root.title("PONG-IT")
root.attributes("-fullscreen", True)
root.resizable(True, True)
root.bind("<Escape>", lambda x: root.destroy())

root.rowconfigure((0), weight=1)
root.rowconfigure((1), weight=7)
root.columnconfigure((0, 1, 2), weight=1)
app_title = ctk.CTkLabel(root, text="PONG IT", font=("default", 40, "bold"))
exit_button = ctk.CTkButton(root, text="Exit", font=(
    "default", 10), command=root.destroy, width=50)

readings_frame = ctk.CTkFrame(root, corner_radius=15)
readings_title = ctk.CTkLabel(
    readings_frame, text="Readings", font=("default", 22, "bold"))
anglevar = ctk.StringVar(
    readings_frame, f"Turret angle: {main_turret.get_angle()} degrees")
angle_label = ctk.CTkLabel(
    readings_frame, textvariable=anglevar, font=("default", 15))
topvar = ctk.StringVar(readings_frame, f"Top wheel speed: 0 rpm")
top_label = ctk.CTkLabel(
    readings_frame, textvariable=topvar, font=("default", 15))
bottomvar = ctk.StringVar(readings_frame, f"Bottom wheel speed: 0 rpm")
bottom_label = ctk.CTkLabel(
    readings_frame, textvariable=bottomvar, font=("default", 15))


def update_readings():
    anglevar.set(
        f"Turret angle: {'{0:.2f}'.format(main_turret.get_angle())} degrees")
    top_speed = main_flywheels.get_top()
    bottom_speed = main_flywheels.get_bottom()
    if top_speed == 0:
        top_speed = 7.5
    if bottom_speed == 0:
        bottom_speed = 7.5
    topvar.set(
        f"Top wheel speed: {'{0:.2f}'.format((top_speed - 7.5) * 2497.33 * 0.85)} rpm")
    bottomvar.set(
        f"Bottom wheel speed: {'{0:.2f}'.format((bottom_speed - 7.5) * 2497.33 * 0.85)} rpm")
    root.after(100, update_readings)


update_readings()

still_shooting = True


def random_shooting():
    if still_shooting:
        auto.randshot(main_turret, main_flywheels)
        root.after(2000, random_shooting)


def random_shoot():
    still_shooting = True
    random_shooting()


def stop_shoot():
    still_shooting = False


auto_frame = ctk.CTkFrame(root, corner_radius=15)
auto_title = ctk.CTkLabel(
    auto_frame, text="Auto Routines", font=("default", 22, "bold"))
auto_first = ctk.CTkButton(auto_frame, text="Simple", font=(
    "default", 15), command=lambda: auto.routine1(main_turret, main_flywheels))
auto_second = ctk.CTkButton(auto_frame, text="Routine 1", font=(
    "default", 15), command=lambda: auto.routine2(main_turret, main_flywheels))
auto_third = ctk.CTkButton(auto_frame, text="Routine 2", font=(
    "default", 15), command=lambda: auto.routine3(main_turret, main_flywheels))
auto_rand = ctk.CTkButton(auto_frame, text="Random Shots", font=(
    "default", 15), command=random_shoot)
auto_stop = ctk.CTkButton(auto_frame, text="Stop Random", font=(
    "default", 15), command=stop_shoot)


def stop_manual(event):
    main_turret.stop_turning()


manual_frame = ctk.CTkFrame(root, corner_radius=15)
manual_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
manual_frame.columnconfigure((0, 1, 2, 3), weight=1)
manual_title = ctk.CTkLabel(
    manual_frame, text="Manual Control", font=("default", 22, "bold"))
left_button = ctk.CTkButton(manual_frame, text="<", font=(
    "default", 30, "bold"), command=main_turret.turn_left, width=75, height=75, corner_radius=12)
left_button.bind("<ButtonRelease-1>", stop_manual)
right_button = ctk.CTkButton(manual_frame, text=">", font=(
    "default", 30, "bold"), command=main_turret.turn_right, width=75, height=75, corner_radius=12)
right_button.bind("<ButtonRelease-1>", stop_manual)
spin_frame = ctk.CTkFrame(manual_frame)
spin_title = ctk.CTkLabel(
    spin_frame, text="Type of Spin", font=("default", 15, "bold"))
spin_type = ctk.IntVar(spin_frame)
spin_type.set(0)
spin_nospin = ctk.CTkRadioButton(
    spin_frame, text="None", variable=spin_type, value=0, font=("default", 10))
spin_topspin = ctk.CTkRadioButton(
    spin_frame, text="Topspin", variable=spin_type, value=1, font=("default", 10))
spin_backspin = ctk.CTkRadioButton(spin_frame, text="Backspin", variable=spin_type,
                                   value=-1, command=lambda: main_flywheels.set_spin(-1), font=("default", 10))

strength_frame = ctk.CTkFrame(manual_frame)
strength_title = ctk.CTkLabel(
    strength_frame, text="Stength", font=("default", 17, "bold"))
strength_amount = ctk.IntVar(strength_frame)
strength_amount.set(0)
strength_low = ctk.CTkRadioButton(
    strength_frame, text="Low", variable=strength_amount, value=0, font=("default", 10))
strength_high = ctk.CTkRadioButton(
    strength_frame, text="High", variable=strength_amount, value=1, font=("default", 10))

fire_button = ctk.CTkButton(manual_frame, text="Fire", font=("default", 20), width=90, height=40,
                            corner_radius=5, command=lambda: main_flywheels.fire(spin_type.get(), strength_amount.get()))


app_title.grid(row=0, column=1, pady=20)
exit_button.grid(row=0, column=0, sticky="nw", pady=5, padx=5)

readings_title.pack(pady=10)
angle_label.pack(pady=5)
top_label.pack(pady=5)
bottom_label.pack(pady=5)
readings_frame.grid(row=1, column=0, sticky="nesw", padx=20, pady=20)

auto_title.pack(pady=10)
auto_first.pack(pady=5)
auto_second.pack(pady=5)
auto_third.pack(pady=5)
auto_rand.pack(pady=5)
auto_stop.pack(pady=5)
auto_frame.grid(row=1, column=1, sticky="nesw", padx=10, pady=20)

manual_title.grid(row=0, column=1, columnspan=2, sticky="n", pady=10)
left_button.grid(row=1, column=1, sticky="n")
right_button.grid(row=1, column=2, sticky="n")
spin_title.pack(pady=5, padx=5)
spin_nospin.pack(pady=2)
spin_topspin.pack(pady=2)
spin_backspin.pack(pady=2)
spin_frame.grid(row=3, column=1)
strength_title.pack(pady=5, padx=5)
strength_low.pack(pady=2)
strength_high.pack(pady=2)
strength_frame.grid(row=3, column=2)
fire_button.grid(row=4, column=1, columnspan=2)
manual_frame.grid(row=1, column=2, sticky="nesw", padx=20, pady=20)


root.mainloop()
