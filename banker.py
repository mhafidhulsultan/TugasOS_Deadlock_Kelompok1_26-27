"""Percobaan 3: Banker's Algorithm (safety algorithm + penanganan request)."""

def need_matrix(maks, alokasi):
    return [[m - a for m, a in zip(rm, ra)] for rm, ra in zip(maks, alokasi)]

def cek_aman(available, alokasi, need):
    work = available[:]
    selesai = [False] * len(alokasi)
    urutan = []
    ada = True
    while ada:
        ada = False
        for i in range(len(alokasi)):
            if not selesai[i] and all(n <= w for n, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alokasi[i])]
                selesai[i] = True
                urutan.append(f"P{i}")
                ada = True
    return all(selesai), urutan

def minta(i, req, available, alokasi, need):
    """Kembalikan (diberikan, keterangan)."""
    if any(r > n for r, n in zip(req, need[i])):
        return False, "ditolak: melebihi klaim maksimum"
    
    if any(r > a for r, a in zip(req, available)):
        return False, "menunggu: resource belum tersedia"
        
    av = [a - r for a, r in zip(available, req)]
    al = [row[:] for row in alokasi]
    nd = [row[:] for row in need]
    
    al[i] = [a + r for a, r in zip(al[i], req)]
    nd[i] = [n - r for n, r in zip(nd[i], req)]
    
    aman, urutan = cek_aman(av, al, nd)
    if aman:
        return True, "dikabulkan, urutan aman: " + " -> ".join(urutan)
    return False, "ditolak: akan membuat sistem tidak aman"

if __name__ == "__main__":
    total = [10, 5, 7]
    maks = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    alokasi = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    
    need = need_matrix(maks, alokasi)
    available = [t - sum(col) for t, col in zip(total, zip(*alokasi))]
    
    print("Need :", need)
    print("Available:", available)
    print("Aman? :", cek_aman(available, alokasi, need))
    print("P1 minta (1,0,2):", minta(1, [1, 0, 2], available, alokasi, need))
    print("P4 minta (3,3,0):", minta(4, [3, 3, 0], available, alokasi, need))
    print("P0 minta (0,2,0):", minta(0, [0, 2, 0], available, alokasi, need))