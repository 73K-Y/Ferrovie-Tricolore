"""
Importa il corridoio ferroviario reale Torino Porta Nuova - Genova Brignole
dentro Blender, come tante curve separate (una per binario/segmento OSM reale).

USO:
1. Apri Blender, vai su Scripting (in alto)
2. Apri questo file (o incollane il contenuto in un nuovo script)
3. Cambia CSV_PATH sotto con il percorso reale del file CSV sul tuo PC
4. Esegui (tasto Play, o Alt+P)

Scala: 1502.4 studs/km, stessa origine di tutto il progetto Roblox
(Torino Porta Nuova = 0,0). 1 stud Roblox = 1 unita' Blender in questo import,
cosi' quello che modelli qui corrisponde 1:1 a quello che poi importi su Roblox.

Nota importante: l'estensione totale del corridoio e' di circa 155.000 x 112.000
unita' - Roblox non accetta parti singole sopra i 2048 studs per asse, quindi
quando esporti da Blender dovrai comunque spezzare la mesh in segmenti piu' corti
(qui trovi gia' il corridoio diviso per binario reale, un buon punto di partenza).
"""

import bpy
import csv
from collections import defaultdict

CSV_PATH = "corridoio_torino_genova_coordinate.csv"  # <-- cambia con il percorso vero sul tuo PC

# raggruppo i punti per segmento
segmenti = defaultdict(list)
nomi_segmenti = {}

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for riga in reader:
        seg_id = int(riga['segmento_id'])
        x = float(riga['x_studs'])
        z = float(riga['z_studs'])
        segmenti[seg_id].append((x, 0.0, z))  # Y=0, il binario e' piatto sul terreno
        nomi_segmenti[seg_id] = riga['nome_linea'] or f"Segmento_{seg_id}"

# collezione dedicata, per tenere tutto ordinato
collezione = bpy.data.collections.new("CorridoioTorinoGenova")
bpy.context.scene.collection.children.link(collezione)

creati = 0
for seg_id, punti in segmenti.items():
    if len(punti) < 2:
        continue

    nome = nomi_segmenti[seg_id]
    curva_data = bpy.data.curves.new(name=f"{nome}_{seg_id}", type='CURVE')
    curva_data.dimensions = '3D'
    curva_data.bevel_depth = 0.7  # spessore visivo del binario, aggiustabile

    spline = curva_data.splines.new('POLY')
    spline.points.add(len(punti) - 1)
    for i, (x, y, z) in enumerate(punti):
        spline.points[i].co = (x, y, z, 1.0)

    oggetto = bpy.data.objects.new(f"{nome}_{seg_id}", curva_data)
    collezione.objects.link(oggetto)
    creati += 1

print(f"Importati {creati} binari reali dentro la collezione 'CorridoioTorinoGenova'")
