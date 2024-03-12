import random, os
import flet as ft
import PySimpleGUI as sg
from assets import verificador_de_musicas, extraidor_de_metadados, extraidor_de_capa

def main(page: ft.Page):
    global indice_da_musica, indice_da_musica_max, auto_next_on_off, loop, alt, DIRETORIO_CAPA_PRINCIPAL, DIRETORIO_CACHE_MUSICAS, DIRETORIO_MUSICAS
    page.bgcolor = '2d2d2d'
    page.title = 'Next Player'
    page.padding = 0
    page.window_min_width = 1150
    page.window_min_height = 600

    auto_next_on_off = True
    loop = True
    alt = False

    DIRETORIO_CACHE_MUSICAS = 'assets/cache_musicas/'
    DIRETORIO_CAPA_PRINCIPAL = 'assets/next_player.png'
    DIRETORIO_CAPA_PRINCIPAL_ICO = 'assets/next_player.ico'
    sg.theme('PythonPlus')
    DIRETORIO_MUSICAS = sg.PopupGetFolder('Selecione o Diretorio da Musica:', icon=DIRETORIO_CAPA_PRINCIPAL_ICO)
    if DIRETORIO_MUSICAS == None:
        page.window_destroy()
        page.update()
    elif DIRETORIO_MUSICAS == '':
        page.window_destroy()
        page.update()

    def deletar_arquivos(diretorio):
        """
        Deleta todos os arquivos dentro de um diretório, mantendo o diretório intacto.

        Args:
            diretorio (str): O caminho para o diretório contendo os arquivos a serem deletados.
            
        Returns:
            bool: True se a deleção foi bem-sucedida, False caso contrário.
        """
        try:
            # Garante que o diretório existe
            if os.path.exists(diretorio):
                # Remove todos os arquivos do diretório
                for arquivo in os.listdir(diretorio):
                    caminho_arquivo = os.path.join(diretorio, arquivo)
                    if os.path.isfile(caminho_arquivo):
                        os.remove(caminho_arquivo)
                print(f"Todos os arquivos dentro do diretório '{diretorio}' foram deletados com sucesso.")
                return True
            else:
                print(f"O diretório '{diretorio}' não existe.")
                return False
        except Exception as e:
            print(f"Erro ao deletar os arquivos dentro do diretório '{diretorio}': {e}")
            return False

    def window_event(e):
        global DIRETORIO_CACHE_MUSICAS
        if e.data == "close":
            deletar_arquivos(DIRETORIO_CACHE_MUSICAS)
            page.window_destroy()
            page.update()

    page.window_prevent_close = True
    page.on_window_event = window_event

    def milissegundos_para_horas_min_seg(milissegundos):
        segundos = milissegundos // 1000
        minutos = segundos // 60
        horas = minutos // 60
        minutos_restantes = minutos % 60
        segundos_restantes = segundos % 60
        return horas, minutos_restantes, segundos_restantes
    def slider_tr(e):
        global auto_next_on_off
        audio1.seek(int(e.control.value))
    try:
        musicas, musicas_com_diretorio = verificador_de_musicas.listar_musicas(DIRETORIO_MUSICAS)
        if musicas == []:
            page.window_destroy()
            page.update()
        indice_da_musica = 0
        indice_da_musica_max = len(musicas)
    except:
        pass
    #print(indice_da_musica_max)

    tempo_agr = ft.Text(value='0:0')
    slider_tempo = ft.Slider(min=0, max=100, height=10, width=400, on_change=slider_tr)
    tempo_maximo = ft.Text(value='0:0')

    def trocador_valor_slider(e):
            try:
                duracao = milissegundos_para_horas_min_seg(audio1.get_duration())
                posicao_duracao = milissegundos_para_horas_min_seg(audio1.get_current_position())
                if duracao[0] == 0:
                    tempo_maximo.value = f'{duracao[1]}:{duracao[2]}'
                    tempo_agr.value = f'{posicao_duracao[1]}:{posicao_duracao[2]}'
                else:
                    tempo_maximo.value = f'{duracao[0]}:{duracao[1]}:{duracao[2]}'
                    tempo_agr.value = f'{posicao_duracao[0]}:{posicao_duracao[1]}:{posicao_duracao[2]}'
                slider_tempo.max = audio1.get_duration()
                slider_tempo.value = audio1.get_current_position()
                tempo_maximo.update()
                tempo_agr.update()
                slider_tempo.update()
            except:
                pass
    
    def auto_next():
        global indice_da_musica, indice_da_musica_max, auto_next_on_off, loop, alt
        print('ok')
        if alt == False:
            if auto_next_on_off == True:
                if indice_da_musica == indice_da_musica_max - 1:
                    if loop == True:
                        indice_da_musica = 0
                        print('ok1')
                        tocador_de_musica()
                else:
                    indice_da_musica += 1
                    print('ok2')
                    tocador_de_musica()
        else:
            indice_da_musica = random.randint(0, indice_da_musica_max - 1)
            print('ok3')
            tocador_de_musica()
    
    def funcoes_musica(e):
        global loop, alt
        print(e.control.data)
        if e.control.selected == False:
            e.control.selected = True
        else:
            e.control.selected = False
        e.control.update()
        if e.control.data == 'loop':
            if loop == True:
                loop = False
            else:
                loop = True
        elif e.control.data == 'alt':
            if alt == True:
                alt = False
            else:
                alt = True

    def skip_musicas(e):
        global indice_da_musica, indice_da_musica_max, auto_next_on_off, loop, alt
        #print(e.control.data)
        if e.control.data == 1:
            if alt == False:
                if indice_da_musica == indice_da_musica_max - 1:
                    if loop == True:
                        indice_da_musica = 0
                        print('ok1')
                        tocador_de_musica()
                else:
                    indice_da_musica += e.control.data
                    print('ok2')
                    tocador_de_musica()
            else:
                indice_da_musica = random.randint(0, indice_da_musica_max - 1)
                print('ok3')
                tocador_de_musica()
        elif e.control.data == -1:
            if indice_da_musica == 0:
                if loop ==True:
                    indice_da_musica  = indice_da_musica_max - 1
                    tocador_de_musica()
            else:
                indice_da_musica += e.control.data
                tocador_de_musica()

    def trocador_de_volume(e):
        audio1.volume = e.control.value
        audio1.update()
    
    def estado_da_musica(e):
        resume_pause_var.append(e.data)
        print('ok', e.data)
        if e.data == 'completed':
            print('ok3')
            auto_next()


    resume_pause_var = ['paused']

    audio1 = ft.Audio(
        src=musicas_com_diretorio[0],
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_position_changed=lambda e: trocador_valor_slider(e),
        on_state_changed=lambda e: estado_da_musica(e),
    )
    page.overlay.append(audio1)
    page.update()

    def pausa_despausar(e):
        #print(resume_pause_var[0], 'ok')
        if resume_pause_var[0] == 'paused':
            #print('ok')
            audio1.resume()
            resume_pause_var[0] = 'stopped'
            e.control.selected = True
            e.control.update()
        else:
            audio1.pause()
            e.control.selected = False
            e.control.update()
            resume_pause_var[0] = 'paused'

    img_capa = ft.Image(
                    src=DIRETORIO_CAPA_PRINCIPAL,
                    width=400,
                    height=400,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                    gapless_playback=True
                    )
    
    img_capa2 = ft.Image(
                    src=DIRETORIO_CAPA_PRINCIPAL,
                    width=80,
                    height=80,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                    gapless_playback=True
                    )
    
    informacoes_musica = ft.ListView(
        [
            ft.Text('Nenhuma musica tocando.', theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.W_900, width=300),
            ft.Text('Sem Artista.', color=ft.colors.GREY, width=300)
        ]
    )
    informacoes_musica2 = ft.ListView(
        [
            ft.Text('Nenhuma musica tocando.', theme_style=ft.TextThemeStyle.TITLE_SMALL, width=200)
        ]
    )

    lista_musicas = ft.ListView(
        expand=True,
    )

    coluna_lm = ft.Container(
        content=lista_musicas,
        expand=True,
        bgcolor=ft.colors.GREY_900,
        border_radius=10,
        )
    coluna_info = ft.Container(
        content=ft.Column(
            [
                img_capa,
                informacoes_musica
            ],
        alignment=ft.alignment.top_right,
        width=400,
        expand=True,
        ),
        width=400,
        bgcolor=ft.colors.GREY_900,
        border_radius=10,
    )

    coluna_controles = ft.Container(
        height=80,
        bgcolor=ft.colors.BLACK,
        border_radius=10,
        )
    
    page.add(ft.Row([coluna_lm, coluna_info], expand=True))
    page.add(coluna_controles)
    page.update()

    imagem_controlhe = ft.ListView(
        [ft.Row([
            img_capa2,
            ft.ListView([
            informacoes_musica2
            ], width=200, height=80)
                ], width=200, height=80)
        ], width=200, height=80,
    )

    play_pause_botao = ft.IconButton(
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.PLAY_CIRCLE_ROUNDED,
                    selected_icon=ft.icons.PAUSE_CIRCLE_ROUNDED,
                    on_click=pausa_despausar,
                    icon_size=40
                    )
    alt_botao = ft.IconButton(
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.SHUFFLE_ROUNDED,
                    selected_icon=ft.icons.SHUFFLE_ROUNDED,
                    selected_icon_color=ft.colors.BLUE,
                    data='alt',
                    on_click=funcoes_musica,
                    )
    loop_botao = ft.IconButton(
                    selected=True,
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.LOOP_ROUNDED,
                    selected_icon=ft.icons.LOOP_ROUNDED,
                    selected_icon_color=ft.colors.BLUE,
                    data='loop',
                    on_click=funcoes_musica,
                )

    lista_de_controles = ft.ListView([
            ft.Row([
                alt_botao,
                ft.IconButton(
                    data=-1,
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.SKIP_PREVIOUS_ROUNDED,
                    on_click=skip_musicas
                ),
                play_pause_botao,
                ft.IconButton(
                    data=1,
                    icon_color=ft.colors.WHITE,
                    icon=ft.icons.SKIP_NEXT_ROUNDED,
                    on_click=skip_musicas
                ),
                loop_botao,
            
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True),
            ft.Row([
                tempo_agr,
                slider_tempo,
                tempo_maximo,
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
            ], expand=True)

    coluna_controles.content = ft.Row([imagem_controlhe, lista_de_controles, ft.Row([ft.Icon(ft.icons.AUDIOTRACK_ROUNDED), ft.Slider(min=0, value=1, max=1, on_change=trocador_de_volume)])])
    coluna_controles.update()

    def tocador_de_musica(e=None):
        global indice_da_musica, auto_next_on_off, DIRETORIO_CAPA_PRINCIPAL
        try:
            if e != None:
                if type(e.control.data) == int:
                    indice_da_musica = e.control.data
                print(e.control.data)
        except:
            pass
        if musicas_com_diretorio[indice_da_musica] == audio1.src:
            pass
        else:
            print(musicas_com_diretorio[indice_da_musica])
            #print(e.control.data, 'oi')
            resume_pause_var[0] = 'stopped'
            play_pause_botao.selected = True
            play_pause_botao.update()
            audio1.src = musicas_com_diretorio[indice_da_musica]
            audio1.update()
            audio1.release()
            audio1.play()
            nome_musica, nome_artista = extraidor_de_metadados.extrair_metadados_musica(musicas_com_diretorio[indice_da_musica])
            if nome_musica == None:
                nome_musica = musicas[indice_da_musica]
            if nome_artista == None:
                nome_artista = 'Artista desconhecido.'
            if extraidor_de_capa.extrair_capa(musicas_com_diretorio[indice_da_musica], f'{DIRETORIO_CACHE_MUSICAS}{musicas[indice_da_musica]}') == None:
                imagem = DIRETORIO_CAPA_PRINCIPAL
            else:
                imagem = f'{DIRETORIO_CACHE_MUSICAS}{musicas[indice_da_musica]}'
            informacoes_musica.controls.clear()
            informacoes_musica2.controls.clear()
            informacoes_musica.controls.append(ft.Text(nome_musica, theme_style=ft.TextThemeStyle.TITLE_SMALL, weight=ft.FontWeight.W_900, width=300))
            informacoes_musica.controls.append(ft.Text(nome_artista, color=ft.colors.GREY, width=300))
            informacoes_musica.update()
            informacoes_musica2.controls.append(ft.Text(nome_musica, theme_style=ft.TextThemeStyle.TITLE_SMALL, width=200))
            informacoes_musica2.controls.append(ft.Text(nome_artista, color=ft.colors.GREY, width=200))
            informacoes_musica2.update()
            img_capa.src = imagem
            img_capa2.src = imagem
            img_capa.update()
            img_capa2.update()

    def carregamento_de_musicas(musicas, lista_musicas):
        global DIRETORIO_CAPA_PRINCIPAL, DIRETORIO_CACHE_MUSICAS
        lista_musicas.controls = None
        lista_musicas.update()
        for i in range(len(musicas)):
            nome_musica, nome_artista = extraidor_de_metadados.extrair_metadados_musica(musicas_com_diretorio[i])
            if nome_musica == None:
                nome_musica = musicas[i]
            if nome_artista == None:
                nome_artista = 'Artista desconhecido.'
            if extraidor_de_capa.extrair_capa(musicas_com_diretorio[i], f'{DIRETORIO_CACHE_MUSICAS}{musicas[i]}') == None:
                imagem = DIRETORIO_CAPA_PRINCIPAL
            else:
                imagem = f'{DIRETORIO_CACHE_MUSICAS}{musicas[i]}'
            lista_musicas.controls.append(
                ft.Container(
                ft.ListTile(
                        leading=ft.Image(imagem, width=50, height=50, fit=ft.ImageFit.COVER, border_radius=10),
                        title=ft.Text(nome_musica),
                        data=i,
                        on_click=tocador_de_musica,
                        subtitle=ft.Text(nome_artista),
                        ),
                bgcolor=ft.colors.BLACK,
                padding=2,
                )
            )
        #lista_musicas.update()    
    carregamento_de_musicas(musicas, lista_musicas)
    lista_musicas.update()


ft.app(target=main)
