# MeetFlow - Sistema de Gestão de Eventos

Este projeto é o Trabalho Final da disciplina de **Programação para Web I** do curso de Análise e Desenvolvimento de Sistemas (4º Período), ministrada pelo Professor Carlos Anderson.

O sistema foi desenvolvido utilizando **Django** e **Bootstrap**, focando na implementação de autenticação, permissões e operações CRUD completas utilizando exclusivamente **Function-Based Views (FBV)**.

## 🎯 Objetivo

Desenvolver uma aplicação web para o gerenciamento completo do ciclo de vida de eventos, permitindo o cadastro de usuários, criação de eventos, gestão de inscrições, controle de presença e geração de relatórios.

## 🚀 Funcionalidades (CRUDs)

O sistema conta com 5 funcionalidades completas (Listagem, Criação, Edição, Exclusão e Detalhe):

1.  **Gestão de Eventos:** Criação, aprovação, publicação e gerenciamento de eventos.
2.  **Gestão de Usuários:** Cadastro, edição de perfil e controle de tipos (Administrador, Organizador, Participante).
3.  **Inscrições:** Sistema de inscrição em eventos com status (Pendente, Confirmado, Cancelado).
4.  **Controle de Presença:** Registro de presença dos participantes inscritos.
5.  **Relatórios:** Geração e visualização de métricas dos eventos (total de inscritos e presentes).

Além disso, o sistema possui:

- Sistema de Autenticação (Login/Logout/Cadastro).
- Controle de acesso baseado em permissões e grupos.

## 🛠️ Tecnologias Utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## ⚙️ Instruções de Execução

### 🐳 Execução com Docker (Recomendado)

A maneira mais fácil de rodar o projeto é utilizando Docker. Certifique-se de ter o **Docker** e o **Docker Compose** instalados.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Maikoandre/MeetFlow.git
    cd MeetFlow
    ```

2.  **Suba os containers:**

    ```bash
    docker compose up --build
    ```

    _Isso irá construir a imagem, iniciar o banco de dados MySQL e o servidor Django._

3.  **Acesse no navegador:**
    - Sistema: `http://localhost:8000/`
    - Admin: `http://localhost:8000/admin/`

---

### 🔧 Execução Manual

Caso prefira rodar sem Docker, você precisará de uma instância **MySQL** rodando localmente.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Maikoandre/MeetFlow.git
    cd MeetFlow
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    Certifique-se de ter um banco MySQL criado e exporte as variáveis de ambiente ou ajuste o `settings.py` se necessário.
    Exemplo de variáveis (Linux/Mac):

    ```bash
    export DB_NAME=meetflow_db
    export DB_USER=seu_usuario
    export DB_PASSWORD=sua_senha
    export DB_HOST=localhost
    ```

5.  **Realize as migrações:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crie um superusuário (Admin):**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```

## 👥 Integrantes do Grupo

- Maiko André Antunes de Sousa - 20241GBI02GT0010
- Adalvan Lima dos Anjos - 20241GBI02GT0005

## 📺 Vídeo de Apresentação

Confira a demonstração do funcionamento do sistema no link abaixo:

**[INSIRA AQUI O LINK DO VÍDEO NO YOUTUBE]**

---

_Projeto desenvolvido para fins acadêmicos._
