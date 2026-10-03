# ClassPulse 🎓

**ClassPulse** is a lightweight, real-time classroom feedback system built entirely in Python. 

Often, students in large lectures feel too shy to raise their hands when they are confused or when the professor is going too fast. ClassPulse solves this by allowing students to use a simple web page on their phones to submit quick, anonymous feedback. The professor sees this feedback instantly on a desktop dashboard.

The beauty of this project is that it requires **zero external dependencies** or large web frameworks (like Django or Flask). It relies entirely on Python's built-in standard libraries (like `http.server`, `tkinter`, and `socket`), making it incredibly easy to set up and demonstrate!

---

## 🏗️ How It Works (Architecture)

The system operates across three main components using a local network:

1. **Student Web App (`index.html`)**: A clean, mobile-friendly HTML interface where students can click quick-feedback buttons (e.g., "Confused", "Going Too Fast") or submit custom text questions.
2. **CGI Request Handler (`cgi-bin/submit_feedback.py`)**: A Python CGI script that intercepts the HTML form data. It sanitizes the input and instantly transmits it over a TCP socket connection to the professor's computer.
3. **Professor Dashboard (`professor_app.py`)**: A Python desktop GUI built with `Tkinter`. It runs a background socket server on a separate thread to listen for incoming feedback without freezing the user interface. It updates the dashboard counters and text boxes in real-time.

---

## 🚀 How to Run (Localhost)

If you just want to test this on your own computer, follow these steps:

1. **Prerequisites:** Make sure you have **Python 3** installed (Tested on Python 3.13). No `pip install` is required!
2. Open a terminal in the project folder and start the web server:
   ```bash
   python setup_and_run.py
   ```
3. Open a *second* terminal in the project folder and start the professor's dashboard:
   ```bash
   python professor_app.py
   ```
4. Open your web browser and go to: `http://localhost:8000`
5. Try clicking the feedback buttons on the website and watch your Tkinter dashboard update instantly!

---

## 📱 How to Demo on a Local Wi-Fi Network

If you want to demonstrate this live in a classroom (using your laptop as the dashboard and your phone as the student device), you can easily run it over a local Wi-Fi network.

1. **Connect to the same network:** Ensure both your laptop and your phone are connected to the exact same Wi-Fi network.
2. **Find your Laptop's IP Address:**
   * **Windows:** Open Command Prompt / PowerShell and run `ipconfig`. Look for the "IPv4 Address" (e.g., `192.168.1.5` or `172.25.x.x`).
   * **Mac/Linux:** Open Terminal and run `ifconfig` or `ip a` to find your local IP.
3. **Start the Servers:** Run `setup_and_run.py` and `professor_app.py` on your laptop just like you did in the Localhost instructions.
4. **Access on your Phone:** Open the web browser on your phone and type in your laptop's IP address followed by `:8000`. 
   * *Example:* `http://192.168.1.5:8000`

### ⚠️ Troubleshooting Network Demos
If the webpage hangs and refuses to load on your phone, your laptop's firewall is likely blocking incoming connections to port 8000.
* **On Windows:** Press the Windows key, search for *"Allow an app through Windows Firewall"*. Click *"Change settings"*, scroll down to **Python**, and make sure both the "Private" and "Public" checkboxes are ticked. Click OK and refresh your phone!

---

## 📝 License
This project was created for a university Python Programming course. Feel free to fork, modify, and use it as you see fit!
