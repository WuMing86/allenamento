"""Genera programma.json, i dati della webapp.

Le schede vengono tutte da qui: per cambiare il programma si modifica questo
file e lo si rilancia con `python genera_programma.py`.
I kg non sono salvati: li calcola la pagina partendo dai massimali di calcolo
(percentuale x massimale, arrotondata a 2,5 kg).
"""
import datetime as dt
import json

INIZIO = dt.date(2026, 11, 23)
MASSIMALI = {"panca": 122.5, "military": 60, "m2": 62.5, "stacco": 110}

pm = [65, 70, 75, 67.5, 72.5, 77.5, 70, 75, 80, 72.5, 77.5, 82.5]
pt = [80, 85, 90, 82.5, 87.5, 92.5, 85, 90, 95, 87.5, 92.5, 97.5]
ps = [60, 65, 70, 62.5, 67.5, 72.5, 65, 70, 75, 67.5, 72.5, 77.5]
rip_onda = [6, 5, 4] * 4
rip_g = [3, 2, 1] * 4
serie_l = [9, 8, 6, 8, 6, 6, 6, 5, 6, 6, 5, 5]
serie_g = [8, 8, 6, 6, 7, 6, 5, 5, 6, 5, 5, 4]
var_ven = ["Panca 3 fermi in discesa"] * 3 + ['Panca discesa 5"'] * 3 + \
          ["Panca fermo lungo al petto (2-3\")"] * 3 + ["Panca piana"] * 3
rif_ven = {0: "rif. ciclo scorso: 3 MAV 90, 2 MAV 95, 1 MAV 100",
           3: "rif. ciclo scorso: 3 MAV non chiuso a 95, 2 MAV 102,5, 1 MAV 105",
           6: "nessun riferimento: trovare il MAV a piccoli salti",
           9: "rif. ciclo scorso: 3 MAV 107,5, 2 MAV 110"}
dl_pct = [65, 70, 75, 80, 70, 75, 80, 85, 75, 80, 85, 75]
dl_rip = [5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 2, 5]
dl_var = ["Stacco fermo in incastro"] * 4 + ["Stacco fermo al ginocchio"] * 4 + ["Stacco standard"] * 4
dl_mav = [("5 MAV", "5", "1", ""), ("3 MAV + back-off 90%", "3 / 3", "1 + 4", ""),
          ("2 MAV + back-off 90%", "2 / 2", "1 + 4", ""), ("1 MAV", "1", "1", "nessun back-off")]
pressa = [170, 180, 190, 180, 190, 200, 190, 200, 210, 200, 210, 220]
mil_mar = [(70, 6, 6), (75, 6, 6), (80, 4, 6), (80, 5, 5), (85, 3, 6), None]
mil_ven = [("6 MAV + back-off 80%", "6 / 8", "1 + 4"), ("5 MAV + back-off 90%", "5 / 6", "1 + 4"),
           ("4 MAV + back-off 90%", "4 / 5", "1 + 5"), ("3 MAV + back-off 90%", "3 / 4", "1 + 4"),
           ("2 MAV + back-off 80%", "2 / 5", "1 + 5")]


def pct(es, p, base, rip, serie, nota=""):
    return {"es": es, "pct": p, "base": base, "rip": str(rip), "serie": str(serie), "nota": nota}


def kg(es, k, rip, serie, nota=""):
    return {"es": es, "kg": k, "rip": str(rip), "serie": str(serie), "nota": nota}


def libero(es, schema="", rip="", serie="", nota=""):
    return {"es": es, "schema": schema, "rip": str(rip), "serie": str(serie), "nota": nota}


