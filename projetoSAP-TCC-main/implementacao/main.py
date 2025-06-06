# main.py
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.core.text import LabelBase
from database import DatabaseManager

# Importações das telas
from screens.telaDeInicializacao import TelaDeInicializacao
from screens.telaLogin import TelaLogin
from screens.telaBoasVindas import BoasVindasScreen
from screens.telaPedidos import TelaPedidos
from screens.telaMenu import TelaMenu
from screens.telaCozinha import TelaCozinha
from screens.telaStatus import TelaStatus
from screens.telaGestao import TelaGestao
from screens.telaMenuGestao import TelaMenuGestao
from screens.telaCadastroFuncionario import TelaCadastroFuncionario
from screens.telaCadastroPrato import TelaCadastroPrato
from screens.telaListarPratos import TelaListarPratos
from screens.telaListarFuncionarios import TelaListarFuncionarios
from screens.telaHistoricoPedidos import TelaHistoricoPedidos

from database import DatabaseManager

Window.size = (360, 800)

LabelBase.register(
    name="MontserratBold",
    fn_regular="assets/fonts/Montserrat-Bold.ttf"
)

class SistemaPedidosApp(MDApp):
    db = None
    logged_in_user = None
    user_type_ids = {}

    def build(self):
        self.title = "Sistema de Pedidos - SAP"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        # Configuração do banco de dados
        self.db = DatabaseManager()
        if not self.db.connect():
            print("Erro crítico: Não foi possível conectar ao banco de dados.")
            exit()

        # Carrega os tipos de usuário
        user_types = self.db.get_all_user_types()
        if user_types:
            for tid, tname in user_types:
                self.user_type_ids[tname] = tid

        # Configuração do gerenciador de telas
        sm = MDScreenManager()
        sm.add_widget(TelaDeInicializacao(name="tela_inicial"))
        sm.add_widget(TelaLogin(name="tela_login"))
        sm.add_widget(BoasVindasScreen(name="tela_boas_vindas"))  
        sm.add_widget(TelaPedidos(name="tela_pedido"))
        sm.add_widget(TelaMenu(name="tela_menu"))
        sm.add_widget(TelaCozinha(name="tela_cozinha"))
        sm.add_widget(TelaStatus(name="tela_status"))
        sm.add_widget(TelaGestao(name="tela_gestao"))
        sm.add_widget(TelaMenuGestao(name="tela_menu_gestao")) 
        sm.add_widget(TelaCadastroFuncionario(name='cadastro_funcionario'))
        sm.add_widget(TelaCadastroPrato(name='cadastro_prato'))
        sm.add_widget(TelaListarPratos(name='listar_pratos'))
        sm.add_widget(TelaListarFuncionarios(name='listar_funcionarios'))
        sm.add_widget(TelaHistoricoPedidos(name='tela_historico'))
        return sm
    
    def mudar_tela(self, screen_name):
        self.root.current = screen_name

    def on_stop(self):
        if self.db:
            self.db.disconnect()

if __name__ == "__main__":
    SistemaPedidosApp().run()
