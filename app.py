# Substitua o CSS atual por este:
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
    
    /* ESTILO PARA O NOME DO VERBETE (GRANDE E EM DESTAQUE) */
    .nome-verbete {
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
    
    h1 {
        text-align: center;
        color: #0066cc;
        font-size: 32px;
    }
    
    .stSuccess {
        background-color: #e6f7ff;
        border-left: 4px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)
