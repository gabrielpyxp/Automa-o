Automação Onitel - Instalação e Uso
Este projeto automatiza a extração de relatórios de SLA do sistema Onitel, processa os dados e gera um dashboard interativo.

🚀 Pré-requisitos
Antes de começar, certifique-se de ter instalado:

Python 3.7+ (Download Python)

Google Chrome (Download Chrome)

Git (Opcional - para versionamento) (Download Git)

🛠 Instalação
1. Clone o repositório (ou baixe manualmente)
bash
git clone https://github.com/gabrielpyxp/Automa-o.git
cd Automa-o
2. Instale as dependências
bash
pip install -r requirements.txt
(Caso não tenha o arquivo requirements.txt, instale manualmente:)

bash
pip install selenium webdriver-manager pandas openpyxl flask
3. Configure o arquivo config.txt
Edite o arquivo config.txt na pasta raiz do projeto com as datas no formato DD/MM/AAAA:

text
01/01/2025  
31/12/2025
(Data inicial e final para filtro do relatório)

⚙️ Como Executar
Opção 1: Via Launcher (Interface Gráfica)
Execute o arquivo principal:

bash
python launcher.py
Siga os passos na janela que abrir

O sistema irá:

Baixar o relatório automaticamente

Processar os dados

Iniciar o dashboard Flask

Opção 2: Manual (Terminal)
Execute o script de automação:

bash
python zap.py
Processe os dados:

bash
python criar_db.py
Inicie o servidor web:

bash
python app.py
Acesse o dashboard:
Abra no navegador:

text
http://127.0.0.1:5000
📊 Funcionalidades do Dashboard
Filtros de SLA:

✅ Adequado (≥ 90)

❌ Crítico (≤ -90)

📊 Todos (sem filtro)

Destaque em vermelho para SLAs críticos

Ordenação automática por piores SLAs

🔧 Solução de Problemas
1. Erro "No module named 'selenium'"
bash
pip install selenium webdriver-manager
2. Download não concluído
Verifique se o Chrome está instalado

Confira a pasta downloads/ (deve ter permissão de escrita)

3. Erro no push para o GitHub
bash
git branch -M main
git push -u origin main
📦 Como Criar um Executável (.exe)
Instale o PyInstaller:

bash
pip install pyinstaller
Gere o executável:

bash
pyinstaller --onefile --windowed --add-data "config.txt;." --add-data "templates;templates" launcher.py
O arquivo estará em:

text
dist/launcher.exe
📜 Estrutura do Projeto
text
Automa-o/
├── launcher.py          # Interface gráfica
├── zap.py               # Automação web
├── criar_db.py          # Processamento de dados
├── app.py               # Servidor Flask
├── templates/           # Páginas HTML
│   └── index.html
├── downloads/           # Pasta de relatórios
├── config.txt           # Datas para filtro
└── relatorios.db        # Banco de dados gerado
💡 Dicas Extras
Agendamento: Use o Agendador de Tarefas (Windows) ou cron (Linux) para rodar automaticamente.

Deploy: Hospede o Flask em serviços como PythonAnywhere ou Heroku para acesso remoto.

Backup: Mantenha cópias da pasta downloads/ e relatorios.db.

