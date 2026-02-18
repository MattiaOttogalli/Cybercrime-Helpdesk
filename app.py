import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA E STILE
st.set_page_config(
    page_title="Cybercrime Advisor",
    page_icon="⚖️",
    layout="wide"
)

# Titolo principale (assicurati che non ci sia spazio a sinistra)
st.title("⚖️ Cybercrime Advisor")
st.markdown("### Analisi giuridica avanzata dei reati informatici")
st.divider()

# CSS Personalizzato per un look moderno
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stAlert { border-radius: 12px; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE COMPLETO DEI REATI (Dal tuo Notebook)
database_reati = {
    '615-ter': {
        'titolo': "Accesso abusivo ad un sistema informatico protetto",
        'pena_base': "Fino a 3 anni",
        'gravita': 3,
        'note': "Il reato è commesso nel momento in cui si entra in un sistema informatico senza il consenso del proprietario."
    },
    '615-aggravato': {
        'titolo': "Accesso abusivo da parte di Pubblico Ufficiale",
        'pena_base': "Aumento fino a 1/3",
        'gravita': 4,
        'note': "Aggravante specifica prevista per chi riveste la qualifica di Pubblico Ufficiale o incaricato di pubblico servizio."
    },
    '635-bis': {
        'titolo': "Danneggiamento di dati, informazioni o programmi informatici",
        'pena_base': "Da 2 a 6 anni",
        'gravita': 6,
        'note': "Il reato sussiste anche se i dati sono recuperabili. Il ripristino tecnico non esclude il reato."
    },
    '635-quater': {
        'titolo': "Danneggiamento di sistemi informatici o telematici",
        'pena_base': "Da 2 a 6 anni (fino a 8)",
        'gravita': 6,
        'note': "Riguarda l'integrità del sistema hardware o della rete stessa."
    },
    '635-ter': {
        'titolo': "Danneggiamento di sistemi di Pubblica Utilità",
        'pena_base': "Da 3 a 8 anni",
        'gravita': 8,
        'note': "Fattispecie aggravata quando il sistema è di interesse pubblico o essenziale."
    },
    '640': {
        'titolo': "Truffa",
        'pena_base': "Da 0.5 a 3 anni",
        'gravita': 3,
        'note': "Art. 640 c.p. - Prevede anche multe da 51 a 1032 euro."
    },
    '640-bis': {
        'titolo': "Truffa aggravata per erogazioni pubbliche",
        'pena_base': "Da 2 a 7 anni",
        'gravita': 7,
        'note': "Specifico per l'indebito conseguimento di contributi o finanziamenti pubblici."
    },
    '640-ter': {
        'titolo': "Frode informatica",
        'pena_base': "Da 2 a 6 anni",
        'gravita': 6,
        'note': "Alterazione del funzionamento di un sistema per procurare a sé o ad altri un ingiusto profitto."
    },
    '648-bis': {
        'titolo': "Riciclaggio di beni",
        'pena_base': "Da 4 a 12 anni",
        'gravita': 12,
        'note': "Trasferimento di denaro o beni di provenienza delittuosa per ostacolarne l'identificazione."
    },
    '648-ter': {
        'titolo': "Autoriciclaggio",
        'pena_base': "Da 2 a 8 anni",
        'gravita': 8,
        'note': "Impiego di proventi delittuosi in attività economiche o finanziarie da parte dell'autore del reato presupposto."
    },
    '491-bis': {
        'titolo': "Falsità in un documento informatico",
        'pena_base': "Equiparata al cartaceo",
        'gravita': 4,
        'note': "Il documento informatico ha lo stesso valore probatorio dell'atto pubblico o della scrittura privata."
    },
    'AI-insidioso': {
        'titolo': "Crimine commesso con IA (AI Act 2025)",
        'pena_base': "Aggravante Art. 61",
        'gravita': 5,
        'note': "Uso di sistemi di IA come mezzo insidioso per facilitare la commissione del reato."
    }
}

# 3. STRUTTURA A CASCATA (Menu Dinamici)
struttura_menu = {
    'Accesso abusivo': {
        'Accesso standard (Art. 615-ter)': '615-ter',
        'Soggetto Pubblico Ufficiale': '615-aggravato'
    },
    'Danneggiamento': {
        'Dati e programmi (635-bis)': '635-bis',
        'Sistemi informatici (635-quater)': '635-quater',
        'Pubblica Utilità (635-ter)': '635-ter'
    },
    'Truffa e Frode': {
        'Truffa semplice (640)': '640',
        'Truffa per erogazioni pubbliche (640-bis)': '640-bis',
        'Frode informatica (640-ter)': '640-ter'
    },
    'Riciclaggio': {
        'Riciclaggio (648-bis)': '648-bis',
        'Autoriciclaggio (648-ter)': '648-ter'
    },
    'Falsità Documentale': {
        'Documento informatico (491-bis)': '491-bis'
    },
    'Intelligenza Artificiale': {
        'Utilizzo IA come mezzo (AI Act)': 'AI-insidioso'
    }
}

# 4. SIDEBAR (Ricerca e Filtri)
with st.sidebar:
    st.title("Centro Ricerca")
    query = st.text_input("🔍 Cerca parola chiave:")
    st.markdown("---")
    st.info("Strumento di supporto legale basato sugli ultimi aggiornamenti normativi 2025/2026.")

# 5. LOGICA DI SELEZIONE
st.subheader("Configurazione del Caso")
c1, c2 = st.columns(2)

with c1:
    categoria = st.selectbox("Seleziona Categoria:", ["Seleziona..."] + list(struttura_menu.keys()))

with c2:
    if categoria != "Seleziona...":
        sotto_opzioni = struttura_menu[categoria]
        label_specifica = st.selectbox("Specifica il reato:", list(sotto_opzioni.keys()))
        codice_finale = sotto_opzioni[label_specifica]
    else:
        st.selectbox("Specifica il reato:", ["Prima seleziona una categoria"], disabled=True)
        codice_finale = None

# 6. VISUALIZZAZIONE RISULTATI
if codice_finale:
    dati = database_reati[codice_finale]
    
    st.divider()
    
    # Header del Reato
    st.markdown(f"## {dati['titolo']}")
    
    # Layout a schede
    tab1, tab2, tab3 = st.tabs(["📄 Analisi Legale", "⚖️ Pene e Aggravanti", "📊 Comparazione Gravità"])
    
    with tab1:
        st.error("### Descrizione della Fattispecie")
        st.write(dati['note'])
        if query and query.lower() in dati['note'].lower():
            st.success(f"Trovata corrispondenza per la tua ricerca: '{query}'")

    with tab2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Pena Base", dati['pena_base'])
        
        st.markdown("---")
        st.markdown("#### Valutazione Aggravanti")
        agg_ia = st.checkbox("Il reato è stato facilitato da algoritmi di IA?")
        agg_pub = st.checkbox("È coinvolto un ente della Pubblica Amministrazione?")
        
        if agg_ia:
            st.warning("⚠️ **Nota AI Act:** L'uso di IA come mezzo insidioso comporta l'applicazione dell'aggravante Art. 61 c.p.")
        if agg_pub:
            st.warning("⚠️ **Danno Pubblico:** La pena può subire incrementi significativi per danno a sistemi di pubblica utilità.")

    with tab3:
        # Grafico comparativo semplice
        df_chart = pd.DataFrame({
            "Reato": [dati['titolo'], "Media Reati Cyber"],
            "Indice Gravità": [dati['gravita'], 5]
        })
        st.bar_chart(df_chart.set_index("Reato"))
        st.caption("L'indice di gravità è calcolato in base agli anni massimi di reclusione previsti.")

else:
    # Se l'utente usa la barra di ricerca ma non ha selezionato dai menu
    if query:
        st.markdown("### Risultati della ricerca:")
        for k, v in database_reati.items():
            if query.lower() in v['titolo'].lower() or query.lower() in v['note'].lower():
                st.write(f"- **{v['titolo']}** (Codice: {k})")
    else:
        st.info("Benvenuto. Seleziona una categoria o usa la barra di ricerca a sinistra per analizzare un reato.")



