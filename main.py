import flet as ft
from assets import verificador_de_musicas, extraidor_de_metadados, extraidor_de_capa

def main(page: ft.Page):
    page.bgcolor = '2d2d2d'

    chave = ()
    diretorio_musicas = 'assets/musicas/'
    musicas, musicas_com_diretorio = verificador_de_musicas.listar_musicas(diretorio_musicas)

    audio1 = ft.Audio(
        src=musicas_com_diretorio[0],
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
    page.overlay.append(audio1)
    page.update()

    img_capa = ft.Image(
                    src=f"capatst.png",
                    width=400,
                    height=400,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=ft.border_radius.all(10),
                    gapless_playback=True
                    )
    
    informacoes_musica = ft.ListView(
        [
            ft.Text('Nenhuma musica tocando.', theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.W_900),
            ft.Text('Sem Artista.', color=ft.colors.GREY)
        ]
    )

    lista_musicas = ft.ListView(
        expand=True,
    )

    coluna_bibliotecas = ft.Container(
        width=400,
        border_radius=5,
        bgcolor=ft.colors.GREY_900
    )

    coluna_lm = ft.Container(
        content=lista_musicas,
        expand=True,
        border_radius=5,
        bgcolor=ft.colors.GREY_900
        )
    coluna_info = ft.Container(
        content=ft.Column(
            [
                img_capa,
                informacoes_musica
            ],
        alignment=ft.alignment.top_right
        ),
        width=400,
        border_radius=5,
        bgcolor=ft.colors.GREY_900
    )

    coluna_controles = ft.Container(
        height=80,
        bgcolor=ft.colors.BLACK,
        border_radius=5,
        )
    
    page.add(ft.Row([coluna_bibliotecas, coluna_lm, coluna_info], expand=True))
    page.add(coluna_controles)
    page.update()

    imagem_controlhe = ft.ListView(
        [ft.Row([
            ft.Image(
                    src='/assets/cache_musicas/capatst.png',
                    width=80,
                    height=80,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=10
                ),
            ft.ListView([
            ft.Text('Nenhuma musica tocando.', weight=ft.FontWeight.W_900),
            ft.Text('nenhum artista.', color=ft.colors.GREY)
            ])
                ])
        ], width=80
    )

    lista_de_controles = ft.ListView([
            ft.Row([
                ft.IconButton(
                    icon_color=ft.colors.GREY,
                    icon=ft.icons.SHUFFLE_ROUNDED,
                    selected_icon_color=ft.colors.WHITE
                ),
                ft.IconButton(
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.SKIP_PREVIOUS_ROUNDED,
                ),
                ft.IconButton(
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.PLAY_CIRCLE_ROUNDED,
                    selected_icon=ft.icons.PAUSE_CIRCLE_ROUNDED,
                    icon_size=40
                ),
                ft.IconButton(
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.SKIP_NEXT_ROUNDED,
                ),
                ft.IconButton(
                    icon_color=ft.colors.GREY,
                    icon=ft.icons.LOOP_ROUNDED,
                    selected_icon_color=ft.colors.WHITE
                ),
            
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True),
            ft.Row([
                ft.Text('0:0'),
                ft.Slider(value=100, height=10, width=500, scale=0.7),
                ft.Text('0:0'),
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
            ], expand=True)

    coluna_controles.content = ft.Row([imagem_controlhe, lista_de_controles, ft.Row([ft.Icon(ft.icons.AUDIOTRACK_ROUNDED), ft.Slider(value=100)])])
    coluna_controles.update()

    def carregamento_de_musicas_bibliotecas(musicas, lista_musicas):
        if len(lista_musicas.controls) > 0:
            lista_musicas.controls.pop(len(lista_musicas.controls) - 1)
        else:
             pass
        for i in musicas:
            lista_musicas.controls.append(
                ft.Container(
                ft.ListTile(
                        leading=ft.Icon(ft.icons.ALBUM),
                        title=ft.Text(i),
                        subtitle=ft.Text(
                        "Artista desconhecido"
                            ),
                        ),
                bgcolor='2d2d2d',
                )
            )
        lista_musicas.update()

    def carregamento_de_musicas(musicas, lista_musicas):
        lista_musicas.controls = None
        lista_musicas.update()
        for i in musicas:
            nome_musica, nome_artista = extraidor_de_metadados.extrair_metadados_musica(f'assets/musicas/{i}')
            if nome_musica == None:
                nome_musica = i
            if nome_artista == None:
                nome_artista = 'Artista desconhecido.'
            lista_musicas.controls.append(
                ft.Container(
                ft.ListTile(
                        leading=ft.Image('assets/cache_musicas/capa.jpg', width=50, height=50),
                        title=ft.Text(nome_musica),
                        #on_click=,
                        subtitle=ft.Text(nome_artista),
                        ),
                bgcolor=ft.colors.BLACK,
                padding=2
                )
            )
        #lista_musicas.update()

    def valores_bibliotecas(biblioteca_escolhida):
        bibliotecas_amontadas = {}
        with open('assets/bibliotecas.txt', 'r') as arquivo:
                # Iterar sobre cada linha do arquivo
                for linha in arquivo:
                    # Remover espaços em branco e quebras de linha
                    linha = linha.strip()
                    
                    # Dividir a linha em duas partes usando "°º°" como separador
                    nome, informacoes = linha.split("..._.", 1)
                    
                    # Adicionar ao dicionário, usando o nome como chave e as informações como valor
                    bibliotecas_amontadas[nome] = informacoes
        for chave, valor in bibliotecas_amontadas.items():
            if biblioteca_escolhida == chave:
                return valor.split('...__.')

    def carregamento_de_musicas_bibliotecas(e):
        #print(valores_bibliotecas(e.control.key))
        if e.control.key == 'todas as musicas':
            carregamento_de_musicas(musicas, lista_musicas)
            lista_musicas.update()
        else:
            carregamento_de_musicas(valores_bibliotecas(e.control.key), lista_musicas)
            lista_musicas.update()

    def bibliotecas(carregamento_de_musicas, lista_musicas):
        bibliotecas_amontadas = {}
        with open('assets/bibliotecas.txt', 'r') as arquivo:
            # Iterar sobre cada linha do arquivo
            for linha in arquivo:
                # Remover espaços em branco e quebras de linha
                linha = linha.strip()
                
                # Dividir a linha em duas partes usando "°º°" como separador
                nome, informacoes = linha.split("..._.", 1)
                
                # Adicionar ao dicionário, usando o nome como chave e as informações como valor
                bibliotecas_amontadas[nome] = informacoes
        items = []

        for chave, valor in bibliotecas_amontadas.items():
            items.append(
                ft.Container(
                    content=ft.ListView([ft.Row([ft.Image(src=f'/assets/capas_biblioteca/{chave}.jpg', width=80, height=80), ft.Text(value=chave)])]),
                    #alignment=ft.alignment.center,
                    bgcolor='2d2d2d',
                    width=80,
                    height=80,
                    on_click=carregamento_de_musicas_bibliotecas,
                    border_radius=ft.border_radius.all(5),
                    key=chave
                )
            )
        return items
    
    carregamento_de_musicas(musicas, lista_musicas)
    lista_musicas.update()
    coluna_bibliotecas.content = ft.ListView(bibliotecas(carregamento_de_musicas, lista_musicas))
    coluna_bibliotecas.update()

ft.app(target=main, view=ft.WebRenderer, host='127.0.0.1', port=8080)