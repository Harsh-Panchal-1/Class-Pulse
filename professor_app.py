import tkinter as tk
import threading
import socket

# Global State Variables
root = None
server_running = True
counts = {}
lbl_following = None
lbl_confused = None
lbl_fast = None
text_area = None

def start_server():
    """Background thread listening for CGI script messages"""
    global server_running
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 9999))
        server_socket.listen(5)
        server_socket.settimeout(1.0) # Allows loop to check for server_running flag
        
        while server_running:
            try:
                client_socket, addr = server_socket.accept()
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    if data.startswith("CLICK:"):
                        click_type = data.split("CLICK:")[1]
                        # safely update GUI from background thread
                        root.after(0, update_counter, click_type)
                    elif data.startswith("TEXT:"):
                        question = data.split("TEXT:", 1)[1]
                        root.after(0, append_question, question)
                client_socket.close()
            except socket.timeout:
                continue
    except Exception as e:
        print(f"Socket Server error: {e}")
    finally:
        server_socket.close()

def update_counter(click_type):
    """Update Tkinter labels and variables"""
    if click_type in counts:
        current_val = counts[click_type].get()
        counts[click_type].set(current_val + 1)
        
        # Update labels based on new counts
        if click_type == "Following Along":
            lbl_following.config(text=f"Following Along: {counts[click_type].get()}")
        elif click_type == "Confused":
            count = counts[click_type].get()
            lbl_confused.config(text=f"Confused: {count}")
            # Dynamic color change: turn red if it goes over 5
            if count > 5:
                lbl_confused.config(fg="red")
        elif click_type == "Going Too Fast":
            lbl_fast.config(text=f"Going Too Fast: {counts[click_type].get()}")

def append_question(question):
    """Append incoming question to the Text widget"""
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"• {question}\n")
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)

def on_closing():
    """Cleanup socket before closing"""
    global server_running
    server_running = False
    root.destroy()

def setup_gui():
    """Initialize the Tkinter window and layout"""
    global root, counts, lbl_following, lbl_confused, lbl_fast, text_area
    
    root = tk.Tk()
    root.title("ClassPulse Professor Dashboard")
    root.geometry("800x450")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Initialize variables
    counts = {
        "Following Along": tk.IntVar(value=0),
        "Confused": tk.IntVar(value=0),
        "Going Too Fast": tk.IntVar(value=0)
    }
    
    # Layout frames
    left_frame = tk.Frame(root, width=300)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    right_frame = tk.Frame(root, width=500)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Left Frame - Counters
    tk.Label(left_frame, text="Live Feedback Counters", font=("Arial", 16, "bold")).pack(pady=15)
    
    lbl_following = tk.Label(left_frame, text="Following Along: 0", font=("Arial", 14), fg="green")
    lbl_following.pack(pady=10)
    
    lbl_confused = tk.Label(left_frame, text="Confused: 0", font=("Arial", 14))
    lbl_confused.pack(pady=10)
    
    lbl_fast = tk.Label(left_frame, text="Going Too Fast: 0", font=("Arial", 14), fg="orange")
    lbl_fast.pack(pady=10)
    
    # Right Frame - Text Questions
    tk.Label(right_frame, text="Anonymous Questions", font=("Arial", 16, "bold")).pack(pady=15)
    
    scrollbar = tk.Scrollbar(right_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area = tk.Text(right_frame, height=15, width=40, state=tk.DISABLED, font=("Arial", 12), yscrollcommand=scrollbar.set)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_area.yview)
    
    # Start background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Start GUI loop
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
