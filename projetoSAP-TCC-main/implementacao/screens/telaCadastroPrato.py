# screens/telaCadastroPrato.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from database import DatabaseManager
import os
import shutil
from PIL import Image  # Para redimensionamento opcional

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaCadastroPrato>:
    name: 'cadastro_prato'
    md_bg_color: 0.1, 0.1, 0.1, 1

    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(30)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "CADASTRO DE PRATO"
                font_name: "MontserratBold"
                font_size: "24sp"
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1] + dp(30)
                color: get_color_from_hex("#FFFFFF")
                valign: "middle"
                padding: [0, 0, 0, dp(50)]

            MDTextField:
                id: nome_prato
                hint_text: "Nome do Prato"
                mode: "rectangle"
                line_color_normal: 1, 1, 1, 1
                line_color_focus: get_color_from_hex("#2AB630")
                text_color: 1, 1, 1, 1
                hint_text_color: 0.7, 0.7, 0.7, 1
                font_name: "MontserratBold"
                size_hint_y: None
                height: dp(48)
                padding: dp(10)
                multiline: False
                size_hint_x: 0.9
                pos_hint: {'center_x': 0.5}

            MDTextField:
                id: preco
                hint_text: "Preço (R$)"
                mode: "rectangle"
                line_color_normal: 1, 1, 1, 1
                line_color_focus: get_color_from_hex("#2AB630")
                text_color: 1, 1, 1, 1
                hint_text_color: 0.7, 0.7, 0.7, 1
                font_name: "MontserratBold"
                size_hint_y: None
                height: dp(48)
                padding: dp(10)
                multiline: False
                size_hint_x: 0.9
                pos_hint: {'center_x': 0.5}
                input_filter: 'float'
                padding: [0, 0, 0, dp(20)]

            MDRaisedButton:
                id: categoria_btn
                text: "SELECIONE CATEGORIA"
                size_hint: None, None
                size: dp(250), dp(48)
                pos_hint: {'center_x': 0.5}
                md_bg_color: get_color_from_hex("#2AB630")
                text_color: 1, 1, 1, 1
                font_name: "MontserratBold"
                font_size: "16sp"
                on_release: root.abrir_menu_categorias()

            MDRaisedButton:
                id: imagem_btn
                text: "SELECIONAR IMAGEM"
                size_hint: None, None
                size: dp(250), dp(48)
                pos_hint: {'center_x': 0.5}
                md_bg_color: get_color_from_hex("#2AB630")
                text_color: 1, 1, 1, 1
                font_name: "MontserratBold"
                font_size: "16sp"
                on_release: root.abrir_seletor_imagem()

            BoxLayout:
                orientation: 'horizontal'
                size_hint: None, None
                size: dp(250), dp(48)
                pos_hint: {'center_x': 0.5}
                spacing: dp(10)

                MDRaisedButton:
                    text: "VOLTAR"
                    size_hint_x: 0.5
                    md_bg_color: get_color_from_hex("#CF1919")
                    text_color: 1, 1, 1, 1
                    font_name: "MontserratBold"
                    font_size: "16sp"
                    on_release: root.voltar_tela_gestao()

                MDRaisedButton:
                    text: "CADASTRAR"
                    size_hint_x: 0.5
                    md_bg_color: get_color_from_hex("#B8860B")
                    text_color: 1, 1, 1, 1
                    font_name: "MontserratBold"
                    font_size: "16sp"
                    on_release: root.cadastrar_prato()
