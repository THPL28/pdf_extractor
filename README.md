# PDF Extractor

## Descrição

Este projeto é uma aplicação de extração de texto de arquivos PDF usando OCR, seguindo os princípios da Clean Architecture e utilizando orientação a objetos.

## Estrutura do Projeto

pdf_extractor/
│
├── README.md
├── requirements.txt
├── main.py
├── config/
│   ├── __init__.py
│   └── config.py
├── core/
│   ├── __init__.py
│   ├── use_cases/
│   │   ├── __init__.py
│   │   └── extract_text.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── pdf_repository.py
│   │   └── ocr_repository.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── document.py
├── infrastructure/
│   ├── __init__.py
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── tesseract_ocr.py
│   ├── pdf/
│   │   ├── __init__.py
│   │   └── pypdf2_pdf_repository.py
└── app/
    ├── __init__.py
    └── api.py

## Dependências

- Python 3.8+
- fastapi
- uvicorn
- PyPDF2
- pytesseract
- Pillow

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/THPL28/pdf_extractor.git
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd pdf_extractor
    ```
3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Configuração

Edite o arquivo `config/config.py` para definir o caminho do executável do Tesseract.

## Uso

Execute o servidor FastAPI:
```sh
uvicorn app.api:app --reload


Acesse a documentação interativa em http://127.0.0.1:8000/docs para testar o endpoint /extract_text/ enviando arquivos PDF e visualizando o texto extraído.

Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

Licença
Este projeto está licenciado sob a MIT License.


Com essas modificações, você deverá ter um sistema funcional de extração de texto de PDFs usando FastAPI, `PyPDF2` e `pytesseract`. Certifique-se de que todas as dependências estão corretamente instaladas e que os arquivos necessários estão no local correto.
