import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from io import BytesIO

import requests
from PIL import Image, ImageTk


# ============================================================
# CONFIGURAÇÕES
# ============================================================

API_BASE_URL = "https://pokemon.danielpimentel.com.br/v1/pokemon"

POKEMON_IMAGE_URL = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/"
    "master/sprites/pokemon/other/home/{}.png"
)

WINDOW_BACKGROUND = "#fcbbe0"

WINDOW_WIDTH = 740
WINDOW_HEIGHT = 940

BASE_DIR = Path(__file__).resolve().parent
TYPES_DIR = BASE_DIR / "Tipos"


# ============================================================
# FONTES
# ============================================================

FONT_TITLE = ("High Tower Text", 30)
FONT_SUBTITLE = ("High Tower Text", 20)
FONT_NAME = ("High Tower Text", 30, "bold", "italic")
FONT_SECTION = ("High Tower Text", 22, "bold")
FONT_INFO = ("High Tower Text", 17)
FONT_STATS = ("High Tower Text", 15)
FONT_TYPES = ("High Tower Text", 17, "bold")


# ============================================================
# FUNÇÕES DE API
# ============================================================

def buscar_lista_pokemon():
    """Busca a lista de Pokémon disponível na API."""

    url = f"{API_BASE_URL}/lista"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        pokemon_list = data["pokemon"]

        return [pokemon["nome"] for pokemon in pokemon_list]

    except requests.RequestException as error:
        messagebox.showerror(
            "Erro de conexão",
            "Não foi possível acessar a API de Pokémon.\n\n"
            f"Detalhes: {error}"
        )
        return []

    except (ValueError, KeyError):
        messagebox.showerror(
            "Erro",
            "A resposta recebida da API não possui o formato esperado."
        )
        return []


def buscar_pokemon(nome):
    """Busca os dados de um Pokémon pelo nome."""

    url = f"{API_BASE_URL}/nome/{nome}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return data["pokemon"]

    except requests.HTTPError:
        messagebox.showerror(
            "Pokémon não encontrado",
            f"Não foi possível encontrar o Pokémon '{nome}'."
        )
        return None

    except requests.RequestException as error:
        messagebox.showerror(
            "Erro de conexão",
            "Não foi possível acessar a API.\n\n"
            f"Detalhes: {error}"
        )
        return None

    except (ValueError, KeyError):
        messagebox.showerror(
            "Erro",
            "A resposta recebida da API não possui o formato esperado."
        )
        return None


# ============================================================
# FUNÇÕES DE IMAGEM
# ============================================================

def carregar_imagem_tipo(nome_tipo):
    """Carrega a imagem correspondente ao tipo do Pokémon."""

    caminho = TYPES_DIR / f"{nome_tipo}.png"

    try:
        return tk.PhotoImage(file=caminho)

    except tk.TclError:
        return None


def atualizar_imagens_tipos(tipos):
    """Atualiza as imagens dos tipos do Pokémon."""

    tipos_separados = [
        tipo.strip()
        for tipo in tipos.split(",")
    ]

    tipo_1 = tipos_separados[0]

    if len(tipos_separados) > 1:
        tipo_2 = tipos_separados[1]
    else:
        tipo_2 = "tracinho"

    imagem_tipo_1 = carregar_imagem_tipo(tipo_1)
    imagem_tipo_2 = carregar_imagem_tipo(tipo_2)

    if imagem_tipo_1:
        lblFoto2.configure(image=imagem_tipo_1)
        lblFoto2.image = imagem_tipo_1

    if imagem_tipo_2:
        lblFoto3.configure(image=imagem_tipo_2)
        lblFoto3.image = imagem_tipo_2


def carregar_imagem_pokemon(numero):
    """Baixa e prepara a imagem do Pokémon."""

    url = POKEMON_IMAGE_URL.format(numero)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        image = image.resize((200, 200))

        return ImageTk.PhotoImage(image)

    except (requests.RequestException, OSError):
        return None


# ============================================================
# FUNÇÕES DA INTERFACE
# ============================================================

def atualizar_informacoes(pokemon):
    """Atualiza os textos da interface."""

    lblNome["text"] = pokemon["nome"]

    lblNum["text"] = f"Número: {pokemon['numero']}"
    lblAltura["text"] = f"Altura: {pokemon['altura']} cm"
    lblPeso["text"] = f"Peso: {pokemon['peso']} g"
    lblGer["text"] = f"Geração: {pokemon['geracao']}"

    lblTipo["text"] = f"Tipos: {pokemon['tipo']}"

    lblHp["text"] = f"HP: {pokemon['hp']}"
    lblAtk["text"] = f"ATK: {pokemon['atk']}"
    lblDef["text"] = f"DEF: {pokemon['def']}"
    lblSpatk["text"] = f"Sp. Atk: {pokemon['spatk']}"
    lblSpdef["text"] = f"Sp. Def: {pokemon['spdef']}"
    lblSpeed["text"] = f"Speed: {pokemon['speed']}"

    lblEvolucoes["text"] = pokemon["evolucoes"]


