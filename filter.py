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
    "RÁDIO",
    "PLUTO",
    "INTERNACIONAL",
    "TURCA",
    "MÚSICA",
]

r = requests.get(SOURCE, timeout=60)
r.raise_for_status()

lines = r.text.splitlines()

result = []
current_block = []
remove_block = False

for line in lines:

    # Começou um novo canal
    if line.startswith("#EXTINF:"):

        # Salva o canal anterior somente se ele não estiver marcado para remoção
        if current_block and not remove_block:
            result.extend(current_block)

        # Começa o novo canal
        current_block = [line]

        # Analisa a linha inteira do EXTINF
        info = line.casefold()

        # Verifica os termos que devem ser removidos
        remove_block = any(
            termo.casefold() in info
            for termo in REMOVE
        )

    else:
        # Adiciona a URL e demais linhas ao canal atual
        current_block.append(line)

# Salva o último canal
if current_block and not remove_block:
    result.extend(current_block)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"Lista atualizada: {len(result)} linhas.")
