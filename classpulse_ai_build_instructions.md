# SYSTEM PROMPT: Project ClassPulse MVP Build

**To the AI Assistant (Antigravity Tool):** 
You are acting as an expert Python developer. Your task is to generate the functioning codebase for a university project called "ClassPulse." Please read the entire architecture and constraints below before generating the code. The goal is to build a simple, working Minimum Viable Product (MVP) that can be easily demonstrated on a local machine (localhost).

---

## 1. Project Overview
**ClassPulse** is a live classroom feedback system. 
* **The Problem:** Students in large lectures are too shy to raise their hands when confused.
* **The Solution:** Students use a simple web page on their phones to click buttons (e.g., "Confused", "Speed Up") or submit anonymous text questions. The professor has a Tkinter desktop application that receives these clicks and questions in real-time over the local network, displaying them on a dashboard.

---

## 2. The Simplified MVP Architecture
To keep the demonstration simple and avoid complex routing, we will use a 3-part architecture running on `localhost`:

1.  **The Student Web Page (`index.html`):** A basic HTML form.
2.  **The CGI Script (`cgi-bin/submit_feedback.py`):** An HTML form handler that uses Python's `cgi` module. It cleans the input, connects to a local SQLite database (acting as our SQL requirement) to log the entry, and sends a quick TCP socket message to the professor's app.
3.  **The Professor Dashboard (`professor_app.py`):** A Tkinter GUI that uses multithreading. The main thread runs the GUI (charts and text boxes). A background thread runs a Socket Server listening for messages from the CGI script to update the GUI in real-time.

---

## 3. Required Syllabus Implementations (Must be included in the code)

When writing the code, you **MUST** implement the following specific Python concepts:

*   **Tkinter (GUI):** Use event-driven programming, nested frames (Left frame for counters, Right frame for text questions), labels, and buttons. Change label colors dynamically (e.g., turn "Confused" counter red if it goes over 5).
*   **Multithreading:** The Tkinter app `professor_app.py` must import `threading`. Create a background daemon thread that runs `socket.listen()` so the Tkinter `mainloop()` does not freeze.
*   **Client/Server & Networks:** Use the `socket` library. The CGI script is the client; the Tkinter background thread is the server.
*   **CGI & HTML:** Provide a simple `index.html` and a python script inside a `cgi-bin` folder to process the web requests.
*   **Database Programming:** Use `sqlite3` (built into Python) to represent the SQL database requirement. Create a table `feedback (id, type, text, timestamp)`. Every CGI submission must be inserted here.
*   **Regular Expressions:** In the CGI script, import `re`. Use regex to strip out any special characters or HTML tags from the student's text question before sending it or saving it, ensuring plain text only.
*   **File Handling (I/O):** Add an "Export Report" button to the Tkinter app. When clicked, it must query the database, format the results, and write them to a `class_report.txt` file using Python file handling (`with open(...)`). Wrap this in a `try-except` block to catch I/O Exceptions.
*   **Object-Oriented Programming:** Structure the Tkinter app as a class (e.g., `class ClassPulseDashboard:`).

---

## 4. File Generation Instructions
Please generate the following distinct files with the exact code needed to make this run on a single machine for a demonstration.

### File 1: `setup_and_run.py`
A simple Python script to set up the SQLite database file (`pulse.db`) and start Python's built-in CGI HTTP server (`http.server` with `CGIHTTPRequestHandler`) on port 8000. 

### File 2: `index.html`
A clean, mobile-friendly HTML page.
*   Include three submit buttons inside a form: "Following Along", "Confused", "Going Too Fast".
*   Include a text input field for "Anonymous Question" and a separate submit button.
*   The form action must point to `/cgi-bin/submit_feedback.py`.

### File 3: `cgi-bin/submit_feedback.py`
The CGI script.
*   Must read the form fields using the `cgi` module.
*   **Regex Requirement:** Sanitize the text input using `re.sub()`.
*   **Database Requirement:** Connect to `pulse.db` and `INSERT` the feedback.
*   **Network Requirement:** Open a socket, connect to `localhost:9999`, and send a brief string (e.g., "CLICK:Confused" or "TEXT:Can you repeat that?").
*   Return a simple HTML success redirect back to `index.html`.

### File 4: `professor_app.py`
The main Tkinter application.
*   **OOP Requirement:** Wrap the GUI logic in a class.
*   **Tkinter Requirement:** Create a window. Use a nested frame layout. 
    *   Left Frame: 3 Labels showing the count of "Following Along", "Confused", "Too Fast".
    *   Right Frame: A Tkinter `Listbox` or `Text` widget to append incoming questions.
    *   Bottom Frame: "Export Report" button.
*   **Multithreading Requirement:** On `__init__`, start a background thread that binds a socket to `localhost:9999`. When it receives a message from the CGI script, it updates the Tkinter variables using `.after()` or thread-safe methods.
*   **File Handling Requirement:** The "Export Report" button must fetch all rows from `pulse.db` and write them to `report.txt` using a try-except block.

---
**Final Note to AI:** Keep the styling simple. The priority is that the multithreading, sockets, database, and Tkinter GUI work together seamlessly without throwing errors during a live class demonstration. Please provide the code for all 4 files.