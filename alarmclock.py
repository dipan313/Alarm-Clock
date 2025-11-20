import datetime
import time
from playsound import playsound
import tkinter as tk
import threading
import pygame
#making gui
root = tk.Tk()

root.title('Alarm Cloak')

entry = tk.Entry(root, font=("Arial", 20), width=10)
entry.pack(pady=10)
alarm_list = []

listbox = tk.Listbox(root, font=("Arial", 14), height=5)
listbox.pack(pady=10)

repeat_var = tk.BooleanVar()
tk.Checkbutton(root, text="Repeat Daily", variable=repeat_var, font=("Arial", 12)).pack()

label_entry = tk.Entry(root, font=("Arial", 14))
label_entry.pack(pady=5)


# Initialize mixer at the beginning
pygame.mixer.init()

# Replace threading/playsound with this
def play_sound():
    pygame.mixer.music.load("alarm.wav")
    pygame.mixer.music.play(loops=0)

def stop_sound():
    pygame.mixer.music.stop()


def set_alarm():
    value = entry.get()
    if ":" not in value:
        print("Invalid format. Please use HH:MM.")
        return

    try:
        hou, min = value.split(":")
        hou = int(hou)
        min = int(min)
        if 0 <= hou < 24 and 0 <= min < 60:
            label = label_entry.get()

            # Check for duplicates
            for alarm in alarm_list:
                if alarm[:3] == (hou, min, repeat_var.get()) and alarm[3] == label:
                    print("Alarm with same time and label already exists.")
                    return

            # Only add alarm if no duplicate found
            alarm_list.append((hou, min, repeat_var.get(), label))
            listbox.insert(tk.END, f"{hou:02d}:{min:02d} {label} {'(Repeat)' if repeat_var.get() else ''}")
            print("Alarm added:", hou, min)

        else:
            print("Hour must be 0-23 and minute must be 0-59.")
    except ValueError:
        print("Invalid numbers. Please enter in HH:MM format.")



tk.Button(root, text="Set Alarm", command=set_alarm, font=("Arial", 16)).pack(pady=5)


clock_label = tk.Label(root, text="", font=("Arial", 30), fg="green")
clock_label.pack(pady=10)

def update_clock():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    clock_label.config(text=time_str)
    root.after(1000, update_clock)

update_clock()
last_triggered = None
def check_alarms():
    global last_triggered
    now = datetime.datetime.now()
    
    # Make a copy of the list with indices
    alarms_copy = list(enumerate(alarm_list))

    for i, (hour, minute, repeat, label) in alarms_copy:
        if now.hour == hour and now.minute == minute:
            if last_triggered != (hour, minute):
                show_alarm_popup(hour, minute, i, repeat)
                last_triggered = (hour, minute)

                # # Only delete after the popup shows
                # if not repeat:
                #     if i < len(alarm_list):  # Check index is still valid
                #         alarm_list.pop(i)
                #         listbox.delete(i)

    root.after(1000, check_alarms)


def show_alarm_popup(hour, minute, index=None, repeat=False):
    popup = tk.Toplevel(root)
    popup.title("Alarm")
    tk.Label(popup, text="⏰ Alarm ringing!", font=("Arial", 18)).pack(pady=10)

    # threading.Thread(target=playsound, args=("PYTHON/alarm.wav",), daemon=True).start()
    play_sound()

    def dismiss():
        stop_sound()  # stop sound on dismiss
        popup.destroy()
        if not repeat and index is not None:
            if index < len(alarm_list):
                try:
                    alarm_list.pop(index)
                    listbox.delete(index)
                except IndexError:
                    pass
    def snooze():
        popup.destroy()
        snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        original_label = alarm_list[index][3] if index is not None and index < len(alarm_list) else "Snoozed"
        alarm_list.append((snooze_time.hour, snooze_time.minute, False, original_label + " (Snooze)"))
        listbox.insert(tk.END, f"{snooze_time.hour:02d}:{snooze_time.minute:02d} {original_label} (Snooze)")


    tk.Button(popup, text="Dismiss", command=dismiss).pack(pady=5)
    tk.Button(popup, text="Snooze", command=snooze).pack(pady=5)




def delete_alarm():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        listbox.delete(index)
        alarm_list.pop(index)
        print("Alarm deleted.")

tk.Button(root, text="Delete Alarm", command=delete_alarm, font=("Arial", 16)).pack(pady=5)

    
check_alarms()
root.mainloop()













## CLI version
# num = int(input("How many alarms do you want to store? "))
# for i in range(num):
#     target = input(f"Enter alarm #{i+1} time in HH:MM format: ")
#     hou, min = target.split(":")
#     alarm_list.append((int(hou), int(min)))

# repeat = input("Do you want the alarms to repeat daily? (y/n): ")

# stop_alarm = False

# while True:
#     curtime = datetime.datetime.now()
#     print(f"{curtime.hour:02d}:{curtime.minute:02d}")

#     for alarm_hou, alarm_min in alarm_list:
#         if curtime.hour == alarm_hou and curtime.minute == alarm_min:
#             print("🔔 Alarm ringing!")
#             playsound("PYTHON\\alarm.wav")

#             choice = input("Press 's' to snooze for 5 minutes, or any other key to dismiss: ")
#             if choice.lower() == 's':
#                 print("Snoozing for 5 minutes...")
#                 time.sleep(3)  # Testing: 3s instead of 300s
#                 playsound("PYTHON\\alarm.wav")
#             else:
#                 while datetime.datetime.now().minute == alarm_min:
#                     time.sleep(1)
#                 if repeat.lower() != 'y':
#                     stop_alarm = True
#                     break  # Exit for loop

#     if stop_alarm:
#         break  # Exit while loop

#     time.sleep(1