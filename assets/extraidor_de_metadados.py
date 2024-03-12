from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1, TIT2
from PIL import Image
from io import BytesIO

def extrair_metadados_musica(nome_arquivo):
    try:
        audio = MP3(nome_arquivo, ID3=ID3)
        capa = None
        nome_musica = None
        nome_artista = None

        if 'TIT2' in audio:
            nome_musica = audio['TIT2'].text[0]

        if 'TPE1' in audio:
            nome_artista = audio['TPE1'].text[0]

        return nome_musica, nome_artista

    except Exception as e:
        print("Erro ao extrair metadados:", e)
        return None, None

# # Exemplo de uso:
# nome_arquivo = 'caminho/para/sua/musica.mp3'
# capa, nome_musica, nome_artista = extrair_metadados_musica(nome_arquivo)

# if capa:
#     capa.show()  # Mostra a capa da música
# print("Nome da música:", nome_musica)
# print("Nome do artista:", nome_artista)
