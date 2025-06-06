from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

KV_STATUS = '''
<TelaStatus>:
    name: 'tela_status'
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
                size_hint: None, None
                size: dp(50), dp(35)
                font_size: "14sp"
                font_name: "MontserratBold"
                on_release: root.go_back()

            Widget:

            BoxLayout:
                orientation: 'horizontal'
                size_hint_x: None
                width: dp(135)
                pos_hint: {"center_x": 0.5}
                Image:
                    source: 'assets/logoSAP3.png'
                    size_hint_x: None
                    width: dp(135)
                    fit_mode: 'contain'

            Widget:

        ScrollView:
            do_scroll_x: False

            BoxLayout:
                id: pedidos_prontos_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
'''

Builder.load_string(KV_STATUS)

class TelaStatus(MDScreen):
    update_event = None
    
    def on_enter(self):
        self.carregar_status()
        # Atualiza a cada 10 segundos
        self.update_event = Clock.schedule_interval(lambda dt: self.carregar_status(), 10)

    def on_leave(self):
        if hasattr(self, 'update_event'):
            self.update_event.cancel()

    def go_back(self):
        self.manager.current = 'tela_pedido'

    def carregar_status(self):
        app = MDApp.get_running_app()
        if app and app.db:
            pedidos_db = app.db.execute_query(
                """SELECT p.id_pedido, m.numero_mesa, sp.descricao as status, 
                      GROUP_CONCAT(CONCAT(i.nome, ' x', ip.quantidade) SEPARATOR ', ') as itens,
                      p.observacao
                   FROM pedido p
                   JOIN mesa m ON p.mesa_id_mesa = m.id_mesa
                   JOIN status_pedido sp ON p.status_pedido_id_status_pedido = sp.id_status_pedido
                   JOIN item_pedido ip ON p.id_pedido = ip.pedido_id_pedido
                   JOIN item i ON ip.item_id_item = i.id_item
                   WHERE sp.descricao IN ('Pronto', 'Entregue')
                   GROUP BY p.id_pedido
                   ORDER BY FIELD(sp.descricao, 'Pronto', 'Entregue'), p.data_hora""")
            
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

    def atualizar_pedidos(self, pedidos):
        self.ids.pedidos_prontos_layout.clear_widgets()

        if not pedidos:
            lbl_vazio = MDLabel(
                text="Nenhum pedido no momento.",
                halign="center",
                theme_text_color="Hint",
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.pedidos_prontos_layout.add_widget(lbl_vazio)
            return

        for pedido in pedidos:
            card = self.criar_card_pedido_pronto(pedido)
            self.ids.pedidos_prontos_layout.add_widget(card)

    def criar_card_pedido_pronto(self, pedido):
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200),
            md_bg_color=get_color_from_hex("#FFFFFF"),
            radius=[8, 8, 8, 8],
            elevation=8
        )

        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=dp(10),
            padding=dp(10),
            pos_hint={'center_x': 0.5}
        )

        lbl_mesa = MDLabel(
            text=f"Mesa: [b]{pedido.get('mesa', '?')}[/b]",
            markup=True,
            font_style="Body1",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30),
            halign="center"
        )

        status = pedido.get('status', 'Pronto')
        color_map = {
            'Pendente': "#F44336",
            'Em Preparo': "#FF9800",
            'Pronto': "#4CAF50",
            'Entregue': "#D32F2F"
        }
        lbl_status = MDLabel(
            text=f"Status: [b]{status}[/b]",
            markup=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(color_map.get(status, "#388E3C")),
            font_style="Body2",
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )

        itens = pedido.get('itens', {})
        texto_itens = "\n".join([f"{item} x{quant}" for item, quant in itens.items()])

        lbl_itens = MDLabel(
            text=f"Itens:\n{texto_itens}",
            size_hint_y=None,
            height=max(dp(50), dp(18) * len(itens)),
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2"
        )

        botoes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(6),
            pos_hint={'center_x': 0.5}
        )

        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=lambda x: self.ver_detalhes(pedido)
        )
        botoes_layout.add_widget(btn_detalhes)

        btn_entregar = MDRaisedButton(
            text="Entregue" if pedido['status'] == 'Entregue' else "Entregar",
            md_bg_color=get_color_from_hex("#4CAF50" if pedido['status'] != 'Entregue' else "#BDBDBD"),
            on_release=lambda x: self.marcar_entregue(pedido, card, btn_entregar),
            disabled=pedido['status'] == 'Entregue'
        )
        botoes_layout.add_widget(btn_entregar)

        content_layout.add_widget(lbl_mesa)
        content_layout.add_widget(lbl_status)
        content_layout.add_widget(lbl_itens)
        content_layout.add_widget(botoes_layout)

        card.add_widget(content_layout)

        return card

    def ver_detalhes(self, pedido):
        itens_texto = "\n".join([f"{item} x{quant}" for item, quant in pedido['itens'].items()])
        observacao = pedido.get('observacao', "Nenhuma")

        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(8),
            spacing=dp(8)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        lbl_obs = MDLabel(
            text=f"[b]Observação:[/b] {observacao}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            font_style="Body1"
        )

        lbl_itens = MDLabel(
            text=f"[b]Itens:[/b]\n{itens_texto}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=max(dp(90), dp(18) * len(pedido['itens'])),
            font_style="Body2"
        )

        content_layout.add_widget(lbl_obs)
        content_layout.add_widget(lbl_itens)

        scroll = ScrollView(size_hint=(1, None), size=(dp(300), dp(250)))
        scroll.add_widget(content_layout)

        dialog = MDDialog(
            title=f"Detalhes da Mesa {pedido['mesa']}",
            type="custom",
            content_cls=scroll,
            buttons=[MDFlatButton(
                    text="FECHAR",
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: dialog.dismiss()
                ),
            ]
        )
        dialog.open()

    def marcar_entregue(self, pedido, card, btn_entregar):
        app = MDApp.get_running_app()
        if app and app.db:
            status_id = app.db.get_status_id('Entregue')
            if status_id:
                app.db.execute_query(
                    "UPDATE pedido SET status_pedido_id_status_pedido = %s WHERE id_pedido = %s",
                    (status_id, pedido['id']),
                    fetch=False
                )
        
        # Atualiza a UI
        pedido['status'] = 'Entregue'
        btn_entregar.text = "Entregue"
        btn_entregar.disabled = True
        btn_entregar.md_bg_color = get_color_from_hex("#BDBDBD")
        
        # Atualiza o status no card
        for widget in card.children:
            if isinstance(widget, BoxLayout):
                for label in widget.children:
                    if isinstance(label, MDLabel) and label.text.startswith("Status:"):
                        label.text = f"Status: [b]{pedido['status']}[/b]"
                        label.text_color = get_color_from_hex("#D32F2F")