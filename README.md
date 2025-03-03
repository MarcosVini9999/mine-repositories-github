# Extração de Dados do GitHub

Este repositório contém dois scripts em Python que permitem extrair informações de repositórios do GitHub:

- **download_threads.py**: Baixa as threads (issues e pull requests) de um repositório.
- **download_contributors.py**: Coleta os dados dos desenvolvedores que participaram do desenvolvimento do repositório.

> **Atenção:** Em ambos os scripts é necessário configurar um token pessoal do GitHub para acessar a API.

## Pré-requisitos

- **Python 3.x**
- Instalação dos módulos necessários (por exemplo, `requests`)
- Um token pessoal do GitHub

## Scripts

### download_threads.py

- **Função:** Baixa todas as threads (issues e pull requests) de um repositório.
- **Link:** [download_threads.py](https://github.com/MarcosVini9999/mine-repositories-github/blob/main/download_threads.py)

> **Nota:** Insira seu token pessoal do GitHub no script para autenticar as requisições e evitar limitações da API.

### download_contributors.py

- **Função:** Extrai os dados dos desenvolvedores que contribuíram para o repositório.
- **Link:** [download_contributors.py](https://github.com/MarcosVini9999/mine-repositories-github/blob/main/download_contributors.py)

> **Nota:** Assim como no script anterior, é obrigatório inserir seu token pessoal do GitHub para acessar a API.

## Como Utilizar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/MarcosVini9999/mine-repositories-github.git
