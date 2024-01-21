import http.server
import socketserver
import subprocess
import platform

# Masukkan nilai default untuk port
default_port = 8000

# Masukkan nilai port yang ingin dijalankan atau biarkan kosong untuk nilai default
port_input = input(f"Masukkan nomor port (biarkan kosong untuk nilai default {default_port}): ")

# Tetapkan nilai default jika port tidak diisi
try:
    port = int(port_input) if port_input else default_port
except ValueError:
    print("Input port tidak valid. Menggunakan nilai default.")
    port = default_port

# Masukkan path file Python yang ingin dijalankan atau biarkan kosong untuk nilai default
target_file = input("Masukkan path file (contoh: C:\\path\\to\\file.py, biarkan kosong untuk nilai default): ")

# Tetapkan nilai default jika target_file tidak diisi
file_standar = "C:\\path\\to\\default_file.py"
if not target_file:
    target_file = file_standar

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/run':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            try:
                # Menjalankan program Python (ganti path sesuai dengan file Anda)
                result = subprocess.run(["python", target_file], capture_output=True, text=True)
                
                # Mengirimkan output ke browser
                response = f'<html><body>{result.stdout}</body></html>'
                self.wfile.write(response.encode())
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        elif self.path == '/off':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            try:
                # Menjalankan perintah untuk mematikan port pada Windows
                if platform.system().lower() == 'windows':
                    subprocess.run(["netstat", "-ano", "|", "findstr", f"{port}"], shell=True)
                    subprocess.run(["taskkill", "/F", "/PID", "<pid>"], shell=True)  # Ganti <pid> dengan PID yang ditemukan
                else:
                    response = '<html><body>Operasi ini hanya mendukung Windows.</body></html>'
                    self.wfile.write(response.encode())
                    return
                
                response = '<html><body>Port telah dimatikan.</body></html>'
                self.wfile.write(response.encode())
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        else:
            super().do_GET()

with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()
