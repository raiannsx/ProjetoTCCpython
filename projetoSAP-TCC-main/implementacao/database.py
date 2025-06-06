# database.py

import mysql.connector
from mysql.connector import Error
import bcrypt 

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.DB_CONFIG = {
            'host': 'localhost',
            'database': 'mydbSAP',
            'user': 'root',
            'password': ''
        }

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(buffered=True) 
                print("Conexão com o banco de dados estabelecida com sucesso!")
                self.setup_database() 
                return True
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")

    def setup_database(self):
        try:
            self.cursor.execute(f"USE {self.DB_CONFIG['database']};")
            print(f"Banco de dados '{self.DB_CONFIG['database']}' selecionado.")
        except Error as e:
            print(f"Erro ao selecionar banco de dados ou ele não existe: {e}")
            print("Por favor, certifique-se de que o banco de dados 'mydbSAP' e suas tabelas existem.")

    def execute_query(self, query, params=None, fetch=True, commit_immediately=True):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect()

            self.cursor.execute(query, params or ())
            if fetch:
                return self.cursor.fetchall()
            else:
                if commit_immediately:
                    self.connection.commit()
                return True
        except Error as e:
            print(f"Erro ao executar query '{query}': {e}")
            if not fetch and self.connection and self.connection.is_connected() and commit_immediately:
                self.connection.rollback() 
            return None 

    def start_transaction(self):
        if self.connection and self.connection.is_connected():
            if not self.connection.in_transaction: 
                self.connection.start_transaction()
                print("Transação iniciada.")
                return True
            else:
                print("Transação já em andamento. Não é necessário iniciar novamente.")
                return True 
        print("Erro: Não foi possível iniciar a transação. Conexão não está ativa.")
        return False

    def commit_transaction(self):
        if self.connection and self.connection.is_connected():
            if self.connection.in_transaction: 
                self.connection.commit()
                print("Transação confirmada (commit).")
                return True
            else:
                print("Nenhuma transação ativa para confirmar.")
                return False
        print("Erro: Não foi possível confirmar a transação. Conexão não está ativa.")
        return False

    def rollback_transaction(self):
        if self.connection and self.connection.is_connected():
            if self.connection.in_transaction: 
                self.connection.rollback()
                print("Transação revertida (rollback).")
                return True
            else:
                print("Nenhuma transação ativa para reverter.")
                return False
        print("Erro: Não foi possível reverter a transação. Conexão não está ativa.")
        return False

    def insert_user(self, nome_completo, telefone, cpf, email, senha, tipo_usuario_id):
        plain_password = senha 
        query = """
            INSERT INTO usuario (nome_completo, telefone, CPF, email, senha, tipo_usuario_id_tipo_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (nome_completo, telefone, cpf, email, plain_password, tipo_usuario_id), fetch=False, commit_immediately=True)

    def get_user_by_email(self, email):
        query = "SELECT id_usuario, nome_completo, telefone, CPF, email, senha, tipo_usuario_id_tipo_usuario FROM usuario WHERE email = %s;"
        result = self.execute_query(query, (email,))
        return result[0] if result else None

    def check_password(self, plain_password, stored_password):
        return plain_password == stored_password

    def get_user_type_name_by_id(self, type_id):
        query = "SELECT nome_tipo FROM tipo_usuario WHERE id_tipo_usuario = %s;"
        result = self.execute_query(query, (type_id,))
        return result[0][0] if result else None

    def get_all_user_types(self):
        query = "SELECT id_tipo_usuario, nome_tipo FROM tipo_usuario;"
        return self.execute_query(query)
    
    def insert_item(self, nome, preco, categoria_id, imagem_nome=None):
        query = """
            INSERT INTO item (nome, preco, categoria_id_categoria, imagem_nome)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (nome, preco, categoria_id, imagem_nome), fetch=False)

    def update_item(self, item_id, nome, preco, categoria_id, imagem_nome=None):
        query = """
            UPDATE item 
            SET nome = %s, preco = %s, categoria_id_categoria = %s, imagem_nome = %s
            WHERE id_item = %s
        """
        return self.execute_query(query, (nome, preco, categoria_id, imagem_nome, item_id), fetch=False)

    def delete_item(self, item_id):
        query = "DELETE FROM item WHERE id_item = %s"
        return self.execute_query(query, (item_id,), fetch=False)

    def get_all_employees(self):
        query = """
            SELECT id_usuario, nome_completo, CPF, email, telefone, tipo_usuario_id_tipo_usuario
            FROM usuario
            WHERE tipo_usuario_id_tipo_usuario IN (2, 3)
        """
        return self.execute_query(query)

    def update_employee(self, employee_id, nome, cpf, email, telefone, cargo_id):
        query = """
            UPDATE usuario
            SET nome_completo = %s, CPF = %s, email = %s, telefone = %s, tipo_usuario_id_tipo_usuario = %s
            WHERE id_usuario = %s
        """
        return self.execute_query(query, (nome, cpf, email, telefone, cargo_id, employee_id), fetch=False)

    def insert_pedido(self, mesa_id, garcom_id, data_hora, status_id, observacao=None):
        query = """
            INSERT INTO pedido (mesa_id_mesa, usuario_id_garcom, data_hora, status_pedido_id_status_pedido, observacao)
            VALUES (%s, %s, %s, %s, %s)
        """
        success = self.execute_query(query, (mesa_id, garcom_id, data_hora, status_id, observacao), fetch=False, commit_immediately=False)
        if success:
            self.cursor.execute("SELECT LAST_INSERT_ID();")
            return self.cursor.fetchone()[0]
        return None

    def insert_item_pedido(self, pedido_id, item_id, quantidade, preco_unitario):
        query = """
            INSERT INTO item_pedido (pedido_id_pedido, item_id_item, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (pedido_id, item_id, quantidade, preco_unitario), fetch=False, commit_immediately=False)
    
    def get_status_id(self, description):
        query = "SELECT id_status_pedido FROM status_pedido WHERE descricao = %s;"
        result = self.execute_query(query, (description,))
        return result[0][0] if result else None 

    def get_mesa_id(self, mesa_number):
        query = "SELECT id_mesa FROM mesa WHERE numero_mesa = %s;"
        result = self.execute_query(query, (mesa_number,))
        return result[0][0] if result else None

    def get_item_id_by_name(self, item_name):
        query = "SELECT id_item FROM item WHERE nome = %s;"
        result = self.execute_query(query, (item_name,))
        return result[0][0] if result else None 

    def get_all_items(self):
        query = "SELECT id_item, nome, imagem_nome, preco, categoria_id_categoria FROM item;"
        return self.execute_query(query)

    def get_items_by_category(self, category_name):
        query = """
            SELECT i.id_item, i.nome, i.imagem_nome, i.preco, i.categoria_id_categoria
            FROM item i
            JOIN categoria c ON i.categoria_id_categoria = c.id_categoria
            WHERE c.nome = %s;
        """
        return self.execute_query(query, (category_name,))

    def get_all_categories(self):
        query = "SELECT id_categoria, nome FROM categoria;"
        return self.execute_query(query)

    def save_item_image(self, item_id, image_filename):
        query = "UPDATE item SET imagem_nome = %s WHERE id_item = %s"
        return self.execute_query(query, (image_filename, item_id), fetch=False)

    def get_item_image(self, item_id):
        query = "SELECT imagem_nome FROM item WHERE id_item = %s"
        result = self.execute_query(query, (item_id,))
        return result[0][0] if result else None
    
    def get_item_by_id(self, item_id):
        query = """
            SELECT i.id_item, i.nome, i.preco, i.imagem_nome, i.categoria_id_categoria, c.nome as categoria
            FROM item i
            JOIN categoria c ON i.categoria_id_categoria = c.id_categoria
            WHERE i.id_item = %s
        """
        result = self.execute_query(query, (item_id,))
        return result[0] if result else None

    def update_item(self, item_id, nome, preco, categoria_id, imagem_nome=None):
        query = """
            UPDATE item
            SET nome = %s, preco = %s, categoria_id_categoria = %s, imagem_nome = %s
            WHERE id_item = %s
        """
        return self.execute_query(query, (nome, preco, categoria_id, imagem_nome, item_id), fetch=False)

    def get_user_by_id(self, user_id):
        query = """
            SELECT u.id_usuario, u.nome_completo, u.telefone, u.email, 
                u.tipo_usuario_id_tipo_usuario, t.nome_tipo as cargo
            FROM usuario u
            JOIN tipo_usuario t ON u.tipo_usuario_id_tipo_usuario = t.id_tipo_usuario
            WHERE u.id_usuario = %s
        """
        result = self.execute_query(query, (user_id,))
        return result[0] if result else None

    def update_user(self, user_id, nome, telefone, email, tipo_usuario_id):
        query = """
            UPDATE usuario
            SET nome_completo = %s, telefone = %s, email = %s, tipo_usuario_id_tipo_usuario = %s
            WHERE id_usuario = %s
        """
        return self.execute_query(query, (nome, telefone, email, tipo_usuario_id, user_id), fetch=False)

    def get_employees_by_type(self, tipo_usuario_id):
        query = """
            SELECT id_usuario, nome_completo, CPF, email, telefone, tipo_usuario_id_tipo_usuario
            FROM usuario
            WHERE tipo_usuario_id_tipo_usuario = %s
        """
        return self.execute_query(query, (tipo_usuario_id,))
    
    def get_historico_pedidos(self, dias=7):
        query = """
        SELECT 
            p.id_pedido,
            DATE_FORMAT(p.data_hora, '%%d/%%m/%%Y %%H:%%i') as data_formatada,
            m.numero_mesa,
            u.nome_completo as garcom,
            SUM(ip.quantidade * ip.preco_unitario) as total
        FROM pedido p
        JOIN item_pedido ip ON p.id_pedido = ip.pedido_id_pedido
        JOIN usuario u ON p.usuario_id_garcom = u.id_usuario
        JOIN mesa m ON p.mesa_id_mesa = m.id_mesa
        WHERE p.data_hora >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY p.id_pedido
        ORDER BY p.data_hora DESC  -- Ordena do mais recente para o mais antigo
        """
        return self.execute_query(query, (dias,))

    def get_detalhes_pedido(self, pedido_id):
        query = """
        SELECT 
            i.nome,
            ip.quantidade,
            ip.preco_unitario
        FROM item_pedido ip
        JOIN item i ON ip.item_id_item = i.id_item
        WHERE ip.pedido_id_pedido = %s
        ORDER BY i.nome  -- Ordena os itens alfabeticamente
        """
        return self.execute_query(query, (pedido_id,))

if __name__ == "__main__":
    db = DatabaseManager()
    if db.connect():
        print("\nTestando obter tipos de usuário:")
        user_types = db.get_all_user_types()
        if user_types:
            for tid, tname in user_types:
                print(f"ID: {tid}, Nome: {tname}")

        print("\nTestando obter usuário por email (joao.gerente@emp.com):")
        user = db.get_user_by_email('joao.gerente@emp.com')
        if user:
            print(f"Usuário encontrado: {user[1]}, Tipo ID: {user[6]}")
            user_type_name = db.get_user_type_name_by_id(user[6])
            print(f"Tipo de Usuário: {user_type_name}")
            if db.check_password('gerente123', user[5]): 
                print("Senha correta.")
            else:
                print("Senha incorreta.")
        else:
            print("Usuário não encontrado.")

        print("\nTestando obter todas as categorias:")
        all_categories = db.get_all_categories()
        if all_categories:
            for cat_id, cat_name in all_categories:
                print(f"Categoria ID: {cat_id}, Nome: {cat_name}")
        else:
            print("Nenhuma categoria encontrada.")

        print("\nTestando obter todos os itens:")
        all_items = db.get_all_items()
        if all_items:
            for item_id, nome, imagem_nome, preco, categoria_id in all_items:
                print(f"Item ID: {item_id}, Nome: {nome}, Preço: {preco}, Categoria ID: {categoria_id}")
        else:
            print("Nenhum item encontrado.")
        
        print("\nTestando obter ID da mesa pelo número (Mesa 1) usando get_mesa_id:")
        mesa_1_id = db.get_mesa_id(1)
        if mesa_1_id:
            print(f"ID da Mesa 1: {mesa_1_id}")
        else:
            print("Mesa 1 não encontrada.")

        print("\nTestando obter ID do status 'Pendente' usando get_status_id:")
        status_pendente_id = db.get_status_id('Pendente')
        if status_pendente_id:
            print(f"ID do status 'Pendente': {status_pendente_id}")
        else:
            print("Status 'Pendente' não encontrado.")

        db.disconnect()
    else:
        print("Falha na conexão com o banco de dados.")