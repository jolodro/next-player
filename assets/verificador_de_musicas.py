import os
#essa função def serve para pegar as musicas do diretorio e separar sô as musicas para ultilizar, atenção, ele não faz uma copia, e sim salva uma lista e quando ele quiser pegar um musica para TOCAR ele ele pega na lista o diretorio
def listar_musicas(caminho_pasta, act=False):
    nomes_arquivos = []
    caminhos_arquivos = []
    extensoes_musicas = ['.mp3', '.wav', '.flac']  # Lista de extensões de arquivos de música

    # Substitui as barras invertidas por barras inclinadas no estilo UNIX (para garantir compatibilidade)
    caminho_pasta = caminho_pasta.replace('\\', '/')

    # Verifica se o caminho fornecido é um diretório
    if os.path.isdir(caminho_pasta):
        # Percorre todos os arquivos e pastas dentro do diretório fornecido
        for nome_arquivo in os.listdir(caminho_pasta):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            
            # Verifica se o caminho é um arquivo
            if os.path.isfile(caminho_completo):
                # Verifica se a extensão do arquivo está na lista de extensões de música
                _, extensao = os.path.splitext(nome_arquivo)
                if extensao.lower() in extensoes_musicas:
                    nomes_arquivos.append(nome_arquivo)
                    caminhos_arquivos.append(caminho_completo)
            caminhos_arquivos_refeito = []
            for nd in caminhos_arquivos:
                caminhos_arquivos_refeito.append(nd.replace('\\', '/'))
    if act == True:
        nomes_arquivos = sorted(nomes_arquivos, reverse=True)
        caminhos_arquivos_refeito = sorted(caminhos_arquivos_refeito, reverse=True)

    return nomes_arquivos, caminhos_arquivos_refeito

"""# Diretório a ser listado
diretorio = 'musicas'

nomes, caminhos = listar_musicas(diretorio)

print("Nomes dos arquivos de música na pasta:")
print(nomes)

print("\nCaminhos completos dos arquivos de música na pasta:")
print(caminhos)"""

