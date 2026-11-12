"""Percobaan 2b: livelock."""
import threading

printer = threading.Lock()
scanner = threading.Lock()
barrier = threading.Barrier(2)
MAKS_PUTARAN = 20
selesai = {"A": False, "B": False}
percobaan = {"A": 0, "B": 0}

def proses(nama, pertama, kedua):
    for _ in range(MAKS_PUTARAN):
        percobaan[nama] += 1
        pertama.acquire()
        barrier.wait() # keduanya sudah memegang 1 resource
        berhasil = kedua.acquire(blocking=False)
        barrier.wait() # keduanya sudah mencoba memegang 2 resource
        if berhasil:
            kedua.release()
            pertama.release()
            selesai[nama] = True
            return
        pertama.release() # sopan : lepas, lalu ulangi
        barrier.wait() # keduanya sudah melepas

a = threading.Thread(target=proses, args=("A", printer, scanner))
b = threading.Thread(target=proses, args=("B", scanner, printer))
a.start()
b.start()
a.join()
b.join()

print("Percobaan A:", percobaan["A"], "| Percobaan B:", percobaan["B"])
if not any(selesai.values()):
    print("LIVELOCK: keduanya sibuk mencoba terus, tetapi tidak ada yang selesai")
else:
    print("Salah satu berhasil:", selesai)
