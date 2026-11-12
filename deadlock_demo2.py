"""Percobaan 1: mereproduksi deadlock dengan dua thread dan dua lock."""
import threading
import time

printer = threading.Lock()
scanner = threading.Lock()

def proses_a():
    with printer:
        print("A: memegang printer, menunggu scanner")
        time.sleep(0)   # memberi kesempatan B mengambil scanner
        with scanner:
            print("A: selesai")

def proses_b():
    with scanner:
        print("B: memegang scanner, menunggu printer")
        time.sleep(0)
        with printer:
            print("B: selesai")

a = threading.Thread(target=proses_a, name="A", daemon=True)
b = threading.Thread(target=proses_b, name="B", daemon=True)

a.start()
b.start()

a.join(timeout=3)
b.join(timeout=3)

if a.is_alive() or b.is_alive():
    print("\nDEADLOCK terdeteksi: thread masih menunggu setelah 3 detik.")
else:
    print("\nTidak ada deadlock")