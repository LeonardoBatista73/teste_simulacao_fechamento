import streamlit as st
from fpdf import FPDF
import json
import os
from datetime import datetime
from datetime import date
from datetime import date, timedelta
import time
import math

# 1. Configuração inicial
st.set_page_config(page_title="Simulador de Fechamento", layout="wide")


# 2. Inicializa o estado de segurança
if "logado" not in st.session_state:
    st.session_state.logado = False

# FASE 1: TELA DE LOGIN (Bloqueia o resto do código)
if not st.session_state.logado:

    col1, col2, col3 = st.columns([1, 2, 1]) # O meio é mais largo

    with col2:
        with st.container(border=True):
            st.subheader("🔒 Login | Simulador de Fechamento")
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if usuario == "admin" and senha == "123":
                    st.session_state.logado = True
                    st.rerun()
                else:
                    st.error("Dados incorretos.")

    st.stop() 

# Cria o cabeçalho: Título à esquerda e botão Sair à direita

topo_esquerda, topo_direita = st.columns([5, 1])

with topo_esquerda:
    st.title("📊 Simulador de Fechamento")
    
st.write("_________")

with topo_direita:
    # Espaçamento para alinhar verticalmente com o título
    st.write("") 
    if st.button("Sair", type="primary", use_container_width=True):
        st.session_state.logado = False
        st.rerun()

ARQUIVO_DADOS = "dados_planejamento.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_dados():
    dados = {}

    for chave, valor in st.session_state.items():

        if chave == "restaurar_backup_json":
            continue
        try:
            json.dumps(valor)
            dados[chave] = valor
        except TypeError:
            pass

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Carrega apenas uma vez
if "dados_restaurados" not in st.session_state:
    dados_salvos = carregar_dados()
    
    for chave, valor in dados_salvos.items():
        # restaura datas
        if chave.startswith("data_") and isinstance(valor, str):
            try:
                from datetime import datetime
                valor = datetime.strptime(valor, "%Y-%m-%d").date()
            except:
                pass

        st.session_state[chave] = valor

    st.session_state["dados_restaurados"] = True

top1, top2, top3 = st.columns([2, 2, 7.5])

# Obter datas para os campos de data
def obter_datas_semana_atual():
    hoje = date.today()

    segunda = hoje - timedelta(days=hoje.weekday())

    return {
        "data_seg": segunda,
        "data_ter": segunda + timedelta(days=1),
        "data_qua": segunda + timedelta(days=2),
        "data_qui": segunda + timedelta(days=3),
        "data_sex": segunda + timedelta(days=4),
        "data_sab": segunda + timedelta(days=5),
    }

if "cenario_backup" in st.session_state:
    st.session_state["cenario"] = st.session_state.pop("cenario_backup")

with top1:
    semana = st.selectbox(
        "📅 Semana",
        ["Semana 1", "Semana 2"])

# Ajuste prefixos
prefixo = "sem1" if semana == "Semana 1" else "sem2"

with top2:
    cenario = st.selectbox(
        "⚙️ Cenário",
        ["100 mil", "110 mil", "120 mil"],
        key="cenario"
    )

with top3:
    pass
    st.write("")
    st.info(f'{cenario}')

def qtd_noite():
    return {
        "100 mil": 4,
        "110 mil": 5,
        "120 mil": 6
    }.get(st.session_state.cenario, 4)

qtd = qtd_noite()

if "bolinhas" in st.session_state:

    for chave in [
        "seg_noite",
        "ter_noite",
        "qua_noite",
        "qui_noite",
        "sex_noite",
        "sabado_noite"
    ]:

        atual = st.session_state.bolinhas[chave]

        if len(atual) < qtd:
            atual.extend(["Vazio"] * (qtd - len(atual)))

        elif len(atual) > qtd:
            st.session_state.bolinhas[chave] = atual[:qtd]


st.write('')

info1, info2 , info3= st.columns([0.365, 1.5, 1.5])

with info1:
    st.write("")
    st.image(
        "giphy (1).gif")

with info2:

    st.markdown("""
    <div style="
        background-color: #262730;
        border-left: 5px solid #262730;
        padding: 8px;
        font-size: 16px;
        border-radius: 5px;
        margin: 8px 0;
    ">
        <h4 style="margin-top:0;">ℹ️ Informações</h4>
        <p>
            Cada círculo = 10.000 endereços
        </p>
        <p>
            Total de volume carregado = 80.000 endereços
        </p>
    </div>
    """, unsafe_allow_html=True)


