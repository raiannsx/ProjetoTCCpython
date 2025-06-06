# screens/telaBoasVindas.py

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<BoasVindasScreen>:
    name: 'tela_boas_vindas'
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(25)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: "LOGIN REALIZADO COM SUCESSO!"
            font_name: "MontserratBold"
            font_size: "28sp"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: get_color_from_hex("#4CAF50")

        MDLabel:
            id: lbl_boas_vindas
            text: ""
            font_name: "MontserratBold"
            font_size: "18sp"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: 1, 1, 1, 1
'''

Builder.load_string(KV)

class BoasVindasScreen(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        if app.logged_in_user:
            self.ids.lbl_boas_vindas.text = f"Bem-vindo, {app.logged_in_user['nome']}!"
        
        Clock.schedule_once(self.ir_para_tela_principal, 1.0)
    
    def ir_para_tela_principal(self, dt):
        app = MDApp.get_running_app()
        if hasattr(app, 'logged_in_user'):
            tipo_usuario = app.logged_in_user['tipo_usuario_id']
            
            if tipo_usuario == 1:  # Gerente
                self.manager.current = 'tela_gestao'
            elif tipo_usuario == 2:  # Garçom
                self.manager.current = 'tela_pedido'
            elif tipo_usuario == 3:  # Cozinheiro
                self.manager.current = 'tela_cozinha'