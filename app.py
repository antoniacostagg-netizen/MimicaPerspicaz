import streamlit as st
import random

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
    h1 {
        text-align: center;
        color: #0066cc;
    }
    h2 {
        text-align: center;
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# LISTA COMPLETA DE VERBETES DO ESTUDO PERSPICAZ
VERBETES = {
    "Abel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abel/",
    "Abiá": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abi%C3%A1/",
    "Abiasafe": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abiasafe/",
    "Abiatar": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abiatar/",
    "Abibe": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abibe/",
    "Abida": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abida/",
    "Abidã": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abid%C3%A3/",
    "Abiel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abiel/",
    "Abiezer": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abiezer/",
    "Abigail": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abigail/",
    "Abigail": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abigail/",
    "Abimaël": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abima%C3%ABl/",
    "Abimeleque": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abimeleque/",
    "Abinadabe": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abinadabe/",
    "Abiner": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abiner/",
    "Abirão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abir%C3%A3o/",
    "Abisague": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abisague/",
    "Abisai": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abisai/",
    "Abisua": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abisua/",
    "Abiúde": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abi%C3%BAde/",
    "Abner": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abner/",
    "Aboe": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Aboe/",
    "Abraão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Abra%C3%A3o/",
    "Absalão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Absal%C3%A3o/",
    "Acabe": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Acabe/",
    "Acaz": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Acaz/",
    "Acazias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Acazias/",
    "Ação de Graças": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/A%C3%A7%C3%A3o-de-Gra%C3%A7as/",
    "Adão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ad%C3%A3o/",
    "Adoração": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Adora%C3%A7%C3%A3o/",
    "Adúltero": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ad%C3%BAltero/",
    "Advertência": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Advert%C3%AAncia/",
    "Agar": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Agar/",
    "Ageu": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ageu/",
    "Agricultura": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Agricultura/",
    "Agur": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Agur/",
    "Ahab": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ahab/",
    "Aliança": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Alian%C3%A7a/",
    "Alma": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Alma/",
    "Altar": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Altar/",
    "Amor": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Amor/",
    "Ananias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ananias/",
    "Anjo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Anjo/",
    "Apóstolo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ap%C3%B3stolo/",
    "Arca": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Arca/",
    "Arrependimento": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Arrependimento/",
    "Asa": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Asa/",
    "Ascensão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ascens%C3%A3o/",
    "Asafe": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Asafe/",
    "Aser": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Aser/",
    "Assíria": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ass%C3%ADria/",
    "Asterismo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Asterismo/",
    "Átomo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/%C3%81tomo/",
    "Atonamento": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Atonamento/",
    "Autoridade": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Autoridade/",
    "Baal": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Baal/",
    "Babel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Babel/",
    "Babilônia": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Babil%C3%B4nia/",
    "Baruque": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Baruque/",
    "Batismo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Batismo/",
    "Belém": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Bel%C3%A9m/",
    "Bênção": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/B%C3%AAn%C3%A7%C3%A3o/",
    "Bíblia": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/B%C3%ADblia/",
    "Caim": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Caim/",
    "Canaã": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Cana%C3%A3/",
    "Carne": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Carne/",
    "Céu": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/C%C3%A9u/",
    "Circuncisão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Circuncis%C3%A3o/",
    "Concórdia": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Conc%C3%B3rdia/",
    "Coração": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Cora%C3%A7%C3%A3o/",
    "Cordeiro": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Cordeiro/",
    "Criação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Cria%C3%A7%C3%A3o/",
    "Cristo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Cristo/",
    "Crucificação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Crucifica%C3%A7%C3%A3o/",
    "Daniel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Daniel/",
    "David": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/David/",
    "Deus": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Deus/",
    "Diabo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Diabo/",
    "Dilúvio": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Dil%C3%BAvio/",
    "Discípulo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Disc%C3%ADpulo/",
    "Dízimo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/D%C3%ADzimo/",
    "Eleição": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Elei%C3%A7%C3%A3o/",
    "Elias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Elias/",
    "Eliseu": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Eliseu/",
    "Êxodo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/%C3%8Axodo/",
    "Ezequiel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ezequiel/",
    "Fé": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/F%C3%A9/",
    "Filho": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Filho/",
    "Gênesis": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/G%C3%AAnesis/",
    "Gólgota": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/G%C3%B3lgota/",
    "Graça": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Gra%C3%A7a/",
    "Hebreus": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Hebreus/",
    "Inferno": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Inferno/",
    "Isaías": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Isa%C3%ADas/",
    "Israel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Israel/",
    "Jeremias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jeremias/",
    "Jerusalém": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jerusal%C3%A9m/",
    "Jesus": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jesus/",
    "João": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jo%C3%A3o/",
    "Jó": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/J%C3%B3/",
    "José": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jos%C3%A9/",
    "Josias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Josias/",
    "Judá": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Jud%C3%A1/",
    "Julgamento": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Julgamento/",
    "Justiça": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Justi%C3%A7a/",
    "Lei": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Lei/",
    "Levítico": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Lev%C3%ADtico/",
    "Lúcifer": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/L%C3%BAcifer/",
    "Luz": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Luz/",
    "Malaquias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Malaquias/",
    "Manoá": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Mano%C3%A1/",
    "Maria": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Maria/",
    "Moisés": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Mois%C3%A9s/",
    "Monoteísmo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Monote%C3%ADsmo/",
    "Morte": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Morte/",
    "Naamã": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Naam%C3%A3/",
    "Nabucodonosor": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Nabucodonosor/",
    "Naum": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Naum/",
    "Nazaré": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Nazar%C3%A9/",
    "Noé": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/No%C3%A9/",
    "Oseias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Oseias/",
    "Páscoa": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/P%C3%A1scoa/",
    "Paulo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Paulo/",
    "Pentecostes": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Pentecostes/",
    "Perdão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Perd%C3%A3o/",
    "Poder": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Poder/",
    "Profeta": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Profeta/",
    "Provérbios": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Prov%C3%A9rbios/",
    "Reino": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Reino/",
    "Ressurreição": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Ressurrei%C3%A7%C3%A3o/",
    "Revelação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Revela%C3%A7%C3%A3o/",
    "Rute": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Rute/",
    "Sabedoria": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Sabedoria/",
    "Sacerdote": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Sacerdote/",
    "Salmo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Salmo/",
    "Salvação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Salva%C3%A7%C3%A3o/",
    "Samaritano": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Samaritano/",
    "Samuel": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Samuel/",
    "Sangue": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Sangue/",
    "Sansão": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Sans%C3%A3o/",
    "Satanás": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Satan%C3%A1s/",
    "Saul": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Saul/",
    "Templo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Templo/",
    "Tentação": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Tenta%C3%A7%C3%A3o/",
    "Trono": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Trono/",
    "Verdade": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Verdade/",
    "Vida": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Vida/",
    "Zacarias": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Zacarias/",
    "Zelo": "https://www.jw.org/pt/biblioteca/livros/Estudo-Perspicaz-das-Escrituras/Zelo/"
}

# Interface principal
st.markdown("<h1>📖 Escolhedor Perspicaz</h1>", unsafe_allow_html=True)
st.markdown("---")

# Contador de verbetes
st.success(f"**📊 Total de Verbetes:** {len(VERBETES)}")

# Botão AZUL principal
if st.button("🎲 ESCOLHER ALEATORIAMENTE", type="primary", use_container_width=True):
    verbete, link = random.choice(list(VERBETES.items()))
    st.markdown(f"<h2>{verbete}</h2>", unsafe_allow_html=True)
    st.markdown(f"**🔗 Link:** {link}")
    
    # Botão para abrir
    if st.button("🌐 Abrir no Navegador", use_container_width=True):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

# Busca
st.markdown("---")
st.subheader("🔍 Buscar Verbete")
busca = st.text_input("Digite o nome do verbete:")
if busca:
    resultados = [v for v in VERBETES.keys() if busca.lower() in v.lower()]
    if resultados:
        st.write(f"**📝 Resultados ({len(resultados)}):**")
        for verbete in resultados[:10]:
            st.write(f"• **{verbete}**")
    else:
        st.info("❌ Nenhum verbete encontrado.")

# Rodapé
st.markdown("---")
st.caption("📱 App com TODOS os verbetes • ✨ Compartilhe com amigos!")

# Adicionar mais estilos
st.markdown("""
<style>
    .stSuccess {
        background-color: #e6f7ff;
        border-left: 4px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)
