import streamlit as st
import pandas as pd

# Configurazione estetica della pagina
st.set_page_config(
    page_title="Cybercrime Advisor Pro",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS per migliorare l'aspetto
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: RICERCA E INFO ---
with st.sidebar:
    st.title("🔍 Strumenti")
    search_query = st.text_input("Cerca parola chiave (es. 'multa', 'IA'):")
    st.info("Questo applicativo fornisce un'analisi preliminare basata sul Codice Penale Italiano e l'AI Act 2026.")
    
    if st.button("Svuota Selezione"):
        st.cache_data.clear()
        st.rerun()

# --- HEADER ---
st.title("⚖️ Cybercrime Advisor Pro")
st.markdown("Analisi giuridica avanzata dei reati informatici.")

# --- DATI ANALISI (Tratti dal notebook originale) ---
# Ho strutturato i dati in un dizionario per una gestione più complessa
database_reati = {
    '615-ter': {
        'titolo': "Accesso abusivo ad un sistema informatico protetto",
        'pena_base': "Fino a 3 anni",
        'note': "Il reato è commesso nel momento in cui si entra nel sistema senza consenso.",
        'categoria': "Accesso"
    },
    '635-bis': {
        'titolo': "Danneggiamento di dati e programmi",
        'pena_base': "Da 2 a 6 anni",
        'note': "Sussiste anche se i dati sono recuperabili.",
        'categoria': "Danneggiamento"
    },
    '640-ter': {
        'titolo': "Frode informatica",
        'pena_base': "Da 2 a 6 anni (aggravata)",
        'note': "Include la manipolazione del sistema per profitto.",
        'categoria': "Truffa"
    },
    'AI-insidioso': {
        'titolo': "Crimine commesso con IA (AI Act 2026)",
        'pena_base': "Aggravante specifica",
        'note': "Utilizzo di IA come mezzo insidioso (Art. 61 n. 11-undecies).",
        'categoria': "IA"
    }
}

# --- SEZIONE INPUT ---
col1, col2 = st.columns(2)

with col1:
    categoria = st.selectbox(
        "Seleziona la Categoria:",
        options=['Selezione', 'Accesso abusivo', 'Danneggiamento', 'Truffa', 'Riciclaggio', 'IA']
    )

with col2:
    # Aggravanti dinamiche
    st.markdown("**Aggravanti applicabili:**")
    agg_pu = st.checkbox("Soggetto è Pubblico Ufficiale")
    agg_ia = st.checkbox("Utilizzo di Intelligenza Artificiale")

# --- LOGICA DI VISUALIZZAZIONE ---
# Mapping categorie per filtrare i dati del notebook
mapping = {
    'Accesso abusivo': '615-ter',
    'Danneggiamento': '635-bis',
    'Truffa': '640-ter',
    'IA': 'AI-insidioso'
}

codice_scelto = mapping.get(categoria)

if codice_scelto:
    dati = database_reati[codice_scelto]
    
    st.divider()
    
    # Layout a schede per i dettagli
    tab1, tab2, tab3 = st.tabs(["📄 Analisi", "⚖️ Pene e Aggravanti", "📊 Statistiche"])
    
    with tab1:
        st.subheader(f"Fattispecie: {dati['titolo']}")
        st.write(dati['note'])
        
    with tab2:
        pena_finale = dati['pena_base']
        if agg_pu:
            st.error("⚠️ **Aggravante Pubblico Ufficiale:** La pena può essere aumentata fino a un terzo.")
        if agg_ia:
            st.warning("🤖 **Aggravante AI Act:** Applicazione Art. 61 n. 11-undecies.")
        
        st.metric(label="Pena Base Stimata", value=pena_finale)

    with tab3:
        # Mini tabella comparativa
        df_comp = pd.DataFrame({
            "Reato": [dati['titolo']],
            "Pena Max": [6 if "6" in dati['pena_base'] else 3]
        })
        st.bar_chart(df_comp.set_index("Reato"))

else:
    st.info("Seleziona una categoria per iniziare l'analisi.")

# --- FOOTER ---
st.markdown("---")
if st.button("📩 Genera Report PDF (Simulazione)"):
    st.success("Report generato con successo! (Funzionalità scaricabile implementando fpdf)")
