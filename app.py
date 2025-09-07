import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

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
    
    /* BOTÃO SECUNDÁRIO */
    .secondary-button {
        background-color: #6c757d !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
    }
    .secondary-button:hover {
        background-color: #5a6268 !important;
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
        with st.spinner("🔍 Conectando ao jw.org para buscar todos os verbetes..."):
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
                    texto and 
                    2 <= len(texto) <= 50 and  # Nomes entre 2 e 50 caracteres
                    'índice' not in texto.lower() and
                    'mapa' not in texto.lower() and
                    'opções' not in texto.lower() and
                    not any(char.isdigit() for char in texto) and  # Remove números
                    not texto.startswith(('(', '[', '{'))):  # Remove textos que começam com símbolos
                    
                    url_completa = urljoin(BASE_URL, href)
                    verbetes[texto] = url_completa
            
            return verbetes if verbetes else VERBETES_FALLBACK
            
    except Exception as e:
        st.error("⚠️ Não foi possível conectar ao site. Usando lista local de verbetes.")
        return VERBETES_FALLBACK

# Interface principal
st.markdown("<h1 class='titulo-principal'>📖 PERSPICAZ ALEATÓRIO</h1>", unsafe_allow_html=True)
st.markdown("---")

# Inicializar verbetes
if 'verbetes' not in st.session_state:
    st.session_state.verbetes = buscar_verbetes_online()
    st.session_state.verbetes_carregados = True

# Botão principal AZUL - GRANDE E BONITO
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

# Botão para atualizar a lista
if st.button("🔄 ATUALIZAR LISTA DE VERBETES", use_container_width=True, key="atualizar_lista"):
    with st.spinner("Atualizando lista de verbetes..."):
        st.session_state.verbetes = buscar_verbetes_online()
    st.success(f"✅ Lista atualizada! {len(st.session_state.verbetes)} verbetes disponíveis.")

# Contador de verbetes
st.success(f"**📊 TOTAL DE VERBETES DISPONÍVEIS:** {len(st.session_state.verbetes)}")

# Busca de verbetes
st.markdown("---")
st.subheader("🔍 BUSCAR VERBETE ESPECÍFICO")
busca = st.text_input("Digite o nome do verbete que deseja procurar:", placeholder="Ex: amor, fé, Jesus...")

if busca:
    resultados = [v for v in st.session_state.verbetes.keys() if busca.lower() in v.lower()]
    if resultados:
        st.write(f"**📝 RESULTADOS ENCONTRADOS ({len(resultados)}):**")
        for verbete in resultados[:10]:  # Mostra até 10 resultados
            st.write(f"• **{verbete}**")
        
        if len(resultados) > 10:
            st.info(f"Mostrando 10 de {len(resultados)} resultados. Use um termo mais específico para ver mais.")
    else:
        st.info("❌ Nenhum verbete encontrado com esse termo.")

# Último verbete sorteado
if 'ultimo_verbete' in st.session_state:
    st.markdown("---")
    st.subheader("🎯 ÚLTIMO VERBETE ESCOLHIDO")
    verbete, link = st.session_state.ultimo_verbete
    st.markdown(f"**{verbete}**")
    st.markdown(f"🔗 {link}")

# Rodapé
st.markdown("---")
st.markdown("### 📱 COMO USAR:")
st.markdown("""
1. Clique em **🎲 ESCOLHER VERBETE ALEATÓRIO** para sortear um verbete
2. Use a busca para encontrar verbetes específicos  
3. Clique em **🌐 ABRIR VERBETE** para ler no site oficial
4. Compartilhe o app com seus amigos!
""")

st.caption("✨ Desenvolvido para estudar as Escrituras • 📖 Estudo Perspicaz das Escrituras")
