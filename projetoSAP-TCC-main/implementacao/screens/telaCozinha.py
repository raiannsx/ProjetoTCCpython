from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.app import MDApp
from functools import partial

Window.size = (360, 800)

KV = '''
<TelaCozinha>:
    name: 'tela_cozinha'
    md_bg_color: 0.1, 0.1, 0.1, 1

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            MDRaisedButton: 
                text: "VOLTAR"
                md_bg_color: 1, 0, 0, 1 
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1 
                font_size: "16sp"
                font_name: "MontserratBold"
                size_hint: None, None
                size: dp(40), dp(35)
                on_release: root.go_back()

            BoxLayout:
                Widget:

            Image:
                source: 'assets/logoSAP3.png'
                size_hint_x: None
                width: dp(135)
                fit_mode: 'contain'

            Widget:

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: pedidos_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
'''

Builder.load_string(KV)

class TelaCozinha(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_event = None
        self.dialog = None

    def on_enter(self, *args):
        """Called when the screen is displayed"""
        # Schedule the first update immediately
        Clock.schedule_once(lambda dt: self.carregar_pedidos_reais())
        # Set up periodic updates every 10 seconds
        self.update_event = Clock.schedule_interval(
            lambda dt: self.carregar_pedidos_reais(), 
            10
        )

    def on_leave(self, *args):
        """Called when leaving the screen"""
        # Safely cancel the update event if it exists
        if self.update_event is not None:
            self.update_event.cancel()
            self.update_event = None

    def carregar_pedidos_reais(self):
        """Load real orders from database"""
        if not hasattr(self, 'ids') or 'pedidos_layout' not in self.ids:
            return
            
        app = MDApp.get_running_app()
        if app and app.db:
            try:
                pedidos_db = app.db.execute_query(
                    """SELECT p.id_pedido, m.numero_mesa, sp.descricao as status, 
                        GROUP_CONCAT(CONCAT(i.nome, ' x', ip.quantidade) SEPARATOR ', ') as itens,
                        p.observacao
                     FROM pedido p
                     JOIN mesa m ON p.mesa_id_mesa = m.id_mesa
                     JOIN status_pedido sp ON p.status_pedido_id_status_pedido = sp.id_status_pedido
                     JOIN item_pedido ip ON p.id_pedido = ip.pedido_id_pedido
                     JOIN item i ON ip.item_id_item = i.id_item
                     WHERE sp.descricao IN ('Pendente', 'Em Preparo')
                     GROUP BY p.id_pedido
                     ORDER BY FIELD(sp.descricao, 'Pendente', 'Em Preparo'), p.data_hora""")
                
                pedidos = []
                for id_pedido, mesa, status, itens_str, observacao in pedidos_db:
                    itens_dict = {}
                    for item_str in itens_str.split(', '):
                        nome, quant = item_str.split(' x')
                        itens_dict[nome] = int(quant)
                    
                    pedidos.append({
                        'id': id_pedido,
                        'mesa': mesa,
                        'status': status,
                        'itens': itens_dict,
                        'observacao': observacao or "Nenhuma"
                    })
                
                self.atualizar_pedidos(pedidos)
            except Exception as e:
                print(f"Erro ao carregar pedidos: {e}")

    def go_back(self):
        """Return to previous screen"""
        self.manager.current = 'tela_inicial'

    def atualizar_pedidos(self, pedidos):
        """Update orders display"""
        if not hasattr(self, 'ids') or 'pedidos_layout' not in self.ids:
            return
            
        ordem_status = {'Pendente': 0, 'Em Preparo': 1}
        pedidos_ordenados = sorted(pedidos, key=lambda p: ordem_status.get(p.get('status', 'Pendente'), 0))

        self.ids.pedidos_layout.clear_widgets()
        for pedido in pedidos_ordenados:
            pedido.setdefault('status', 'Pendente')
            card = self.criar_card_pedido(pedido)
            self.ids.pedidos_layout.add_widget(card)

    def criar_card_pedido(self, pedido):
        """Create order card widget"""
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200),
            md_bg_color=get_color_from_hex("#DDDDDD"),
            radius=[10, 10, 10, 10],
            elevation=4
        )

        # Mesa label
        lbl_mesa = MDLabel(
            text=f"Mesa: [b]{pedido['mesa']}[/b]",
            markup=True,
            font_name="MontserratBold",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle"
        )

        # Status label with color coding
        status = pedido.get('status', 'Pendente')
        color_map = {
            'Pendente': (1, 0, 0, 1),    # Red
            'Em Preparo': (1, 0.5, 0, 1) # Orange
        }
        status_color = color_map.get(status, (0, 0, 0, 1))

        lbl_status = MDLabel(
            text=f"Status: [b]{status}[/b]",
            markup=True,
            theme_text_color="Custom",
            text_color=status_color,
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle"
        )

        # Items list (showing first 2 items + count if more)
        itens = pedido.get('itens', {})
        itens_lista = list(itens.items())[:2]
        texto_itens = "\n".join([f"{item} x{quant}" for item, quant in itens_lista])
        if len(itens) > 2:
            texto_itens += f"\n... e mais {len(itens) - 2} itens"

        lbl_itens = MDLabel(
            text=f"Itens:\n{texto_itens}",
            font_name="MontserratBold",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(50),
            halign="center",
            valign="top"
        )

        # Buttons layout
        botoes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        # Details button
        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=partial(self.ver_detalhes, pedido)
        )
        botoes_layout.add_widget(btn_detalhes)

        # Action buttons based on status
        if status == 'Pendente':
            btn_preparando = MDRaisedButton(
                text="Preparando",
                md_bg_color=get_color_from_hex("#FF9800"),
                on_release=partial(self.marcar_preparando, pedido)
            )
            botoes_layout.add_widget(btn_preparando)

        if status == 'Em Preparo':
            btn_pronto = MDRaisedButton(
                text="Pronto",
                md_bg_color=get_color_from_hex("#4CAF50"),
                on_release=partial(self.marcar_pronto, pedido)
            )
            botoes_layout.add_widget(btn_pronto)

        # Add all widgets to card
        card.add_widget(lbl_mesa)
        card.add_widget(lbl_status)
        card.add_widget(lbl_itens)
        card.add_widget(botoes_layout)

        return card

    def ver_detalhes(self, pedido, *args):
        """Show order details and automatically mark as 'Em Preparo' if 'Pendente'"""
        app = MDApp.get_running_app()
        if app and app.db and pedido['status'] == 'Pendente':
            status_id = app.db.get_status_id('Em Preparo')
            if status_id:
                app.db.execute_query(
                    "UPDATE pedido SET status_pedido_id_status_pedido = %s WHERE id_pedido = %s",
                    (status_id, pedido['id']),
                    fetch=False
                )
                pedido['status'] = 'Em Preparo'
                self.carregar_pedidos_reais()  # Refresh the list
        
        # Build details dialog
        itens_texto = "\n".join([f"{item} x{quant}" for item, quant in pedido['itens'].items()])
        observacao = pedido.get('observacao', "Nenhuma")

        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(10)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        lbl_obs = MDLabel(
            text=f"[b]Observação:[/b] {observacao}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40)
        )

        lbl_itens = MDLabel(
            text=f"[b]Itens:[/b]\n{itens_texto}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=max(dp(100), dp(20) * len(pedido['itens']))
        )

        content_layout.add_widget(lbl_obs)
        content_layout.add_widget(lbl_itens)

        scroll = ScrollView(size_hint=(1, None), size=(dp(300), dp(250)))
        scroll.add_widget(content_layout)

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=f"Detalhes da Mesa {pedido['mesa']}",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(
                    text="FECHAR",
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ]
        )
        self.dialog.open()

    def marcar_preparando(self, pedido, *args):
        """Mark order as 'Em Preparo'"""
        app = MDApp.get_running_app()
        if app and app.db:
            status_id = app.db.get_status_id('Em Preparo')
            if status_id:
                app.db.execute_query(
                    "UPDATE pedido SET status_pedido_id_status_pedido = %s WHERE id_pedido = %s",
                    (status_id, pedido['id']),
                    fetch=False
                )
        
        # Refresh the list
        self.carregar_pedidos_reais()

    def marcar_pronto(self, pedido, *args):
        """Mark order as 'Pronto'"""
        app = MDApp.get_running_app()
        if app and app.db:
            status_id = app.db.get_status_id('Pronto')
            if status_id:
                app.db.execute_query(
                    "UPDATE pedido SET status_pedido_id_status_pedido = %s WHERE id_pedido = %s",
                    (status_id, pedido['id']),
                    fetch=False
                )
        
        # Refresh the list
        self.carregar_pedidos_reais()