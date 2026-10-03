import requests

# 1. Configurações da Lista 1 (Canais)
SOURCE_TV = "https://short.gy"
REMOVE_TV = [
    "novelas", "pluto tv", "pluto series", "manotv", 
    "quer um test chama", "doação pix", "atualizado", 
    "hallo", "música", "rádios", "pluto", "internacional", "novelas turca"
]

# 2. Configurações da Lista 2 (Servidor de Filmes - Autenticação Xtream Codes)
# Separamos os dados para injetar corretamente na requisição do servidor
SERVER_URL = "http://jphdear.net"
USERNAME = "Eliop2"
PASSWORD = "SmTg36371"

OUTPUT = "lista.m3u"

# User-Agent idêntico ao de um aplicativo de TV para o servidor não bloquear
headers = {
    "User-Agent": "Mozilla/5.0 (QtEmbedded; Linux; arm_64) AppleWebKit/537.36 (KHTML, like Gecko) IPTV/1.0.0"
}

result = []
EPG_LIMPO = '#EXTM3U url-tvg="https://githubusercontent.com"'
result.append(EPG_LIMPO)

# ==========================================
# PARTE 1: PROCESSANDO OS CANAIS (LISTA 1)
# ==========================================
try:
    print(f"Buscando canais de: {SOURCE_TV}")
    r = requests.get(SOURCE_TV, headers=headers, timeout=60, allow_redirects=True)
    r.raise_for_status()
    lines_tv = r.text.splitlines()
    
    skip = False
    for line in lines_tv:
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#EXTM3U"):
            continue

        if clean_line.startswith("#EXTINF:"):
            info = clean_line.lower()
            skip = any(term in info for term in REMOVE_TV)
            if not skip:
                result.append(clean_line)
        elif clean_line.startswith(("http://", "https://")):
            if not skip:
                result.append(clean_line)
            skip = False
        else:
            if not skip and clean_line.startswith("#"):
                result.append(clean_line)
                
    print(f"Canais processados com sucesso. Total parcial: {len(result)} linhas.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar a lista de canais: {e}")


# ==========================================
# PARTE 2: AUTENTICANDO E EXTRAINDO OS FILMES
# ==========================================
# Testamos as duas portas mais comuns de painéis IPTV caso a padrão falhe
ports_to_try = [":80", ":8080", ""] 
movies_downloaded = False

for port in ports_to_try:
    if movies_downloaded:
        break
        
    # Monta a URL de API nativa do Xtream Codes para forçar apenas filmes (get.php)
    api_url = f"{SERVER_URL}{port}/get.php?username={USERNAME}&password={PASSWORD}&action=get_vod_streams&output=mpegts"
    
    try:
        print(f"Tentando autenticar no servidor de filmes usando a porta {port if port else 'padrão'}...")
        r = requests.get(api_url, headers=headers, timeout=30, allow_redirects=True)
        
        # Se retornar 200 e houver conteúdo M3U válido ou links de vídeo
        if r.status_code == 200 and ("#EXTINF" in r.text or "http" in r.text):
            lines_movies = r.text.splitlines()
            movies_count = 0
            
            for line in lines_movies:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#EXTM3U"):
                    continue
                
                # Como a API 'get_vod_streams' só traz filmes, injetamos tudo direto sem precisar filtrar nomes
                if clean_line.startswith("#EXTINF:"):
                    result.append(clean_line)
                    movies_count += 1
                elif clean_line.startswith(("http://", "https://")):
                    result.append(clean_line)
                    
            print(f"Sucesso! Foram importados {movies_count} filmes do seu servidor privado.")
            movies_downloaded = True
            
    except requests.exceptions.RequestException:
        continue

if not movies_downloaded:
    print("Aviso: Não foi possível extrair os filmes. Verifique se o servidor está online ou se as credenciais expiraram.")


# ==========================================
# SALVAMENTO FINAL DO ARQUIVO UNIFICADO
# ==========================================
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"\nProcesso concluído!")
print(f"Arquivo final '{OUTPUT}' gerado com {len(result)} linhas no total.")
