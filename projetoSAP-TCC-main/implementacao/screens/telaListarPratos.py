# screens/telaListarPratos.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.filechooser import FileChooserIconView
from database import DatabaseManager
import os

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaListarPratos>:
    name: 'listar_pratos'
    md_bg_color: 0.1, 0.1, 0.1, 1

    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "[size=24][font=MontserratBold]LISTA DE PRATOS[/font][/size]"
                markup: True
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1] + dp(30)
                color: get_color_from_hex("#FFFFFF")
                valign: "middle"
                padding: [0, 0, 0, dp(20)]

            BoxLayout:
                id: lista_categorias
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(15)

            MDRaisedButton:
                text: "[size=16][font=MontserratBold]VOLTAR[/font][/size]"
                markup: True
                size_hint_x: None
                width: dp(150)
                pos_hint: {'center_x': 0.5}
                md_bg_color: get_color_from_hex("#CF1919")
                text_color: get_color_from_hex("#FFFFFF")
                font_size: "16sp"
                on_release: root.voltar_tela_menu_gestao()

<EditarPratoPopup>:
    title_color: get_color_from_hex("#FFFFFF")
    title_size: "18sp"
    separator_color: get_color_from_hex("#444444")
'''

Builder.load_string(KV)

class PratoListItem(OneLineAvatarIconListItem):
    def __init__(self, prato_id, nome, preco, categoria, imagem_nome=None, callback_editar=None, **kwargs):
        super().__init__(**kwargs)
        self.prato_id = prato_id
        self.text = f"[size=16][font=MontserratBold]{nome}[/font] - [color=#B8860B]R$ {preco:.2f}[/color] [font=MontserratBold]({categoria})[/font][/size]"
        self.markup = True
        self.theme_text_color = "Custom"
        self.text_color = get_color_from_hex("#FFFFFF")
        
        if imagem_nome:
            self.add_widget(ImageLeftWidget(
                source=f"assets/pratos/{imagem_nome}",
                size_hint=(None, None),
                size=(dp(50), dp(50))
            ))
        
        icon = IconRightWidget(
            icon="pencil",
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FFFFFF"),
            on_release=lambda x: callback_editar(prato_id)
        )
        icon.icon_size = dp(24)
        self.add_widget(icon)

class EditarPratoPopup(Popup):
    def __init__(self, prato_data, db_manager, callback_atualizar, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Editar {prato_data['nome']}"
        self.size_hint = (0.9, 0.7)
        self.callback = callback_atualizar
        self.db_manager = db_manager
        self.prato_id = prato_data['id']
        self.categoria_id = prato_data['categoria_id']
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        self.nome = MDTextField(
            hint_text="Nome do Prato",
            text=prato_data['nome'],
            font_name="MontserratBold",
            hint_text_color=get_color_from_hex("#AAAAAA"),
            text_color=get_color_from_hex("#FFFFFF")
        )

        self.preco = MDTextField(
            hint_text="Preço",
            text=str(prato_data['preco']),
            input_filter='float',
            font_name="MontserratBold",
            hint_text_color=get_color_from_hex("#AAAAAA"),
            text_color=get_color_from_hex("#FFFFFF")
        )
        
        self.categoria_btn = MDRaisedButton(
            text=prato_data['categoria'],
            size_hint_y=None,
            height=dp(50),
            font_name="MontserratBold",
            text_color=get_color_from_hex("#FFFFFF"),
            on_release=self.abrir_menu_categorias
        )
        
        self.imagem_btn = MDRaisedButton(
            text="Alterar Imagem" if prato_data['imagem'] else "Adicionar Imagem",
            size_hint_y=None,
            height=dp(50),
            font_name="MontserratBold",
            text_color=get_color_from_hex("#FFFFFF"),
            on_release=self.abrir_seletor_imagem
        )
        
        btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        btn_cancelar = MDRaisedButton(
            text="[size=16]Cancelar[/size]",
            markup=True,
            md_bg_color=get_color_from_hex("#CF1919"),
            text_color=get_color_from_hex("#FFFFFF"),
            font_name="MontserratBold",
            on_release=lambda x: self.dismiss()
        )
        btn_salvar = MDRaisedButton(
            text="[size=16]Salvar[/size]",
            markup=True,
            md_bg_color=get_color_from_hex("#0C8811"),
            text_color=get_color_from_hex("#FFFFFF"),
            font_name="MontserratBold",
            on_release=self.salvar_edicao
        )
        
        btn_box.add_widget(btn_cancelar)
        btn_box.add_widget(btn_salvar)
        
        layout.add_widget(self.nome)
        layout.add_widget(self.preco)
        layout.add_widget(self.categoria_btn)
        layout.add_widget(self.imagem_btn)
        layout.add_widget(btn_box)
        
        self.content = layout
        self.nova_imagem = None
        self.carregar_categorias()

    def carregar_categorias(self):
        categorias = self.db_manager.get_all_categories()
        self.menu_items = [
            {
                "text": f"[color=#FFFFFF]{cat_nome}[/color]",
                "markup": True,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=cat_id, y=cat_nome: self.selecionar_categoria(x, y)
            } for cat_id, cat_nome in categorias
        ]
    
    def abrir_menu_categorias(self, *args):
        menu = MDDropdownMenu(
            caller=self.categoria_btn,
            items=self.menu_items,
            width_mult=4,
            background_color=get_color_from_hex("#111213")
        )
        menu.open()
    
    def selecionar_categoria(self, cat_id, cat_nome):
        self.categoria_id = cat_id
        self.categoria_btn.text = cat_nome
    
    def abrir_seletor_imagem(self, *args):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        content.add_widget(filechooser)
        
        btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        btn_cancelar = MDRaisedButton(
            text="[size=16]Cancelar[/size]",
            markup=True,
            md_bg_color=get_color_from_hex("#CF1919"),
            text_color=get_color_from_hex("#FFFFFF"),
            font_name="MontserratBold",
            on_release=lambda x: popup.dismiss()
        )
        btn_selecionar = MDRaisedButton(
            text="[size=16]Selecionar[/size]",
            markup=True,
            md_bg_color=get_color_from_hex("#0C8811"),
            text_color=get_color_from_hex("#FFFFFF"),
            font_name="MontserratBold",
            on_release=lambda x: self.selecionar_imagem(filechooser.selection, popup)
        )
        
        btn_box.add_widget(btn_cancelar)
        btn_box.add_widget(btn_selecionar)
        content.add_widget(btn_box)
        
        popup = Popup(
            title="Selecione a imagem",
            title_color=get_color_from_hex("#FFFFFF"),
            title_size="18sp",
            content=content,
            size_hint=(0.9, 0.8),
            separator_color=get_color_from_hex("#444444")
        )
        popup.open()
    
    def selecionar_imagem(self, selection, popup):
        if selection:
            self.nova_imagem = os.path.basename(selection[0])
            self.imagem_btn.text = f"Imagem: {self.nova_imagem}"
        popup.dismiss()
    
    def salvar_edicao(self, *args):
        try:
            dados = {
                'id': self.prato_id,
                'nome': self.nome.text,
                'preco': float(self.preco.text),
                'categoria_id': self.categoria_id,
                'imagem': self.nova_imagem
            }
            self.callback(dados)
            self.dismiss()
        except ValueError:
            pass

class TelaListarPratos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

    def on_pre_enter(self, *args):
        if not self.db_manager.connection.is_connected():
            self.db_manager.connect()
        self.carregar_pratos()

    def on_pre_leave(self, *args):
        if self.db_manager.connection.is_connected():
            self.db_manager.disconnect()

    def carregar_pratos(self):
        layout = self.ids.lista_categorias
        layout.clear_widgets()

        categorias = dict(self.db_manager.get_all_categories())
        ordem_categorias = ['Prato Principal', 'Sobremesa', 'Bebidas', 'Lanches']
        
        for cat_nome in ordem_categorias:
            cat_id = [k for k, v in categorias.items() if v == cat_nome][0]
            
            layout.add_widget(Label(
                text=f"[size=18][color=#4CAF50][font=MontserratBold]{cat_nome}[/font][/color][/size]",
                markup=True,
                size_hint_y=None,
                height=dp(30)
            ))
            
            itens = self.db_manager.get_items_by_category(cat_nome)
            if not itens:
                layout.add_widget(Label(
                    text="[color=#AAAAAA]Nenhum prato nesta categoria[/color]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30)
                ))
                continue
                
            for item_id, nome, imagem_nome, preco, _ in itens:
                layout.add_widget(PratoListItem(
                    prato_id=item_id,
                    nome=nome,
                    preco=preco,
                    categoria=cat_nome,
                    imagem_nome=imagem_nome,
                    callback_editar=self.abrir_edicao_prato
                ))

    def abrir_edicao_prato(self, prato_id):
        prato = self.db_manager.get_item_by_id(prato_id)
        if prato:
            prato_data = {
                'id': prato[0],
                'nome': prato[1],
                'preco': prato[2],
                'imagem': prato[3],
                'categoria_id': prato[4],
                'categoria': prato[5]
            }
            popup = EditarPratoPopup(
                prato_data=prato_data,
                db_manager=self.db_manager,
                callback_atualizar=self.atualizar_prato
            )
            popup.open()

    def atualizar_prato(self, dados):
        try:
            success = self.db_manager.update_item(
                item_id=dados['id'],
                nome=dados['nome'],
                preco=dados['preco'],
                categoria_id=dados['categoria_id'],
                imagem_nome=dados['imagem']
            )
            if success:
                self.carregar_pratos()
        except Exception as e:
            print(f"Erro ao atualizar prato: {e}")

    def voltar_tela_menu_gestao(self):
        self.manager.current = 'tela_menu_gestao'