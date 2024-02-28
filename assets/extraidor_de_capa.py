from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

def extrair_capa(caminho_arquivo, caminho_destino):
    try:
        audio = MP3(caminho_arquivo, ID3=ID3)

        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                with open(caminho_destino, 'wb') as imagem:
                    imagem.write(tag.data)
                return True
                
        #Se a capa não for encontrada
        return None

    except Exception as e:
        print(f"Erro ao extrair a capa: {e}")
        return None

"""
# Caminho do arquivo de música
caminho_musica = 'musicas/flow.mp3'
# Caminho para salvar a imagem da capa
caminho_destino = 'capas(cache)/capa.jpg'

if extrair_capa(caminho_musica, caminho_destino):
    print(f"Capa extraída e salva em: {caminho_destino}")
else:
    print("Falha ao extrair a capa.")"""