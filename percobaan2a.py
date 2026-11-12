"""Percobaan 2a: mencegah circular wait dengan urutan lock yang sama."""
import threading
import time

printer = threading.Lock() # nomor urut 1
scanner = threading.Lock() # nomor urut 2

def proses(nama):
    with printer: # semua proses: printer dulu, baru scanner
        print(f"{nama}: memegang printer, menunggu scanner")
        time.sleep(0.5)
        with scanner:
            print(f"{nama}: selesai")

t = [threading.Thread(target=proses, args=(n,), daemon=True) for n in "AB"]
for x in t:
    x.start()
for x in t:
    x. join(timeout=5)

print("\nDEALOCK" if any(x.is_alive() for x in t) else "\nSelesai tanpa deadlock")