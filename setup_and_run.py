import os
from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler


def run_server():
    print("Starting CGI server on port 8000...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server_address = ('', 8000)
    
    # Ensure CGI scripts can be executed
    handler = CGIHTTPRequestHandler
    handler.cgi_directories = ["/cgi-bin"]
    
    httpd = ThreadingHTTPServer(server_address, handler)
    print("Server running at http://localhost:8000/")
    print("Please open this URL in your web browser or phone (if on same network).")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':

    run_server()
