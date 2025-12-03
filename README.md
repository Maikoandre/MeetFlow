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
* Sistema de Autenticação (Login/Logout/Cadastro).
* Controle de acesso baseado em permissões e grupos.

## 🛠️ Tecnologias Utilizadas
* Python
* Django
* SQLite
* Bootstrap
* HTML/CSS/JavaScript

## ⚙️ Instruções de Execução

Siga os passos abaixo para executar o projeto localmente:

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
    pip install django
    # Se houver um requirements.txt: pip install -r requirements.txt
    ```

4.  **Realize as migrações do banco de dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Crie um superusuário (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```

7.  **Acesse no navegador:**
    * Sistema: `http://127.0.0.1:8000/`
    * Admin: `http://127.0.0.1:8000/admin/`

## 👥 Integrantes do Grupo
* Maiko André Antunes de Sousa - 20241GBI02GT0010
* Adalvan Lima dos Anjos - 20241GBI02GT0005

## 📺 Vídeo de Apresentação
Confira a demonstração do funcionamento do sistema no link abaixo:

**[INSIRA AQUI O LINK DO VÍDEO NO YOUTUBE]**

---
*Projeto desenvolvido para fins acadêmicos.*