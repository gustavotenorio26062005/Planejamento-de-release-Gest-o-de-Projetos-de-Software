Sistema Hipotético para Atividade Prática
Este é um sistema web simples e funcional desenvolvido com Python (Flask) para simular um ambiente de atividade prática. Ele inclui funcionalidades de login, cadastro, autenticação e gerenciamento de usuários.

Tecnologias Utilizadas
Backend: Python 3.x com o framework Flask

Frontend: HTML, CSS e Bootstrap 5.3

Banco de Dados: SQLite (embutido, não requer instalação)

Segurança: Criptografia de senhas com hashlib

Pré-requisitos
Para rodar este projeto, você precisa ter o Python 3 instalado na sua máquina.

Estrutura do Projeto
O projeto é organizado na seguinte estrutura de pastas:

projeto-sistemahipoterico/
│
├── app.py           # Onde está toda a lógica do servidor (backend)
│
├── database.db      # Arquivo do banco de dados SQLite (será criado automaticamente)
│
├── static/
│   ├── logobra.png
│   └── style.css
│
└── templates/
    ├── base.html        # Layout base para todas as páginas
    ├── index.html       # Página de login
    ├── cadastro.html    # Página de cadastro
    ├── dashboard.html   # Página principal do usuário (admin/operador)
    └── usuarios.html    # Página de gerenciamento de usuários (apenas para admin)
Como Rodar o Projeto
Siga os passos abaixo para executar o sistema.

Passo 1: Instale o Flask
Abra o seu terminal ou prompt de comando. Navegue até a pasta do projeto e execute o comando abaixo para instalar o Flask e suas dependências.

Bash

pip install Flask
Passo 2: Execute a Aplicação
Com a biblioteca instalada, volte ao terminal e rode o arquivo principal da aplicação.

Bash

python app.py
Passo 3: Acesse o Sistema
Se tudo ocorreu bem, o servidor de desenvolvimento será iniciado e você verá uma mensagem similar a esta no terminal:

 * Running on http://127.0.0.1:5000
Abra seu navegador e acesse o endereço http://127.0.0.1:5000/.

Passo 4: Faça Login ou Cadastre-se
Usuário Admin Padrão: O sistema já vem com um usuário admin pré-cadastrado para facilitar os testes.

Usuário: admin

Senha: admin123

Cadastro: Você pode criar novos usuários (tanto operadores quanto administradores) usando o link "Não tenho cadastro" na página de login.

Funcionalidades Principais
Login e Logout: Autenticação de usuários.

Página de Cadastro: Formulário para registro de novos usuários.

Restrição de Acesso: Páginas diferentes para perfis de administrador e operador.

Gerenciamento de Usuários (Apenas Admin): O administrador tem permissão para visualizar e excluir outros usuários do sistema.

Qualquer dúvida ou problema, sinta-se à vontade para abrir uma issue no repositório.