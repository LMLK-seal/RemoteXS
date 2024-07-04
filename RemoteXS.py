import os
import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from http.server import HTTPServer, SimpleHTTPRequestHandler
from base64 import b64encode, b64decode
import requests
import time


class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, server, password=None, **kwargs):
        self.password = password
        self.authenticated = False
        self.server = server
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if not self.authenticated:
            self.authenticate()
        if self.authenticated:
            super().do_GET()
    
    def authenticate(self):
        auth_header = self.headers.get("Authorization")
        if auth_header:
            auth_type, encoded_credentials = auth_header.split(" ", 1)
            if auth_type.lower() == "basic":
                credentials = b64decode(encoded_credentials).decode()
                username, password = credentials.split(":", 1)
                if password == self.password:
                    self.authenticated = True
        
        if not self.authenticated:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Authentication required"')
            self.end_headers()


class FileServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local File Sharing Web Server(RemoteXS)")
        
        self.port = tk.IntVar(value=8000)
        self.directory = tk.StringVar()
        self.password = tk.StringVar()
        self.server = None
        self.thread = None
        self.ddns_thread = None

        self.use_ddns = tk.BooleanVar(value=False)
        self.ddns_provider = tk.StringVar()
        self.ddns_domain = tk.StringVar()
        self.ddns_token = tk.StringVar()

        self.ip_address = tk.StringVar()
        self.static_ip2 = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.port, width=10).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Shared Folder:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.directory, width=40).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_directory).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.password, show="", width=40).grid(row=2, column=1, padx=5, pady=5)

        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.status_label = tk.Label(self.root, text="Server stopped.", fg="red")
        self.status_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # IP Address search button and display
        tk.Button(self.root, text="Search IP", command=self.search_ip).grid(row=6, column=0, padx=5, pady=5)
        tk.Label(self.root, text="IPv4 Address:").grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.ip_address, state="readonly", width=15).grid(row=6, column=2, padx=5, pady=5)

        tk.Checkbutton(self.root, text="Use Dynamic DNS", variable=self.use_ddns, command=self.toggle_ddns_fields).grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        
        self.ddns_frame = tk.Frame(self.root)
        self.ddns_frame.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        
        tk.Label(self.ddns_frame, text="DDNS Provider:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.ddns_frame, textvariable=self.ddns_provider, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.ddns_frame, text="DDNS Domain:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.ddns_frame, textvariable=self.ddns_domain, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.ddns_frame, text="DDNS Token:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.ddns_frame, textvariable=self.ddns_token, show="", width=20).grid(row=2, column=1, padx=5, pady=5)
        
        self.toggle_ddns_fields()

        # Add input field for the remote user's static IP
        tk.Label(self.root, text="Remote User IP:").grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
        self.remote_ip_entry = tk.Entry(self.root, textvariable=self.static_ip2, width=15)
        self.remote_ip_entry.grid(row=9, column=1, padx=5, pady=5)

        # Help text
        help_text = """
Instructions:

1. Configure the Server:
Port: Enter the desired port number for the web server (default is 8000). This is the port where the remote user will access the shared folder.
Shared Folder: Click the "Browse" button to choose the folder on your computer that you want to share. This folder's contents will be accessible to the remote user.
Password: Enter a strong password. This password will be required for the remote user to access the shared folder.
Remote User IP: Enter the static IPv4 address of the remote user who will be accessing the shared files. (e.g., 192.168.1.10)

2. Start the Server:
Start Server: Click the "Start Server" button to start the web server and make your files accessible.
Search IP: Click "Search IP" to display your computer's current IP address. The remote user will need this IP to access the shared folder.

3. Dynamic DNS (Optional):
Use Dynamic DNS: Check the "Use Dynamic DNS" checkbox if you want to make your shared folder accessible even if your IP address changes.

4. Access the Shared Folder (Remote User):
Open a web browser: The remote user should open a web browser on their device.
Enter the address: They should type the following address in the browser's address bar, replacing [your_IP_address] with the IP address you displayed in the "IPv4 Address" field:
http://[your_IP_address]:[port_number]
Enter the password: The remote user will be prompted to enter the password you set for the shared folder.

Additional Notes:
Firewall: Ensure that your computer's firewall allows connections to the port you selected.

        """
        help_label = tk.Label(self.root, text=help_text, justify=tk.LEFT, fg="#555555", font=("Arial", 8))
        help_label.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    def toggle_ddns_fields(self):
        if self.use_ddns.get():
            self.ddns_frame.grid()
        else:
            self.ddns_frame.grid_remove()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)

    def start_server(self):
        if not self.directory.get() or not self.password.get():
            messagebox.showwarning("Warning", "Please select a directory to share and set a password.")
            return

        port = self.port.get()
        directory = self.directory.get()
        password = self.password.get()
        static_ip2 = self.static_ip2.get()

        # Validate remote user's IP address
        if not self.validate_ip(static_ip2):
            messagebox.showwarning("Warning", "Please enter a valid remote user IP address.")
            return

        print(f"Remote User IP: {static_ip2}")

        def run_server():
            os.chdir(directory)

            # Get local IP using the same method as before
            local_ip = self.get_ip_address()

            # Start the server using the local IP 
            try:
                self.server = HTTPServer((local_ip, port),
                                        lambda *args, **kwargs: AuthHTTPRequestHandler(*args, server=self.server, password=password, **kwargs))
            except OSError as e:
                messagebox.showerror("Error", f"Failed to start server on IP: {local_ip}\nError: {str(e)}")
                return

            self.update_status(f"Serving HTTP on port {port}:\n"
                               f"Access from: http://{local_ip}:{port}/", "green")

            # Start a thread for the server
            thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            thread.start()

            # Start DDNS update thread if enabled
            if self.use_ddns.get():
                domain = self.ddns_domain.get()
                token = self.ddns_token.get()
                if domain and token:
                    self.ddns_thread = threading.Thread(target=self.update_ddns_periodically, 
                                                    args=(domain, token), daemon=True)
                    self.ddns_thread.start()

        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def search_ip(self):
        ip = self.get_ip_address()
        self.ip_address.set(ip)

    def get_ip_address(self):
        try:
            # This method gets the IP address of the first non-loopback interface
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "Unable to get IP"

    def get_public_ip(self):
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"Unable to get public IP: {str(e)}"

    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        if self.ddns_thread:
            # Safely stop the DDNS thread (implement a way to signal it)
            self.ddns_thread = None
        self.update_status("Server stopped.", "red")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_status(self, message, color):
        self.status_label.config(text=message, fg=color)

    def update_ddns_periodically(self, domain, token):
        """Periodically checks for IP changes and updates DDNS."""
        while True:
            # Get the current public IP
            public_ip = self.get_public_ip()

            # Update DDNS if the IP has changed
            self.update_noip(domain, token, public_ip)

            # Sleep for some time before checking again
            time.sleep(60) 

    def update_noip(self, domain, token, public_ip):
        """Updates the IP address for the given domain using NoIP API."""
        url = f"https://dynamicdns.park-your-domain.com/update?hostname={domain}&password={token}&myip={public_ip}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(f"NoIP update successful: {response.text}")
        except requests.RequestException as e:
            print(f"Failed to update NoIP: {str(e)}")
            
def main():
    root = tk.Tk()
    app = FileServerApp(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()
