import subprocess
import platform

def kill_process_by_port(port):
    try:
        system_platform = platform.system().lower()

        if system_platform == 'windows':
            # Mendapatkan informasi tentang proses yang mendengarkan port pada Windows
            command = f"netstat -ano | findstr LISTENING | findstr :{port}"
            result = subprocess.check_output(command, shell=True).decode('utf-8').strip()

            if result:
                # Mendapatkan PID dari hasil pencarian
                pid = result.split()[-1]
                # Membunuh proses dengan PID yang ditemukan
                subprocess.run(f"taskkill /F /PID {pid}", shell=True)
                print(f"Proses dengan port {port} (PID: {pid}) berhasil dimatikan.")
            else:
                print(f"Tidak ada proses yang mendengarkan port {port}.")
        else:
            # Mendapatkan informasi tentang proses yang mendengarkan port pada Unix/Linux
            command = f"lsof -i :{port} -t"
            result = subprocess.check_output(command, shell=True).decode('utf-8').strip()

            if result:
                # Membunuh proses dengan PID yang ditemukan
                subprocess.run(f"kill -9 {result}", shell=True)
                print(f"Proses dengan port {port} (PID: {result}) berhasil dimatikan.")
            else:
                print(f"Tidak ada proses yang mendengarkan port {port}.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    # Masukkan nomor port yang ingin dimatikan
    target_port = int(input("Masukkan nomor port yang ingin dimatikan: "))

    # Memanggil fungsi untuk mematikan proses berdasarkan nomor port
    kill_process_by_port(target_port)
