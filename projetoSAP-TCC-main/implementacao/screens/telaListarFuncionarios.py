# screens/telaListarFuncionarios.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from database import DatabaseManager

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaListarFuncionarios>:
    name: 'listar_funcionarios'
    md_bg_color: 0.1, 0.1, 0.1, 1

    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "[size=24][font=MontserratBold]LISTA DE FUNCIONÁRIOS[/font][/size]"
                markup: True
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1] + dp(30)
                color: get_color_from_hex("#FFFFFF")
                valign: "middle"
                padding: [0, 0, 0, dp(20)]

            BoxLayout:
                id: lista_cargos
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

<EditarFuncionarioPopup>:
    title_color: get_color_from_hex("#FFFFFF")
    title_size: "18sp"
    separator_color: get_color_from_hex("#444444")
'''

Builder.load_string(KV)

class FuncionarioListItem(OneLineAvatarIconListItem):
    def __init__(self, funcionario_id, nome, cargo, callback_editar=None, **kwargs):
        super().__init__(**kwargs)
        self.funcionario_id = funcionario_id
        self.text = f"[size=16][font=MontserratBold]{nome} - {cargo}[/font][/size]"
        self.markup = True
        self.theme_text_color = "Custom"
        self.text_color = get_color_from_hex("#FFFFFF")
        
        self.add_widget(IconLeftWidget(
            icon="account",
            theme_text_color="Custom",
            text_color=get_color_from_hex("#2AB630")
        ))
        
        self.add_widget(IconRightWidget(
            icon="pencil",
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FFFFFF"),
            on_release=lambda x: callback_editar(funcionario_id)
        ))

class EditarFuncionarioPopup(Popup):
    def __init__(self, funcionario_data, db_manager, callback_atualizar, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Editar {funcionario_data['nome']}"
        self.size_hint = (0.9, 0.8)
        self.callback = callback_atualizar
        self.db_manager = db_manager
        self.funcionario_id = funcionario_data['id']
        self.cargo_id = funcionario_data['cargo_id']
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        self.nome = MDTextField(
            hint_text="Nome Completo",
            text=funcionario_data['nome'],
            font_name="MontserratBold",
            hint_text_color=get_color_from_hex("#AAAAAA"),
            text_color=get_color_from_hex("#FFFFFF")
        )

        self.telefone = MDTextField(
            hint_text="Telefone",
            text=funcionario_data['telefone'],
            input_filter='int',
            font_name="MontserratBold",
            hint_text_color=get_color_from_hex("#AAAAAA"),
            text_color=get_color_from_hex("#FFFFFF")
        )

        self.email = MDTextField(
            hint_text="Email",
            text=funcionario_data['email'],
            font_name="MontserratBold",
            hint_text_color=get_color_from_hex("#AAAAAA"),
            text_color=get_color_from_hex("#FFFFFF")
        )
        
        self.cargo_btn = MDRaisedButton(
            text=funcionario_data['cargo'],
            size_hint_y=None,
            height=dp(50),
            font_name="MontserratBold",
            text_color=get_color_from_hex("#FFFFFF"),
            on_release=self.abrir_menu_cargos
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
        layout.add_widget(self.telefone)
        layout.add_widget(self.email)
        layout.add_widget(self.cargo_btn)
        layout.add_widget(btn_box)
        
        self.content = layout
        self.carregar_cargos()

    def carregar_cargos(self):
        cargos = self.db_manager.get_all_user_types()
        self.menu_items = [
            {
                "text": f"[color=#FFFFFF]{cargo_nome}[/color]",
                "markup": True,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=cargo_id, y=cargo_nome: self.selecionar_cargo(x, y)
            } for cargo_id, cargo_nome in cargos if cargo_id in [2, 3]
        ]
    
    def abrir_menu_cargos(self, *args):
        menu = MDDropdownMenu(
            caller=self.cargo_btn,
            items=self.menu_items,
            width_mult=4,
            background_color=get_color_from_hex("#111213")
        )
        menu.open()
    
    def selecionar_cargo(self, cargo_id, cargo_nome):
        self.cargo_id = cargo_id
        self.cargo_btn.text = cargo_nome
    
    def salvar_edicao(self, *args):
        try:
            dados = {
                'id': self.funcionario_id,
                'nome': self.nome.text,
                'telefone': self.telefone.text,
                'email': self.email.text,
                'cargo_id': self.cargo_id
            }
            self.callback(dados)
            self.dismiss()
        except Exception as e:
            print(f"Erro ao salvar edição: {e}")

class TelaListarFuncionarios(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

    def on_pre_enter(self, *args):
        if not self.db_manager.connection.is_connected():
            self.db_manager.connect()
        self.carregar_funcionarios()

    def on_pre_leave(self, *args):
        if self.db_manager.connection.is_connected():
            self.db_manager.disconnect()

    def carregar_funcionarios(self):
        layout = self.ids.lista_cargos
        layout.clear_widgets()

        cargos = {
            2: "Garçom",
            3: "Cozinheiro"
        }

        for cargo_id, cargo_nome in cargos.items():
            layout.add_widget(Label(
                text=f"[size=18][color=#4CAF50][font=MontserratBold]{cargo_nome}[/font][/color][/size]",
                markup=True,
                size_hint_y=None,
                height=dp(30)
            ))
            
            funcionarios = self.db_manager.get_employees_by_type(cargo_id)
            
            if not funcionarios:
                layout.add_widget(Label(
                    text=f"[color=#AAAAAA]Nenhum {cargo_nome.lower()} cadastrado[/color]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30)
                ))
                continue
                
            for id_usuario, nome, _, _, _, _ in funcionarios:
                layout.add_widget(FuncionarioListItem(
                    funcionario_id=id_usuario,
                    nome=nome,
                    cargo=cargo_nome,
                    callback_editar=self.abrir_edicao_funcionario
                ))

    def abrir_edicao_funcionario(self, funcionario_id):
        funcionario = self.db_manager.get_user_by_id(funcionario_id)
        if funcionario:
            funcionario_data = {
                'id': funcionario[0],
                'nome': funcionario[1],
                'telefone': funcionario[2],
                'email': funcionario[3],
                'cargo_id': funcionario[4],
                'cargo': funcionario[5]
            }
            popup = EditarFuncionarioPopup(
                funcionario_data=funcionario_data,
                db_manager=self.db_manager,
                callback_atualizar=self.atualizar_funcionario
            )
            popup.open()

    def atualizar_funcionario(self, dados):
        try:
            success = self.db_manager.update_user(
                user_id=dados['id'],
                nome=dados['nome'],
                telefone=dados['telefone'],
                email=dados['email'],
                tipo_usuario_id=dados['cargo_id']
            )
            if success:
                self.carregar_funcionarios()
        except Exception as e:
            print(f"Erro ao atualizar funcionário: {e}")

    def voltar_tela_menu_gestao(self):
        self.manager.current = 'tela_menu_gestao'