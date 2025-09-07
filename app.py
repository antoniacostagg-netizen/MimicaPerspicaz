import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import random
import time
import re

# Configuração para celular
st.set_page_config(
    page_title="Escolhedor Perspicaz", 
    page_icon="📖", 
    layout="centered"
)

# CSS para botão AZUL personalizado
st.markdown("""
<style>
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #0052a3;
        color: white;
    }
    h1, h2 {
        text-align: center;
        color: #0066cc;
    }
    .stSuccess {
        background-color: #e6f7ff;
        border-left: 4px solid #0066cc;
    }
    .verbete-name {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
        text-align: center;
        margin: 20px 0;
        padding: 10px;
        background-color: #e6f7ff;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Configurações
BASE_URL = "https://www.jw.org"
INDEX_URL = "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Índice-de-Assuntos/"

# Fallback caso não consiga buscar online
VERBETES_FALLBACK = {
    "Abel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abel/",
    "Abraão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abra%C3%A3o/",
    "Amor": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Amor/",
    "Anjos": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Anjos/",
    # ... (mais verbetes de fallback)
}

def extrair_nome_do_url(url):
    """Extrai o nome do verbete a partir do URL"""
    try:
        # Encontra a parte do URL que contém o nome do verbete
        padrao = r"/Estudo-Perspicaz-das-Escrituras/([^/#]+)"
        correspondencia = re.search(padrao, url)
        
        if correspondencia:
            nome_codificado = correspondencia.group(1)
            # Decodifica caracteres especiais (ex: %C3%A3 -> ã)
            nome = unquote(nome_codificado)
            # Remove traços e capitaliza palavras
            nome = nome.replace("-", " ").replace("_", " ").title()
            return nome
    except:
        pass
    return "Nome não disponível"

def buscar_verbetes_online():
    """Busca TODOS os verbetes do site jw.org automaticamente"""
    try:
        with st.spinner("🔄 Conectando ao jw.org..."):
            response = requests.get(INDEX_URL, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            verbetes = {}
            
            # Procura por TODOS os links do Índice
            for link in soup.find_all('a', href=True):
                href = link['href']
                texto = link.get_text(strip=True)
                
                # Filtra apenas links do Estudo Perspicaz
                if ('/Estudo-Perspicaz-das-Escrituras/' in href and 
                    texto and len(texto) < 50 and
                    'índice' not in texto.lower() and
                    'mapa' not in texto.lower() and
                    not texto.startswith('[')):
                    
                    url_completa = urljoin(BASE_URL, href)
                    verbetes[texto] = url_completa
            
            return verbetes if verbetes else VERBETES_FALLBACK
            
    except Exception as e:
        st.error("⚠️ Não foi possível buscar online. Usando lista local.")
        return VERBETES_FALLBACK

# Interface principal
st.markdown("<h1>📖 Escolhedor Perspicaz</h1>", unsafe_allow_html=True)
st.markdown("---")

# Inicializar verbetes
if 'verbetes' not in st.session_state:
    st.session_state.verbetes = buscar_verbetes_online()
    st.session_state.verbetes_carregados = True

# Botão principal AZUL
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🎲 ESCOLHER ALEATORIAMENTE", type="primary", use_container_width=True):
        if st.session_state.verbetes:
            verbete, link = random.choice(list(st.session_state.verbetes.items()))
            st.session_state.ultimo_verbete = (verbete, link)
            
            # Extrai o nome do verbete do URL se necessário
            nome_verbete = extrair_nome_do_url(link)
            
            # Mostra o NOME do verbete em destaque
            st.markdown(f'<div class="verbete-name">{nome_verbete}</div>', unsafe_allow_html=True)
            
            # Mostra também o nome original (se diferente)
            if nome_verbete.lower() != verbete.lower():
                st.markdown(f"<p style='text-align:center'>({verbete})</p>", unsafe_allow_html=True)
            
            # Número de referência (simulado)
            num_ref = f"1:{random.randint(1, 2000)}"
            st.markdown(f"<p style='text-align:center'><strong>Referência:</strong> {num_ref}</p>", unsafe_allow_html=True)
            
            st.markdown(f"**🔗 Link:** {link}")
            
            # Botão para abrir automaticamente
            if st.button("🌐 Abrir no Navegador", key="abrir_link", use_container_width=True):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

with col2:
    if st.button("🔄 Atualizar", use_container_width=True):
        st.session_state.verbetes = buscar_verbetes_online()
        st.success(f"✅ {len(st.session_state.verbetes)} verbetes carregados!")

# Contador de verbetes
st.success(f"**📊 Verbetes Disponíveis:** {len(st.session_state.verbetes)}")

# Busca
st.markdown("---")
st.subheader("🔍 Buscar Verbete")
busca = st.text_input("Digite o nome do verbete:")
if busca:
    resultados = [v for v in st.session_state.verbetes.keys() if busca.lower() in v.lower()]
    if resultados:
        st.write(f"**📝 Resultados ({len(resultados)}):**")
        for verbete in resultados[:8]:
            st.write(f"• **{verbete}**")
    else:
        st.info("❌ Nenhum verbete encontrado.")

# Último verbete escolhido
if 'ultimo_verbete' in st.session_state:
    st.markdown("---")
    st.subheader("📌 Último Verbete Escolhido")
    verbete, link = st.session_state.ultimo_verbete
    nome_verbete = extrair_nome_do_url(link)
    st.markdown(f"**{nome_verbete}**")
    if nome_verbete.lower() != verbete.lower():
        st.markdown(f"({verbete})")
    st.markdown(f"🔗 {link}")

# Rodapé
st.markdown("---")
st.caption("📱 App com TODOS os verbetes • ✨ Compartilhe com amigos!")
