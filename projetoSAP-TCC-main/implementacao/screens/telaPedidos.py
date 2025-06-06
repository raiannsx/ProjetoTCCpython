# screens/telaPedidos.py

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.utils import get_color_from_hex
from functools import partial
from datetime import datetime
from database import DatabaseManager

class PedidoStyledButton(Button):
    button_bg_color = ListProperty([0, 0.5, 0, 1])
    button_radius = NumericProperty(dp(12))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0, 0, 0, 0]
        self.color = [1, 1, 1, 1]
        self.font_name = "MontserratBold"

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<PedidoStyledButton>:
    canvas.before:
        Color:
            rgba: self.button_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.button_radius]

<TelaPedidos>:
    name: 'tela_pedido'
    md_bg_color: 0.1, 0.1, 0.1, 1

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 0.05, 0.05, 0.05, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            PedidoStyledButton:
                text: "SAIR"
                on_release: root.go_back_to_initial_screen()
                size_hint: None, None
                size: dp(50), dp(35)
                font_size: "14sp"
                button_bg_color: get_color_from_hex("#CF1919")
                button_radius: dp(5)

            BoxLayout:
                Widget:
                Image:
                    source: 'assets/logoSAP3.png'
                    size_hint_x: None
                    width: dp(135)
                    fit_mode: 'contain'
                Widget:

            PedidoStyledButton:
                text: "MENU"
                on_release: root.go_to_menu_screen()
                size_hint: None, None
                size: dp(50), dp(35)
                font_size: "14sp"
                button_bg_color: get_color_from_hex("#0C8811")
                button_radius: dp(5)

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            Label:
                text: "Número da Mesa:"
                size_hint_y: None
                height: dp(30)
                font_name: "MontserratBold"
                color: 1,1,1,1

            TextInput:
                id: mesa_input
                hint_text: "Digite o número da mesa"
                size_hint_y: None
                height: dp(40)
                foreground_color: 1,1,1,1
                background_color: 0.2,0.2,0.2,1
                hint_text_color: 0.6,0.6,0.6,1

            Label:
                text: "Observação:"
                size_hint_y: None
                height: dp(30)
                font_name: "MontserratBold"
                color: 1,1,1,1

            TextInput:
                id: observacao_input
                hint_text: "Ex: Sem cebola"
                size_hint_y: None
                height: dp(40)
                foreground_color: 1,1,1,1
                background_color: 0.2,0.2,0.2,1
                hint_text_color: 0.6,0.6,0.6,1

            ScrollView:
                BoxLayout:
                    id: categorias_layout
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)

            Label:
                text: "Itens Selecionados:"
                size_hint_y: None
                height: dp(30)
                font_name: "MontserratBold"
                color: 1,1,1,1

            ScrollView:
                BoxLayout:
                    id: lista_pedidos
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(5)
            BoxLayout:
                size_hint_y: None
                height: dp(50)
                spacing: dp(10)

                PedidoStyledButton:
                    text: "CANCELAR"
                    button_bg_color: get_color_from_hex("#CF1919")
                    on_release: root.cancelar_pedido()
                    size_hint: None, None
                    size: dp(105), dp(40)
                    font_size: "14sp"
                    button_radius: dp(5)

                PedidoStyledButton:
                    text: "EDITAR"
                    button_bg_color: get_color_from_hex("#4F4F4F")
                    on_release: root.editar_pedido()
                    size_hint: None, None
                    size: dp(105), dp(40)
                    font_size: "14sp"
                    button_radius: dp(5)

                PedidoStyledButton:
                    text: "CONFIRMAR"
                    button_bg_color: get_color_from_hex("#2AB630")
                    on_release: root.confirmar_pedido()
                    size_hint: None, None
                    size: dp(105), dp(40)
                    font_size: "14sp"
                    button_radius: dp(5)
