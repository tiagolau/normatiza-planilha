# Normalizador de Planilhas RhinoCRM

Aplicação web simples para normalizar planilhas de "Relatório Pós Vendas" para o padrão de importação do RhinoCRM.

## Funcionalidades
- Upload de arquivo `.xlsx`.
- Normalização de colunas (`ALUNO` -> `Nome`, `EMAIL` -> `Email`, `CELULAR` -> `Numero`).
- Limpeza e formatação de números de telefone (apenas dígitos, remove +55, adiciona 9º dígito se necessário).
- Exportação automática.

## Como rodar localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Rode o servidor:
```bash
python app.py
```

3. Acesse `http://localhost:5000`.

## Deploy no EasyPanel

Este projeto já possui um `Dockerfile` configurado.

1. Faça o push para o GitHub.
2. No EasyPanel, crie um novo App.
3. Conecte o repositório do GitHub.
4. O EasyPanel detectará o Dockerfile automaticamente.
5. Defina a porta do container como `80`.
