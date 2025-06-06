# screens/telaHistoricoPedidos.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from database import DatabaseManager

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaHistoricoPedidos>:
    name: 'tela_historico'
    md_bg_color: 0.1, 0.1, 0.1, 1

    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "[size=24][font=MontserratBold]HISTÓRICO DE PEDIDOS[/font][/size]"
                markup: True
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1] + dp(30)
                color: get_color_from_hex("#FFFFFF")
                valign: "middle"
                padding: [0, 0, 0, dp(20)]

            BoxLayout:
                id: lista_pedidos
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
                on_release: root.voltar()
'''

Builder.load_string(KV)

class PedidoListItem(OneLineAvatarIconListItem):
    def __init__(self, pedido_id, data_hora, mesa, total, callback_detalhes=None, **kwargs):
        super().__init__(**kwargs)
        self.pedido_id = pedido_id
        self.text = f"[size=16][font=MontserratBold]Pedido #{pedido_id}[/font] • Mesa {mesa}[/size]\n[size=14]{data_hora} • [color=#B8860B]R$ {total:.2f}[/color][/size]"
        self.markup = True
        self.theme_text_color = "Custom"
        self.text_color = get_color_from_hex("#FFFFFF")
        
        self.add_widget(IconLeftWidget(
            icon="notebook",
            theme_text_color="Custom",
            text_color=get_color_from_hex("#2AB630")
        ))
        
        self.bind(on_release=lambda x: callback_detalhes(pedido_id, total))

class TelaHistoricoPedidos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = DatabaseManager()
    
    def on_pre_enter(self, *args):
        self.carregar_pedidos()

    def carregar_pedidos(self):
        layout = self.ids.lista_pedidos
        layout.clear_widgets()
        
        try:
            pedidos = self.db_manager.get_historico_pedidos(dias=7)
            
            if not pedidos:
                layout.add_widget(Label(
                    text="[color=#AAAAAA]Nenhum pedido registrado[/color]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30)
                ))
                return
            
            for pedido in pedidos:
                layout.add_widget(PedidoListItem(
                    pedido_id=pedido[0],
                    data_hora=pedido[1],
                    mesa=pedido[2],
                    total=float(pedido[4]),
                    callback_detalhes=self.mostrar_detalhes
                ))

        except Exception as e:
            print(f"Erro ao carregar pedidos: {e}")
            layout.add_widget(Label(
                text="[color=#FF0000]Erro ao carregar histórico[/color]",
                markup=True,
                size_hint_y=None,
                height=dp(30)
            ))

    def mostrar_detalhes(self, pedido_id, total_pedido):
        try:
            itens = self.db_manager.get_detalhes_pedido(pedido_id)
            content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
            
            # Título do pedido
            content.add_widget(Label(
                text=f"[size=18][b]Pedido #{pedido_id}[/b][/size]",
                markup=True,
                color=get_color_from_hex("#FFFFFF"),
                size_hint_y=None,
                height=dp(40)
            ))
            
            # Lista de itens
            for item in itens:
                total_item = float(item[1]) * float(item[2])
                item_layout = BoxLayout(size_hint_y=None, height=dp(30))
                item_layout.add_widget(Label(
                    text=f"{item[1]}x {item[0]}",
                    color=get_color_from_hex("#FFFFFF"),
                    size_hint_x=0.7,
                    halign='left'
                ))
                item_layout.add_widget(Label(
                    text=f"R$ {total_item:.2f}",
                    color=get_color_from_hex("#B8860B"),
                    size_hint_x=0.3,
                    halign='right'
                ))
                content.add_widget(item_layout)
            
            # Linha divisória
            content.add_widget(Label(size_hint_y=None, height=dp(1)))
            
            # Total do pedido
            total_layout = BoxLayout(size_hint_y=None, height=dp(40))
            total_layout.add_widget(Label(
                text="[b]TOTAL:[/b]",
                markup=True,
                color=get_color_from_hex("#FFFFFF"),
                size_hint_x=0.7,
                halign='left'
            ))
            total_layout.add_widget(Label(
                text=f"[b][color=#B8860B]R$ {total_pedido:.2f}[/color][/b]",
                markup=True,
                size_hint_x=0.3,
                halign='right'
            ))
            content.add_widget(total_layout)
            
            popup = Popup(
                title="Detalhes da Comanda",
                title_color=get_color_from_hex("#FFFFFF"),
                title_size="18sp",
                content=content,
                size_hint=(0.9, 0.8),
                separator_color=get_color_from_hex("#444444")
            )
            popup.open()
            
        except Exception as e:
            print(f"Erro ao carregar detalhes: {e}")

    def voltar(self):
        self.manager.current = 'tela_menu'