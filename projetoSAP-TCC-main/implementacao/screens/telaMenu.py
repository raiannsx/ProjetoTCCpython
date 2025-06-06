# screens/telaMenu.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex

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

<TelaMenu>:
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
                text: 'STATUS'
                button_bg_color: 0.047, 0.533, 0.066, 1
                button_radius: dp(12)
                on_release: root.go_to_status()

            CustomStyledButton:
                text: 'HISTÓRICO'
                button_bg_color: 0.101, 0.513, 0.917, 1
                button_radius: dp(12)
                on_release: root.go_to_historico()

            CustomStyledButton:
                text: 'AVALIAÇÃO'
                button_bg_color: 0.721, 0.525, 0.043, 1
                button_radius: dp(12)
                on_release: root.mostrar_qrcode_avaliacao()

            CustomStyledButton:
                text: 'VOLTAR'
                button_bg_color: 0.309, 0.309, 0.309, 1
                button_radius: dp(12)
                on_release: root.go_back()
'''

Builder.load_string(KV_CONTENT)

class TelaMenu(MDScreen):
    dialog = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mostrar_qrcode_avaliacao = self._mostrar_qrcode_avaliacao

    def go_back(self):
        self.manager.current = 'tela_pedido' 

    def go_to_status(self):
        self.manager.current = 'tela_status'

    def go_to_historico(self):
        self.manager.current = 'tela_historico'

    def _mostrar_qrcode_avaliacao(self, *args):

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None,
            height=dp(400),
            md_bg_color=get_color_from_hex("#111213")
        )
        

        qr_image = Image(
            source='assets/images/QRcodeParaAvaliacao.png',
            size_hint=(1, 0.8),
            allow_stretch=True,
            keep_ratio=True
        )
        content.add_widget(qr_image)
        

        btn_fechar = MDRaisedButton(
            text="FECHAR",
            md_bg_color=get_color_from_hex("#CF1919"),
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FFFFFF"),
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5},
            font_name="MontserratBold",
            font_size="16sp"
        )
        content.add_widget(btn_fechar)
        
 
        self.dialog = MDDialog(
            title="[color=#FFFFFF]QrCode para Avaliação[/color]",
            type="custom",
            content_cls=content,
            size_hint=(0.8, None),
            height=dp(500),
            md_bg_color=get_color_from_hex("#111213"),
            radius=[dp(15), dp(15), dp(15), dp(15)]
        )
        
 
        btn_fechar.bind(on_release=lambda x: self.dialog.dismiss())
        

        self.dialog.open()