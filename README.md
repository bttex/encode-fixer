# CSV Encoding Fixer

Script Python para corrigir problemas de encoding (acentuação) em arquivos CSV e padronizá-los em UTF-8 com BOM (compatível com Excel).

## 🎯 Funcionalidades

- ✅ Detecta automaticamente o encoding correto do arquivo
- ✅ Corrige problemas de acentuação
- ✅ Remove quebras de linha internas nos campos
- ✅ Salva em UTF-8-SIG (compatível com Excel brasileiro)
- ✅ Lida com campos contendo vírgulas e aspas
- ✅ Suporta diferentes separadores (`;`, `,`, etc.)

## 📋 Requisitos

- Python 3.6+
- Biblioteca pandas:
  ```bash
  pip install pandas
  ```

## 🚀 Instalação

```bash
# Clone ou baixe o script
chmod +x csv_fixer.py

# Instale as dependências
pip install pandas
```

## 📖 Uso Básico

### Sintaxe

```bash
python csv_fixer.py --csv-path <arquivo> [opções]
```

### Argumentos

| Argumento | Obrigatório | Descrição | Exemplo |
|-----------|-------------|-----------|---------|
| `--csv-path` | ✅ Sim | Caminho do arquivo CSV original | `--csv-path dados.csv` |
| `--save-name` | ❌ Não | Nome do arquivo de saída* | `--save-name corrigido.csv` |
| `--sep` | ❌ Não | Separador de campos (padrão: `;`) | `--sep ","` |

\* Se não informado, adiciona `_utf8` ao nome original

## 💡 Exemplos de Uso

### 1. Uso básico (separador padrão `;`)

```bash
python csv_fixer.py --csv-path dados.csv
```

**Resultado**: Cria `dados_utf8.csv` na mesma pasta

### 2. Definir nome personalizado para saída

```bash
python csv_fixer.py --csv-path dados.csv --save-name dados_corrigidos.csv
```

**Resultado**: Cria `dados_corrigidos.csv` na mesma pasta

### 3. CSV com vírgula como separador

```bash
python csv_fixer.py --csv-path dados.csv --sep ","
```

### 4. CSV com ponto-e-vírgula (explícito)

```bash
python csv_fixer.py --csv-path dados.csv --sep ";"
```

### 5. Arquivo em caminho completo

```bash
python csv_fixer.py --csv-path /home/usuario/documentos/dados.csv
```

### 6. Combinando todas as opções

```bash
python csv_fixer.py \
  --csv-path /home/usuario/dados_originais.csv \
  --save-name dados_processados.csv \
  --sep ","
```

## 🔄 Processo de Conversão

O script executa as seguintes etapas:

1. **Detecção automática de encoding**
   - Testa: UTF-8, Latin1, ISO-8859-1, Windows-1252
   - Usa o primeiro que funcionar

2. **Leitura do CSV**
   - Parser tolerante a problemas de formatação
   - Respeita campos entre aspas
   - Pula linhas com erros (modo `skip`)

3. **Limpeza de dados**
   - Remove `\r` (carriage return)
   - Remove `\n` (quebras de linha internas)
   - Substitui por espaço simples

4. **Adiciona coluna CICLO**
   - Insere coluna `CICLO` com valor fixo "2025.1"

5. **Salva arquivo**
   - Encoding: UTF-8-SIG (inclui BOM)
   - Mesmo separador do arquivo original
   - Na mesma pasta do arquivo original

## 🎓 Encodings Testados

O script tenta automaticamente os seguintes encodings (nesta ordem):

1. **UTF-8** - Padrão moderno
2. **Latin1** - Comum em sistemas Linux/Unix
3. **ISO-8859-1** - Padrão europeu ocidental
4. **Windows-1252** - Padrão Windows (português/BR)

## 📂 Estrutura de Saída

### Antes
```
/pasta/
  └── dados.csv  (encoding desconhecido, com problemas)
```

### Depois (padrão)
```
/pasta/
  ├── dados.csv  (original preservado)
  └── dados_utf8.csv  (UTF-8-SIG, corrigido)
```

