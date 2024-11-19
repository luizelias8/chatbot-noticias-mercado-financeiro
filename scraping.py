# Importa o Playwright para controlar o navegador, o BeautifulSoup para processar o HTML
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

# Função para obter o HTML da página usando Playwright
def obter_html_com_playwright(url):
    # Inicia o Playwright e abre um navegador (modo headless por padrão)
    with sync_playwright() as p:
        # Configura o navegador (pode usar 'firefox' ou 'webkit' se preferir)
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        # Navega até a URL fornecida
        pagina.goto(url)

        # Aguarda que a página esteja totalmente carregada (carregamento dinâmico)
        pagina.wait_for_load_state('networkidle')

        # Extrai o conteúdo HTML da página
        html = pagina.content()

        # Fecha o navegador
        navegador.close()

        return html

# Função para extrair informações usando BeautifulSoup
def extrair_informacoes(html):
    # Cria o objeto BeautifulSoup para processar o HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Define a expressão regular para procurar qualquer classe que contenha 'text-base'
    regex = re.compile(r'text-base')

    # Extrai as notícias usando o atributo 'aria-label' dos elementos <a>
    noticias = []

    # Encontra todos os <h2> ou <h3> cujas classes contenham 'text-base'
    for h_tag in soup.find_all(['h2', 'h3'], class_=regex):
        # Dentro de cada <h2> ou <h3>, procura o <a> (sem verificar o atributo 'aria-label')
        a_tag = h_tag.find('a')

        # Se o <a> com 'aria-label' for encontrado, extrai o conteúdo
        if a_tag:
            # descricao = a_tag['aria-label'].strip() # Obtém a descrição da notícia
            descricao = a_tag.get_text(strip=True) # Obtém o texto do <a>, removendo espaços extras
            noticias.append(descricao)

    return noticias

# Função para raspar notícias de várias páginas
def raspar_noticias():
    # Lista das URLs a serem processadas
    urls = [
        'https://www.infomoney.com.br/mercados/',
        'https://www.infomoney.com.br/ultimas-noticias/',
        'https://www.infomoney.com.br/politica/'
    ]

    # Lista para armazenar todas as notícias extraídas
    todas_noticias = []

    # Loop para percorrer todas as URLs e coletar as notícias
    for url in urls:
        print(f"Capturando notícias de: {url}")

        # Obtém o HTML renderizado pelo Playwright
        html = obter_html_com_playwright(url)

        # Extrai as informações desejadas usando o BeautifulSoup
        noticias = extrair_informacoes(html)

        # Adiciona as notícias extraídas à lista geral
        todas_noticias.extend(noticias)

    return todas_noticias

# Este bloco será executado apenas se o script for rodado diretamente
if __name__ == '__main__':
    noticias = raspar_noticias()
    for i, noticia in enumerate(noticias, start=1):
        print(f'{i}. {noticia}')