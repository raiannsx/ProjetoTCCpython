# screens/telaGestao.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import webbrowser
from kivy.graphics import Color, RoundedRectangle


class PedidoStyledButton(MDRaisedButton):
    button_bg_color = ColorProperty([0.2, 0.2, 0.2, 1])
    button_radius = NumericProperty(dp(5))
    text_color = ColorProperty([1, 1, 1, 1])  # Nova propriedade para cor do texto

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = self.text_color  # Usa a cor definida na propriedade


KV_CONTENT = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Color kivy.graphics.Color
#:import RoundedRectangle kivy.graphics.RoundedRectangle

<PedidoStyledButton>:
    canvas.before:
        Color:
            rgba: self.button_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.button_radius]

<TelaGestao>:
    name: 'tela_gestao'
    md_bg_color: 0.1, 0.1, 0.1, 1

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(15)

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(60)
            padding: dp(10)
            spacing: dp(10)
            md_bg_color: 0.15, 0.15, 0.15, 1 

            PedidoStyledButton:
                text: "SAIR"
                on_release: root.logout()
                size_hint: None, None
                size: dp(50), dp(35) 
                button_bg_color: get_color_from_hex("#F44336") 
                button_radius: dp(5) 

            Widget:
                size_hint_x: 1

            PedidoStyledButton:
                text: "MENU"
                on_release: root.go_to_menu_gestao()
                size_hint: None, None
                size: dp(50), dp(35)
                font_size: "14sp"
                button_bg_color: get_color_from_hex("#0C8811")
                button_radius: dp(5)

        MDLabel:
            text: "O QUE DESEJA CADASTRAR?"
            font_name: "MontserratBold"
            font_size: "24sp"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + dp(20)
            color: get_color_from_hex("#FFFFFF")
            valign: "middle"

        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            padding: dp(20)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint_y: 1
            height: self.minimum_height

            MDCard:
                size_hint_x: 0.9
                height: dp(250)
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.15, 0.15, 0.15, 1

                canvas.before:
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [dp(12)]

                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)
                    size_hint: 1, 1

                    Image:
                        allow_stretch: True
                        keep_ratio: False
                        size_hint_y: 0.7
                        source: 'assets/images/img_pratos.png'

                    PedidoStyledButton:
                        text: "PRATO"
                        on_release: on_release: root.go_to_screen('cadastro_prato')
                        size_hint: None, None
                        size: dp(150), dp(40)
                        font_size: "16sp"
                        button_bg_color: get_color_from_hex("#2AB630")
                        button_radius: dp(5) 
                        pos_hint: {'center_x': 0.5} 

            MDCard:
                size_hint_x: 0.9 
                height: dp(250)
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.15, 0.15, 0.15, 1

                canvas.before:
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [dp(12)]

                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)
                    size_hint: 1, 1 

                    Image:
                        allow_stretch: True
                        keep_ratio: False
                        size_hint_y: 0.7
                        source: 'assets/images/img_funcionarios.png'

                    PedidoStyledButton:
                        text: "FUNCIONÁRIO"
                        on_release: on_release: root.go_to_screen('cadastro_funcionario')
                        size_hint: None, None
                        size: dp(150), dp(40)
                        font_size: "16sp"
                        button_bg_color: get_color_from_hex("#2AB630")
                        button_radius: dp(5)
                        pos_hint: {'center_x': 0.5} 
'''

Builder.load_string(KV_CONTENT)


class TelaGestao(MDScreen):
    def logout(self):
        app = MDApp.get_running_app()
        app.logged_in_user = None
        app.root.current = 'tela_inicial'

    def go_to_screen(self, screen_name):
        app = MDApp.get_running_app()
        app.root.current = screen_name

    def go_to_menu_gestao(self):
        self.manager.current = 'tela_menu_gestao'