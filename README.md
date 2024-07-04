<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RemoteXS - README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            color: #0366d6;
        }
        code {
            background-color: #f6f8fa;
            padding: 2px 4px;
            border-radius: 3px;
        }
        ul {
            padding-left: 20px;
        }
        .note {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 4px;
            padding: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>RemoteXS - Remote File Sharing Made Easy</h1>
    
    <h2>1. Setup</h2>
    <ul>
        <li><strong>Install Python:</strong> Ensure you have Python installed on your system. You can download it from <a href="https://www.python.org/">https://www.python.org/</a>.</li>
        <li><strong>Run the program:</strong> Save the provided Python code as a file named <code>RemoteXS.py</code> and then run it from your terminal using <code>python RemoteXS.py</code>.</li>
    </ul>

    <h2>2. Configure the Server</h2>
    <ul>
        <li><strong>Port:</strong> Enter the desired port number for the web server (default is 8000). This is the port where the remote user will access the shared folder.</li>
        <li><strong>Shared Folder:</strong> Click the "Browse" button to choose the folder on your computer that you want to share. This folder's contents will be accessible to the remote user.</li>
        <li><strong>Password:</strong> Enter a strong password. This password will be required for the remote user to access the shared folder.</li>
        <li><strong>Remote User IP:</strong> Enter the static IPv4 address of the remote user who will be accessing the shared files. (e.g., 192.168.1.10)</li>
    </ul>

    <h2>3. Start the Server</h2>
    <ul>
        <li><strong>Start Server:</strong> Click the "Start Server" button to start the web server and make your files accessible.</li>
        <li><strong>Search IP:</strong> Click "Search IP" to display your computer's current IP address. The remote user will need this IP to access the shared folder.</li>
    </ul>

    <h2>4. Dynamic DNS (Optional)</h2>
    <ul>
        <li><strong>Use Dynamic DNS:</strong> Check the "Use Dynamic DNS" checkbox if you want to make your shared folder accessible even if your IP address changes.</li>
        <li><strong>DDNS Provider:</strong> Enter the name of your dynamic DNS provider (e.g., No-IP).</li>
        <li><strong>DDNS Domain:</strong> Enter the domain name associated with your DDNS account.</li>
        <li><strong>DDNS Token:</strong> Enter your DDNS token or password. This is used for updating the IP address with your DNS provider.</li>
    </ul>

    <h2>5. Access the Shared Folder (Remote User)</h2>
    <ol>
        <li><strong>Open a web browser:</strong> The remote user should open a web browser on their device.</li>
        <li><strong>Enter the address:</strong> They should type the following address in the browser's address bar, replacing <code>[your_IP_address]</code> with the IP address you displayed in the "IPv4 Address" field:
            <br><code>http://[your_IP_address]:[port_number]</code></li>
        <li><strong>Enter the password:</strong> The remote user will be prompted to enter the password you set for the shared folder.</li>
    </ol>

    <h2>6. Stop the Server</h2>
    <ul>
        <li><strong>Click "Stop Server":</strong> When you are finished sharing the files, click the "Stop Server" button to stop the web server.</li>
    </ul>

    <div class="note">
        <h3>Additional Notes:</h3>
        <ul>
            <li><strong>Firewall:</strong> Ensure that your computer's firewall allows connections to the port you selected.</li>
            <li><strong>Security:</strong> Be mindful of the files you are sharing and always use a strong password.</li>
            <li><strong>DDNS:</strong> Make sure your DDNS provider has been configured correctly to update your IP address automatically.</li>
        </ul>
    </div>
</body>
</html>