'''

Builder.load_string(KV)

class TelaPedidos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.itens_selecionados = {}
        self.popup_edicao_ref = None
        self._items_list_layout_popup = None
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

    def on_enter(self, *args):
        """Chamado quando a tela é exibida"""
        if not hasattr(self, 'db_manager') or not self.db_manager.connection.is_connected():
            self.db_manager = DatabaseManager()
            self.db_manager.connect()
        self.mostrar_todas_categorias()

    def on_pre_leave(self, *args):
        """Chamado quando a tela está prestes a ser deixada"""
        if hasattr(self, 'db_manager') and self.db_manager.connection.is_connected():
            self.db_manager.disconnect()

    def go_back_to_initial_screen(self):
        self.manager.current = 'tela_inicial'

    def go_to_menu_screen(self):
        self.manager.current = 'tela_menu'

    def mostrar_todas_categorias(self, *args):
        layout = self.ids.categorias_layout
        layout.clear_widgets()
        layout.bind(minimum_height=layout.setter('height'))

        # Ordem desejada das categorias (nomes exatos como estão no banco)
        ORDEM_CATEGORIAS = [
            'Prato Principal',
            'Sobremesa',
            'Bebidas',
            'Lanches'
        ]

        # Pega todas categorias do banco uma única vez
        todas_categorias = dict(self.db_manager.get_all_categories())
        
        # Filtra e ordena conforme a ordem definida
        categorias_ordenadas = [
            (id, nome) for nome in ORDEM_CATEGORIAS 
            for id, cat_nome in todas_categorias.items() 
            if cat_nome == nome
        ]

        for cat_id, cat_name in categorias_ordenadas:
            layout.add_widget(Label(
                text=f"[b]{cat_name}[/b]",
                markup=True,
                font_name="MontserratBold",
                color=(1,1,1,1),
                size_hint_y=None,
                height=dp(30)
            ))
            
            itens = self.db_manager.get_items_by_category(cat_name)
            
            if not itens:
                layout.add_widget(Label(
                    text="Nenhum item nesta categoria.",
                    color=(1,1,1,1),
                    size_hint_y=None,
                    height=dp(30)
                ))
                continue
                
            for item_id, nome, imagem_nome, preco, categoria_id in itens:
                box = BoxLayout(
                    orientation='horizontal', 
                    size_hint_y=None, 
                    height=dp(80), 
                    spacing=dp(10)
                )
                
                imagem_path = f"assets/pratos/{imagem_nome}" if imagem_nome else "assets/placeholder.png"
                
                box.add_widget(Image(
                    source=imagem_path, 
                    size_hint_x=None, 
                    width=dp(80), 
                    fit_mode='contain'
                ))
                
                box.add_widget(Label(
                    text=f"{nome}\nR$ {preco:.2f}", 
                    color=(1,1,1,1), 
                    font_name="MontserratBold", 
                    size_hint_x=0.7
                ))
                
                btn = PedidoStyledButton(
                    text="ADICIONAR",
                    button_bg_color=get_color_from_hex("#2AB630"),
                    size_hint=(None, None),
                    size=(dp(85), dp(40)),
                    button_radius=dp(5),
                    font_size="12sp"
                )
                btn.bind(on_release=partial(self.adicionar_item, item_id, nome, preco))
                box.add_widget(btn)
                layout.add_widget(box)

    def adicionar_item(self, item_id, nome, preco, *args):
        if item_id not in self.itens_selecionados:
            self.itens_selecionados[item_id] = {
                'nome': nome,
                'preco': float(preco),
                'quantidade': 1
            }
        else:
            self.itens_selecionados[item_id]['quantidade'] += 1
            
        self.atualizar_lista_pedidos()

    def atualizar_lista_pedidos(self):
        lista = self.ids.lista_pedidos
        lista.clear_widgets()
        lista.bind(minimum_height=lista.setter('height'))
        
        for item_id, dados in self.itens_selecionados.items():
            lista.add_widget(Label(
                text=f"{dados['nome']} ({dados['quantidade']}) - R$ {dados['preco'] * dados['quantidade']:.2f}", 
                font_name="MontserratBold", 
                color=(1,1,1,1), 
                size_hint_y=None, 
                height=dp(30)
            ))

    def editar_pedido(self):
        self.mostrar_popup_edicao_pedido()

    def mostrar_popup_edicao_pedido(self):
        if self.popup_edicao_ref and self.popup_edicao_ref._is_open:
            self.popup_edicao_ref.dismiss()

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self._items_list_layout_popup = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._items_list_layout_popup.bind(minimum_height=self._items_list_layout_popup.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self._items_list_layout_popup)
        layout.add_widget(scroll)

        self._atualizar_conteudo_popup_edicao(self._items_list_layout_popup)

        btn_fechar = PedidoStyledButton(
            text="FECHAR",
            button_bg_color=get_color_from_hex("#CF1919"),
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            font_size="14sp",
            button_radius=dp(5),
            pos_hint={"center_x": 0.5}
        )
        btn_fechar.bind(on_release=lambda x: self.popup_edicao_ref.dismiss())
        layout.add_widget(btn_fechar)

        self.popup_edicao_ref = Popup(
            title="Editar Pedido",
            content=layout,
            size_hint=(0.9, 0.8),
            title_color=get_color_from_hex("#FFFFFF"),
            separator_color=get_color_from_hex("#FFFFFF"),
            background_color=get_color_from_hex("#111213")
        )
        self.popup_edicao_ref.open()

    def _atualizar_conteudo_popup_edicao(self, layout):
        layout.clear_widgets()
        if not self.itens_selecionados:
            layout.add_widget(Label(text="Nenhum item para editar.", color=(1,1,1,1), font_name="MontserratBold", size_hint_y=None, height=dp(40)))
            return

        for item_id, dados in sorted(self.itens_selecionados.items(), key=lambda x: x[1]['nome']):
            linha = BoxLayout(orientation='horizontal', 
                            size_hint_y=None, 
                            height=dp(45),
                            spacing=dp(5),
                            padding=[dp(5), 0, dp(5), 0])
            
            lbl = Label(text=f"{dados['nome']} ({dados['quantidade']})", 
                      font_name="MontserratBold", 
                      color=(1,1,1,1),
                      size_hint_x=0.7,
                      text_size=(None, None),
                      halign='left',
                      valign='middle',
                      shorten=True,
                      shorten_from='right')
            linha.add_widget(lbl)
            
            btn_menos = PedidoStyledButton(
                text="-", 
                button_bg_color=get_color_from_hex("#CF1919"), 
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                font_size="20sp",
                button_radius=dp(5),
                padding=[dp(-1), dp(-1)]
            )
            btn_menos.bind(on_release=partial(self.decrementar_quantidade_item, item_id))
            linha.add_widget(btn_menos)
            
            btn_mais = PedidoStyledButton(
                text="+", 
                button_bg_color=get_color_from_hex("#2AB630"), 
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                font_size="20sp",
                button_radius=dp(5),
                padding=[dp(-2), dp(-2)]
            )
            btn_mais.bind(on_release=partial(self.incrementar_quantidade_item, item_id))
            linha.add_widget(btn_mais)
            
            layout.add_widget(linha)

    def decrementar_quantidade_item(self, item_id, *args):
        if item_id in self.itens_selecionados:
            self.itens_selecionados[item_id]['quantidade'] -= 1
            if self.itens_selecionados[item_id]['quantidade'] <= 0:
                del self.itens_selecionados[item_id]
        self.atualizar_lista_pedidos()
        self._atualizar_conteudo_popup_edicao(self._items_list_layout_popup)

    def incrementar_quantidade_item(self, item_id, *args):
        if item_id in self.itens_selecionados:
            self.itens_selecionados[item_id]['quantidade'] += 1
        self.atualizar_lista_pedidos()
        self._atualizar_conteudo_popup_edicao(self._items_list_layout_popup)

    def cancelar_pedido(self):
        self.itens_selecionados.clear()
        self.ids.mesa_input.text = ""
        self.ids.observacao_input.text = ""
        self.atualizar_lista_pedidos()

    def confirmar_pedido(self):
        mesa = self.ids.mesa_input.text.strip()
        observacao_geral = self.ids.observacao_input.text.strip() or None
        
        if not mesa or not self.itens_selecionados:
            self.mostrar_popup("Erro", "Mesa e itens são obrigatórios!")
            return
        
        try:
            # Garçom padrão (deve ser substituído pelo ID do usuário logado)
            garcom_id = 2
            
            # Validação do número da mesa
            try:
                mesa_numero = int(mesa)
            except ValueError:
                self.mostrar_popup("Erro", "Número da mesa inválido! Deve ser um valor inteiro.")
                return
            
            # Obtém o ID da mesa
            mesa_id = self.db_manager.get_mesa_id(mesa_numero)
            if not mesa_id:
                self.mostrar_popup("Erro", f"Mesa {mesa_numero} não encontrada!")
                return
                
            # Obtém o ID do status "Pendente"
            status_id = self.db_manager.get_status_id('Pendente')
            if not status_id:
                raise Exception("Status 'Pendente' não configurado no sistema")
            
            # Inicia transação
            self.db_manager.start_transaction()
            
            try:
                # Insere o pedido principal
                pedido_id = self.db_manager.insert_pedido(
                    garcom_id=garcom_id,
                    mesa_id=mesa_id,
                    status_id=status_id,
                    data_hora=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    observacao=observacao_geral
                )
                
                if not pedido_id:
                    raise Exception("Falha ao criar pedido")
                
                # Insere os itens do pedido
                for item_id, dados in self.itens_selecionados.items():
                    success = self.db_manager.insert_item_pedido(
                        pedido_id=pedido_id,
                        item_id=item_id,
                        quantidade=dados['quantidade'],
                        preco_unitario=dados['preco']
                    )
                    if not success:
                        raise Exception(f"Falha ao inserir item {item_id}")
                
                # Confirma a transação
                self.db_manager.commit_transaction()
                
                # Log para depuração
                print(f"Pedido #{pedido_id} confirmado com sucesso!")
                print(f"Itens: {len(self.itens_selecionados)}")
                print(f"Mesa: {mesa_id} | Status: {status_id}")
                
                self.mostrar_popup("Sucesso", f"Pedido #{pedido_id} registrado com sucesso!")
                self.cancelar_pedido()
                
            except Exception as e:
                # Em caso de erro, faz rollback
                self.db_manager.rollback_transaction()
                print(f"Erro durante a transação: {e}")
                raise
                
        except Exception as e:
            print(f"Erro ao confirmar pedido: {e}")
            self.mostrar_popup("Erro", f"Falha ao registrar pedido:\n{str(e)}")

    def mostrar_popup(self, titulo, mensagem):
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        message_layout = BoxLayout(size_hint_y=0.7)
        lbl = Label(text=mensagem, 
                  font_name="MontserratBold", 
                  color=(1,1,1,1),
                  halign='center',
                  valign='middle')
        message_layout.add_widget(lbl)
        main_layout.add_widget(message_layout)
        
        button_layout = BoxLayout(size_hint_y=0.3, padding=(dp(20), 0, dp(20), 0))
        btn = PedidoStyledButton(
            text="FECHAR", 
            button_bg_color=get_color_from_hex("#CF1919"), 
            size_hint=(None, None),
            size=(dp(120), dp(40)), 
            font_size="14sp",
            button_radius=dp(5),
            pos_hint={'center_x': 0.5})
        btn.bind(on_release=lambda x: popup.dismiss())
        button_layout.add_widget(btn)
        main_layout.add_widget(button_layout)

        popup = Popup(
            title=titulo, 
            content=main_layout, 
            size_hint=(0.8, None), 
            height=dp(200),
            title_color=get_color_from_hex("#FFFFFF"),
            separator_color=get_color_from_hex("#FFFFFF"),
            background_color=get_color_from_hex("#111213"))
        popup.open()
