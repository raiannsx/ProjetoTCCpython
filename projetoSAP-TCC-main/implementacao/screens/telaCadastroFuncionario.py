# screens/telaCadastroFuncionario.py

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
from database import DatabaseManager

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaCadastroFuncionario>:
    name: 'cadastro_funcionario'
    md_bg_color: 0.1, 0.1, 0.1, 1

    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "CADASTRO DE FUNCIONÁRIO"
                font_name: "MontserratBold"
                font_size: "24sp"
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
                color: get_color_from_hex("#FFFFFF")
                valign: "middle"
                padding: [0, 0, 0, dp(50)]

            MDTextField:
                id: nome_completo
                hint_text: "Nome Completo"
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
                id: telefone
                hint_text: "Telefone"
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
                input_filter: 'int'
                max_text_length: 11

            MDTextField:
                id: cpf
                hint_text: "CPF"
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
                input_filter: 'int'
                max_text_length: 11

            MDTextField:
                id: email
                hint_text: "Email"
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
                id: senha
                hint_text: "Senha"
                mode: "rectangle"
                password: True
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
                padding: [0, 0, 0, dp(20)]

            MDRaisedButton:
                id: tipo_usuario_btn
                text: "TIPO DE USUÁRIO"
                size_hint: None, None
                size: dp(250), dp(48)
                text_color: 1, 1, 1, 1
                font_name: "MontserratBold"
                font_size: "16sp"
                pos_hint: {'center_x': 0.5}
                md_bg_color: get_color_from_hex("#2AB630")
                on_release: root.abrir_menu_tipo_usuario()

            BoxLayout:
                orientation: 'horizontal'
                size_hint: None, None
                size: dp(250), dp(48)
                pos_hint: {'center_x': 0.5}
                spacing: dp(10)

                MDRaisedButton:
                    text: "VOLTAR"
                    size_hint_x: 0.5
                    text_color: 1, 1, 1, 1
                    font_name: "MontserratBold"
                    font_size: "16sp"
                    md_bg_color: get_color_from_hex("#CF1919")
                    on_release: root.voltar_tela_gestao()

                MDRaisedButton:
                    text: "CADASTRAR"
                    size_hint_x: 0.5
                    text_color: 1, 1, 1, 1
                    font_name: "MontserratBold"
                    font_size: "16sp"
                    md_bg_color: get_color_from_hex("#B8860B")
                    on_release: root.cadastrar_funcionario()
'''

Builder.load_string(KV)

class TelaCadastroFuncionario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_tipo_usuario = None
        self.tipo_usuario_selecionado = None
        self.db_manager = DatabaseManager()  # Inicializa o db_manager aqui
        self.db_manager.connect()  # Conecta imediatamente

    def on_pre_enter(self, *args):
        """Chamado antes da tela ser exibida"""
        if not self.db_manager.connection.is_connected():
            self.db_manager.connect()
        
        self.carregar_tipos_usuario()

    def on_pre_leave(self, *args):
        """Chamado quando a tela está prestes a ser deixada"""
        if self.db_manager.connection.is_connected():
            self.db_manager.disconnect()

    def carregar_tipos_usuario(self):
        tipos_usuario = [
            {"text": "Garçom", "viewclass": "OneLineListItem", "on_release": lambda x="Garçom": self.selecionar_tipo_usuario(x)},
            {"text": "Cozinheiro", "viewclass": "OneLineListItem", "on_release": lambda x="Cozinheiro": self.selecionar_tipo_usuario(x)},
        ]
        
        self.menu_tipo_usuario = MDDropdownMenu(
            caller=self.ids.tipo_usuario_btn,
            items=tipos_usuario,
            width_mult=4,
            background_color=get_color_from_hex("#111213"),
            border_margin=dp(10),
            max_height=dp(150))

    def abrir_menu_tipo_usuario(self):
        if self.menu_tipo_usuario:
            self.menu_tipo_usuario.open()

    def selecionar_tipo_usuario(self, tipo):
        self.tipo_usuario_selecionado = tipo
        self.ids.tipo_usuario_btn.text = tipo
        if self.menu_tipo_usuario:
            self.menu_tipo_usuario.dismiss()

    def cadastrar_funcionario(self):
        nome = self.ids.nome_completo.text.strip()
        telefone = self.ids.telefone.text.strip()
        cpf = self.ids.cpf.text.strip()
        email = self.ids.email.text.strip()
        senha = self.ids.senha.text.strip()
        
        if not nome or not telefone or not cpf or not email or not senha or not self.tipo_usuario_selecionado:
            self.mostrar_popup("Erro", "Todos os campos são obrigatórios!")
            return
            
        if len(telefone) < 10 or len(telefone) > 11:
            self.mostrar_popup("Erro", "Telefone inválido! Deve ter 10 ou 11 dígitos.")
            return
            
        if len(cpf) != 11:
            self.mostrar_popup("Erro", "CPF inválido! Deve ter 11 dígitos.")
            return
            
        if "@" not in email or "." not in email:
            self.mostrar_popup("Erro", "Email inválido!")
            return
            
        if len(senha) < 4:
            self.mostrar_popup("Erro", "Senha muito curta! Mínimo 4 caracteres.")
            return
        
        tipo_usuario_id = 2 if self.tipo_usuario_selecionado == "Garçom" else 3
        
        try:
            if not self.db_manager.connection.is_connected():
                self.db_manager.connect()
            
            if self.db_manager.get_user_by_email(email):
                self.mostrar_popup("Erro", "Email já cadastrado!")
                return
                
            success = self.db_manager.insert_user(
                nome_completo=nome,
                telefone=telefone,
                cpf=cpf,
                email=email,
                senha=senha,
                tipo_usuario_id=tipo_usuario_id
            )
            
            if success:
                self.mostrar_popup("Sucesso", "Funcionário cadastrado com sucesso!")
                self.limpar_campos()
            else:
                self.mostrar_popup("Erro", "Falha ao cadastrar funcionário!")
                
        except Exception as e:
            print(f"Erro ao cadastrar funcionário: {e}")
            self.mostrar_popup("Erro", f"Ocorreu um erro: {str(e)}")

    def limpar_campos(self):
        self.ids.nome_completo.text = ""
        self.ids.telefone.text = ""
        self.ids.cpf.text = ""
        self.ids.email.text = ""
        self.ids.senha.text = ""
        self.ids.tipo_usuario_btn.text = "Selecione o Tipo de Usuário"
        self.tipo_usuario_selecionado = None

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
            md_bg_color=get_color_from_hex("#0C8811"))
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