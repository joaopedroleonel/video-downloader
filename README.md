# Video Downloader

Um site de download de vídeos construído com Flask, que utiliza o `yt-dlp` para baixar conteúdos de diversas plataformas. O projeto integra `Flask-SocketIO` para comunicação em tempo real, `gevent` para gerenciamento de conexões assíncronas e `JWT` (JSON Web Tokens) para autenticação de usuários.

## Tecnologias Utilizadas

* **Python 3.8+**
* **Flask**: Microframework web
* **Flask-SocketIO**: Comunicação em tempo real via WebSockets
* **gevent**: Servidor WSGI assíncrono
* **yt-dlp**: Ferramenta de download de vídeos de plataformas como YouTube
* **PyJWT**: Geração e validação de tokens JWT para autenticação
* **HTML/CSS/JavaScript**: Frontend

## Funcionalidades Principais

1. **Download de vídeos**: permiti que o usuário insira a URL do vídeo e escolha o formato desejado.
2. **Interface em tempo real**: status de progresso do download exibido ao vivo.
3. **Autenticação JWT**: apenas usuários autenticados podem iniciar downloads.
4. **Escalabilidade**: executando em `gevent`, suporta múltiplas conexões simultâneas.

## Estrutura do Projeto

```
video-downloader/
│
├── service/                 # Lógica de backend
│   ├── __init__.py          # Inicialização do módulo
│   ├── auth.py              # Rotas e utils de autenticação JWT
│   ├── clean.py             # Limpa a pasta de arquivos do usuário
│   └── yt.py                # Integração com yt-dlp
│
├── web/                     # Frontend estático e templates
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css   # Estilos customizados
│   │   ├── images/
│   │   │   └── icon.svg     # Ícone do site
│   │   └── js/
│   │       └── socket.io.min.js  # Biblioteca do Socket.IO
│   ├── auth.html            # Página de login/cadastro
│   └── index.html           # Página principal do downloader
│
├── main.py                  # Ponto de entrada (app Flask)
├── requirements.txt         # Dependências do projeto
├── .gitignore               # Arquivos e pastas ignorados pelo Git
└── README.md                # Documentação do projeto
```

## Como Executar a Aplicação

1. **Criar arquivo `.env`**

   * Na raiz do projeto, crie um arquivo chamado `.env` e defina as variáveis de ambiente necessárias:

     ```bash
     FLASK_ENV=development
     JWT_SECRET=seu_segredo_aqui
     ```
2. **Preparar o ambiente**

   * Crie e ative um ambiente virtual (recomendado):

     ```bash
     python3 -m venv venv
     source venv/bin/activate  # Linux/Mac
     venv\Scripts\activate     # Windows
     ```
3. **Instalar dependências**

   ```bash
   pip install -r requirements.txt
   ```
4. **Criar pasta para arquivos**

   ```bash
   mkdir files
   ```
5. **Iniciar o servidor**

   ```bash
   python main.py
   ```
6. **Acessar a interface**

   * Abra o navegador em `http://localhost:5000` e faça login para começar a baixar vídeos.
