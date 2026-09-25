import requests

SOURCE = "https://cr7v.short.gy/TV"
OUTPUT = "lista.m3u"

REMOVE = [
    "novelas",
    "pluto tv",
    "pluto series",
    "manotv",
    "quer um test chama",
    "doação pix",
    "atualizado",
    "hallo",
    "MÚSICA",
    "RÁDIOS",
    "PLUTO",
    "INTERNACIONAL",
    "NOVELAS TURCA",
    "MÚSICA",
]

r = requests.get(SOURCE, timeout=60)
r.raise_for_status()

lines = r.text.splitlines()

result = []
skip = False

for line in lines:
    if line.startswith("#EXTINF:"):
        info = line.lower()
        skip = any(term in info for term in REMOVE)

        if not skip:
            result.append(line)

    elif line.startswith(("http://", "https://")):
        if not skip:
            result.append(line)

    else:
        if not skip:
            result.append(line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print("Lista atualizada com sucesso.")
