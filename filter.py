import requests

SOURCE = "https://cr7v.short.gy/TV"
OUTPUT = "lista.m3u"

REMOVE = [
 REMOVE = [
    "novelas",
    "pluto tv",
    "pluto series",
    "manotv",
    "quer um test chama",
    "doação pix",
    "atualizado",
]

r = requests.get(SOURCE, timeout=60)
r.raise_for_status()

lines = r.text.splitlines()

result = []
skip = False

for line in lines:

    # Identifica o início de um canal
    if line.startswith("#EXTINF:"):

        # Converte para minúsculas para facilitar a comparação
        info = line.lower()

        # Verifica se algum termo proibido aparece na linha inteira
        skip = any(term in info for term in REMOVE)

        if not skip:
            result.append(line)

    # URL pertencente ao canal anterior
    elif line.startswith(("http://", "https://")):

        if not skip:
            result.append(line)

    # Outras linhas da M3U
    else:

        if not skip:
            result.append(line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print("Lista atualizada com sucesso.")