with info3:
    st.markdown("""
    <div style="
        background-color: #262730;
        border-left: 6px solid #262730;
        padding: 12px;
        border-radius: 5px;
        margin: 8px 0;
        font-size: 18px;
        line-height: 1.48;
    ">
        <p>
            🟨 Fechamento de SP (⏰18:00)
        </p>
        <p>
            🟦 Fechamento de outros estados (⏰18:30)
        </p>
        <p>
            🟧 Fechamento de Londrina (⏰18:01)
        </p>
    </div>

    """, unsafe_allow_html=True)

st.write('')

btn1, btn2, btn3, btn4 = st.columns([0.1, 0.1, 0.1 ,1.7])

with btn1:
    st.write("")
    if st.button("🔄 Limpar cores"):

        prefixes = [
            "s_d_", "s_n_",
            "t_d_", "t_n_",
            "q_d_", "q_n_",
            "qu_d_", "qu_n_",
            "sex_d_", "sex_n_",
            "sabado_d_", "sabado_n_"
        ]

        for key in list(st.session_state.keys()):

            if any(key.startswith(prefix) for prefix in prefixes):
                st.session_state[key] = "Vazio"

        salvar_dados()
        st.rerun()

with btn2:
    st.write("")
    dados_exportacao = {}

    IGNORAR = {
        "restaurar_backup_json",
        "bolinhas"
    }

    for chave, valor in st.session_state.items():


        if chave in IGNORAR:
            continue

        try:
            if isinstance(valor, date):
                dados_exportacao[chave] = valor.isoformat()
            else:
                json.dumps(valor)
                dados_exportacao[chave] = valor

        except TypeError:
            pass
    
    # Salva o cenário atual
    dados_exportacao["cenario"] = st.session_state.get("cenario", "100 mil")
            
    json_download = json.dumps(
        dados_exportacao,
        ensure_ascii=False,
        indent=4
    )

    st.download_button(

        label="📥 Baixar Backup",
        data=json_download,
        file_name=f"planejamento_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )
    
with btn3:
    st.write("")
    if st.button("🆕 Novo Layout"):
        # Atualiza datas
        for chave, valor in obter_datas_semana_atual().items():
            st.session_state[chave] = valor

        # Limpa cores
        prefixes = [
            "s_d_", "s_n_",
            "t_d_", "t_n_",
            "q_d_", "q_n_",
            "qu_d_", "qu_n_",
            "sex_d_", "sex_n_",
            "sabado_d_", "sabado_n_"
        ]

        for key in list(st.session_state.keys()):

            if any(key.startswith(prefix) for prefix in prefixes):
                st.session_state[key] = "Vazio"

        # Zera volumes
        for key in list(st.session_state.keys()):

            if (
                key.startswith("valor1_")
                or key.startswith("valor2_")
                or key.startswith("valor3_")
            ):
                st.session_state[key] = 0

        salvar_dados()

        st.toast("Novo layout iniciado!", icon="✔️")
        time.sleep(2)
        st.rerun()

with btn4:
    arquivo_json = st.file_uploader(
        "Restaurar backup salvo:",
        type=["json"],
        key="restaurar_backup_json"
    )

    if arquivo_json is not None:
        if st.button("🔄 Restaurar", key="btn_restaurar_json"):
            try:    
                dados = json.load(arquivo_json)
                for chave, valor in dados.items():
                    # Ignora widgets internos
                    if chave in [
                        "restaurar_backup_json",
                        "dados_restaurados",
                        "logado",
                        "btn_restaurar_json",
                        "backup_restaurado",
                        "bolinhas"
                    ]:
                        continue
                    if chave == "cenario":
                        st.session_state["cenario_backup"] = valor
                        continue       
                    if chave.startswith("data_") and isinstance(valor, str):

                        try:
                            valor = datetime.strptime(
                                valor,
                                "%Y-%m-%d"
                            ).date()
                        except:
                            pass

                    st.session_state[chave] = valor

                salvar_dados()
            
                st.toast("Backup restaurado com sucesso!", icon="📃")
                time.sleep(2)
                st.rerun()

            except Exception as erro:

                st.error(f"Erro ao restaurar: {erro}")

st.write("")

# Função quantidade de quadrados
def quantidade_por_volume(valor):
    if valor <= 0:
        return 0

    return math.ceil(valor / 10000)

# Inicializa o estado das bolinhas nos campos se não existir

if "bolinhas" not in st.session_state:
    st.session_state.bolinhas = {
        "seg_dia": ["Vazio"] * 4,
        "seg_noite": ["Vazio"] * qtd_noite,
        "ter_dia": ["Vazio"] * 4,
        "ter_noite": ["Vazio"] * qtd_noite,
        "qua_dia": ["Vazio"] * 4,
        "qua_noite": ["Vazio"] * qtd_noite,
        "qui_dia": ["Vazio"] * 4,
        "qui_noite": ["Vazio"] * qtd_noite,
        "sex_dia": ["Vazio"] * 4,
        "sex_noite": ["Vazio"] * qtd_noite,
        "sabado": ["Vazio"] * 4,
        "sabado_noite": ["Vazio"] * qtd_noite
    }

# Deletar session para inclusão de campos
#if "bolinhas" in st.session_state:
    #del st.session_state["bolinhas"]

# Cria a estrutura de colunas na tela para organizar lado a lado

col_label, col_seg, col_ter, col_qua, col_qui, col_sex, col_sab = st.columns([0.2, 1, 1, 1, 1, 1, 1])

# --- COLUNA DA ESQUERDA: RÓTULOS DOS TURNOS ---

with col_label:
    st.markdown("<br><br><br>**Dia**", unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br><br><br>**Noite**", unsafe_allow_html=True)

# --- COLUNA: SEGUNDA-FEIRA ---

with col_seg:
    col_titulo_seg, col_data_seg = st.columns([2, 3])

    with col_titulo_seg:
        st.markdown(
            "<div style='margin-top:8px;'><b>Segunda-feira</b></div>",
            unsafe_allow_html=True
        )

    with col_data_seg:
        data_seg = st.date_input(
            "",
            key="data_seg",
            format="DD/MM/YYYY",
            label_visibility="collapsed"

        )

    # Caixa do turno do Dia (Segunda)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Seg Dia P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"s_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["seg_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Segunda)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(qtd_noite()):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Seg Noite P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"s_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["seg_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA SEGUNDA ---
    # Conta quantas de cada cor foram usadas na segunda (somando dia e noite)
    todas_seg = [st.session_state[f"s_d_{i}"]for i in range(4)] + [st.session_state[f"s_n_{i}"]for i in range(4)]
    usadas_amarela_seg = todas_seg.count("🟨")
    usadas_laranja_seg = todas_seg.count("🟧")
    usadas_azul_seg = todas_seg.count("🟦")

    # Exibição dos Dados e do Estoque Atualizado de Segunda
    st.write("---")

    cd1, cd2 = st.columns(2)

    with cd1:
        st.markdown("**Segunda-feira**")
        valor1_seg_sp = int(st.number_input("SP (18:00)    ", key="valor1_seg_sp"))
        valor2_seg_pr = int(st.number_input("PR (18:01)   ", key="valor2_seg_pr"))
        valor3_seg_outros = int(st.number_input("RS/SC/MG/RJ (18:30)    ", key="valor3_seg_outros"))

        st.metric("Total Dia", f"{valor1_seg_sp + valor2_seg_pr + valor3_seg_outros:,}".replace(",", "."))
    
        disponivel_amarela_seg = quantidade_por_volume(valor1_seg_sp)
        disponivel_laranja_seg = quantidade_por_volume(valor2_seg_pr)
        disponivel_azul_seg = quantidade_por_volume(valor3_seg_outros)

        saldo_amarela_seg = max(
            0,
            disponivel_amarela_seg - usadas_amarela_seg
        )

        saldo_laranja_seg = max(
            0,
            disponivel_laranja_seg - usadas_laranja_seg
        )

        saldo_azul_seg = max(
            0,
            disponivel_azul_seg - usadas_azul_seg
        )

    with cd2:
        st.markdown("**Restante:**")
        # Monta a linha visual das bolinhas restantes
        linha_amarela = "🟨" * saldo_amarela_seg
        linha_laranja = "🟧" * saldo_laranja_seg
        linha_azul = "🟦" * saldo_azul_seg

        st.write('')
        st.write('')
        st.write(f"{linha_amarela}" if linha_amarela else "Sem amarelas")
        st.write('')
        st.write('')
        st.write('')
        st.write(f"{linha_laranja}" if  linha_laranja else "Sem laranjas")
        st.write('')
        st.write('')
        st.write('')
        st.write(f"{linha_azul}" if linha_azul else "Sem azuis")

# --- COLUNA: TERÇA-FEIRA ---

with col_ter:
    col_titulo_ter, col_data_ter = st.columns([2, 3])

    with col_titulo_ter:
        st.markdown(
            "<div style='margin-top:8px;'><b>Terça-feira</b></div>",
            unsafe_allow_html=True
        )

    with col_data_ter:
        data_ter = st.date_input(
            "",
            key="data_ter",
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )


    # Caixa do turno do Dia (Terça)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Ter Dia P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"t_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["ter_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Terça)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(qtd_noite()):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Ter Noite P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"t_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["ter_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA TERÇA ---
    # Conta quantas de cada cor foram usadas na terça

    todas_ter = [st.session_state[f"t_d_{i}"]for i in range(4)] + [st.session_state[f"t_n_{i}"]for i in range(4)]
    usadas_amarela_ter = todas_ter.count("🟨")
    usadas_laranja_ter = todas_ter.count("🟧")
    usadas_azul_ter = todas_ter.count("🟦")

    # Exibição dos Dados e do Estoque Atualizado de Terça
    st.write("---")

    cdt1, cdt2 = st.columns(2)

    with cdt1:
        st.markdown("**Terça-feira**")
        valor1_ter_sp = int(st.number_input("SP (18:00)  ",key="valor1_ter_sp"))
        valor2_ter_pr = int(st.number_input("PR (18:01)  ", key="valor2_ter_pr"))
        valor3_ter_outros = int(st.number_input("RS/SC/MG/RJ (18:30)   ", key="valor3_ter_outros"))

        st.metric("Total Dia", f"{valor1_ter_sp + valor2_ter_pr + valor3_ter_outros:,}".replace(",", "."))

        disponivel_amarela_ter = quantidade_por_volume(valor1_ter_sp)
        disponivel_laranja_ter = quantidade_por_volume(valor2_ter_pr)
        disponivel_azul_ter = quantidade_por_volume(valor3_ter_outros)

        saldo_amarela_ter = max(
            0,
            disponivel_amarela_ter - usadas_amarela_ter
        )

        saldo_laranja_ter = max(
            0,
            disponivel_laranja_ter - usadas_laranja_ter
        )

        saldo_azul_ter = max(
            0,
            disponivel_azul_ter - usadas_azul_ter
        )

    with cdt2:
        st.markdown("**Restante:**")
        linha_amarela_t = "🟨" * saldo_amarela_ter
        linha_laranja_t = "🟧" * saldo_laranja_ter
        linha_azul_t = "🟦" * saldo_azul_ter

        st.write("")
        st.write("")
        st.write(f"{linha_amarela_t}" if (linha_amarela_t) else "Sem amarelas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_laranja_t}" if (linha_laranja_t) else "Sem laranjas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_azul_t}" if linha_azul_t else "Sem azuis")

# --- COLUNA: QUARTA-FEIRA ---

with col_qua:
    col_titulo_qua, col_data_qua = st.columns([2, 3])

    with col_titulo_qua:
        st.markdown(
            "<div style='margin-top:8px;'><b>Quarta-feira</b></div>",
            unsafe_allow_html=True
        )

    with col_data_qua:
        data_qua = st.date_input(
            "",
            key="data_qua",
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )

    # Caixa do turno do Dia (Quarta)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Qua Dia P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"q_d_{i}", label_visibility="collapsed")

            st.session_state.bolinhas["qua_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Quarta)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(qtd_noite()):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Qua Noite P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"q_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["qua_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA QUARTA ---
    # Conta quantas de cada cor foram usadas na Quarta
    todas_qua = [st.session_state[f"q_d_{i}"]for i in range(4)] + [st.session_state[f"q_n_{i}"]for i in range(4)]
    usadas_amarela_qua = todas_qua.count("🟨")
    usadas_laranja_qua = todas_qua.count("🟧")
    usadas_azul_qua = todas_qua.count("🟦")

    # Exibição dos Dados e do Estoque Atualizado de Quarta
    st.write("---")

    cdq1, cdq2 = st.columns(2)

    with cdq1:
        st.markdown("**Quarta-feira**")
        valor1_qua_sp = int(st.number_input("SP (18:00)  ", key="valor1_qua_sp"))
        valor2_qua_pr = int(st.number_input("PR (18:01) ",  key="valor2_qua_pr"))
        valor3_qua_outros = int(st.number_input("RS/SC/MG/RJ (18:30) ", key="valor3_qua_outros"))

        st.metric("Total Dia", f"{valor1_qua_sp + valor2_qua_pr + valor3_qua_outros:,}".replace(",", "."))

        disponivel_amarela_qua = quantidade_por_volume(valor1_qua_sp)
        disponivel_laranja_qua = quantidade_por_volume(valor2_qua_pr)
        disponivel_azul_qua = quantidade_por_volume(valor3_qua_outros)

        saldo_amarela_qua = max(
            0,
            disponivel_amarela_qua - usadas_amarela_qua
        )

        saldo_laranja_qua = max(
            0,
            disponivel_laranja_qua - usadas_laranja_qua
        )

        saldo_azul_qua = max(
            0,
            disponivel_azul_qua - usadas_azul_qua
        )

    with cdq2:
        st.markdown("**Restante:**")
        linha_amarela_q = "🟨" * saldo_amarela_qua
        linha_laranja_q = "🟧" * saldo_laranja_qua
        linha_azul_q = "🟦" * saldo_azul_qua

        st.write("")
        st.write("")
        st.write(f"{linha_amarela_q}" if linha_amarela_q else "Sem amarelas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_laranja_q}" if linha_laranja_q else "Sem laranjas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_azul_q}" if linha_azul_q else "Sem azuis")

# --- COLUNA: QUINTA-FEIRA ---

with col_qui:
    col_titulo_qui, col_data_qui = st.columns([2, 3])

    with col_titulo_qui:
        st.markdown(
            "<div style='margin-top:8px;'><b>Quinta-feira</b></div>",
            unsafe_allow_html=True
        )

    with col_data_qui:
        data_qui = st.date_input(
            "",
            key="data_qui",
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )

    # Caixa do turno do Dia (Quinta)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Qui Dia P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"qu_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["qui_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Quinta)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(qtd_noite()):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Qui Noite P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"qu_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["qui_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA QUINTA ---
    # Conta quantas de cada cor foram usadas na Quinta
    todas_qui = [st.session_state[f"qu_d_{i}"]for i in range(4)] + [st.session_state[f"qu_n_{i}"]for i in range(4)]
    usadas_amarela_qui = todas_qui.count("🟨")
    usadas_laranja_qui = todas_qui.count("🟧")
    usadas_azul_qui = todas_qui.count("🟦")

    # Exibição dos Dados e do Estoque Atualizado de Quinta
    st.write("---")

    cdqu1, cdqu2 = st.columns(2)

    with cdqu1:
        st.markdown("**Quinta-feira**")
        valor1_qui_sp = int(st.number_input("SP (18:00)", key="valor1_qui_sp"))
        valor2_qui_pr = int(st.number_input("PR (18:01)", key="valor2_qui_pr"))
        valor3_qui_outros = int(st.number_input("RS/SC/MG/RJ (18:30)", key="valor3_qui_outros"))

        st.metric("Total Dia", f"{valor1_qui_sp + valor2_qui_pr + valor3_qui_outros:,}".replace(",", "."))

        disponivel_amarela_qui = quantidade_por_volume(valor1_qui_sp)
        disponivel_laranja_qui = quantidade_por_volume(valor2_qui_pr)
        disponivel_azul_qui = quantidade_por_volume(valor3_qui_outros)

        saldo_amarela_qui = max(
            0,
            disponivel_amarela_qui - usadas_amarela_qui
        )

        saldo_laranja_qui = max(
            0,
            disponivel_laranja_qui - usadas_laranja_qui
        )

        saldo_azul_qui = max(
            0,
            disponivel_azul_qui - usadas_azul_qui
        )

    with cdqu2:
        st.markdown("**Restante:**")
        linha_amarela_qu = "🟨" * saldo_amarela_qui
        linha_laranja_qu = "🟧" * saldo_laranja_qui
        linha_azul_qu = "🟦" * saldo_azul_qui

        st.write("")
        st.write("")
        st.write(f"{linha_amarela_qu}" if (linha_amarela_qu) else "Sem amarelas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_laranja_qu}" if (linha_laranja_qu) else "Sem laranjas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_azul_qu}" if linha_azul_qu else "Sem azuis")

# --- COLUNA: SEXTA-FEIRA ---
with col_sex:
    col_titulo_sex, col_data_sex = st.columns([2, 3])

    with col_titulo_sex:
        st.markdown(
            "<div style='margin-top:8px;'><b>Sexta-feira</b></div>",
            unsafe_allow_html=True
        )

    with col_data_sex:
        data_sex = st.date_input(
            "",
            key="data_sex",
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )

    # Caixa do turno do Dia (Sexta)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Sex Dia P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"sex_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["sex_dia"][i] = opcao

    st.write(" ") # Espaçador

    # Caixa do turno da Noite (Sexta)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(qtd_noite()):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Sex Noite P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"sex_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["sex_noite"][i] = opcao

    # --- CÁLCULO DO ESTOQUE DA Sexta ---
    # Conta quantas de cada cor foram usadas na Sexta

    todas_sex = [st.session_state[f"sex_d_{i}"]for i in range(4)] + [st.session_state[f"sex_n_{i}"]for i in range(4)]
    usadas_amarela_sex = todas_sex.count("🟨")
    usadas_laranja_sex = todas_sex.count("🟧")
    usadas_azul_sex = todas_sex.count("🟦")

    # Exibição dos Dados e do Estoque Atualizado de Sexta
    st.write("---")

    cdsex1, cdsex2 = st.columns(2)

    with cdsex1:
        st.markdown("**Sexta-feira**")
        valor1_sex_sp = int(st.number_input("SP (18:00) ", key="valor1_sex_sp"))
        valor2_sex_pr = int(st.number_input("PR (18:01) ", key="valor2_sex_pr"))
        valor3_sex_outros = int(st.number_input("RS/SC/MG/RJ (18:30) ", key="valor3_sex_outros"))   

        st.metric("Total Dia", f"{valor1_sex_sp + valor2_sex_pr + valor3_sex_outros:,}".replace(",", "."))

        disponivel_amarela_sex = quantidade_por_volume(valor1_sex_sp)
        disponivel_laranja_sex = quantidade_por_volume(valor2_sex_pr)
        disponivel_azul_sex = quantidade_por_volume(valor3_sex_outros)

        saldo_amarela_sex = max(
            0,
            disponivel_amarela_sex - usadas_amarela_sex
        )

        saldo_laranja_sex = max(
            0,
            disponivel_laranja_sex - usadas_laranja_sex
        )

        saldo_azul_sex = max(
            0,
            disponivel_azul_sex - usadas_azul_sex
        )

    with cdsex2:
        st.markdown("**Restante:**")
        linha_amarela_sex = "🟨" * saldo_amarela_sex
        linha_laranja_sex = "🟧" * saldo_laranja_sex
        linha_azul_sex = "🟦" * saldo_azul_sex

        st.write("")
        st.write("")
        st.write(f"{linha_amarela_sex}" if linha_amarela_sex  else "Sem amarelas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_laranja_sex}" if linha_laranja_sex else "Sem laranjas")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"{linha_azul_sex}" if linha_azul_sex else "Sem azuis")

# Somando as regiões

sp_total_semana = valor1_seg_sp + valor1_ter_sp + valor1_qua_sp + valor1_qui_sp + valor1_sex_sp
pr_total_semana = valor2_seg_pr + valor2_ter_pr + valor2_qua_pr + valor2_qui_pr + valor2_sex_pr
outros_total_semana = valor3_seg_outros + valor3_ter_outros + valor3_qua_outros + valor3_qui_outros + valor3_sex_outros

# --- COLUNA: SABADO ---
with col_sab:
    col_titulo_sab, col_data_sab = st.columns([2, 3])

    with col_titulo_sab:
        st.markdown(
            "<div style='margin-top:8px;'><b>Sábado</b></div>",
            unsafe_allow_html=True
        )


    with col_data_sab:
        data_sab = st.date_input(
            "",
            key="data_sab",
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )

    # Caixa do turno do Dia (Sabado)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(4):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Sab Dia P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"sabado_d_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["sabado"][i] = opcao
    
    st.write("")

    # Caixa do turno da Noite (Sabado)
    with st.container(border=True):
        c1, c2 = st.columns(2)

        for i in range(qtd_noite()):
            col_alvo = c1 if i % 2 == 0 else c2
            opcao = col_alvo.selectbox(f"Sab Noite P{i+1}", ["Vazio", "🟨", "🟦", "🟧"], key=f"sabado_n_{i}", label_visibility="collapsed")
            st.session_state.bolinhas["sabado_noite"][i] = opcao


    st.write("---")
    
    cdsab1, cdsab2 = st.columns(2)

    with cdsab1:
        st.markdown("**Total**")
        sp_total_semana = st.number_input("SP(18:00)      ", value=sp_total_semana, disabled=True)
        pr_total_semana = st.number_input("PR(18:01)      ", value=pr_total_semana, disabled=True)
        outros_total_semana = st.number_input("RS/SC/MG/RJ(18:30)       ", value=outros_total_semana, disabled=True)

        st.metric("Total Semana", f"{sp_total_semana + pr_total_semana + outros_total_semana:,}".replace(",", "."))

