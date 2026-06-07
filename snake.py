import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Jogo da Cobrinha 🐍", page_icon="🐍", layout="centered")
st.title("🐍 Jogo da Cobrinha da Família")

# Atualiza a tela a cada 0.3 segundos para a cobrinha andar
st_autorefresh(interval=300, key="game_loop")

# Tamanho do tabuleiro
LARGURA = 15
ALTURA = 15

# --- INICIALIZAÇÃO DO JOGO ---
if "cobrinha" not in st.session_state:
    st.session_state.cobrinha = [[7, 7], [7, 8], [7, 9]] # Corpo inicial
    st.session_state.direcao = "CIMA"
    st.session_state.comida = [3, 3]
    st.session_state.pontos = 0
    st.session_state.fim_de_jogo = False

# --- CONTROLES (BOTÕES NA TELA) ---
st.write("### Controle a Cobrinha:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅️ Esquerda"): st.session_state.direcao = "ESQUERDA"
with col2:
    if st.button("⬆️ Cima"): st.session_state.direcao = "CIMA"
with col3:
    if st.button("⬇️ Baixo"): st.session_state.direcao = "BAIXO"
with col4:
    if st.button("➡️ Direita"): st.session_state.direcao = "DIREITA"

# --- LÓGICA DO MOVIMENTO ---
if not st.session_state.fim_de_jogo:
    cabeca = st.session_state.cobrinha[0].copy()
    
    if st.session_state.direcao == "CIMA": cabeca[0] -= 1
    elif st.session_state.direcao == "BAIXO": cabeca[0] += 1
    elif st.session_state.direcao == "ESQUERDA": cabeca[1] -= 1
    elif st.session_state.direcao == "DIREITA": cabeca[1] += 1

    # Verificar se bateu nas paredes ou nela mesma
    if (cabeca[0] < 0 or cabeca[0] >= ALTURA or 
        cabeca[1] < 0 or cabeca[1] >= LARGURA or 
        cabeca in st.session_state.cobrinha):
        st.session_state.fim_de_jogo = True
    else:
        # Move a cabeça
        st.session_state.cobrinha.insert(0, cabeca)
        
        # Verificar se comeu a comida
        if cabeca == st.session_state.comida:
            st.session_state.pontos += 10
            # Gera nova comida em posição aleatória
            while True:
                nova_comida = [random.randint(0, ALTURA-1), random.randint(0, LARGURA-1)]
                if nova_comida not in st.session_state.cobrinha:
                    st.session_state.comida = nova_comida
                    break
        else:
            # Se não comeu, remove o rabo para continuar do mesmo tamanho
            st.session_state.cobrinha.pop()

# --- DESENHAR O TABULEIRO ---
st.write(f"### Pontuação: **{st.session_state.pontos}**")

tabuleiro_visual = ""
for l in range(ALTURA):
    linha_texto = ""
    for c in range(LARGURA):
        if [l, c] == st.session_state.cobrinha[0]:
            linha_texto += "🟢" # Cabeça da cobrinha
        elif [l, c] in st.session_state.cobrinha:
            linha_texto += "🟩" # Corpo da cobrinha
        elif [l, c] == st.session_state.comida:
            linha_texto += "🍎" # Comida
        else:
            linha_texto += "⬜" # Espaço vazio
    tabuleiro_visual += linha_texto + "\n\n"

# Mostra o tabuleiro na tela formatado
st.markdown(f"<div style='font-size:20px; letter-spacing: 2px; line-height: 1;'>{tabuleiro_visual}</div>", unsafe_allow_html=True)

# --- TELA DE GAME OVER ---
if st.session_state.fim_de_jogo:
    st.error("💥 FIM DE JOGO! A cobrinha bateu!")
    if st.button("Reiniciar Jogo 🔄"):
        st.session_state.cobrinha = [[7, 7], [7, 8], [7, 9]]
        st.session_state.direcao = "CIMA"
        st.session_state.comida = [3, 3]
        st.session_state.pontos = 0
        st.session_state.fim_de_jogo = False
        st.rerun()
