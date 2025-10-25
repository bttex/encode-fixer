# 🔧 CSV Encoding Fixer

Script Python para corrigir problemas de encoding (acentuação) em arquivos CSV e padronizá-los em UTF-8 com BOM (compatível com Excel).

## ✨ Características

- ✅ **Detecção inteligente de encoding** com chardet (análise automática)
- ✅ Corrige problemas de acentuação automaticamente
- ✅ Remove quebras de linha internas nos campos
- ✅ Salva em UTF-8-SIG (compatível com Excel brasileiro)
- ✅ Lida com campos contendo vírgulas e aspas
- ✅ Suporta diferentes separadores (`;`, `,`, etc.)
- ✅ Validação automática de arquivos com Typer

## 📋 Requisitos

- Python 3.6+
- Bibliotecas:

```bash
pip install pandas typer chardet
```

## 🚀 Instalação

```bash
# Clone ou baixe o script
git clone https://github.com/bttex/encode-fixer.git
cd encode-fixer

# Instale as dependências
pip install -r requirements.txt
```

## 💻 Uso

```bash
python csv_fixer.py --csv-path <arquivo> [opções]
```

### Parâmetros

| Argumento | Obrigatório | Descrição | Exemplo |
|-----------|-------------|-----------|---------|
| `--csv-path` | ✅ Sim | Caminho do arquivo CSV original | `--csv-path dados.csv` |
| `--save-name` | ❌ Não | Nome do arquivo de saída* | `--save-name corrigido.csv` |
| `--sep` | ❌ Não | Separador de campos (padrão: `;`) | `--sep ","` |

\* Se não informado, adiciona `_utf8` ao nome original

## 📝 Exemplos

### Uso básico (detecta encoding automaticamente)
```bash
python csv_fixer.py --csv-path dados.csv
```
**Resultado:** Cria `dados_utf8.csv` na mesma pasta

### Com nome personalizado
```bash
python csv_fixer.py --csv-path dados.csv --save-name dados_corrigidos.csv
```
**Resultado:** Cria `dados_corrigidos.csv` na mesma pasta

### CSV com vírgula como separador
```bash
python csv_fixer.py --csv-path dados.csv --sep ","
```

### Caminho absoluto
```bash
python csv_fixer.py --csv-path /home/usuario/documentos/dados.csv
```

### Exemplo completo
```bash
python csv_fixer.py \
  --csv-path /home/usuario/dados_originais.csv \
  --save-name dados_processados.csv \
  --sep ","
```

## 🔍 Como Funciona

O script executa as seguintes etapas:

### 1. **Detecção Inteligente de Encoding**
- Usa a biblioteca `chardet` para analisar o arquivo
- Lê uma amostra (1MB) para detectar o encoding
- Mostra a confiança da detecção (ex: 85%)
- Fallback automático para encodings comuns se necessário

### 2. **Ordem de Tentativa**
Se chardet detectar um encoding, ele é testado primeiro. Depois, tenta:
- UTF-8 (padrão moderno)
- Windows-1252 (padrão Windows/português BR)
- Latin1 (comum em sistemas Linux/Unix)
- ISO-8859-1 (padrão europeu ocidental)

### 3. **Leitura do CSV**
- Parser tolerante a problemas de formatação
- Respeita campos entre aspas
- Pula linhas com erros (modo `skip`)

### 4. **Limpeza de Dados**
- Remove `\r` (carriage return)
- Remove `\n` (quebras de linha internas)
- Substitui por espaço simples

### 5. **Salva Arquivo**
- Encoding: UTF-8-SIG (inclui BOM)
- Mesmo separador do arquivo original
- Na mesma pasta do arquivo original

## 📊 Saída do Console

### Detecção bem-sucedida:
```
[i] Detecção automática (chardet): windows-1252 (Confiança: 85%)
[i] Ordem de tentativa: ['windows-1252', 'utf-8', 'latin1', 'iso-8859-1']
✅ [OK] Lido com sucesso (encoding=windows-1252, sep=';')
✅ Arquivo corrigido salvo em: /pasta/dados_utf8.csv
```

