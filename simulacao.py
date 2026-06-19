import streamlit as st

# Configura a página do Streamlit para tela cheia
st.set_page_config(layout="wide")

# Título principal da página
st.title("📊 Painel Semanal Interativo")
st.markdown("### Primeira semana VA")

# Inicializa o estado das bolinhas nos campos se não existir
if "bolinhas" not in st.session_state:
    st.session_state.bolinhas = {
        "seg_dia": ["Vazio"] * 4,
        "seg_noite": ["Vazio"] * 6,
        "ter_dia": ["Vazio"] * 4,
        "ter_noite": ["Vazio"] * 6,
    }

# Cria a estrutura de colunas na tela para organizar lado a lado
col_label, col_seg, col_regiao, col_ter = st.columns([1, 4, 2, 4])

# --- COLUNA DA ESQUERDA: RÓTULOS DOS TURNOS ---
with col_label:
    st.markdown("<br><br><br>**Dia**", unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br><br><br><br>**Noite**", unsafe_allow_html=True)

# --- COLUNA: SEGUNDA-FEIRA ---
with col_seg:
    st.subheader("segunda 04/01")
    
    # Caixa do turno do Dia (Segunda)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Seg Dia P{i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"s_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["seg_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Segunda)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(6):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Seg Noite P{i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"s_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["seg_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA SEGUNDA ---
    # Conta quantas de cada cor foram usadas na segunda (somando dia e noite)
    todas_seg = st.session_state.bolinhas["seg_dia"] + st.session_state.bolinhas["seg_noite"]
    usadas_amarela_seg = todas_seg.count("🟡 Amarela")
    usadas_laranja_seg = todas_seg.count("🟠 Laranja")
    usadas_azul_seg = todas_seg.count("🔵 Azul")

    # Estoque Inicial da Imagem: 5 Amarelas, 1 Laranja, 6 Azuis
    saldo_amarela_seg = max(0, 5 - usadas_amarela_seg)
    saldo_laranja_seg = max(0, 1 - usadas_laranja_seg)
    saldo_azul_seg = max(0, 6 - usadas_azul_seg)

    # Exibição dos Dados e do Estoque Atualizado de Segunda
    st.write("---")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.code("39117\n12433\n49165\n100715")
    with cd2:
        st.markdown("**Restante:**")
        # Monta a linha visual das bolinhas restantes
        linha_amarela = "🟡 " * saldo_amarela_seg
        linha_laranja = "🟠 " * saldo_laranja_seg
        linha_azul = "🔵 " * saldo_azul_seg
        
        st.write(f"{linha_amarela}{linha_laranja}" if (linha_amarela or linha_laranja) else "Sem amarelas/laranjas")
        st.write(f"{linha_azul}" if linha_azul else "Sem azuis")

# --- COLUNA CENTRAL: IDENTIFICADORES DE REGIÃO ---
with col_regiao:
    st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
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
            opcao = col_alvo.selectbox(f"Ter Dia P{i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"t_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["ter_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Terça)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        for i in range(6):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Ter Noite P{i+1}", ["Vazio", "🟡 Amarela", "🔵 Azul", "🟠 Laranja"], key=f"t_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["ter_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA TERÇA ---
    # Conta quantas de cada cor foram usadas na terça
    todas_ter = st.session_state.bolinhas["ter_dia"] + st.session_state.bolinhas["ter_noite"]
    usadas_amarela_ter = todas_ter.count("🟡 Amarela")
    usadas_laranja_ter = todas_ter.count("🟠 Laranja")
    usadas_azul_ter = todas_ter.count("🔵 Azul")

    # Estoque Inicial da Imagem: 5 Amarelas, 0 Laranja, 8 Azuis
    saldo_amarela_ter = max(0, 5 - usadas_amarela_ter)
    saldo_laranja_ter = max(0, 0 - usadas_laranja_ter)
    saldo_azul_ter = max(0, 8 - usadas_azul_ter)

    # Exibição dos Dados e do Estoque Atualizado de Terça
    st.write("---")
    cdt1, cdt2 = st.columns(2)
    with cdt1:
        st.code("42634\n1888\n75444\n119966")
    with cdt2:
        st.markdown("**Restante:**")
        linha_amarela_t = "🟡 " * saldo_amarela_ter
        linha_laranja_t = "🟠 " * saldo_laranja_ter
        linha_azul_t = "🔵 " * saldo_azul_ter
        
        st.write(f"{linha_amarela_t}{linha_laranja_t}" if (linha_amarela_t or linha_laranja_t) else "Sem amarelas/laranjas")
        st.write(f"{linha_azul_t}" if linha_azul_t else "Sem azuis")
