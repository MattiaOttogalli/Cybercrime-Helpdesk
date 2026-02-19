import streamlit as st

# 1. CONFIGURAZIONE DELLA PAGINA
st.set_page_config(
    page_title="Cybercrime Incident Advisor Pro",
    page_icon="🚨",
    layout="wide"
)

# Custom CSS per l'interfaccia
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stAlert { border-radius: 12px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE COMPLETO (Tutti gli articoli con focus su Azione Legale)
database_reati = {
    '615-ter': {
        'titolo': "Accesso abusivo ad un sistema informatico protetto",
        'tags': ["hacker", "password", "profilo", "account", "intrusione", "email violata", "social", "instagram", "facebook"],
        'soluzione': ["Cambia password immediatamente", "Attiva 2FA", "Disconnetti dispositivi sospetti"],
        'azione_legale': "Raccogli gli screenshot delle notifiche di accesso (email 'nuovo accesso') e gli ID delle sessioni sospette. Non cancellare i log. Presenta querela entro 90 giorni.",
        'prevenzione': "Usa password diverse per ogni servizio e un Password Manager."
    },
    '615-aggravato': {
        'titolo': "Accesso abusivo da parte di Pubblico Ufficiale",
        'tags': ["pubblico ufficiale", "polizia", "comune", "abuso potere", "database statale", "dipendente pubblico"],
        'soluzione': ["Richiedi un audit interno se l'accesso è avvenuto in ambito istituzionale."],
        'azione_legale': "Richiedi un audit interno all'ente di appartenenza del Pubblico Ufficiale. Identifica il database specifico che è stato violato indebitamente e porta le prove della tua qualifica o del danno subito.",
        'prevenzione': "Monitoraggio rigoroso degli accessi ai database sensibili tramite log inalterabili."
    },
    '635-bis': {
        'titolo': "Danneggiamento di dati, informazioni o programmi",
        'tags': ["virus", "malware", "file cancellati", "ransomware", "criptati", "dati persi", "hard disk"],
        'soluzione': ["Isola il dispositivo", "Tenta ripristino da backup offline", "Non pagare riscatti"],
        'azione_legale': "Non formattare il dispositivo. Salva i file danneggiati su un supporto esterno come prova. Se possibile, ottieni una perizia informatica che attesti l'alterazione dei dati.",
        'prevenzione': "Effettua backup periodici su dischi non collegati alla rete."
    },
    '635-ter': {
        'titolo': "Danneggiamento di sistemi di Pubblica Utilità",
        'tags': ["ospedale", "energia", "trasporti", "infrastruttura", "servizi pubblici", "luce", "acqua"],
        'soluzione': ["Attivazione immediata del piano di Business Continuity."],
        'azione_legale': "Segnala immediatamente l'incidente al CNAIPIC (Polizia Postale). Documenta l'interruzione del servizio pubblico e coordina la denuncia con i responsabili della sicurezza dell'ente.",
        'prevenzione': "Segregazione delle reti industriali (OT) da quelle amministrative (IT)."
    },
    '635-quater': {
        'titolo': "Danneggiamento di sistemi informatici o telematici",
        'tags': ["rete bloccata", "server down", "dos", "ddos", "rallentamento", "connessione"],
        'soluzione': ["Analisi del traffico per filtrare attacchi DDoS", "Potenziamento firewall"],
        'azione_legale': "Documenta il periodo di inattività (downtime) tramite log del server. Raccogli prove degli indirizzi IP sorgente dell'attacco (file log del firewall) per la denuncia.",
        'prevenzione': "Uso di sistemi anti-DDoS e bilanciamento del carico."
    },
    '640': {
        'titolo': "Truffa Online",
        'tags': ["finto annuncio", "truffa", "inganno", "venditore falso", "raggiro", "subito", "vinted"],
        'soluzione': ["Interrompi ogni contatto", "Segnala il sito/profilo"],
        'azione_legale': "Salva tutte le conversazioni (WhatsApp, email), l'annuncio di vendita e la prova del pagamento effettuato. Non cancellare il profilo del venditore anche se scompare.",
        'prevenzione': "Verifica recensioni e usa solo metodi di pagamento protetti (es. PayPal Beni e Servizi)."
    },
    '640-bis': {
        'titolo': "Truffa aggravata per erogazioni pubbliche",
        'tags': ["bonus", "finanziamento", "stato", "inps", "agevolazioni", "indebito"],
        'soluzione': ["Rettifica immediata presso l'ente erogatore."],
        'azione_legale': "Prepara tutta la documentazione inviata per ottenere il bonus. Se l'errore è involontario, procedi con un ravvedimento operoso prima che inizi l'azione penale ufficiale.",
        'prevenzione': "Verifica scrupolosa dei requisiti prima di inoltrare istanze telematiche."
    },
    '640-ter': {
        'titolo': "Frode informatica (Bancaria)",
        'tags': ["soldi rubati", "conto svuotato", "banca", "bonifico falso", "phishing", "smishing"],
        'soluzione': ["Blocca conti e carte", "Disconosci le operazioni"],
        'azione_legale': "Stampa l'estratto conto evidenziando le transazioni illecite. Recati in banca per il disconoscimento formale e allega copia della denuncia per richiedere il rimborso.",
        'prevenzione': "Non cliccare mai su link in SMS o email bancarie sospette."
    },
    '648-bis': {
        'titolo': "Riciclaggio e Autoriciclaggio",
        'tags': ["pulizia soldi", "denaro sporco", "prestanome", "crypto sospette", "money mule"],
        'soluzione': ["Blocco dei flussi sospetti e segnalazione interna."],
        'azione_legale': "Identifica l'origine dei fondi. Se sei stato coinvolto come 'Money Mule', collabora immediatamente con le autorità per dimostrare la tua buona fede o il raggiro subito.",
        'prevenzione': "Procedure KYC (Know Your Customer) e tracciamento rigoroso dei pagamenti."
    },
    '491-bis': {
        'titolo': "Falsità in un documento informatico",
        'tags': ["firma rubata", "documento falso", "pec falsa", "alterazione atto", "firma digitale"],
        'soluzione': ["Revoca certificati di firma digitale", "Segnala al provider"],
        'azione_legale': "Revoca immediatamente il certificato di firma. Richiedi al gestore (Aruba/InfoCert) i log di utilizzo della firma per dimostrare l'uso abusivo in date/ore specifiche.",
        'prevenzione': "Proteggi i token di firma con PIN complessi e non lasciarli inseriti nel PC."
    },
    'AI-insidioso': {
        'titolo': "Reato commesso tramite IA (AI Act)",
        'tags': ["deepfake", "ia", "intelligenza artificiale", "bot", "audio falso", "video manipolato"],
        'soluzione': ["Uso di software di rilevamento Synthetic Media."],
        'azione_legale': "Documenta la natura 'sintetica' della prova (Deepfake). Indica nella denuncia che il reato è stato facilitato da strumenti di IA per l'applicazione delle aggravanti previste.",
        'prevenzione': "Diffida di richieste insolite via audio/video, verifica sempre attraverso un secondo canale sicuro."
    }
}

# --- SIDEBAR: HEALTH CHECK ---
with st.sidebar:
    st.title("📊 Security Health Check")
    st.markdown("Verifica le azioni compiute per mettere in sicurezza la situazione:")
    c1 = st.checkbox("Password cambiate")
    c2 = st.checkbox("2FA attivata")
    c3 = st.checkbox("Dispositivi isolati")
    c4 = st.checkbox("Prove salvate (screenshot/log)")
    
    score = sum([c1, c2, c3, c4])
    st.markdown("---")
    st.subheader("Stato della Sicurezza:")
    if score == 0:
        st.error("🔴 PERICOLO CRITICO")
        st.progress(5)
    elif score <= 2:
        st.warning("🟡 RISCHIO ELEVATO")
        st.progress(50)
    elif score == 3:
        st.info("🔵 QUASI AL SICURO")
        st.progress(75)
    else:
        st.success("🟢 SICUREZZA RIPRISTINATA")
        st.progress(100)
    
    if st.button("🔄 Reset Totale"):
        st.rerun()

# --- MAIN PAGE ---
st.title("🚨 Cybercrime Incident Advisor Pro")
st.markdown("Strumento di supporto per l'identificazione dei reati informatici e la gestione dell'emergenza.")

# BARRA DI RICERCA
st.subheader("🔍 Descrivi il problema o usa parole chiave")
query = st.text_input("Esempio: 'hacker su instagram', 'mi hanno svuotato il conto', 'file criptati', 'ransomware'").lower()

codice_identificato = None

if query:
    # Algoritmo di ricerca per titoli e tag
    for cod, info in database_reati.items():
        if query in info['titolo'].lower() or any(tag in query for tag in info['tags']):
            codice_identificato = cod
            break

    if codice_identificato:
        res = database_reati[codice_identificato]
        st.success(f"### Reato Identificato: {res['titolo']}")
        
        # Creazione Tab (Tab 2 ora include l'azione legale pratica)
        tab1, tab2, tab3 = st.tabs(["🛠️ Azioni Immediate", "👮 Procedura di Denuncia", "🛡️ Prevenzione"])
        
        with tab1:
            st.markdown("#### Protocollo tecnico di emergenza:")
            for s in res['soluzione']:
                st.write(f"- {s}")
        
        with tab2:
            st.markdown("#### Iter Legale (Cosa deve fare il soggetto):")
            st.info(res['azione_legale'])
            st.warning("⚠️ **Termini legali:** Hai 90 giorni di tempo dalla scoperta del fatto per sporgere querela.")
            
            if st.button("📝 Genera Bozza per la Denuncia"):
                bozza = (f"AL RESPONSABILE DELLA POLIZIA POSTALE\n\n"
                         f"Il sottoscritto espone quanto segue: in data odierna ho riscontrato anomalie riconducibili al reato di {res['titolo']}.\n"
                         f"Azioni di contenimento già effettuate: {res['soluzione'][0]}.\n"
                         f"Si richiede l'identificazione dei responsabili e si resta a disposizione per fornire le prove digitali raccolte.")
                st.code(bozza, language="text")
        
        with tab3:
            st.markdown("#### Misure di sicurezza per il futuro:")
            st.success(res['prevenzione'])
            
    else:
        st.error("❌ Nessun reato specifico identificato. Prova termini più generici (es. 'soldi', 'virus', 'hacker').")
else:
    st.info("Inizia digitando cosa è successo nella barra di ricerca sopra.")

st.markdown("---")
st.caption("Nota: Questo applicativo ha scopo puramente informativo. In caso di reato, consulta sempre un avvocato o la Polizia Postale.")
