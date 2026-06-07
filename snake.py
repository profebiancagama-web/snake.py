import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Jogo da Cobrinha 🐍", page_icon="🐍", layout="centered")

# CSS para travar a rolagem da página quando apertar as setas do teclado
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden; /* Trava a rolagem da página */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🐍 Jogo da Cobrinha")

# Velocidade do jogo: Atualiza a tela a cada 0.25 segundos
st_autorefresh(interval=250, key="game_loop")

# Tamanho do tabuleiro
LARGURA = 15
ALTURA = 15

# --- INICIALIZAÇÃO DO JOGO ---
if "cobrinha" not in st.session_state:
    st.session_state.cobrinha = [[7, 7], [7, 8], [7, 9]]
    st.session_state.direcao = "CIMA"
    st.session_state.comida = [3, 3]
    st.session_state.pontos = 0
    st.session_state.fim_de_jogo = False

# --- CAPTURA DE TECLAS DO TECLADO (COMPUTADOR) ---
# Esse script impede o navegador de rolar a página com as setas e muda a direção do jogo
components.html(
    f"""
    <script>
    const doc = window.parent.document;
    doc.onkeydown = function(e) {{
        if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].indexOf(e.key) > -1) {{
            e.preventDefault(); // Impede a página de se mexer!
        }}
        if (e.key === 'ArrowUp' && '{st.session_state.direcao}' !== 'BAIXO') window.parent.postMessage({{type: 'DIR', value: 'CIMA'}}, '*');
        if (e.key === 'ArrowDown' && '{st.session_state.direcao}' !== 'CIMA') window.parent.postMessage({{type: 'DIR', value: 'BAIXO'}}, '*');
        if (e.key === 'ArrowLeft' && '{st.session_state.direcao}' !== 'DIREITA') window.parent.postMessage({{type: 'DIR', value: 'ESQUERDA'}}, '*');
        if (e.key === 'ArrowRight' && '{st.session_state.direcao}' !== 'ESQUERDA') window.parent.postMessage({{type: 'DIR', value: 'DIREITA'}}, '*');
    }};
    </script>
    """,
    height=0
)

# Captura a mensagem enviada pelo JavaScript acima
if "direcao_nova" in st.session_state:
    st.session_state.direcao = st.session_state.direcao_nova

# --- LÓGICA DO MOVIMENTO ---
if not st.session_state.fim_de_jogo:
    cabeca = st.session_state.cobrinha[0].copy()
    
    if st.session_state.direcao == "CIMA": cabeca[0] -= 1
    elif st.session_state.direcao == "BAIXO": cabeca[0] += 1
    elif st.session_state.direcao == "ESQUERDA": cabeca[1] -= 1
    elif st.session_state.direcao == "DIREITA": cabeca[1] += 1

    # Verificar batidas
    if (cabeca[0] < 0 or cabeca[0] >= ALTURA or 
        cabeca[1] < 0 or cabeca[1] >= LARGURA or 
        cabeca in st.session_state.cobrinha):
        st.session_state.fim_de_jogo = True
    else:
        st.session_state.cobrinha.insert(0, cabeca)
        if cabeca == st.session_state.comida:
            st.session_state.pontos += 10
            while True:
                nova_comida = [random.randint(0, ALTURA-1), random.randint(0, LARGURA-1)]
                if nova_comida not in st.session_state.cobrinha:
                    st.session_state.comida = nova_comida
                    break
        else:
            st.session_state.cobrinha.pop()

# --- PLACAR ---
st.write(f"### Pontuação: **{st.session_state.pontos}**")

# --- CONTROLES VISUAIS (BONS PARA CELULAR) ---
# Organizados em formato de cruz para não empurrar a tela
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔼 Cima", use_container_width=True): st.session_state.direcao = "CIMA"

col4, col5, col6 = st.columns([1, 2, 1])
with col4:
    if st.button("◀️ Esquerda", use_container_width=True): st.session_state.direcao = "ESQUERDA"
with col5:
    st.write("") # Espaço em branco no meio
with col6:
    if st.button("▶️ Direita", use_container_width=True): st.session_state.direcao = "DIREITA"

col7, col8, col9 = st.columns([1, 2, 1])
with col8:
    if st.button("🔽 Baixo", use_container_width=True): st.session_state.direcao = "BAIXO"

st.write("---")

# --- DESENHAR O TABULEIRO ---
tabuleiro_visual = ""
for l in range(ALTURA):
    linha_texto = ""
    for c in range(LARGURA):
        if [l, c] == st.session_state.cobrinha[0]:
            linha_texto += "🟢"
        elif [l, c] in st.session_state.cobrinha:
            linha_texto += "🟩"
        elif [l, c] == st.session_state.comida:
            linha_texto += "🍎"
        else:
            linha_texto += "⬜"
    tabuleiro_visual += linha_texto + "\n"

# Mostra o tabuleiro sem deixar as linhas se separarem
st.markdown(f"<div style='font-size:22px; font-family: monospace; letter-spacing: 0px; line-height: 1.1; text-align: center;'>{tabuleiro_visual}</div>", unsafe_allow_html=True)

# --- TELA DE GAME OVER ---
if st.session_state.fim_de_jogo:
    st.error("💥 FIM DE JOGO!")
    if st.button("Reiniciar Jogo 🔄"):
        st.session_state.cobrinha = [[7, 7], [7, 8], [7, 9]]
        st.session_state.direcao = "CIMA"
        st.session_state.comida = [3, 3]
        st.session_state.pontos = 0
        st.session_state.fim_de_jogo = False
        st.rerun()