def atualizar_imagem_pokemon(numero):
    """Atualiza a imagem principal do Pokémon."""

    imagem = carregar_imagem_pokemon(numero)

    if imagem:
        lblFoto.configure(image=imagem)
        lblFoto.image = imagem


def selecionar_pokemon(event=None):
    """Busca o Pokémon selecionado e atualiza a interface."""

    nome = cmbPoke.get().strip()

    if not nome:
        return

    pokemon = buscar_pokemon(nome)

    if pokemon is None:
        return

    atualizar_informacoes(pokemon)
    atualizar_imagens_tipos(pokemon["tipo"])
    atualizar_imagem_pokemon(pokemon["numero"])


def filtrar_pokemon(event=None):
    """Filtra a lista de Pokémon conforme o usuário digita."""

    texto = cmbPoke.get().lower().strip()

    if not texto:
        cmbPoke["values"] = pokemon_names
        return

    resultados = [
        nome
        for nome in pokemon_names
        if texto in nome.lower()
    ]

    cmbPoke["values"] = resultados

# ============================================================
# CARREGAR LISTA DE POKÉMON
# ============================================================

pokemon_names = buscar_lista_pokemon()


# ============================================================
# CONFIGURAÇÃO DA JANELA
# ============================================================

janela = tk.Tk()

janela.title("Pokédex")
janela.configure(bg=WINDOW_BACKGROUND)

janela.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
)

janela.resizable(False, False)


# ============================================================
# CONTAINER PRINCIPAL
# ============================================================

frame_principal = tk.Frame(
    janela,
    bg=WINDOW_BACKGROUND
)

frame_principal.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)


# ============================================================
# TÍTULO
# ============================================================

lblQuem = tk.Label(
    frame_principal,
    text="Quem é esse Pokémon?",
    background=WINDOW_BACKGROUND,
    font=FONT_TITLE
)

lblQuem.pack(
    pady=(0, 15)
)


# ============================================================
# ÁREA DE PESQUISA
# ============================================================

frame_busca = tk.Frame(
    frame_principal,
    bg=WINDOW_BACKGROUND
)

frame_busca.pack(
    fill="x",
    pady=5
)


lblSelecione = tk.Label(
    frame_busca,
    text="Pesquisar Pokémon:",
    background=WINDOW_BACKGROUND,
    font=FONT_SUBTITLE
)

lblSelecione.pack(
    side="left",
    padx=(0, 10)
)


cmbPoke = ttk.Combobox(
    frame_busca,
    font=("High Tower Text", 15),
    width=25
)

cmbPoke.pack(
    side="left"
)

cmbPoke["values"] = pokemon_names

cmbPoke.bind(
    "<KeyRelease>",
    filtrar_pokemon
)

cmbPoke.bind(
    "<<ComboboxSelected>>",
    selecionar_pokemon
)

cmbPoke.bind(
    "<Return>",
    selecionar_pokemon
)


# ============================================================
# ÁREA PRINCIPAL DO POKÉMON
# ============================================================

frame_pokemon = tk.Frame(
    frame_principal,
    bg=WINDOW_BACKGROUND
)

frame_pokemon.pack(
    fill="x",
    pady=15
)


# ============================================================
# IMAGEM DO POKÉMON
# ============================================================

imagem_inicial = TYPES_DIR / "Quem.png"

foto = tk.PhotoImage(
    file=imagem_inicial
)

lblFoto = tk.Label(
    frame_pokemon,
    background=WINDOW_BACKGROUND,
    image=foto
)

lblFoto.pack()


# ============================================================
# NOME
# ============================================================

lblNome = tk.Label(
    frame_pokemon,
    text="Nome",
    background=WINDOW_BACKGROUND,
    font=FONT_NAME
)

lblNome.pack(
    pady=(0, 10)
)


# ============================================================
# INFORMAÇÕES
# ============================================================

frame_informacoes = tk.Frame(
    frame_principal,
    bg=WINDOW_BACKGROUND
)

frame_informacoes.pack(
    pady=5
)


lblInfo = tk.Label(
    frame_informacoes,
    text="Informações",
    background=WINDOW_BACKGROUND,
    font=FONT_SECTION
)

lblInfo.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=(0, 8)
)


# ------------------------------------------------------------
# COLUNA 1
# ------------------------------------------------------------

lblNum = tk.Label(
    frame_informacoes,
    text="Número:",
    background=WINDOW_BACKGROUND,
    font=FONT_INFO
)

lblNum.grid(
    row=1,
    column=0,
    sticky="w",
    padx=25
)


lblAltura = tk.Label(
    frame_informacoes,
    text="Altura:",
    background=WINDOW_BACKGROUND,
    font=FONT_INFO
)

lblAltura.grid(
    row=2,
    column=0,
    sticky="w",
    padx=25
)


