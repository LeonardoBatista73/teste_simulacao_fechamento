import streamlit as st

# Configura a página do Streamlit para tela cheia
st.set_page_config(layout="wide")

# Título principal da página
st.title("📊 Painel Semanal Interativo")
st.markdown("### Primeira semana VA")

# Inicializa o estoque de bolinhas alocadas se não existirem
if "bolinhas" not in st.session_state:
    st.session_state.bolinhas = {
        "seg_dia": ["Vazio", "Vazio", "Vazio", "Vazio"],
        "seg_noite": ["Vazio", "Vazio", "Vazio", "Vazio", "Vazio", "Vazio"],
        "ter_dia": ["Vazio", "Vazio", "Vazio", "Vazio"],
        "ter_noite": ["Vazio", "Vazio", "Vazio", "Vazio", "Vazio", "Vazio"],
    }

# Cria a estrutura de colunas na tela para organizar lado a lado
col_label, col_seg, col_regiao, col_ter = st.columns([1, 3, 2, 3])

# --- COLUNA DA ESQUERDA: RÓTULOS DOS TURNOS ---
with col_label:
    st.write("### ")
    st.markdown("<br><br>**Dia**", unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br><br>**Noite**", unsafe_allow_html=True)

# --- COLUNA: SEGUNDA-FEIRA ---
with col_seg:
    st.subheader("segunda 04/01")
    
    # Caixa do turno do Dia (Segunda)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Posição {i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"s_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["seg_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Segunda)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(6):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Posição {i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"s_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["seg_noite"][i] = opcao

    # Dados inferiores de segunda
    st.write("---")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.code("39117\n12433\n49165\n100715")
    with cd2:
        st.write("🟡 🟡 🟡 🟡 🟡 🟠")
        st.write("🔵 🔵 🔵 🔵 🔵 🔵")

# --- COLUNA CENTRAL: IDENTIFICADORES DE REGIÃO ---
with col_regiao:
    st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("**SP**")
    st.markdown("**PR**")
    st.markdown("**RS/SC/MG/RJ**")
    st.markdown("**Total Dia**")

# --- COLUNA: TERÇA-FEIRA ---
with col_ter:
    st.subheader("terça 05/01")
    
    # Caixa do turno do Dia (Terça)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Posição {i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"t_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["ter_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Terça)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(6):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Posição {i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"t_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["ter_noite"][i] = opcao

    # Dados inferiores de terça
    st.write("---")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.code("42634\n1888\n75444\n119966")
    with cd2:
        st.write("🟡 🟡 🟡 🟡 🟡")
        st.write("🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵")
