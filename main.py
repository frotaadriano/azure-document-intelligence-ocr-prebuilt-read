import os
import numpy as np
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

def initialize_client(endpoint: str, key: str) -> DocumentIntelligenceClient:
    """Inicializa o cliente do Azure AI Document Intelligence."""
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_words(page, line):
    """Retorna as palavras que pertencem a uma linha específica."""
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

def _in_span(word, spans):
    """Verifica se uma palavra está dentro dos spans de uma linha."""
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

def analyze_document(client: DocumentIntelligenceClient, file_path: str = None, url: str = None) -> AnalyzeResult:
    """Analisa um documento local ou remoto usando o modelo prebuilt-read."""
    if file_path and url:
        raise ValueError("Forneça apenas um: file_path ou url.")
    if not file_path and not url:
        raise ValueError("Forneça um file_path ou url.")

    try:
        if file_path:
            with open(file_path, "rb") as f:
                poller = client.begin_analyze_document(
                    "prebuilt-read",  # model_id
                    f.read()  # body: conteúdo do arquivo em bytes
                )
        else:
            poller = client.begin_analyze_document(
                "prebuilt-read",  # model_id
                {"urlSource": url}  # body: dicionário com URL
            )
        return poller.result()
    except Exception as e:
        raise Exception(f"Erro ao analisar o documento: {str(e)}")

def analyze_read(file_path: str = None, url: str = None):
    """Função para executar o OCR e exibir os resultados."""
    # Configurações - use variáveis de ambiente
    endpoint = os.getenv("DI_ENDPOINT", "SUA_ENDPOINT_AQUI")
    key = os.getenv("DI_KEY", "SUA_CHAVE_AQUI")

    if endpoint == "SUA_ENDPOINT_AQUI" or key == "SUA_CHAVE_AQUI":
        raise ValueError("Por favor, configure as variáveis de ambiente DI_ENDPOINT e DI_KEY.")

    # Inicializa o cliente
    client = initialize_client(endpoint, key)

    # Analisa o documento
    result: AnalyzeResult = analyze_document(client, file_path=file_path, url=url)

    # Exibe os resultados
    print("----Languages detected in the document----")
    if result.languages is not None:
        for language in result.languages:
            print(f"Language code: '{language.locale}' with confidence {language.confidence}")

    print("----Styles detected in the document----")
    if result.styles:
        for style in result.styles:
            if style.is_handwritten:
                print("Found the following handwritten content: ")
                print(",".join([result.content[span.offset : span.offset + span.length] for span in style.spans]))
            if style.font_style:
                print(f"The document contains '{style.font_style}' font style, applied to the following text: ")
                print(",".join([result.content[span.offset : span.offset + span.length] for span in style.spans]))

    for page in result.pages:
        print(f"----Analyzing document from page #{page.page_number}----")
        print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        if page.lines:
            for line_idx, line in enumerate(page.lines):
                words = get_words(page, line)
                print(
                    f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{line.polygon}'"
                )

                for word in words:
                    print(f"......Word '{word.content}' has a confidence of {word.confidence}")

        if page.selection_marks:
            for selection_mark in page.selection_marks:
                print(
                    f"...Selection mark is '{selection_mark.state}' within bounding polygon "
                    f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
                )

    if result.paragraphs:
        print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
        for paragraph in result.paragraphs:
            print(f"Found paragraph with role: '{paragraph.role}' within {paragraph.bounding_regions} bounding region")
            print(f"...with content: '{paragraph.content}'")

        result.paragraphs.sort(key=lambda p: (p.spans.sort(key=lambda s: s.offset), p.spans[0].offset))
        print("-----Print sorted paragraphs-----")
        for idx, paragraph in enumerate(result.paragraphs):
            print(
                f"...paragraph:{idx} with offset: {paragraph.spans[0].offset} and length: {paragraph.spans[0].length}"
            )

    print("----------------------------------------")

if __name__ == "__main__":
    # Escolha um documento: arquivo local ou URL
    file_path = "page1-ocean.pdf"  # Substitua pelo caminho do seu arquivo local, se aplicável
    url = None  # Ou use "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"

    try:
        analyze_read(file_path=file_path, url=url)
    except Exception as e:
        print(f"Erro: {str(e)}")