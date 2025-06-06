# screens/telaLogin.py

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from database import DatabaseManager 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget 

class LoginStyledButton(Button):
    button_bg_color = ListProperty([0, 0, 0, 1])
    button_radius = NumericProperty(dp(12))

KV_CONTENT = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<LoginStyledButton>:
    background_normal: ''
    background_down: ''
    background_color: 0,0,0,0
    color: 1, 1, 1, 1
    font_name: "MontserratBold"
    font_size: "14sp"
    size_hint: None, None
    size: dp(250), dp(45)

    canvas.before:
        Color:
            rgba: self.button_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.button_radius]

<TelaLogin>:
    name: 'tela_login'
    md_bg_color: 0.066, 0.071, 0.075, 1

    MDBoxLayout: # Main vertical layout for the whole screen
        orientation: 'vertical'
        padding: dp(20) 
        spacing: dp(10) 

        # Espaçador no topo para empurrar o conteúdo para baixo
        Widget:
            size_hint_y: 0.3 

        MDBoxLayout: # Seção do logo (contêiner para a imagem)
            orientation: 'vertical'
            size_hint_y: None 
            height: dp(200) 
            padding: dp(10)
            Image:
                source: 'assets/logoSAP.png'
                size_hint: None, None 
                size: dp(600), dp(400)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5} # Centraliza a imagem dentro do contêiner
                fit_mode: 'contain'

        MDBoxLayout: # Seção do formulário (Label, TextFields, Buttons)
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(15)
            size_hint_y: None 
            height: self.minimum_height 
            pos_hint: {'center_x': 0.5} 

            MDLabel:
                text: "ACESSE SUA CONTA"
                font_name: "MontserratBold"
                font_size: "24sp"
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1]
                color: 1, 1, 1, 1

            MDTextField:
                id: user
                hint_text: "Email"
                mode: "rectangle"
                line_color_normal: 1, 1, 1, 1
                line_color_focus: get_color_from_hex("#0C8811")
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
                id: password
                hint_text: "Senha"
                mode: "rectangle"
                password: True
                line_color_normal: 1, 1, 1, 1
                line_color_focus: get_color_from_hex("#0C8811")
                text_color: 1, 1, 1, 1
                hint_text_color: 0.7, 0.7, 0.7, 1
                font_name: "MontserratBold"
                size_hint_y: None
                height: dp(48)
                padding: dp(10)
                multiline: False
                size_hint_x: 0.9
                pos_hint: {'center_x': 0.5}

            LoginStyledButton:
                text: "ENTRAR"
                button_bg_color: get_color_from_hex("#0C8811")
                button_radius: dp(8)
                on_release: root.login()
                font_name: "MontserratBold"
                font_size: "16sp"
                size_hint_x: 0.9
                pos_hint: {"center_x": 0.5}

            LoginStyledButton:
                text: "VOLTAR"
                button_bg_color: 0.309, 0.309, 0.309, 1
                button_radius: dp(8)
                font_name: "MontserratBold"
                font_size: "16sp"
                on_release: root.go_to_initial_screen()
                size_hint_x: 0.9
                pos_hint: {"center_x": 0.5}
        
        # Espaçador no final para empurrar o conteúdo para cima
        Widget:
            size_hint_y: 0.1 

'''

Builder.load_string(KV_CONTENT)

class TelaLogin(MDScreen):
    login_type_expected = None

    def on_enter(self, *args):
        self.ids.user.text = ""
        self.ids.password.text = ""

    def login(self):
        username = self.ids.user.text
        password = self.ids.password.text

        db = DatabaseManager()
        if db.connect():
            user_data = db.get_user_by_email(username)
            db.disconnect()

            if user_data:
                stored_password = user_data[5]
                
                if password == stored_password:
                    app = MDApp.get_running_app()
                    app.logged_in_user = {
                        'id': user_data[0],
                        'nome': user_data[1],
                        'tipo_usuario_id': user_data[6]
                    }
                    
                    # Configura a tela de boas-vindas
                    tela_boas_vindas = self.manager.get_screen('tela_boas_vindas')
                    tela_boas_vindas.ids.lbl_boas_vindas.text = f"Bem-vindo, {user_data[1]}!"
                    
                    # Redireciona para tela de boas-vindas
                    self.manager.current = 'tela_boas_vindas'
                else:
                    self.show_popup("Erro", "Senha incorreta.")
            else:
                self.show_popup("Erro", "Usuário não encontrado.")
        else:
            self.show_popup("Erro", "Falha na conexão com o banco de dados.")

    def go_to_initial_screen(self):
        self.manager.current = 'tela_inicial'

    def show_popup(self, titulo, mensagem):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(MDLabel(
            text=mensagem,
            font_name="MontserratBold",
            halign='center'
        ))
        
        btn = Button(
            text="FECHAR",
            size_hint=(None, None),
            size=(dp(120), dp(40)),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=get_color_from_hex("#0C8811"),
            color=(1, 1, 1, 1),
            font_name="MontserratBold"
        )
        btn.bind(on_release=lambda x: self._popup.dismiss())
        content.add_widget(btn)
        
        self._popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.4),
            separator_color=get_color_from_hex("#0C8811"),
            title_color=(1, 1, 1, 1),
            title_size="20sp",
            title_font="MontserratBold"
        )
        self._popup.open()