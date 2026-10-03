import requests
import urllib3

# Desativa avisos de conexões inseguras (essencial para servidores IPTV que barram robôs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Configurações da Lista 1 (Canais)
SOURCE_TV = "https://short.gy"
REMOVE_TV = [
    "novelas", "pluto tv", "pluto series", "manotv", 
    "quer um test chama", "doação pix", "atualizado", 
    "hallo", "música", "rádios", "pluto", "internacional", "novelas turca"
]

# 2. Configurações da Lista 2 (Servidor Privado - URL Direta com Porta Comum de API)
# Testamos o link direto forçando a porta 8080 e o formato completo m3u_plus
SOURCE_MOVIES = "http://jphdear.net"

OUTPUT = "lista.m3u"

# User-Agent simulando o navegador Chrome completo atualizado para burlar firewalls de servidores
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
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
# PARTE 2: EXTRAINDO OS FILMES (LISTA 2)
# ==========================================
try:
    print(f"Conectando ao servidor jphdear.net para baixar os filmes...")
    # Usamos verify=False para ignorar bloqueios de SSL/TLS do painel IPTV
    r = requests.get(SOURCE_MOVIES, headers=headers, timeout=60, verify=False, allow_redirects=True)
    
    # Se a porta 8080 der erro ou não responder, tentamos na porta padrão automaticamente
    if r.status_code != 200:
        print("Porta 8080 recusada, tentando conectar através da porta padrão (80)...")
        URL_BACKUP = SOURCE_MOVIES.replace(":8080", "")
        r = requests.get(URL_BACKUP, headers=headers, timeout=60, verify=False, allow_redirects=True)

    r.raise_for_status()
    lines_movies = r.text.splitlines()
    
    keep_movie = False
    movies_count = 0
    
    for line in lines_movies:
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#EXTM3U"):
            continue
            
        if clean_line.startswith("#EXTINF:"):
            info_lower = clean_line.lower()
            
            # Filtro inteligente ultra amplo: valida se é filme/movie VOD (procurando na tag de grupo)
            # Evita puxar canais ao vivo caso o seu painel também tenha canais ativos
            if 'group-title=' in info_lower:
                if 'filme' in info_lower or 'movie' in info_lower or 'vod' in info_lower:
                    keep_movie = True
                    result.append(clean_line)
                    movies_count += 1
                else:
                    keep_movie = False
            else:
                # Se o arquivo vier sem grupo mas for link de mídia individual (.mp4, .mkv), aceita
                keep_movie = True
                result.append(clean_line)
                movies_count += 1
                
        elif clean_line.startswith(("http://", "https://")):
            if keep_movie:
                result.append(clean_line)
            keep_movie = False
            
    print(f"Filmes processados! Foram adicionados {movies_count} filmes encontrados.")

except requests.exceptions.RequestException as e:
    print(f"Não foi possível extrair os filmes do servidor. Detalhe do erro: {e}")


# ==========================================
# SALVAMENTO FINAL DO ARQUIVO UNIFICADO
# ==========================================
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"\nProcesso concluído!")
print(f"Arquivo final '{OUTPUT}' gerado com {len(result)} linhas no total.")
