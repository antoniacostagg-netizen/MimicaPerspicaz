import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import re

# Configuração para celular
st.set_page_config(
    page_title="Perspicaz Aleatório", 
    page_icon="📖", 
    layout="centered"
)

# CSS personalizado - BOTÃO AZUL e DESIGN MODERNO
st.markdown("""
<style>
    /* BOTÃO AZUL PRINCIPAL */
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border: none;
        padding: 20px 40px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 15px;
        width: 100%;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0052a3;
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(0,102,204,0.3);
    }
    
    /* NOME DO VERBETE EM DESTAQUE */
    .verbete-destaque {
        text-align: center;
        color: #0066cc;
        font-size: 36px;
        font-weight: bold;
        margin: 25px 0;
        padding: 25px;
        background: linear-gradient(135deg, #e6f7ff 0%, #ffffff 100%);
        border-radius: 20px;
        border: 4px solid #0066cc;
        box-shadow: 0 8px 25px rgba(0,102,204,0.15);
    }
    
    /* TÍTULO PRINCIPAL */
    .titulo-principal {
        text-align: center;
        color: #0066cc;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* CONTADOR */
    .stSuccess {
        background: linear-gradient(135deg, #e6f7ff 0%, #d1ecff 100%);
        border-left: 5px solid #0066cc;
        border-radius: 15px;
        padding: 20px;
        font-size: 18px;
        text-align: center;
    }
    
    /* LINK */
    .link-verbete {
        font-size: 18px;
        color: #0066cc;
        text-decoration: none;
        word-break: break-all;
        text-align: center;
        display: block;
        margin: 15px 0;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #e9ecef;
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
    "Batismo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Batismo/",
    "Céu": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/C%C3%A9u/",
    "Fé": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/F%C3%A9/",
    "Jesus": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jesus/",
    "Paraíso": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Para%C3%ADso/",
    "Esperança": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Esperan%C3%A7a/"
}

def buscar_verbetes_online():
    """Busca TODOS os verbetes do site jw.org automaticamente"""
    try:
        with st.spinner("🔍 Conectando ao jw.org para buscar verbetes..."):
            response = requests.get(INDEX_URL, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            verbetes = {}
            
            # Estratégia MELHORADA para encontrar verbetes
            # Procurar em listas e parágrafos que contêm links
            for elemento in soup.find_all(['li', 'p', 'div']):
                links = elemento.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    texto = link.get_text(strip=True)
                    
                    # Filtro MAIS RESTRITIVO para pegar apenas verbetes
                    if ('/Estudo-Perspicaz-das-Escrituras/' in href and 
                        texto and 
                        2 <= len(texto) <= 40 and
                        not any(palavra in texto.lower() for palavra in [
                            'índice', 'mapa', 'opções', 'voltar', 'pesquisa', 
                            'busca', 'pesquisar', 'procurar'
                        ]) and
                        not re.search(r'\d', texto) and  # Remove textos com números
                        not texto.startswith(('(', '[', '{', '<')) and
                        texto[0].isalpha() and  # Começa com letra
                        texto.isprintable()):  # Apenas caracteres imprimíveis
                        
                        url_completa = urljoin(BASE_URL, href)
                        verbetes[texto] = url_completa
            
            # Se não encontrou muitos verbetes, tentar método alternativo
            if len(verbetes) < 50:
                verbetes = VERBETES_FALLBACK.copy()
                st.info("ℹ️ Usando lista pré-definida de verbetes")
            
            return verbetes
            
    except Exception as e:
        st.error("⚠️ Não foi possível conectar ao site. Usando lista local de verbetes.")
        return VERBETES_FALLBACK

# Interface principal
st.markdown("<h1 class='titulo-principal'>📖 PERSPICAZ ALEATÓRIO</h1>", unsafe_allow_html=True)
st.markdown("---")

# Inicializar verbetes
if 'verbetes' not in st.session_state:
    st.session_state.verbetes = buscar_verbetes_online()

# Botão principal AZUL
if st.button("🎲 ESCOLHER VERBETE ALEATÓRIO", type="primary", use_container_width=True):
    if st.session_state.verbetes:
        verbete, link = random.choice(list(st.session_state.verbetes.items()))
        st.session_state.ultimo_verbete = (verbete, link)
        
        # Mostra o NOME DO VERBETE EM GRANDE DESTAQUE
        st.markdown(f"<div class='verbete-destaque'>{verbete}</div>", unsafe_allow_html=True)
        
        # Mostra o link
        st.markdown(f"<div class='link-verbete'>🔗 <strong>Link:</strong> {link}</div>", unsafe_allow_html=True)
        
        # Botão para abrir automaticamente
        if st.button("🌐 ABRIR VERBETE NO NAVEGADOR", use_container_width=True, key="abrir_verbete"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

# Contador de verbetes
st.success(f"**📊 VERBETES DISPONÍVEIS:** {len(st.session_state.verbetes)}")

# Botão para atualizar
if st.button("🔄 ATUALIZAR LISTA", use_container_width=True, key="atualizar"):
    with st.spinner("Buscando verbetes atualizados..."):
        st.session_state.verbetes = buscar_verbetes_online()
    st.success(f"✅ {len(st.session_state.verbetes)} verbetes carregados!")

# Busca de verbetes
st.markdown("---")
st.subheader("🔍 BUSCAR VERBETE")
busca = st.text_input("Digite o nome do verbete:", placeholder="Ex: amor, fé, Jesus...")

if busca:
    resultados = [v for v in st.session_state.verbetes.keys() if busca.lower() in v.lower()]
    if resultados:
        st.write(f"**📝 RESULTADOS ({len(resultados)}):**")
        for verbete in resultados[:8]:
            st.write(f"• **{verbete}**")
    else:
        st.info("❌ Nenhum verbete encontrado.")

# Último verbete escolhido
if 'ultimo_verbete' in st.session_state:
    st.markdown("---")
    st.subheader("🎯 ÚLTIMO VERBETE")
    verbete, link = st.session_state.ultimo_verbete
    st.markdown(f"**{verbete}**")
    st.markdown(f"🔗 {link}")

# Rodapé
st.markdown("---")
st.markdown("### 📱 COMO USAR:")
st.markdown("""
1. Clique em **🎲 ESCOLHER VERBETE ALEATÓRIO**
2. Use a busca para verbetes específicos  
3. Clique em **🌐 ABRIR VERBETE** para ler
4. Compartilhe com amigos!
""")

st.caption("✨ Desenvolvido para estudar as Escrituras • 📖 Estudo Perspicaz")
