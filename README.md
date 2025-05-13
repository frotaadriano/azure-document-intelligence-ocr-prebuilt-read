# Azure AI Document Intelligence OCR - Prebuilt Read

Este projeto demonstra como utilizar o **Azure AI Document Intelligence** para realizar **Reconhecimento Óptico de Caracteres (OCR)** usando o modelo `prebuilt-read`. Ele extrai texto de documentos, como PDFs e imagens, detectando idiomas, estilos (ex.: texto manuscrito), linhas, palavras, marcas de seleção e parágrafos. O código é implementado em Python e foi projetado para ser modular, reutilizável e compatível com a versão 1.8.0 do SDK do Azure AI Document Intelligence. Ideal para automação de extração de texto ou como parte de um portfólio.

## Funcionalidades
- Extrai texto de documentos locais (PDFs, imagens) ou remotos (via URL).
- Detecta idiomas e níveis de confiança.
- Identifica estilos, incluindo texto manuscrito e estilos de fonte.
- Processa linhas, palavras (com confiança) e marcas de seleção.
- Extrai e ordena parágrafos com informações de posição.
- Suporte a coordenadas de bounding box para linhas e parágrafos.

## Pré-requisitos
- **Conta no Azure**: Crie uma conta gratuita em [azure.microsoft.com](https://azure.microsoft.com).
- **Recurso Azure AI Document Intelligence**:
  - Crie um recurso no [Azure Portal](https://portal.azure.com).
  - Obtenha o **endpoint** e a **chave de API** (configure como variáveis de ambiente `DI_ENDPOINT` e `DI_KEY`).
- **Python 3.8+**: Instale a versão mais recente do Python.
- **Dependências**: Listadas em `requirements.txt`.

## Instalação
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/azure-document-intelligence-ocr-prebuilt-read.git
   cd azure-document-intelligence-ocr-prebuilt-read
   ```

2. **Crie um ambiente virtual** (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as credenciais**:
   - Defina as variáveis de ambiente:
     **No Prompt de Comando (cmd):**
     ```cmd
     set DI_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
     set DI_KEY=sua_chave_aqui
     ```
     **No PowerShell:**
     ```powershell
     $env:DI_ENDPOINT="https://seu-recurso.cognitiveservices.azure.com/"
     $env:DI_KEY="sua_chave_aqui"
     ```
     - Para configuração permanente, adicione ao perfil do PowerShell ou use `setx` (veja detalhes abaixo).
   - Ou edite o arquivo `main.py` diretamente (não recomendado para produção).

## Uso
### Via Linha de Comando
1. **Prepare um documento**:
   - Coloque um arquivo local (ex.: `page_1-ocean_pdf.pdf`) no diretório do projeto ou use uma URL pública.
   - Edite o `main.py` para especificar o documento:
     ```python
     file_path = "page_1-ocean_pdf.pdf"  # Para arquivo local
     url = None  # Ou use "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"
     ```

2. **Execute o script**:
   ```bash
   python main.py
   ```

3. **Exemplo de saída**:
   ```
   ----Languages detected in the document----
   Language code: 'en' with confidence 0.95
   ----Styles detected in the document----
   ----Analyzing document from page #1----
   Page has width: 612 and height: 792, measured with unit: point
   ...Line # 0 has 2 words and text 'Lorem ipsum' within bounding polygon '[...]'
   ......Word 'Lorem' has a confidence of 0.99
   ----Detected #1 paragraphs in the document----
   Found paragraph with role: 'None' within [...] bounding region
   ...with content: 'Lorem ipsum...'
   ----------------------------------------
   ```

### Via Jupyter Notebook (Opcional)
1. Instale o Jupyter:
   ```bash
   pip install jupyter
   ```
2. Inicie o Jupyter:
   ```bash
   jupyter notebook
   ```
3. Abra o notebook (se disponível) ou crie um novo com o código de `main.py`.
4. Configure as variáveis de ambiente no notebook:
   ```python
   import os
   os.environ["DI_ENDPOINT"] = "https://seu-recurso.cognitiveservices.azure.com/"
   os.environ["DI_KEY"] = "sua_chave_aqui"
   ```
5. Execute as células para ver os resultados interativamente.

## Configuração Permanente de Variáveis de Ambiente
- **No PowerShell:**
  1. Abra o perfil:
     ```powershell
     if (-not (Test-Path $PROFILE)) { New-Item -Path $PROFILE -ItemType File -Force }
     notepad $PROFILE
     ```
  2. Adicione:
     ```powershell
     $env:DI_ENDPOINT="https://seu-recurso.cognitiveservices.azure.com/"
     $env:DI_KEY="sua_chave_aqui"
     ```
  3. Salve e recarregue:
     ```powershell
     . $PROFILE
     ```
- **No Prompt de Comando:**
  ```cmd
  setx DI_ENDPOINT "https://seu-recurso.cognitiveservices.azure.com/"
  setx DI_KEY "sua_chave_aqui"
  ```
  - Reabra o terminal após usar `setx`.

## Estrutura do Projeto
```
azure-document-intelligence-ocr-prebuilt-read/
├── main.py              # Script principal para OCR
├── requirements.txt     # Dependências do projeto
├── README.md            # Documentação do projeto
├── .gitignore           # Arquivos ignorados pelo Git
├── LICENSE              # Licença MIT
└── page_1-ocean_pdf.pdf # Exemplo de documento local (opcional)
```

## Personalização
- **Outros Modelos**: Substitua `"prebuilt-read"` por outros modelos, como `"prebuilt-layout"` ou `"prebuilt-invoice"`, dependendo das necessidades.
- **Saída**: Modifique a função `analyze_read` para salvar resultados em JSON, CSV ou banco de dados.
- **Documentos**: Adicione suporte a múltiplos arquivos passando uma lista de `file_path` ou `url`.

## Recursos Adicionais
- [Documentação Oficial](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [Azure SDK para Python](https://github.com/Azure/azure-sdk-for-python)
- [Exemplos no GitHub](https://github.com/Azure-Samples/document-intelligence-code-samples)

## Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Contato
Para dúvidas ou sugestões, abra uma issue neste repositório ou entre em contato  