### Depois (com --save-name)
```
/pasta/
  ├── dados.csv  (original preservado)
  └── dados_corrigidos.csv  (UTF-8-SIG, corrigido)
```

### Desabilitar remoção de quebras de linha

Comente as linhas 44-48:

```python
# df = df.map(
#     lambda x: str(x).replace("\r", " ").replace("\n", " ")
#     if isinstance(x, str)
#     else x
# )
```

### Mudar encoding de saída

Linha 53, altere `utf-8-sig` para outro encoding:

```python
df.to_csv(caminho_saida, index=False, encoding="utf-8", sep=sep or ";")
```

## ⚠️ Notas Importantes

1. **Arquivo original preservado**: O script NUNCA sobrescreve o arquivo original
2. **UTF-8-SIG vs UTF-8**: O BOM (Byte Order Mark) permite que o Excel reconheça acentos corretamente
3. **Quebras de linha**: São removidas automaticamente para evitar problemas de importação
4. **Linhas problemáticas**: São ignoradas automaticamente (`on_bad_lines="skip"`)
5. **Coluna CICLO**: É sempre adicionada ao final do arquivo

## 🐛 Resolução de Problemas

### Erro: "Arquivo não encontrado"

**Causa**: Caminho incorreto ou arquivo não existe

**Solução**: Verifique o caminho completo do arquivo
```bash
# Use caminho absoluto
python csv_fixer.py --csv-path /caminho/completo/arquivo.csv

# Ou navegue até a pasta
cd /pasta/do/arquivo
python csv_fixer.py --csv-path arquivo.csv
```

### Erro: "Não foi possível ler o CSV"

**Causa**: Encoding muito específico ou arquivo corrompido

**Solução**: 
1. Abra o arquivo no Excel ou LibreOffice
2. Salve novamente como CSV UTF-8
3. Rode o script no novo arquivo

### Acentos ainda errados no Excel

**Causa**: Excel não reconheceu o encoding

**Solução**: O script já usa UTF-8-SIG. Se persistir:
1. Abra o Excel
2. Vá em "Dados" > "De Texto/CSV"
3. Selecione o arquivo gerado
4. Escolha "UTF-8" manualmente

### Separador errado

**Causa**: CSV usa separador diferente de `;`

**Solução**: Use o parâmetro `--sep`
```bash
python csv_fixer.py --csv-path dados.csv --sep ","
```

### Dados ficaram em uma única coluna no Excel

**Causa**: Separador incompatível com configuração regional do Excel

**Solução**:
- Para Excel brasileiro: use `;` (padrão)
- Para Excel internacional: use `,`

```bash
python csv_fixer.py --csv-path dados.csv --sep ";"
```

## 📊 Output do Console

### Sucesso
```
[OK] Lido com sucesso (encoding=windows-1252, sep=';')
✅ Arquivo corrigido salvo em: /pasta/dados_utf8.csv
```

### Falha de Encoding
```
[!] Falhou com utf-8: 'utf-8' codec can't decode byte...
[!] Falhou com latin1: invalid continuation byte
[OK] Lido com sucesso (encoding=windows-1252, sep=';')
✅ Arquivo corrigido salvo em: /pasta/dados_utf8.csv
```

### Arquivo não encontrado
```
❌ Arquivo não encontrado: /caminho/errado.csv
```

## 📝 Casos de Uso

- ✅ Corrigir CSVs exportados de sistemas legados
- ✅ Padronizar encoding para importação no BigQuery
- ✅ Preparar dados para Excel brasileiro
- ✅ Limpar campos com quebras de linha indesejadas
- ✅ Adicionar colunas de controle (CICLO, data, etc.)

## 🔗 Compatibilidade

- **Sistema Operacional**: Windows, Linux, macOS
- **Python**: 3.6 ou superior
- **Excel**: Todas as versões (graças ao UTF-8-SIG)
- **Google Sheets**: Importa corretamente
- **BigQuery**: Pronto para upload

## 📄 Licença

Este script é fornecido como está, sem garantias.