# 🚀 Automação Onitel - Gestão de SLA

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)

Sistema automatizado para coleta, processamento e visualização de dados de SLA da plataforma Onitel.

## 📦 Pré-requisitos
- Python 3.7+
- Google Chrome
- Git (opcional)

```bash
# Dependências essenciais
pip install selenium pandas flask openpyxl
```

## 🛠 Configuração
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/gabrielpyxp/Automa-o.git
   cd Automa-o
   ```

2. **Configure as datas**:
   Edite `config.txt` com o formato:
   ```
   DD/MM/AAAA  # Data inicial
   DD/MM/AAAA  # Data final
   ```

## ▶️ Execução
### Opção 1: Interface Gráfica
```bash
python launcher.py
```

### Opção 2: Terminal
```bash
python zap.py           # Coleta dados
python criar_db.py      # Processa dados
python app.py           # Inicia dashboard
```
Acesse: http://127.0.0.1:5000

## 🖥️ Dashboard Features
| Funcionalidade       | Descrição                          |
|----------------------|------------------------------------|
| Filtro por SLA       | Adequado (≥90) ou Crítico (≤-90)   |
| Destaque visual      | Alertas vermelhos para SLAs baixos |
| Exportação           | Dados em SQLite e Excel            |

## 📁 Estrutura de Arquivos
```
.
├── app.py                # Servidor Flask
├── criar_db.py           # Processamento de dados
├── launcher.py           # Interface gráfica
├── zap.py                # Automação web
├── config.txt            # Configuração de datas
├── requirements.txt      # Dependências
├── downloads/            # Relatórios baixados
├── templates/            # Páginas web
│   └── index.html        # Dashboard HTML
└── relatorios.db         # Banco de dados
```

## 💻 Como Transformar em Executável
```bash
pyinstaller --onefile --windowed \
--add-data "config.txt;." \
--add-data "templates;templates" \
launcher.py
```

## ❓ Suporte
Encontrou problemas? [Abra uma issue](https://github.com/gabrielpyxp/Automa-o/issues) ou contate:

✉️ gabrielrocha@onitel.com.br  
🔗 [LinkedIn](https://www.linkedin.com/in/seu-perfil)

---

> **Nota:** Mantenha seu Chrome atualizado para compatibilidade com o WebDriver.
