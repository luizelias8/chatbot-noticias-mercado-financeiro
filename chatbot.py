from langchain_groq import ChatGroq
from dotenv  import load_dotenv
import os
from scraping import raspar_noticias # Importa a função de raspagem de notícias

# Carrega as variáveis de ambiente do arquivo .env, incluindo a chave da API do OpenAI.
load_dotenv()

# Configura o modelo de linguagem
cliente = ChatGroq(
    model='llama-3.1-70b-versatile',
    temperature=0, # Controla a criatividade do modelo
    api_key=os.getenv('GROQ_API_KEY')
)

# Raspa as notícias (chama a função do script de scraping)
noticias = raspar_noticias()
contexto_noticias = '\n'.join([f'{i}. {noticia}' for i, noticia in enumerate(noticias, start=1)])

# Mensagens iniciais para o contexto do chatbot
mensagens = [
    {'role': 'system', 'content': 'Você é um assistente com acesso às últimas notícias e informações sobre o mercado financeiro, pronto para fornecer dados atualizados e esclarecer dúvidas sobre o cenário econômico.'},
    {'role': 'system', 'content': f'As últimas notícias sobre o mercado financeiro são:\n\n{contexto_noticias}'}
]

print("Assistente com acesso às últimas notícias e informações sobre o mercado financeiro iniciado! (Digite 'sair' para encerrar)\n")

# Loop de interação
while True:
    # Recebe a entrada do usuário
    entrada_usuario = input('Você: ').strip()

    # Condição para encerrar o chat
    if entrada_usuario.lower() == 'sair':
        print("Assistente: Foi um prazer ajudar você. Até logo!")
        break

    # Adiciona a mensagem do usuário no histórico
    mensagens.append({'role': 'human', 'content': entrada_usuario})

    # Gera uma resposta usando o modelo Llama
    resposta = cliente.invoke(mensagens)

    # Adiciona a resposta da IA no histórico
    mensagens.append({'role': 'ai', 'content': resposta.content})

    # Exibe a resposta no terminal
    print(f"Assistente: {resposta.content}")