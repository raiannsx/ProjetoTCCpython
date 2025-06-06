import requests
import mimetypes

PRATOS_URL = "http://localhost:3000/pratos"
FUNCIONARIOS_URL = "http://localhost:3000/funcionarios"
API_TOKEN = "seu_token_aqui"  # Remova se não usar autenticação


def enviar_prato_para_api(nome: str, preco: str, categoria: str, imagem_path: str):
    
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria
    }

    try:
        with open(imagem_path, "rb") as imagem_file:
            files = {"imagem": imagem_file}
            response = requests.post(PRATOS_URL, data=data, files=files, headers=headers)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar dados para a API:", e)
    return None

def atualizar_prato_api(id_prato: str, nome: str, preco: str, categoria: str, imagem_path: str = None):
   
    url = f"{PRATOS_URL}/{id_prato}"
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "preco": str(preco),
        "categoria": categoria
    }

    try:
        if imagem_path:
            mime_type = mimetypes.guess_type(imagem_path)[0] or 'application/octet-stream'
            with open(imagem_path, "rb") as file_obj:
                files = {'imagem': (imagem_path, file_obj, mime_type)}
                response = requests.put(url, data=data, files=files, headers=headers)
        else:
            response = requests.put(url, data=data, headers=headers)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar dados para a API:", e)

    return None

def listar_pratos_da_api():
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    try:
        response = requests.get(PRATOS_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao buscar pratos na API:", e)
    return []

def deletar_prato_api(id_prato: str):
    url = f"{PRATOS_URL}/{id_prato}"
    try:
        response = requests.delete(url)
        response.raise_for_status()
        print("Prato deletado com sucesso:", response.json())
        return True
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao deletar prato na API:", e)
    return False


def enviar_funcionario_para_api(nome: str, cpf: str, cargo: str, telefone: str):
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "cpf": cpf,
        "cargo": cargo,
        "telefone": telefone
    }

    try:
        response = requests.post(FUNCIONARIOS_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Erro ao salvar funcionário:", e)
        return None

def atualizar_funcionario_api(id_funcionario: str, nome: str, cpf: str, cargo: str, telefone: str):
    url = f"{FUNCIONARIOS_URL}/{id_funcionario}"
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "cpf": cpf,
        "cargo": cargo,
        "telefone": telefone
    }

    try:
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Erro ao atualizar funcionário:", e)
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao atualizar funcionário: {http_err}")
        return {"erro": True, "mensagem": str(http_err), "status_code": response.status_code}

    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição ao atualizar funcionário: {err}")
        return {"erro": True, "mensagem": str(err), "status_code": None}

def listar_funcionarios_da_api():
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    try:
        response = requests.get(FUNCIONARIOS_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Erro ao buscar funcionários:", e)
        return []

def deletar_funcionario_api(id_funcionario: str):
    url = f"{FUNCIONARIOS_URL}/{id_funcionario}"
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        print("Funcionário deletado com sucesso.")
        return True
    except requests.exceptions.RequestException as e:
        print("Erro ao deletar funcionário:", e)
        return False