'''

Builder.load_string(KV)

class TelaCadastroPrato(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_categorias = None
        self.categoria_selecionada = None
        self.caminho_imagem = None
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

    def on_pre_enter(self, *args):
        if not self.db_manager.connection.is_connected():
            self.db_manager.connect()
        
        self.carregar_categorias()

    def on_pre_leave(self, *args):
        if self.db_manager.connection.is_connected():
            self.db_manager.disconnect()

    def carregar_categorias(self):
        categorias = [
            {"text": "Prato Principal", "viewclass": "OneLineListItem", "on_release": lambda x="Prato Principal": self.selecionar_categoria(x)},
            {"text": "Sobremesa", "viewclass": "OneLineListItem", "on_release": lambda x="Sobremesa": self.selecionar_categoria(x)},
            {"text": "Bebidas", "viewclass": "OneLineListItem", "on_release": lambda x="Bebidas": self.selecionar_categoria(x)},
            {"text": "Lanches", "viewclass": "OneLineListItem", "on_release": lambda x="Lanches": self.selecionar_categoria(x)},
        ]
        
        self.menu_categorias = MDDropdownMenu(
            caller=self.ids.categoria_btn,
            items=categorias,
            width_mult=4,
            background_color=get_color_from_hex("#111213"),
            border_margin=dp(10),
            max_height=dp(200))

    def abrir_menu_categorias(self):
        if self.menu_categorias:
            self.menu_categorias.open()

    def selecionar_categoria(self, categoria):
        self.categoria_selecionada = categoria
        self.ids.categoria_btn.text = categoria
        if self.menu_categorias:
            self.menu_categorias.dismiss()

    def abrir_seletor_imagem(self):
        # Caminho absoluto para a pasta de pratos
        caminho_padrao = os.path.abspath("assets/pratos")
        
        # Cria a pasta se não existir
        if not os.path.exists(caminho_padrao):
            os.makedirs(caminho_padrao)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        filechooser = FileChooserIconView(
            path=caminho_padrao,  # Abre diretamente na pasta de pratos
            filters=['*.png', '*.jpg', '*.jpeg']
        )
        content.add_widget(filechooser)
        
        btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_cancelar = MDRaisedButton(
            text="CANCELAR",
            md_bg_color=get_color_from_hex("#CF1919"),
            text_color=(1, 1, 1, 1),
            size_hint_x=0.5
        )
        btn_cancelar.bind(on_release=lambda x: popup.dismiss())
        
        btn_selecionar = MDRaisedButton(
            text="SELECIONAR",
            md_bg_color=get_color_from_hex("#0C8811"),
            text_color=(1, 1, 1, 1),
            size_hint_x=0.5
        )
        btn_selecionar.bind(on_release=lambda x: self.selecionar_imagem(filechooser.path, filechooser.selection, popup))
        
        btn_box.add_widget(btn_cancelar)
        btn_box.add_widget(btn_selecionar)
        content.add_widget(btn_box)
        
        popup = Popup(
            title="Selecione a imagem do prato",
            content=content,
            size_hint=(0.9, 0.8),
            separator_color=get_color_from_hex("#0C8811"),
            title_color=(1, 1, 1, 1),
            background_color=get_color_from_hex("#111213")
        )
        popup.open()

    def selecionar_imagem(self, path, selection, popup):
        if selection:
            try:
                extensao = os.path.splitext(selection[0])[1].lower()
                if extensao not in ['.png', '.jpg', '.jpeg']:
                    self.mostrar_popup("Erro", "Formato inválido! Use .png, .jpg ou .jpeg")
                    return
                
                pasta_destino = os.path.abspath("assets/pratos")
                if not os.path.exists(pasta_destino):
                    os.makedirs(pasta_destino)
                
                nome_arquivo = os.path.basename(selection[0])
                destino = os.path.join(pasta_destino, nome_arquivo)
                
                # Copia o arquivo para a pasta de destino
                shutil.copy2(selection[0], destino)
                
                # Opcional: Redimensionar a imagem
                try:
                    img = Image.open(destino)
                    img = img.resize((800, 600))  # Tamanho padrão
                    img.save(destino)
                except Exception as e:
                    print(f"Erro ao redimensionar imagem: {e}")
                
                self.caminho_imagem = nome_arquivo
                self.ids.imagem_btn.text = f"Imagem: {nome_arquivo}"
                
            except Exception as e:
                print(f"Erro ao processar imagem: {e}")
                self.mostrar_popup("Erro", "Não foi possível salvar a imagem")
        
        popup.dismiss()

    def cadastrar_prato(self):
        nome = self.ids.nome_prato.text.strip()
        preco = self.ids.preco.text.strip()
        
        if not nome or not preco or not self.categoria_selecionada:
            self.mostrar_popup("Erro", "Nome, preço e categoria são obrigatórios!")
            return
            
        try:
            preco_float = float(preco)
            if preco_float <= 0:
                self.mostrar_popup("Erro", "O preço deve ser maior que zero!")
                return
        except ValueError:
            self.mostrar_popup("Erro", "Preço inválido! Use números decimais (ex: 25.90)")
            return
            
        if not self.db_manager.connection.is_connected():
            self.db_manager.connect()
        
        try:
            categorias = dict(self.db_manager.get_all_categories())
            categoria_id = [k for k, v in categorias.items() if v == self.categoria_selecionada][0]
            
            # Se uma imagem foi selecionada, usa o nome do arquivo
            imagem_nome = self.caminho_imagem if self.caminho_imagem else None
            
            success = self.db_manager.insert_item(
                nome=nome,
                preco=preco_float,
                categoria_id=categoria_id,
                imagem_nome=imagem_nome
            )
            
            if success:
                self.mostrar_popup("Sucesso", "Prato cadastrado com sucesso!")
                self.limpar_campos()
            else:
                self.mostrar_popup("Erro", "Falha ao cadastrar prato!")
                
        except Exception as e:
            print(f"Erro ao cadastrar prato: {e}")
            self.mostrar_popup("Erro", f"Ocorreu um erro: {str(e)}")

    def limpar_campos(self):
        self.ids.nome_prato.text = ""
        self.ids.preco.text = ""
        self.ids.categoria_btn.text = "Selecione a Categoria"
        self.ids.imagem_btn.text = "Selecionar Imagem"
        self.categoria_selecionada = None
        self.caminho_imagem = None

    def voltar_tela_gestao(self):
        self.manager.current = 'tela_gestao'

    def mostrar_popup(self, titulo, mensagem):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(
            text=mensagem,
            font_name="MontserratBold",
            halign='center',
            color=(1, 1, 1, 1)))
        
        btn = MDRaisedButton(
            text="FECHAR",
            size_hint=(None, None),
            size=(dp(120), dp(40)),
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#0C8811"),
            text_color=(1, 1, 1, 1))
        btn.bind(on_release=lambda x: self._popup.dismiss())
        content.add_widget(btn)
        
        self._popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.4),
            separator_color=get_color_from_hex("#0C8811"),
            title_color=(1, 1, 1, 1),
            title_size="20sp",
            title_font="MontserratBold",
            background_color=get_color_from_hex("#111213"))
        self._popup.open()