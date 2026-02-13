diff --git a/README.md b/README.md
index accb54876256fa3a8fcbc04afa3b69972d8b7567..1a5a8f836edc5737a155d0e810146952e56f7408 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,85 @@
-# imp_coll
\ No newline at end of file
+# Verifica volume utile MDB (CLI)
+
+Tool Python 3 per verificare se i punti 3D di un tubo (letti da file `.mdb`) entrano nel volume utile di una macchina di collaudo, considerando il margine dato da diametro esterno e gioco.
+
+## Requisiti
+
+- Python 3.10+
+- Driver ODBC Microsoft Access installato (Windows):
+  - `Microsoft Access Driver (*.mdb, *.accdb)`
+  - incluso tipicamente in **Access Database Engine**
+- Dipendenze Python in `requirements.txt`
+
+## Installazione
+
+```bash
+python -m venv .venv
+source .venv/bin/activate  # su Windows: .venv\Scripts\activate
+pip install -r requirements.txt
+```
+
+## Configurazione (`config.yaml`)
+
+Esempio:
+
+```yaml
+machine:
+  Xmin: 0
+  Xmax: 3000
+  Zmin: 0
+  Zmax: 1500
+  Ymin: 0
+  Y1_max: 1200
+  Y2_max: 900
+  y_var_along: Z  # X oppure Z
+
+tube:
+  OD: 80
+  gioco: 10
+```
+
+Margine usato dal tool:
+
+- `m = OD/2 + gioco`
+
+## Esecuzione
+
+```bash
+python src/check_mdb.py \
+  --input ./cartella_mdb \
+  --config ./config.yaml \
+  --out ./results/esito.csv
+```
+
+Il tool:
+
+- legge tutti i `.mdb` nella cartella input
+- crea la cartella `results` se mancante
+- scrive un CSV con una riga per file
+- stampa avanzamento su console
+
+## Logica MDB
+
+Per ogni file `.mdb`:
+
+1. Elenca le tabelle.
+2. Usa `tbPuntiUVW` se presente e valida.
+3. Altrimenti cerca una tabella con colonne `X,Y,Z` (case-insensitive).
+4. Se è presente la colonna `Numero`, applica `ORDER BY Numero`.
+5. Scarta righe con valori `NULL` o non numerici.
+
+## Output CSV
+
+Colonne:
+
+- `file, table, n_points`
+- `xmin,xmax,ymin,ymax,zmin,zmax` (dopo traslazione)
+- `dx,dy,dz`
+- `result` (`PASS`/`FAIL`)
+- `max_violation_mm`
+- `note`
+
+## Note compatibilità
+
+- La connessione ODBC Access è prevista principalmente su Windows.
+- In ambienti Linux/macOS la lettura MDB può non funzionare senza driver compatibili.
