import threading

printer = threading.Lock()
scanner = threading.Lock()

MAKS_PUTARAN = 20
selesai = {"A": False, "B": False}
percobaan = {"A": 0, "B": 0}

def proses(nama, pertama, kedua):
    for _ in range(MAKS_PUTARAN):
        percobaan[nama] += 1
        
        # 1. Mengambil resource pertama
        pertama.acquire()
        
        # 2. Mencoba resource kedua
        berhasil = kedua.acquire(blocking=False)
        
        if berhasil:
            kedua.release()
            pertama.release()
            selesai[nama] = True
            return
            
        # 3. Sopan: lepas jika gagal, lalu ulangi
        pertama.release()

# PERBAIKAN: Menggunakan urutan lock yang sama (printer lalu scanner)
a = threading.Thread(target=proses, args=("A", printer, scanner))
b = threading.Thread(target=proses, args=("B", printer, scanner))

a.start()
b.start()

a.join()
b.join()

print("Percobaan A:", percobaan["A"], "| Percobaan B:", percobaan["B"])

if not any(selesai.values()):
    print("LIVELOCK: keduanya sibuk mencoba terus, tetapi tidak ada yang selesai")
else:
    print("Salah satu berhasil:", selesai)