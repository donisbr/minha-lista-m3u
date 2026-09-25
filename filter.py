import requests

SOURCE = "https://cr7v.short.gy/TV"
OUTPUT = "lista.m3u"

REMOVE = [
    "novelas",
    "pluto tv",
     "MANOTV TVG-CHNO=1",
     "QUER UM TEST CHAMA" tvg-chno="3",Whats 75991634025",
      "DOAÇÃO PIX" tvg-chno="2",75 991634025",
       "ATUALIZADO" tvg-chno="4",21/09/26",
        "pluto tv",
] 

r = requests.get(SOURCE, timeout=60)
r.raise_for_status()

lines = r.text.splitlines()

result = []
skip = False

for line in lines:
    if line.startswith("#EXTINF:"):
        channel_info = line.lower()
        skip = any(term in channel_info for term in REMOVE)

        if not skip:
            result.append(line)

    elif line.startswith("http://") or line.startswith("https://"):
        if not skip:
            result.append(line)

    else:
        if not skip:
            result.append(line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print("Lista atualizada.")
