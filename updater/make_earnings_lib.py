def K(kz, ke, vz, ve, yoy=None, qoq=None, nz=None, ne=None, d=False):
    return {"k": [kz, ke], "v": [vz, ve], "yoy": yoy, "qoq": qoq, "note": [nz, ne] if nz else None, "derived": d}
def L(*pairs): return [list(p) for p in pairs]
def S(t, u): return {"t": t, "u": u}

