import datetime
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pygame

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title('Alarm Clock')
        self.root.geometry('500x700')
        self.root.minsize(400, 600)
        
        # Configure colors
        self.bg_color = '#f5f5f5'
        self.card_color = '#ffffff'
        self.primary_color = '#218085'
        self.text_color = '#1f2121'
        self.secondary_text = '#626c71'
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Alarm data
        self.alarm_list = []
        self.last_triggered = {}  # Changed from None to dict to track multiple alarms
        
        # Build UI
        self.create_widgets()
        
        # Start clock and alarm checker
        self.update_clock()
        self.check_alarms()
    
    def create_widgets(self):
        # Main container with padding - now expands with window
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ===== CLOCK DISPLAY =====
        clock_frame = tk.Frame(main_frame, bg=self.card_color, relief='solid', bd=1)
        clock_frame.pack(fill='x', pady=(0, 20))
        
        self.clock_label = tk.Label(
            clock_frame,
            text="00:00:00",
            font=("Arial", 48, "bold"),
            fg=self.primary_color,
            bg=self.card_color
        )
        self.clock_label.pack(pady=20)
        
        self.date_label = tk.Label(
            clock_frame,
            text="",
            font=("Arial", 12),
            fg=self.secondary_text,
            bg=self.card_color
        )
        self.date_label.pack(pady=(0, 20))
        
        # ===== SET ALARM SECTION =====
        alarm_card = tk.Frame(main_frame, bg=self.card_color, relief='solid', bd=1)
        alarm_card.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            alarm_card,
            text="Set New Alarm",
            font=("Arial", 16, "bold"),
            fg=self.text_color,
            bg=self.card_color,
            anchor='w'
        )
        title_label.pack(fill='x', padx=20, pady=(20, 15))
        
        # Time input
        time_frame = tk.Frame(alarm_card, bg=self.card_color)
        time_frame.pack(fill='x', padx=20, pady=(0, 12))
        
        tk.Label(
            time_frame,
            text="Alarm Time (HH:MM)",
            font=("Arial", 11, "bold"),
            fg=self.text_color,
            bg=self.card_color,
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.time_entry = tk.Entry(
            time_frame,
            font=("Arial", 14),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color
        )
        self.time_entry.pack(fill='x', ipady=8)
        self.time_entry.insert(0, "07:00")
        
        # Label input
        label_frame = tk.Frame(alarm_card, bg=self.card_color)
        label_frame.pack(fill='x', padx=20, pady=(0, 12))
        
        tk.Label(
            label_frame,
            text="Label (Optional)",
            font=("Arial", 11, "bold"),
            fg=self.text_color,
            bg=self.card_color,
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.label_entry = tk.Entry(
            label_frame,
            font=("Arial", 14),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color
        )
        self.label_entry.pack(fill='x', ipady=8)
        self.label_entry.insert(0, "Wake Up")
        
        # Repeat checkbox
        self.repeat_var = tk.BooleanVar()
        repeat_check = tk.Checkbutton(
            alarm_card,
            text="Repeat Daily",
            variable=self.repeat_var,
            font=("Arial", 11),
            fg=self.text_color,
            bg=self.card_color,
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground=self.text_color,
            cursor="hand2"
        )
        repeat_check.pack(anchor='w', padx=20, pady=(0, 15))
        
        # Add alarm button
        add_btn = tk.Button(
            alarm_card,
            text="Add Alarm",
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg='white',
            relief='flat',
            cursor="hand2",
            command=self.set_alarm
        )
        add_btn.pack(fill='x', padx=20, pady=(0, 20), ipady=10)

    
    def show_empty_state(self):
        """Display empty state when no alarms"""
        for widget in self.alarm_frame.winfo_children():
            widget.destroy()
        
        empty_label = tk.Label(
            self.alarm_frame,
            text="⏰\n\nNo alarms set yet.\nAdd one above!",
            font=("Arial", 12),
            fg=self.secondary_text,
            bg=self.card_color,
            justify='center'
        )
        empty_label.pack(pady=40)
    
    def update_clock(self):
        """Update the current time display"""
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        
        self.clock_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        self.root.after(1000, self.update_clock)
    
    def set_alarm(self):
        """Add a new alarm to the list"""
        value = self.time_entry.get().strip()
        label = self.label_entry.get().strip() or "Alarm"
        
        if ":" not in value:
            messagebox.showerror("Invalid Format", "Please use HH:MM format (e.g., 07:30)")
            return
        
        try:
            hour, minute = value.split(":")
            hour = int(hour)
            minute = int(minute)
            
            if not (0 <= hour < 24 and 0 <= minute < 60):
                messagebox.showerror("Invalid Time", "Hour must be 0-23 and minute must be 0-59")
                return
            
            repeat = self.repeat_var.get()
            
            # Check for duplicates
            for alarm in self.alarm_list:
                if alarm[:3] == (hour, minute, repeat) and alarm[3] == label:
                    messagebox.showwarning("Duplicate Alarm", 
                        "An alarm with the same time and label already exists.")
                    return
            
            # Add alarm with unique ID
            alarm_id = f"{hour}:{minute}:{label}:{repeat}"
            self.alarm_list.append((hour, minute, repeat, label, alarm_id))
            self.render_alarms()
            
            # Show success message
            messagebox.showinfo("Success", f"Alarm set for {hour:02d}:{minute:02d}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in HH:MM format")
    
    def render_alarms(self):
        """Render all alarms in the list"""
        # Clear existing alarms
        for widget in self.alarm_frame.winfo_children():
            widget.destroy()
        
        if not self.alarm_list:
            self.show_empty_state()
            return
        
        # Create alarm items
        for idx, alarm_data in enumerate(self.alarm_list):
            hour, minute, repeat, label = alarm_data[:4]
            
            item_frame = tk.Frame(
                self.alarm_frame,
                bg='#f8f9fa',
                relief='solid',
                bd=1
            )
            item_frame.pack(fill='x', pady=(0, 8))
            
            # Left side - alarm info
            info_frame = tk.Frame(item_frame, bg='#f8f9fa')
            info_frame.pack(side='left', fill='both', expand=True, padx=15, pady=12)
            
            # Time
            time_label = tk.Label(
                info_frame,
                text=f"{hour:02d}:{minute:02d}",
                font=("Arial", 18, "bold"),
                fg=self.text_color,
                bg='#f8f9fa'
            )
            time_label.pack(anchor='w')
            
            # Label and badge
            label_frame = tk.Frame(info_frame, bg='#f8f9fa')
            label_frame.pack(anchor='w', fill='x')
            
            label_text = tk.Label(
                label_frame,
                text=label,
                font=("Arial", 11),
                fg=self.secondary_text,
                bg='#f8f9fa'
            )
            label_text.pack(side='left')
            
            if repeat:
                badge = tk.Label(
                    label_frame,
                    text="Daily",
                    font=("Arial", 9, "bold"),
                    fg=self.primary_color,
                    bg='#e6f5f5',
                    padx=6,
                    pady=2
                )
                badge.pack(side='left', padx=(8, 0))
            
            # Right side - delete button
            delete_btn = tk.Button(
                item_frame,
                text="✕",
                font=("Arial", 14, "bold"),
                fg='white',
                bg='#c0152f',
                relief='flat',
                cursor="hand2",
                width=3,
                command=lambda i=idx: self.delete_alarm(i)
            )
            delete_btn.pack(side='right', padx=12, pady=12)
    
    def delete_alarm(self, index):
        """Delete an alarm from the list"""
        if 0 <= index < len(self.alarm_list):
            # Remove from last_triggered if present
            alarm_data = self.alarm_list[index]
            alarm_id = alarm_data[4] if len(alarm_data) > 4 else None
            if alarm_id and alarm_id in self.last_triggered:
                del self.last_triggered[alarm_id]
            
            self.alarm_list.pop(index)
            self.render_alarms()
    
    def check_alarms(self):
        """Check if any alarm should trigger - FIXED VERSION"""
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        current_second = now.second
        
        # Create a copy to avoid modification during iteration
        alarms_to_check = list(self.alarm_list)
        
        for idx, alarm_data in enumerate(alarms_to_check):
            hour, minute, repeat, label = alarm_data[:4]
            alarm_id = alarm_data[4] if len(alarm_data) > 4 else f"{hour}:{minute}:{label}"
            
            # Check if alarm time matches current time
            if current_hour == hour and current_minute == minute:
                # Only trigger if not already triggered this minute
                if alarm_id not in self.last_triggered:
                    print(f"Alarm triggered: {hour:02d}:{minute:02d} - {label}")
                    self.last_triggered[alarm_id] = True
                    self.show_alarm_popup(hour, minute, idx, repeat, label)
        
        # Clear last_triggered at the start of each new minute (when seconds = 0)
        if current_second == 0:
            self.last_triggered.clear()
        
        # Schedule next check
        self.root.after(1000, self.check_alarms)
    
    def show_alarm_popup(self, hour, minute, index, repeat, label):
        """Show alarm notification popup"""
        popup = tk.Toplevel(self.root)
        popup.title("Alarm!")
        popup.geometry('350x250')
        popup.resizable(False, False)
        popup.configure(bg='white')
        
        # Center the popup on screen
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (350 // 2)
        y = (popup.winfo_screenheight() // 2) - (250 // 2)
        popup.geometry(f'350x250+{x}+{y}')
        
        # Make popup stay on top
        popup.attributes('-topmost', True)
        popup.transient(self.root)
        popup.grab_set()
        
        # Play sound
        self.play_sound()
        
        # Content
        icon_label = tk.Label(
            popup,
            text="⏰",
            font=("Arial", 48),
            bg='white'
        )
        icon_label.pack(pady=(30, 10))
        
        title_label = tk.Label(
            popup,
            text="Alarm Ringing!",
            font=("Arial", 18, "bold"),
            fg=self.text_color,
            bg='white'
        )
        title_label.pack()
        
        time_label = tk.Label(
            popup,
            text=f"{hour:02d}:{minute:02d} - {label}",
            font=("Arial", 12),
            fg=self.secondary_text,
            bg='white'
        )
        time_label.pack(pady=(5, 20))
        
        # Buttons
        button_frame = tk.Frame(popup, bg='white')
        button_frame.pack(fill='x', padx=30, pady=(0, 30))
        
        def dismiss():
            self.stop_sound()
            popup.destroy()
            if not repeat and index < len(self.alarm_list):
                self.delete_alarm(index)
        
        def snooze():
            self.stop_sound()
            popup.destroy()
            snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            snooze_id = f"{snooze_time.hour}:{snooze_time.minute}:{label}_snooze_{datetime.datetime.now().timestamp()}"
            self.alarm_list.append((
                snooze_time.hour,
                snooze_time.minute,
                False,
                f"{label} (Snooze)",
                snooze_id
            ))
            self.render_alarms()
        
        snooze_btn = tk.Button(
            button_frame,
            text="Snooze (1 min)",
            font=("Arial", 11, "bold"),
            bg='#f0f0f0',
            fg=self.text_color,
            relief='flat',
            cursor="hand2",
            command=snooze
        )
        snooze_btn.pack(side='left', fill='x', expand=True, ipady=10, padx=(0, 5))
        
        dismiss_btn = tk.Button(
            button_frame,
            text="Dismiss",
            font=("Arial", 11, "bold"),
            bg=self.primary_color,
            fg='white',
            relief='flat',
            cursor="hand2",
            command=dismiss
        )
        dismiss_btn.pack(side='right', fill='x', expand=True, ipady=10, padx=(5, 0))
    
    def play_sound(self):
        """Play alarm sound"""
        try:
            pygame.mixer.music.load("alarm.wav")
            pygame.mixer.music.play(loops=-1)  # Loop indefinitely until stopped
        except Exception as e:
            print(f"Could not load alarm.wav: {e}")
            # Fallback: play system beep
            try:
                import winsound
                winsound.Beep(1000, 500)
            except:
                print("No audio available")
    
    def stop_sound(self):
        """Stop alarm sound"""
        pygame.mixer.music.stop()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()































# import datetime
# import time
# from playsound import playsound
# import tkinter as tk
# import threading
# import pygame
# #making gui
# root = tk.Tk()

# root.title('Alarm Cloak')

# entry = tk.Entry(root, font=("Arial", 20), width=10)
# entry.pack(pady=10)
# alarm_list = []

# listbox = tk.Listbox(root, font=("Arial", 14), height=5)
# listbox.pack(pady=10)

# repeat_var = tk.BooleanVar()
# tk.Checkbutton(root, text="Repeat Daily", variable=repeat_var, font=("Arial", 12)).pack()

# label_entry = tk.Entry(root, font=("Arial", 14))
# label_entry.pack(pady=5)


# # Initialize mixer at the beginning
# pygame.mixer.init()

# # Replace threading/playsound with this
# def play_sound():
#     pygame.mixer.music.load("alarm.wav")
#     pygame.mixer.music.play(loops=0)

# def stop_sound():
#     pygame.mixer.music.stop()


# def set_alarm():
#     value = entry.get()
#     if ":" not in value:
#         print("Invalid format. Please use HH:MM.")
#         return

#     try:
#         hou, min = value.split(":")
#         hou = int(hou)
#         min = int(min)
#         if 0 <= hou < 24 and 0 <= min < 60:
#             label = label_entry.get()

#             # Check for duplicates
#             for alarm in alarm_list:
#                 if alarm[:3] == (hou, min, repeat_var.get()) and alarm[3] == label:
#                     print("Alarm with same time and label already exists.")
#                     return

#             # Only add alarm if no duplicate found
#             alarm_list.append((hou, min, repeat_var.get(), label))
#             listbox.insert(tk.END, f"{hou:02d}:{min:02d} {label} {'(Repeat)' if repeat_var.get() else ''}")
#             print("Alarm added:", hou, min)

#         else:
#             print("Hour must be 0-23 and minute must be 0-59.")
#     except ValueError:
#         print("Invalid numbers. Please enter in HH:MM format.")






# clock_label = tk.Label(root, text="", font=("Arial", 30), fg="green")
# clock_label.pack(pady=10)

# def update_clock():
#     now = datetime.datetime.now()
#     time_str = now.strftime("%H:%M:%S")
#     clock_label.config(text=time_str)
#     root.after(1000, update_clock)

# update_clock()
# last_triggered = None
# def check_alarms():
#     global last_triggered
#     now = datetime.datetime.now()
    
#     # Make a copy of the list with indices
#     alarms_copy = list(enumerate(alarm_list))

#     for i, (hour, minute, repeat, label) in alarms_copy:
#         if now.hour == hour and now.minute == minute:
#             if last_triggered != (hour, minute):
#                 show_alarm_popup(hour, minute, i, repeat)
#                 last_triggered = (hour, minute)

#                 # # Only delete after the popup shows
#                 # if not repeat:
#                 #     if i < len(alarm_list):  # Check index is still valid
#                 #         alarm_list.pop(i)
#                 #         listbox.delete(i)

#     root.after(1000, check_alarms)


# def show_alarm_popup(hour, minute, index=None, repeat=False):
#     popup = tk.Toplevel(root)
#     popup.title("Alarm")
#     tk.Label(popup, text="⏰ Alarm ringing!", font=("Arial", 18)).pack(pady=10)

#     # threading.Thread(target=playsound, args=("PYTHON/alarm.wav",), daemon=True).start()
#     play_sound()

#     def dismiss():
#         stop_sound()  # stop sound on dismiss
#         popup.destroy()
#         if not repeat and index is not None:
#             if index < len(alarm_list):
#                 try:
#                     alarm_list.pop(index)
#                     listbox.delete(index)
#                 except IndexError:
#                     pass
#     def snooze():
#         popup.destroy()
#         snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
#         original_label = alarm_list[index][3] if index is not None and index < len(alarm_list) else "Snoozed"
#         alarm_list.append((snooze_time.hour, snooze_time.minute, False, original_label + " (Snooze)"))
#         listbox.insert(tk.END, f"{snooze_time.hour:02d}:{snooze_time.minute:02d} {original_label} (Snooze)")


#     tk.Button(popup, text="Dismiss", command=dismiss).pack(pady=5)
#     tk.Button(popup, text="Snooze", command=snooze).pack(pady=5)




# def delete_alarm():
#     selected = listbox.curselection()
#     if selected:
#         index = selected[0]
#         listbox.delete(index)
#         alarm_list.pop(index)
#         print("Alarm deleted.")

# tk.Button(root, text="Delete Alarm", command=delete_alarm, font=("Arial", 16)).pack(pady=5)

    
# check_alarms()
# root.mainloop()













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