settimane = []
for w in range(12):
    s3 = w in (2, 5, 8)
    lun = [
        pct("Panca piana · progressione 1", pm[w], "panca", rip_onda[w], serie_l[w],
            "ultime 2 serie solo se le prime 4 sono veloci" if s3 else ""),
        pct("Stacco · carico fisso", dl_pct[w], "stacco", dl_rip[w], 5),
        libero("Pulley", serie=5),
        libero("Bicipiti e tricipiti, core"),
    ]
    if w < 6:
        m = mil_mar[w]
        mil = (pct("Military · progressione", m[0], "military", m[1], m[2]) if m else
               libero("Military · TEST (1 MAV)", "1 MAV", 1, 1, "il risultato è M2: inseriscilo nei massimali"))
    elif w < 11:
        m = mil_mar[w - 6]
        mil = pct("Military · progressione", m[0], "m2", m[1], m[2])
    else:
        mil = pct("Military · progressione", 80, "m2", 2, 4, "scarico")
    mar = [
        mil,
        pct("Panca stretta · carico fisso", ps[w], "panca", rip_onda[w], 5,
            "−2,5% se troppo pesante dopo la military"),
        kg("Pressa · pesante", pressa[w], rip_onda[w], 5, "da confermare dopo l'onda 2" if w >= 9 else ""),
        libero("Shoulder press", "doppia progressione" if w < 11 else "senza progressione",
               "8-12", 3 if w < 11 else 2, "da ~60 kg; tutte a 12 → +10 kg" if w < 11 else ""),
        libero("Lat machine", serie=5),
        libero("Core"),
    ]
    if w < 6:
        mil_g = pct("Military · media", 67.5, "military", 5, 5, "veloce, lontano dal cedimento")
    elif w < 11:
        mil_g = pct("Military · media", 67.5, "m2", 5, 5, "veloce, lontano dal cedimento")
    else:
        mil_g = pct("Military · media", 65, "m2", 5, 3, "scarico")
    mv = dl_mav[w % 4]
    gio = [
        pct("Panca piana · progressione 2", pt[w], "panca", rip_g[w], serie_g[w],
            "ultime 2 singole solo se le prime 4 sono veloci" if s3 else ""),
        libero(dl_var[w], mv[0], mv[1], mv[2], (mv[3] + "; " if mv[3] else "") + "back-off = % del MAV del giorno"),
        mil_g,
        libero("Pulley", serie=5),
        libero("Core"),
    ]
    if w in (5, 11):
        mil_v = pct("Military", 80, "m2", 2, 4, "scarico")
    else:
        f = mil_ven[w if w < 6 else w - 6]
        mil_v = libero("Military · ramping", f[0], f[1], f[2],
                       "back-off = % del MAV del giorno" +
                       (" · rif. ciclo scorso: 4 MAV 50, 3 MAV 52,5, 2 MAV 57,5" if w in (0, 6) else ""))
    sch = [("3 MAV + back-off 85%", "3 / 3"), ("2 MAV + back-off 85%", "2 / 2"), ("1 MAV + back-off 85%", "1 / 1")][w % 3]
    ven = [
        mil_v,
        libero(var_ven[w] + " · ramping", sch[0], sch[1], "1 + 4", rif_ven.get(w, "back-off = % del MAV del giorno")),
        (libero("Pressa · volume", "carico attuale", 8, 3, "scarico prima del test") if w == 11 else
         libero("Pressa · volume", "doppia progressione", "8-12", 4, "da 140 kg; tutte a 12 → +5 kg")),
        libero("Shoulder press", "doppia progressione" if w < 11 else "senza progressione",
               "6-8", 3 if w < 11 else 2, "da ~70 kg; tutte a 8 → +10 kg" if w < 11 else ""),
        libero("Core"),
    ]
    settimane.append({"n": w + 1, "lunedi": (INIZIO + dt.timedelta(weeks=w)).isoformat(),
                      "titolo": f"Onda {w // 3 + 1} · settimana {w % 3 + 1}",
                      "giorni": {"lun": lun, "mar": mar, "gio": gio, "ven": ven}})

settimane.append({
    "n": 13, "lunedi": (INIZIO + dt.timedelta(weeks=12)).isoformat(), "titolo": "Scarico e test",
    "giorni": {
        "lun": [kg("Panca piana", 100, 2, 5, "80% di 125, come prima del test di novembre"),
                libero("Pulley", serie=5, nota="niente stacco"), libero("Core")],
        "mar": [libero("Military · TEST", "ramping a singole", 1, "",
                       "es. 40×3, 45×2, 50×1, 55×1, 57,5×1, poi +2,5"),
                kg("Pressa · leggera", 160, 5, 3), libero("Lat machine", serie=5), libero("Core")],
        "gio": [libero("Panca piana · TEST", "ramping a singole", 1, "",
                       "60×4, 70×2, 80×1, 90×1, 100×1, 110×1, 120×1, poi 127,5 e se va 130"),
                libero("Pulley", serie=5, nota="leggero")],
        "ven": [libero("Pressa · TEST 6RM", "ramping", 6, "", "es. 120×5, 160×5, 200×3, poi a salire; rif. 200×6"),
                libero("Core", nota="niente stacco: nessun test")],
    }})

dati = {"inizio": INIZIO.isoformat(), "massimali": MASSIMALI, "settimane": settimane}
with open("programma.json", "w", encoding="utf-8") as f:
    json.dump(dati, f, ensure_ascii=False, indent=1)
print("programma.json:", len(settimane), "settimane")