lblPeso = tk.Label(
    frame_informacoes,
    text="Peso:",
    background=WINDOW_BACKGROUND,
    font=FONT_INFO
)

lblPeso.grid(
    row=3,
    column=0,
    sticky="w",
    padx=25
)


lblGer = tk.Label(
    frame_informacoes,
    text="Geração:",
    background=WINDOW_BACKGROUND,
    font=FONT_INFO
)

lblGer.grid(
    row=4,
    column=0,
    sticky="w",
    padx=25
)


# ------------------------------------------------------------
# COLUNA 2
# ------------------------------------------------------------

lblTipo = tk.Label(
    frame_informacoes,
    text="Tipos:",
    background=WINDOW_BACKGROUND,
    font=FONT_INFO
)

lblTipo.grid(
    row=1,
    column=1,
    sticky="w",
    padx=25
)


lblIlustra = tk.Label(
    frame_informacoes,
    text="Tipos",
    background=WINDOW_BACKGROUND,
    font=FONT_TYPES
)

lblIlustra.grid(
    row=2,
    column=1,
    sticky="w",
    padx=25
)


# ------------------------------------------------------------
# IMAGENS DOS TIPOS
# ------------------------------------------------------------

frame_tipos = tk.Frame(
    frame_informacoes,
    bg=WINDOW_BACKGROUND
)

frame_tipos.grid(
    row=3,
    column=1,
    rowspan=2,
    sticky="w",
    padx=25
)


imagem_interrogacao = TYPES_DIR / "Interrogação.png"

foto_tipo_inicial = tk.PhotoImage(
    file=imagem_interrogacao
)


lblFoto2 = tk.Label(
    frame_tipos,
    background=WINDOW_BACKGROUND,
    image=foto_tipo_inicial
)

lblFoto2.pack(
    side="left",
    padx=(0, 5)
)


lblFoto3 = tk.Label(
    frame_tipos,
    background=WINDOW_BACKGROUND
)

lblFoto3.pack(
    side="left"
)

# ============================================================
# STATUS
# ============================================================

frame_status = tk.Frame(
    frame_principal,
    bg=WINDOW_BACKGROUND
)

frame_status.pack(
    pady=10
)


lblStatusTitulo = tk.Label(
    frame_status,
    text="Status",
    background=WINDOW_BACKGROUND,
    font=FONT_SECTION
)

lblStatusTitulo.pack(
    pady=(0, 10)
)


frame_stats = tk.Frame(
    frame_status,
    bg=WINDOW_BACKGROUND
)

frame_stats.pack()


# ------------------------------------------------------------
# FUNÇÃO PARA CRIAR OS CARDS DE STATUS
# ------------------------------------------------------------

def criar_card_status(parent, nome, linha, coluna):
    """Cria um card para exibir um atributo do Pokémon."""

    card = tk.Frame(
        parent,
        bg="#f7d5e8",
        width=120,
        height=65,
        highlightthickness=1,
        highlightbackground="#d99abb"
    )

    card.grid(
        row=linha,
        column=coluna,
        padx=6,
        pady=6
    )

    card.grid_propagate(False)

    titulo = tk.Label(
        card,
        text=nome,
        background="#f7d5e8",
        font=("High Tower Text", 12, "bold")
    )

    titulo.pack(
        pady=(5, 0)
    )

    valor = tk.Label(
        card,
        text="-",
        background="#f7d5e8",
        font=("High Tower Text", 17, "bold")
    )

    valor.pack()

    return valor


# ------------------------------------------------------------
# CARDS
# ------------------------------------------------------------

lblHp = criar_card_status(
    frame_stats,
    "HP",
    0,
    0
)

lblAtk = criar_card_status(
    frame_stats,
    "ATK",
    0,
    1
)

lblDef = criar_card_status(
    frame_stats,
    "DEF",
    0,
    2
)

lblSpatk = criar_card_status(
    frame_stats,
    "SP. ATK",
    1,
    0
)

lblSpdef = criar_card_status(
    frame_stats,
    "SP. DEF",
    1,
    1
)

lblSpeed = criar_card_status(
    frame_stats,
    "SPEED",
    1,
    2
)

# ============================================================
# EVOLUÇÕES
# ============================================================

frame_evolucoes = tk.Frame(
    frame_principal,
    bg=WINDOW_BACKGROUND
)

frame_evolucoes.pack(
    pady=10
)


lblEvolucoesTitulo = tk.Label(
    frame_evolucoes,
    text="Evoluções",
    background=WINDOW_BACKGROUND,
    font=FONT_SECTION
)

lblEvolucoesTitulo.pack(
    pady=(0, 5)
)


lblEvolucoes = tk.Label(
    frame_evolucoes,
    text="-",
    background="#f7d5e8",
    font=FONT_INFO,
    padx=15,
    pady=8,
    highlightthickness=1,
    highlightbackground="#d99abb"
)

lblEvolucoes.pack()


# ============================================================
# INICIAR APLICAÇÃO
# ============================================================

janela.mainloop()