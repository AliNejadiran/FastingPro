import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
import json
import os

class ModernFastingApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔥 Fasting Pro")
        self.window.geometry("420x750")
        self.window.configure(bg='#1a1a2e')
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        self.water_glasses = 0
        self.meals = 0
        self.workouts = 0
        self.fasting_hours = 16
        self.current_status = "Fasting 🚫"
        self.start_time = time.time()
        
        self.colors = {
            'dark': '#1a1a2e',
            'primary': '#0f4c75',
            'secondary': '#3282b8',
            'accent': '#bbe1fa',
            'success': '#4ecdc4',
            'danger': '#ff6b6b',
            'warning': '#ffd166',
            'card': '#16213e'
        }
        
        self.load_data()
        self.setup_ui()
        self.update_clock()
    
    def save_data(self):
        data = {
            'water_glasses': self.water_glasses,
            'meals': self.meals,
            'workouts': self.workouts,
            'start_time': self.start_time,
            'last_date': datetime.now().strftime("%Y-%m-%d")
        }
        with open('data/user_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        try:
            with open('data/user_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            last_date = data.get('last_date', '')
            today = datetime.now().strftime("%Y-%m-%d")
            
            if last_date != today:
                self.water_glasses = 0
                self.meals = 0
                self.workouts = 0
                self.start_time = time.time()
            else:
                self.water_glasses = data.get('water_glasses', 0)
                self.meals = data.get('meals', 0)
                self.workouts = data.get('workouts', 0)
                self.start_time = data.get('start_time', time.time())
        except FileNotFoundError:
            pass
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.window, bg=self.colors['primary'], height=120)
        header_frame.pack(fill='x')
        
        title_label = tk.Label(header_frame, 
                              text="🔥 FASTING PRO", 
                              font=("Segoe UI", 26, "bold"), 
                              bg=self.colors['primary'], 
                              fg='white')
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Professional Fasting & Fitness Tracker", 
                                 font=("Segoe UI", 11), 
                                 bg=self.colors['primary'], 
                                 fg=self.colors['accent'])
        subtitle_label.pack()
        
        # Status Card
        status_card = self.create_card(self.window)
        status_card.pack(pady=15, padx=20, fill='x')
        
        time_frame = tk.Frame(status_card, bg=self.colors['card'])
        time_frame.pack(fill='x', pady=(10, 5))
        
        self.clock_label = tk.Label(time_frame, 
                                   text="", 
                                   font=("Segoe UI", 22, "bold"), 
                                   bg=self.colors['card'], 
                                   fg=self.colors['accent'])
        self.clock_label.pack()
        
        self.date_label = tk.Label(time_frame, 
                                  text="", 
                                  font=("Segoe UI", 12), 
                                  bg=self.colors['card'], 
                                  fg='#a0a0a0')
        self.date_label.pack()
        
        status_display = tk.Frame(status_card, bg=self.colors['card'])
        status_display.pack(pady=15)
        
        self.status_indicator = tk.Label(status_display, 
                                        text=self.current_status, 
                                        font=("Segoe UI", 16, "bold"), 
                                        bg=self.colors['danger'], 
                                        fg='white',
                                        width=20,
                                        height=2,
                                        relief='flat')
        self.status_indicator.pack()
        
        # Stats Cards
        stats_frame = tk.Frame(self.window, bg=self.colors['dark'])
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        row1 = tk.Frame(stats_frame, bg=self.colors['dark'])
        row1.pack(fill='x', pady=(0, 10))
        
        self.water_card = self.create_stat_card(row1, "💧", "Water", f"{self.water_glasses}/8", self.colors['secondary'], 0)
        self.meal_card = self.create_stat_card(row1, "🍎", "Meals", f"{self.meals}/3", self.colors['success'], 1)
        self.workout_card = self.create_stat_card(row1, "💪", "Workouts", f"{self.workouts}/2", self.colors['warning'], 2)
        
        # Progress Bar
        progress_card = self.create_card(self.window)
        progress_card.pack(pady=10, padx=20, fill='x')
        
        tk.Label(progress_card, 
                text="⏳ Fasting Progress", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors['card'], 
                fg='white').pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(progress_card, 
                                          length=300, 
                                          mode='determinate',
                                          style="modern.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10)
        
        self.progress_label = tk.Label(progress_card, 
                                      text="0%", 
                                      font=("Segoe UI", 14, "bold"), 
                                      bg=self.colors['card'], 
                                      fg=self.colors['accent'])
        self.progress_label.pack(pady=(0, 10))
        
        # Action Buttons
        actions_frame = tk.Frame(self.window, bg=self.colors['dark'])
        actions_frame.pack(pady=15, padx=20, fill='x')
        
        row2 = tk.Frame(actions_frame, bg=self.colors['dark'])
        row2.pack(fill='x', pady=(0, 10))
        
        self.create_action_button(row2, "💧 Drink Water", self.drink_water, self.colors['secondary'], 0)
        self.create_action_button(row2, "🍎 Log Meal", self.log_meal, self.colors['success'], 1)
        self.create_action_button(row2, "💪 Workout", self.log_workout, self.colors['warning'], 2)
        
        row3 = tk.Frame(actions_frame, bg=self.colors['dark'])
        row3.pack(fill='x')
        
        self.create_action_button(row3, "🔄 Toggle Status", self.toggle_status, self.colors['primary'], 0, width=14)
        self.create_action_button(row3, "📊 Show Report", self.show_report, "#9b59b6", 1, width=14)
        
        # Daily Routine
        routine_card = self.create_card(self.window)
        routine_card.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(routine_card, 
                text="📅 Smart Daily Routine", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors['card'], 
                fg='white').pack(pady=(10, 5))
        
        self.create_routine_table(routine_card)
        
        # Footer
        footer = tk.Frame(self.window, bg=self.colors['dark'], height=40)
        footer.pack(fill='x', side='bottom')
        
        tk.Label(footer, 
                text="💪 Stronger than yesterday", 
                font=("Segoe UI", 10), 
                bg=self.colors['dark'], 
                fg='#666').pack(pady=10)
    
    def create_card(self, parent):
        card = tk.Frame(parent, 
                       bg=self.colors['card'],
                       relief='flat',
                       bd=0)
        return card
    
    def create_stat_card(self, parent, icon, title, value, color, position):
        card = tk.Frame(parent, 
                       bg=color,
                       relief='flat',
                       bd=0,
                       width=100,
                       height=80)
        card.pack_propagate(False)
        card.pack(side='left', padx=5, expand=True, fill='both')
        
        tk.Label(card, 
                text=icon, 
                font=("Segoe UI", 20), 
                bg=color, 
                fg='white').pack(pady=(10, 0))
        
        tk.Label(card, 
                text=title, 
                font=("Segoe UI", 10), 
                bg=color, 
                fg='white').pack()
        
        value_label = tk.Label(card, 
                              text=value, 
                              font=("Segoe UI", 14, "bold"), 
                              bg=color, 
                              fg='white')
        value_label.pack(pady=(0, 10))
        
        return value_label
    
    def create_action_button(self, parent, text, command, color, position, width=10):
        btn = tk.Button(parent,
                       text=text,
                       font=("Segoe UI", 11, "bold"),
                       bg=color,
                       fg='white',
                       activebackground=color,
                       activeforeground='white',
                       relief='flat',
                       bd=0,
                       height=2,
                       width=width,
                       cursor='hand2',
                       command=command)
        btn.pack(side='left', padx=5, expand=True, fill='both')
        
        def on_enter(e):
            btn['bg'] = self.lighten_color(color, 20)
        
        def on_leave(e):
            btn['bg'] = color
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def create_routine_table(self, parent):
        container = tk.Frame(parent, bg=self.colors['card'])
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        routine_data = [
            ("🌅 06:00", "Wake Up", "Warm water + Meditation"),
            ("💪 06:30", "Morning Workout", "20 min HIIT"),
            ("☕ 07:00", "Breakfast", "Protein shake"),
            ("🧠 08:00", "Work", "Focus mode"),
            ("🍎 12:00", "First Meal", "Protein + Veggies"),
            ("🥗 15:00", "Snack", "Nuts + Fruit"),
            ("🏋️ 17:00", "Evening Workout", "45 min Strength"),
            ("🍗 19:00", "Main Meal", "Fish/Chicken + Veggies"),
            ("🚫 20:00", "Start Fasting", "Last meal"),
            ("😴 22:00", "Sleep", "7-8 hours recovery")
        ]
        
        for i, (time, activity, details) in enumerate(routine_data):
            item_frame = tk.Frame(scrollable_frame, bg='#1e2a47' if i % 2 == 0 else '#253458')
            item_frame.pack(fill='x', padx=5, pady=2)
            
            tk.Label(item_frame, 
                    text=time, 
                    font=("Segoe UI", 11, "bold"), 
                    bg=item_frame['bg'], 
                    fg=self.colors['accent'],
                    width=10).pack(side='left', padx=10)
            
            tk.Label(item_frame, 
                    text=activity, 
                    font=("Segoe UI", 11), 
                    bg=item_frame['bg'], 
                    fg='white').pack(side='left', padx=10)
            
            tk.Label(item_frame, 
                    text=details, 
                    font=("Segoe UI", 10), 
                    bg=item_frame['bg'], 
                    fg='#aaa').pack(side='right', padx=10)
            
            var = tk.BooleanVar()
            cb = tk.Checkbutton(item_frame,
                               text="",
                               variable=var,
                               bg=item_frame['bg'],
                               activebackground=item_frame['bg'],
                               fg='white',
                               selectcolor=self.colors['success'])
            cb.pack(side='right', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def lighten_color(self, color, percent):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        r = min(255, r + percent)
        g = min(255, g + percent)
        b = min(255, b + percent)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def update_clock(self):
        now = datetime.now()
        
        time_str = now.strftime("%H:%M:%S")
        self.clock_label.config(text=time_str)
        
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_label.config(text=date_str)
        
        hour = now.hour
        if 20 <= hour or hour < 12:
            self.current_status = "Fasting 🚫"
            self.status_indicator.config(text=self.current_status, bg=self.colors['danger'])
        else:
            self.current_status = "Eating Window ✅"
            self.status_indicator.config(text=self.current_status, bg=self.colors['success'])
        
        progress = self.calculate_fasting_progress()
        self.progress_bar['value'] = progress
        self.progress_label.config(text=f"{int(progress)}%")
        
        self.window.after(1000, self.update_clock)
    
    def calculate_fasting_progress(self):
        hour = datetime.now().hour
        minute = datetime.now().minute
        
        if 20 <= hour or hour < 12:
            if hour >= 20:
                elapsed = (hour - 20) * 60 + minute
            else:
                elapsed = (hour + 4) * 60 + minute
            
            total_minutes = self.fasting_hours * 60
            progress = (elapsed / total_minutes) * 100
            return min(progress, 100)
        else:
            elapsed = (hour - 12) * 60 + minute
            total_minutes = 8 * 60
            progress = (elapsed / total_minutes) * 100
            return min(progress, 100)
    
    def drink_water(self):
        if self.water_glasses < 8:
            self.water_glasses += 1
            self.water_card.config(text=f"{self.water_glasses}/8")
            self.show_notification("💧 Water Logged!", f"Total: {self.water_glasses} glasses")
            self.save_data()
        else:
            self.show_notification("✅ Complete!", "You've had enough water today!")
    
    def log_meal(self):
        if self.meals < 3:
            self.meals += 1
            self.meal_card.config(text=f"{self.meals}/3")
            self.show_notification("🍎 Meal Logged!", f"Today's meals: {self.meals}")
            self.save_data()
        else:
            self.show_notification("✅ Complete!", "All meals logged for today!")
    
    def log_workout(self):
        if self.workouts < 2:
            self.workouts += 1
            self.workout_card.config(text=f"{self.workouts}/2")
            self.show_notification("💪 Workout Logged!", f"Today's sessions: {self.workouts}")
            self.save_data()
        else:
            self.show_notification("✅ Complete!", "All workouts completed for today!")
    
    def toggle_status(self):
        if "Fasting" in self.current_status:
            self.current_status = "Eating Window ✅"
            self.status_indicator.config(text=self.current_status, bg=self.colors['success'])
            self.show_notification("🔄 Status Changed", "Eating mode activated")
        else:
            self.current_status = "Fasting 🚫"
            self.status_indicator.config(text=self.current_status, bg=self.colors['danger'])
            self.show_notification("🔄 Status Changed", "Fasting mode activated")
    
    def show_report(self):
        elapsed_time = int(time.time() - self.start_time)
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        
        report = f"""📊 Performance Report:

⏰ Session time: {hours}h {minutes}m
💧 Water intake: {self.water_glasses}/8 glasses
🍎 Meals logged: {self.meals}/3 meals
💪 Workout sessions: {self.workouts}/2 sessions
🎯 Current status: {self.current_status}

📈 Today's Progress:
{'✅' if self.water_glasses >= 8 else '🔄'} Water: {self.water_glasses}/8
{'✅' if self.meals >= 3 else '🔄'} Meals: {self.meals}/3
{'✅' if self.workouts >= 2 else '🔄'} Workouts: {self.workouts}/2

💡 Smart Recommendation:
{self.get_ai_recommendation()}"""
        
        messagebox.showinfo("📊 Full Report", report)
    
    def get_ai_recommendation(self):
        recommendations = [
            "Drinking more water boosts metabolism",
            "Adequate protein preserves muscle during fasting",
            "Fasted workouts increase fat burning",
            "Quality sleep improves recovery"
        ]
        return recommendations[0]
    
    def show_notification(self, title, message):
        notification = tk.Toplevel(self.window)
        notification.title(title)
        notification.geometry("350x150")
        notification.configure(bg=self.colors['primary'])
        notification.attributes('-topmost', True)
        
        header = tk.Frame(notification, bg=self.colors['secondary'], height=40)
        header.pack(fill='x')
        
        tk.Label(header, 
                text=title, 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors['secondary'], 
                fg='white').pack(pady=10)
        
        tk.Label(notification, 
                text=message, 
                font=("Segoe UI", 11), 
                bg=self.colors['primary'], 
                fg='white',
                wraplength=300,
                justify='center').pack(pady=20, padx=20)
        
        tk.Button(notification,
                 text="✓ Got it",
                 font=("Segoe UI", 10, "bold"),
                 bg=self.colors['success'],
                 fg='white',
                 command=notification.destroy).pack(pady=(0, 10))
        
        notification.after(3000, notification.destroy)
    
    def run(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("modern.Horizontal.TProgressbar",
                       background=self.colors['success'],
                       troughcolor=self.colors['dark'],
                       bordercolor=self.colors['card'],
                       lightcolor=self.colors['success'],
                       darkcolor=self.colors['success'])
        
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernFastingApp()
    app.run()