### Detecção com fallback:
```
[i] Detecção automática (chardet): ascii (Confiança: 45%)
[i] Ordem de tentativa: ['ascii', 'utf-8', 'windows-1252', 'latin1', 'iso-8859-1']
[!] Falhou com ascii: UnicodeDecodeError
✅ [OK] Lido com sucesso (encoding=utf-8, sep=';')
✅ Arquivo corrigido salvo em: /pasta/dados_utf8.csv
```

## 📂 Estrutura de Arquivos

### Antes:
```
/pasta/
└── dados.csv (encoding desconhecido, com problemas)
```

### Depois (uso básico):
```
/pasta/
├── dados.csv (original preservado)
└── dados_utf8.csv (UTF-8-SIG, corrigido)
```

### Depois (com --save-name):
```
/pasta/
├── dados.csv (original preservado)
└── dados_corrigidos.csv (UTF-8-SIG, corrigido)
```

## ⚙️ Personalizações Avançadas

### Desabilitar remoção de quebras de linha

Comente as linhas 81-85 em `csv_fixer.py`:
```python
# df = df.map(
#     lambda x: str(x).replace("\r", " ").replace("\n", " ")
#     if isinstance(x, str)
#     else x
# )
```

### Mudar encoding de saída

Linha 88, altere `utf-8-sig` para outro encoding:
```python
df.to_csv(caminho_saida, index=False, encoding="utf-8", sep=sep)
```

## ⚠️ Avisos Importantes

- **Arquivo original preservado:** O script NUNCA sobrescreve o arquivo original
- **UTF-8-SIG vs UTF-8:** O BOM (Byte Order Mark) permite que o Excel reconheça acentos corretamente
- **Quebras de linha:** São removidas automaticamente para evitar problemas de importação
- **Linhas problemáticas:** São ignoradas automaticamente (`on_bad_lines="skip"`)
- **Detecção automática:** O chardet tem alta precisão, mas em casos raros pode errar (o fallback ajuda)

## 🐛 Solução de Problemas

### ❌ Erro: "Arquivo não encontrado"
**Causa:** Caminho incorreto ou arquivo não existe

**Solução:** Verifique o caminho completo do arquivo
```bash
# Use caminho absoluto
python csv_fixer.py --csv-path /caminho/completo/arquivo.csv

# Ou navegue até a pasta
cd /pasta/do/arquivo
python csv_fixer.py --csv-path arquivo.csv
```

### ❌ Erro: "Não foi possível ler o CSV com nenhum dos encodings testados"
**Causa:** Encoding muito específico, arquivo corrompido, ou não é um CSV válido

**Solução:**
1. Abra o arquivo no Excel ou LibreOffice
2. Salve novamente como CSV UTF-8
3. Rode o script no novo arquivo

### ❌ Acentos aparecem errados no Excel
**Causa:** Excel não reconheceu o encoding (raro, pois usamos UTF-8-SIG)

**Solução:** 
1. Abra o Excel
2. Vá em "Dados" > "De Texto/CSV"
3. Selecione o arquivo gerado
4. Escolha "UTF-8" manualmente

### ❌ Separador não funciona no Excel
**Causa:** Separador incompatível com configuração regional do Excel

**Solução:**
- Para Excel brasileiro: use `;` (padrão)
- Para Excel internacional: use `,`

```bash
python csv_fixer.py --csv-path dados.csv --sep ";"
```

### ⚠️ Detecção reporta baixa confiança
**Causa:** Arquivo pequeno ou com encoding ambíguo

**Solução:** O script tentará automaticamente outros encodings. Se falhar, especifique manualmente editando a lista de fallbacks no código.

## 🎯 Casos de Uso

- ✅ Corrigir CSVs exportados de sistemas legados
- ✅ Padronizar encoding para importação no BigQuery
- ✅ Preparar dados para Excel brasileiro
- ✅ Limpar campos com quebras de linha indesejadas
- ✅ Converter CSVs de múltiplas origens para um padrão único

## 🖥️ Compatibilidade

- **Sistema Operacional:** Windows, Linux, macOS
- **Python:** 3.6 ou superior
- **Excel:** Todas as versões (graças ao UTF-8-SIG)
- **Google Sheets:** Importa corretamente
- **BigQuery:** Pronto para upload

## 📄 Licença

Este script é fornecido como está, sem garantias.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Desenvolvido com ❤️ para facilitar o trabalho com CSVs problemáticos**