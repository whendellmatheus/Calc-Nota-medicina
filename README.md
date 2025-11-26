🧮 Calculadora de Notas - Flask

Aplicação web desenvolvida em Python + Flask, utilizada para calcular médias acadêmicas tanto do ciclo básico quanto do ciclo clínico, permitindo ao usuário selecionar livremente o período desejado. O sistema possui login simples e utiliza um banco SQLite.

🚀 Funcionalidades

🔐 Login com armazenamento em SQLite

📚 Seleção de período diretamente na tela

🧮 Cálculo automático das médias baseado no peso de cada componente

🧹 Botão Limpar que apenas reseta os campos, sem trocar o período

🚪 Logout funcional

🎨 Interface organizada e responsiva

📦 Estrutura do Projeto
Calculadora-backend/
├── app.py
├── banco.py
├── database.db
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── calculadora.html
└── venv/  (opcional no GitHub)

🔧 Como rodar o projeto
1️⃣ Criar o ambiente virtual
python -m venv venv

2️⃣ Ativar o ambiente virtual

PowerShell:

venv\Scripts\Activate.ps1


CMD:

venv\Scripts\activate.bat

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Criar o banco (somente na primeira vez)
python banco.py

5️⃣ Iniciar o servidor Flask
python app.py


Abra no navegador:

👉 http://127.0.0.1:5000

👥 Como adicionar usuários ao banco

Para adicionar usuários usando o script já existente:

python banco.py


Ou use qualquer editor SQLite (ex: DB Browser for SQLite).

📄 requirements.txt sugerido

Se quiser manter explicitamente:

Flask==3.0.0


(Outras dependências serão incluídas se você adicionar novas funções.)

🧹 .gitignore recomendado

Crie um .gitignore assim:

venv/
__pycache__/
*.pyc
database.db


Se quiser incluir o banco no GitHub, remova database.db.