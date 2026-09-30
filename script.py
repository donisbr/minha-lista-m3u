import requests

# URL real da sua lista fornecedora original (coloque o link completo da sua fonte aqui)
SOURCE = "https://coloque_aqui_o_link_da_sua_fonte_original.m3u8"
OUTPUT = "lista.m3u"

# Termos para remover da lista de canais (sempre em letras minúsculas)
REMOVE = [
    "novelas", "pluto tv", "pluto series", "manotv", 
    "quer um test chama", "doação pix", "atualizado", 
    "hallo", "música", "rádios", "pluto", "internacional", "novelas turca"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    print(f"Buscando lista de: {SOURCE}")
    r = requests.get(SOURCE, headers=headers, timeout=60, allow_redirects=True)
    r.raise_for_status()
    lines = r.text.splitlines()
except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar a lista: {e}")
    exit(1)

result = []
skip = False

# Cabeçalho limpo com links de guias de programação (EPG) reais
EPG_LIMPO = '#EXTM3U url-tvg="https://githubusercontent.com"'
result.append(EPG_LIMPO)

for line in lines:
    clean_line = line.strip()
    if not clean_line or clean_line.startswith("#EXTM3U"):
        continue

    if clean_line.startswith("#EXTINF:"):
        info = clean_line.lower()
        skip = any(term in info for term in REMOVE)
        if not skip:
            result.append(clean_line)
    elif clean_line.startswith(("http://", "https://")):
        if not skip:
            result.append(clean_line)
        skip = False
    else:
        if not skip and clean_line.startswith("#"):
            result.append(clean_line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"Lista organizada com sucesso! Total de linhas salvas: {len(result)}")
