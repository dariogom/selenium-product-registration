# 🤖 Selenium Product Registration Bot

> Automação de cadastro em massa de produtos via Selenium WebDriver — lê uma planilha CSV e preenche o sistema web automaticamente, produto por produto, com logs completos de execução.

---

## 📌 Sobre o Projeto

Cadastrar centenas de produtos manualmente em um sistema web é lento, repetitivo e sujeito a erros humanos. Este projeto resolve esse problema com um **bot de automação em Python** que:

- Lê uma planilha `produtos.csv` com todos os itens a cadastrar
- Faz login automaticamente no sistema **TechStock**
- Preenche e submete o formulário de cadastro para cada produto
- Registra tudo em um arquivo de log (`bot.log`) para rastreabilidade

---

## 📂 Estrutura do Repositório

```
selenium-product-registration/
│
├── main.py           # Ponto de entrada — lê o CSV e orquestra o bot
├── automation.py     # Classe BotEstoque com toda a lógica de automação
├── config.py         # Configurações: URL, credenciais e parâmetros do bot
├── produtos.csv      # Planilha com os produtos a serem cadastrados
└── bot.log           # Log gerado automaticamente a cada execução
```

---

## ⚙️ Como Funciona

```
produtos.csv  →  main.py  →  BotEstoque  →  TechStock (sistema web)
                                   ↓
                               bot.log
```

**1. Leitura do CSV** — `main.py` carrega `produtos.csv` com Pandas e itera linha por linha

**2. Login automático** — O bot abre o navegador, acessa a URL do TechStock e preenche email + senha

**3. Cadastro em série** — Para cada produto, o bot preenche os campos do formulário e submete, aguardando o reset antes de ir ao próximo

**4. Logging completo** — Cada ação é registrada no terminal e em `bot.log` com timestamp e nível (INFO / ERROR)

---

## 🗂️ Campos do Formulário Automatizados

| Campo | Descrição | Obrigatório |
|---|---|---|
| `codigo` | Código identificador do produto | ✅ |
| `marca` | Marca do produto | ✅ |
| `tipo` | Tipo / categoria geral | ✅ |
| `categoria` | Subcategoria | ✅ |
| `preco_unitario` | Preço de venda | ✅ |
| `custo` | Custo de aquisição | ✅ |
| `obs` | Observações adicionais | ❌ opcional |

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Uso |
|---|---|
| Python 3.x | Linguagem principal |
| Selenium WebDriver | Automação do navegador |
| Pandas | Leitura e manipulação do CSV |
| ChromeDriver | Driver do Google Chrome |
| logging | Registro de execução em arquivo e terminal |

---

## ▶️ Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/dariogom/selenium-product-registration.git
cd selenium-product-registration
```

### 2. Instale as dependências
```bash
pip install selenium pandas
```

> Certifique-se de ter o **Google Chrome** instalado. O ChromeDriver é gerenciado automaticamente pelo Selenium 4+.

### 3. Configure o `config.py`
```python
SISTEMA_URL          = "https://url-do-sistema.com"
EMAIL_SISTEMA        = "seu@email.com"
SENHA_SISTEMA        = "sua_senha"
PAUSA_ENTRE_CAMPOS   = 0.05   # segundos entre cada campo
```

### 4. Prepare o `produtos.csv`
```
codigo,marca,tipo,categoria,preco_unitario,custo,obs
P001,Samsung,Smartphone,Eletrônicos,1999.90,1200.00,Versão 5G
P002,Dell,Notebook,Informática,3499.90,2100.00,
```

### 5. Execute
```bash
python main.py
```

O bot abrirá o Chrome, fará login e cadastrará todos os produtos automaticamente. Acompanhe o progresso no terminal ou em `bot.log`.

---

## 📋 Exemplo de Log

```
2025-05-20 14:32:01 [INFO] Abrindo TechStock...
2025-05-20 14:32:05 [INFO] Login no TechStock realizado.
2025-05-20 14:32:06 [INFO] Cadastrando: P001 — Samsung
2025-05-20 14:32:12 [INFO] Cadastrando: P002 — Dell
2025-05-20 14:32:18 [ERROR] Erro ao cadastrar P003: timeout ao localizar elemento
```

---

## 🧠 Destaques Técnicos

- **WebDriverWait + Expected Conditions** — sem `time.sleep()` fixo para aguardar elementos; o bot espera apenas o tempo necessário
- **Digitação humana simulada** — cada caractere é enviado individualmente com pequena pausa, evitando bloqueios por sistemas anti-bot
- **Reset detection** — após cada submit, o bot detecta o reset do formulário antes de iniciar o próximo cadastro, garantindo sequência segura
- **Tratamento de erros por produto** — falhas em um item não interrompem o processo; o erro é logado e o bot segue para o próximo

---

## 📬 Contato

Feito por **Dário Gomes**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dariogomesdev/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dariogom)

---

<p align="center">
  <i>Projeto desenvolvido como parte do meu portfólio em automação com Python e Selenium.</i>
</p>
