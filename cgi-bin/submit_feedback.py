import sys
import os
import urllib.parse
import re

import socket

# Parse POST form data manually
content_length = int(os.environ.get('CONTENT_LENGTH', 0))
post_data = sys.stdin.read(content_length)
form = urllib.parse.parse_qs(post_data)

feedback_type = form.get('feedback_type', [''])[0]
question_text = form.get('question_text', [''])[0]

# Sanitize input using regex (remove everything except alphanumeric and basic punctuation)
if question_text:
    question_text = re.sub(r'[^a-zA-Z0-9\s.,?!;:\"\'-]', '', question_text)
else:
    question_text = ''

log_type = feedback_type
log_text = question_text



# Network Requirement: Send TCP socket message to Professor App
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1.0) # Short timeout so CGI script doesn't hang
    client_socket.connect(('127.0.0.1', 9999))
    
    if feedback_type == 'Question':
        message = f"TEXT:{log_text}"
    else:
        message = f"CLICK:{feedback_type}"
        
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()
except Exception as e:
    pass # If professor app is not running, just fail silently without breaking student experience

# Return simple HTML success redirect back to index.html
print("Content-Type: text/html\r\nConnection: close\r\n\r\n")
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Success</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            margin-top: 50px; 
            background-color: #f4f7f6; 
        }
        .message { 
            background: #ffffff; 
            padding: 30px; 
            border-radius: 12px; 
            display: inline-block; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
        }
        h2 { color: #27ae60; margin-top: 0; }
        .btn {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
        }
        .btn:hover { background-color: #2980b9; }
    </style>
</head>
<body>
    <div class="message">
        <h2>Feedback Submitted!</h2>
        <p>Thank you for your feedback.</p>
        <a href="/" class="btn">Return to Homepage</a>
    </div>
</body>
</html>
""")
