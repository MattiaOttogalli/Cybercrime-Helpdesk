import streamlit as st

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Cybercrime Incident Advisor Pro",
    page_icon="🚨",
    layout="wide"
)

# CSS per forzare l'aggiornamento visivo e migliorare il design
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f2f6; 
        border-radius: 5px 5px 0px 0px; 
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff !important; color: white !important; }

    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: #6c757d !important;
    }
    
    </style>
    """, unsafe_allow_html=True)


# 2. DATABASE COMPLETO (Tutti i reati con Pene e Azioni Legali)
database_reati = {
    '615-ter': {
        'titolo': "Accesso abusivo ad un sistema informatico protetto",
        'tags': ["hacker", "password", "profilo", "account", "intrusione", "email", "social"],
        'soluzione': ["Cambia password immediatamente", "Attiva 2FA", "Disconnetti dispositivi sospetti"],
        'azione_legale': "Raccogli gli screenshot delle notifiche di accesso e gli ID delle sessioni sospette. Presenta querela entro 90 giorni.",
        'pena': "Reclusione fino a 3 anni. Se il sistema è di interesse pubblico, da 1 a 5 anni.",
        'prevenzione': "Usa password complesse e un Password Manager."
    },
    '615-aggravato': {
        'titolo': "Accesso abusivo da parte di Pubblico Ufficiale",
        'tags': ["pubblico ufficiale", "polizia", "comune", "abuso potere"],
        'soluzione': ["Richiedi un audit interno se l'accesso è avvenuto in ambito istituzionale."],
        'azione_legale': "Richiedi un audit interno formale all'ente di appartenenza. Allega alla querela le prove del danno o della violazione della privacy.",
        'pena': "Reclusione da 1 a 5 anni (Aggravante specifica per la qualifica del soggetto).",
        'prevenzione': "Monitoraggio rigoroso dei log di accesso nei sistemi della PA."
    },
    '635-bis': {
        'titolo': "Danneggiamento di dati, informazioni o programmi",
        'tags': ["virus", "malware", "file cancellati", "ransomware", "criptati"],
        'soluzione': ["Isola il dispositivo", "Tenta ripristino da backup offline", "Non pagare riscatti"],
        'azione_legale': "Salva i file danneggiati su supporto esterno. Ottieni una perizia informatica che attesti l'alterazione dei dati.",
        'pena': "Reclusione da 2 a 6 anni.",
        'prevenzione': "Effettua backup periodici su dischi non collegati alla rete."
    },
    '635-ter': {
        'titolo': "Danneggiamento di sistemi di Pubblica Utilità",
        'tags': ["ospedale", "energia", "trasporti", "infrastruttura", "luce", "acqua"],
        'soluzione': ["Attivazione immediata del piano di Business Continuity."],
        'azione_legale': "Segnala l'incidente al CNAIPIC. Documenta l'interruzione del servizio e coordina la denuncia con l'ufficio legale.",
        'pena': "Reclusione da 3 a 8 anni.",
        'prevenzione': "Segregazione delle reti industriali (OT) da quelle IT."
    },
    '635-quater': {
        'titolo': "Danneggiamento di sistemi informatici o telematici",
        'tags': ["rete bloccata", "server down", "dos", "ddos", "rallentamento"],
        'soluzione': ["Analisi del traffico per filtrare attacchi DDoS", "Potenziamento firewall"],
        'azione_legale': "Documenta il downtime tramite log del server. Raccogli prove degli indirizzi IP sorgente dell'attacco.",
        'pena': "Reclusione da 2 a 6 anni.",
        'prevenzione': "Uso di sistemi anti-DDoS e bilanciamento del carico."
    },
    '640': {
        'titolo': "Truffa Online (Generica)",
        'tags': ["finto annuncio", "truffa", "inganno", "venditore falso", "raggiro"],
        'soluzione': ["Interrompi ogni contatto", "Segnala il profilo alla piattaforma"],
        'azione_legale': "Salva chat, annuncio e prova del pagamento. Non cancellare il profilo del venditore anche se scompare.",
        'pena': "Reclusione da 6 mesi a 3 anni e multa da 51€ a 1.032€.",
        'prevenzione': "Verifica recensioni e usa solo metodi di pagamento protetti."
    },
    '640-bis': {
        'titolo': "Truffa aggravata per erogazioni pubbliche",
        'tags': ["bonus", "finanziamento", "stato", "inps", "agevolazioni"],
        'soluzione': ["Rettifica immediata presso l'ente erogatore."],
        'azione_legale': "Prepara tutta la documentazione inviata. Se l'errore è involontario, procedi con un ravvedimento operoso.",
        'pena': "Reclusione da 2 a 7 anni.",
        'prevenzione': "Verifica dei requisiti prima di inoltrare istanze telematiche."
    },
    '640-ter': {
        'titolo': "Frode informatica (Bancaria)",
        'tags': ["soldi rubati", "conto svuotato", "banca", "phishing", "smishing"],
        'soluzione': ["Blocca conti e carte", "Disconosci le operazioni presso la banca"],
        'azione_legale': "Stampa l'estratto conto. Recati in banca per il disconoscimento formale e allega copia della denuncia.",
        'pena': "Reclusione da 2 a 6 anni e multa da 600€ a 3.000€.",
        'prevenzione': "Non cliccare mai su link in SMS o email bancarie sospette."
    },
    '648-bis': {
        'titolo': "Riciclaggio di beni informatici",
        'tags': ["pulizia soldi", "denaro sporco", "prestanome", "money mule"],
        'soluzione': ["Blocco dei flussi sospetti e segnalazione al responsabile."],
        'azione_legale': "Identifica l'origine dei fondi. Se coinvolto come 'Money Mule', collabora con le autorità per dimostrare il raggiro.",
        'pena': "Reclusione da 4 a 12 anni e multa da 5.000€ a 25.000€.",
        'prevenzione': "Verifica dell'identità delle controparti nelle transazioni."
    },
    '648-ter': {
        'titolo': "Autoriciclaggio",
        'tags': ["reinvestimento", "denaro illecito", "azienda", "crypto"],
        'soluzione': ["Analisi dei flussi finanziari interni."],
        'azione_legale': "Identifica i flussi di denaro reinvestiti. Dimostra che l'uso dei beni non ha ostacolato l'identificazione della provenienza.",
        'pena': "Reclusione da 2 a 8 anni e multa da 5.000€ a 25.000€.",
        'prevenzione': "Sistemi di tracciamento finanziario trasparenti."
    },
    '491-bis': {
        'titolo': "Falsità in un documento informatico",
        'tags': ["firma rubata", "documento falso", "pec falsa", "firma digitale"],
        'soluzione': ["Revoca certificati di firma digitale", "Segnala al provider"],
        'azione_legale': "Revoca il certificato. Richiedi ai gestori i log di utilizzo della firma per dimostrare l'uso abusivo.",
        'pena': "Pene equiparate a quelle per i falsi in atti cartacei (Art. 476 ss. c.p.).",
        'prevenzione': "Proteggi i token di firma con PIN complessi."
    },
    'AI-insidioso': {
        'titolo': "Reato commesso tramite IA (AI Act 2026)",
        'tags': ["deepfake", "ia", "intelligenza artificiale", "audio falso", "video manipolato"],
        'soluzione': ["Uso di software di rilevamento Synthetic Media."],
        'azione_legale': "Documenta la natura 'sintetica' del file. Indica l'uso di IA per l'applicazione delle aggravanti (Art. 61 n. 11-undecies).",
        'pena': "Aggravante specifica che aumenta la pena del reato base.",
        'prevenzione': "Verifica le richieste insolite attraverso un secondo canale sicuro."
    }
}

# --- SIDEBAR: HEALTH CHECK ---
with st.sidebar:
    st.title("📊 Security Health Check")
    c1 = st.checkbox("Password cambiate")
    c2 = st.checkbox("2FA attivata")
    c3 = st.checkbox("Dispositivi isolati")
    c4 = st.checkbox("Prove salvate (log/screenshot)")
    
    score = sum([c1, c2, c3, c4])
    st.markdown("---")
    st.subheader("Stato della Sicurezza:")
    if score == 0: st.error("🔴 CRITICO"); st.progress(5)
    elif score <= 2: st.warning("🟡 ELEVATO"); st.progress(50)
    elif score == 3: st.info("🔵 QUASI AL SICURO"); st.progress(75)
    else: st.success("🟢 RIPRISTINATA"); st.progress(100)
    
    if st.button("🔄 Reset Totale"): st.rerun()

# --- MAIN PAGE ---
st.title("🚨 Cybercrime Incident Advisor")
st.markdown("Identifica il reato e scopri la procedura completa per la gestione dell'incidente.")

# BARRA DI RICERCA
query = st.text_input("Descrivi il problema (es: 'hacker', 'soldi rubati', 'ransomware'):").lower()

if query:
    codice_id = None
    for cod, info in database_reati.items():
        if query in info['titolo'].lower() or any(tag in query for tag in info['tags']):
            codice_id = cod
            break

    if codice_id:
        res = database_reati[codice_id]
        st.success(f"### Reato Riconosciuto: {res['titolo']}")
        
        # DEFINIZIONE DELLE 4 TAB
        tab1, tab2, tab3, tab4 = st.tabs([
            "🛠️ Azioni Immediate", 
            "👮 Procedura di Denuncia", 
            "⚖️ Pene Previste", 
            "🛡️ Prevenzione"
        ])
        
        with tab1:
            st.subheader("🛠️ Cosa fare nei primi 5 minuti")
            for s in res['soluzione']:
                st.write(f"- {s}")
        
        with tab2:
            st.subheader("👮 Iter Legale (Cosa deve fare il soggetto)")
            st.info(res['azione_legale'])
            st.warning("⚠️ Hai 90 giorni di tempo dalla scoperta del fatto per sporgere querela.")
            
            if st.button("📝 Genera Bozza Denuncia"):
                bozza = f"AL RESPONSABILE DELLA POLIZIA POSTALE\n\nIl sottoscritto espone quanto segue: ho riscontrato anomalie riconducibili al reato di {res['titolo']}.\nAzioni effettuate: {res['soluzione'][0]}.\nResto a disposizione per fornire le prove digitali raccolte."
                st.code(bozza, language="text")
        
        with tab3:
            st.subheader("⚖️ Quadro Sanzionatorio")
            # Titolo grande per la pena
            st.markdown(f"<h2 style='color: #E74C3C; font-size: 35px;'>Pena Prevista</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 28px; font-weight: bold;'>{res['pena']}</p>", unsafe_allow_html=True)
        
        with tab4:
            st.subheader("🛡️ Misure di Prevenzione")
            st.success(res['prevenzione'])
            
    else:
        st.error("❌ Nessuna corrispondenza trovata. Prova parole diverse.")
else:
    st.info("Digita una parola chiave nella barra di ricerca sopra per iniziare.")

st.markdown("---")
st.caption("Nota: Questo strumento ha scopo informativo. In caso di reato, consulta sempre un legale o la Polizia Postale.")

