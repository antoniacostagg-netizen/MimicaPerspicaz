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

# CSS personalizado
st.markdown("""
<style>
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
    }
    .stButton > button:hover {
        background-color: #0052a3;
    }
    .verbete-destaque {
        text-align: center;
        color: #0066cc;
        font-size: 36px;
        font-weight: bold;
        margin: 25px 0;
        padding: 25px;
        background: #e6f7ff;
        border-radius: 20px;
        border: 4px solid #0066cc;
    }
    .titulo-principal {
        text-align: center;
        color: #0066cc;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .stSuccess {
        background: #e6f7ff;
        border-left: 5px solid #0066cc;
        border-radius: 15px;
        padding: 20px;
        font-size: 18px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Configurações
BASE_URL = "https://www.jw.org"
INDEX_URL = "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Índice-de-Assuntos/"

# Fallback com verbetes principais
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
    "Esperança": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Esperan%C3%A7a/",
    "Deus": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Deus/",
    "Espírito Santo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Esp%C3%ADrito-Santo/",
    "Igreja": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Igreja/",
    "Bíblia": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/B%C3%ADblia/",
    "Criação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Cria%C3%A7%C3%A3o/",
    "Salvação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Salva%C3%A7%C3%A3o/",
    "Ressurreição": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ressurrei%C3%A7%C3%A3o/",
    "Alma": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Alma/",
    "Inferno": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Inferno/",
    "Profecia": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Profecia/",
    "Milagres": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Milagres/",
    "Apóstolos": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ap%C3%B3stolos/"
}

def buscar_todos_verbetes():
    """Busca TODOS os verbetes diretamente do índice do site JW.org"""
    try:
        with st.spinner("🌐 Conectando ao JW.org para buscar todos os verbetes..."):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(INDEX_URL, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            verbetes = {}
            
            # Estratégia MELHORADA: Buscar em todas as tags que podem conter links de verbetes
            for tag in soup.find_all(['a', 'li', 'p', 'div', 'span']):
                if tag.name == 'a' and tag.has_attr('href'):
                    href = tag['href']
                    texto = tag.get_text(strip=True)
                else:
                    # Para outras tags, procurar links dentro delas
                    link = tag.find('a', href=True)
                    if not link:
                        continue
                    href = link['href']
                    texto = link.get_text(strip=True) or tag.get_text(strip=True)
                
                # Filtro PRECISO para verbetes do Estudo Perspicaz
                if ('/Estudo-Perspicaz-das-Escrituras/' in href and 
                    texto and 2 <= len(texto) <= 60 and
                    not any(palavra in texto.lower() for palavra in [
                        'índice', 'mapa', 'opções', 'voltar', 'pesquisa', 
                        'busca', 'pesquisar', 'procurar', 'download', 'pdf',
                        'epub', 'jw.org', 'biblioteca', 'livros'
                    ]) and
                    not re.search(r'\d', texto) and  # Remove textos com números
                    texto[0].isalpha() and  # Começa com letra
                    not texto.startswith(('(', '[', '{', '<')) and
                    '..' not in texto and
                    '...' not in texto):
                    
                    url_completa = urljoin(BASE_URL, href)
                    # Garantir que é um URL válido do JW.org
                    if 'jw.org' in url_completa and '/Estudo-Perspicaz-das-Escrituras/' in url_completa:
                        verbetes[texto] = url_completa
            
            # Se encontrou verbetes, retornar; senão usar fallback
            if verbetes:
                return dict(sorted(verbetes.items()))
            else:
                st.warning("⚠️ Não foram encontrados verbetes. Usando lista pré-definida.")
                return VERBETES_FALLBACK
            
    except Exception as e:
        st.error(f"❌ Erro ao conectar: {str(e)}")
        st.info("📋 Usando lista pré-definida de verbetes")
        return VERBETES_FALLBACK

# Interface principal
st.markdown("<h1 class='titulo-principal'>📖 PERSPICAZ ALEATÓRIO</h1>", unsafe_allow_html=True)
st.markdown("---")

# Inicializar verbetes
if 'verbetes' not in st.session_state:
    st.session_state.verbetes = buscar_todos_verbetes()
    st.session_state.carregado = True

# Botão principal
col1, col2 = st.columns([3, 1])

with col1:
    if st.button("🎲 ESCOLHER VERBETE ALEATÓRIO", type="primary", use_container_width=True):
        if st.session_state.verbetes:
            verbete, link = random.choice(list(st.session_state.verbetes.items()))
            st.session_state.ultimo_verbete = (verbete, link)
            
            st.markdown(f"<div class='verbete-destaque'>{verbete}</div>", unsafe_allow_html=True)
            st.markdown(f"**🔗 Link:** {link}")
            
            if st.button("🌐 ABRIR NO NAVEGADOR", use_container_width=True):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

with col2:
    if st.button("🔄 ATUALIZAR", use_container_width=True):
        with st.spinner("Atualizando..."):
            st.session_state.verbetes = buscar_todos_verbetes()
        st.success(f"✅ {len(st.session_state.verbetes)} verbetes!")

# Contador
st.success(f"**📊 TOTAL DE VERBETES:** {len(st.session_state.verbetes)}")

# Busca
st.markdown("---")
st.subheader("🔍 BUSCAR VERBETE")
busca = st.text_input("Digite o nome do verbete:", placeholder="Ex: amor, fé, Jesus...")

if busca:
    resultados = [v for v in st.session_state.verbetes.keys() if busca.lower() in v.lower()]
    if resultados:
        st.write(f"**📝 Resultados ({len(resultados)}):**")
        for verbete in resultados[:8]:
            st.write(f"• **{verbete}**")
    else:
        st.info("❌ Nenhum verbete encontrado.")

# Último verbete
if 'ultimo_verbete' in st.session_state:
    st.markdown("---")
    st.subheader("🎯 ÚLTIMO VERBETE")
    verbete, link = st.session_state.ultimo_verbete
    st.markdown(f"**{verbete}**")
    st.markdown(f"🔗 {link}")

# Rodapé
st.markdown("---")
st.caption("✨ Desenvolvido para estudo das Escrituras • 📖 Estudo Perspicaz")
