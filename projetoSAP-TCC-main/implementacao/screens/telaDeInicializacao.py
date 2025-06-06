# screens/telaDeInicializacao.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

class CustomStyledButton(Button):
    button_bg_color = ListProperty([0, 0, 0, 1])
    button_radius = NumericProperty(dp(12))

KV_CONTENT = '''
#:import dp kivy.metrics.dp

<CustomStyledButton>:
    background_normal: ''
    background_down: ''
    background_color: 0,0,0,0
    color: 1, 1, 1, 1
    font_name: "MontserratBold"
    font_size: "18sp"
    size_hint: None, None
    size: dp(250), dp(50)
    pos_hint: {"center_x": 0.5}

    canvas.before:
        Color:
            rgba: self.button_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.button_radius]

<TelaDeInicializacao>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.066, 0.071, 0.075, 1
        padding: dp(20)
        spacing: dp(30)

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.5
            spacing: dp(10)
            MDBoxLayout:
                size_hint: None, None
                size: dp(600), dp(400)
                pos_hint: {'center_x': 0.5}
                Image:
                    source: 'assets/logoSAP.png'
                    fit_mode: 'contain'

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.5
            spacing: dp(20)
            padding: dp(20)

            CustomStyledButton:
                text: 'PEDIDOS'
                button_bg_color: 0.047, 0.533, 0.066, 1
                button_radius: dp(12)
                on_release: root.go_to_login('Garçom')

            CustomStyledButton:
                text: 'COZINHA'
                button_bg_color: 0.101, 0.513, 0.917, 1
                button_radius: dp(12)
                on_release: root.go_to_login('Cozinheiro')

            CustomStyledButton:
                text: 'GESTÃO'
                button_bg_color: 0.309, 0.309, 0.309, 1
                button_radius: dp(12)
                on_release: root.go_to_login('Gerente')
'''

Builder.load_string(KV_CONTENT)

class TelaDeInicializacao(MDScreen):
    def go_to_login(self, user_type):
        login_screen = self.manager.get_screen('tela_login')
        login_screen.login_type_expected = user_type
        print(f"DEBUG: Em TelaDeInicializacao.go_to_login - 'login_type_expected' definido para: '{login_screen.login_type_expected}'")
        self.manager.current = 'tela_login'
