import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Cybercrime Incident Advisor", page_icon="🚨", layout="wide")

# 2. DATABASE ESTESO
database_reati = {
    '615-ter': {
        'titolo': "Accesso abusivo ad un sistema informatico protetto",
        'tags': ["hacker", "password", "profilo", "account", "intrusione", "email violata", "social"],
        'pena': "Reclusione fino a 3 anni",
        'soluzione': ["Cambia password immediatamente", "Attiva 2FA", "Disconnetti dispositivi sospetti"],
        'denuncia': "Art. 615-ter c.p. - Porta i log di accesso o gli avvisi di login sospetti alla Polizia Postale.",
        'azione_legale': "Raccogli gli screenshot delle notifiche di accesso (email 'nuovo accesso') e gli ID delle sessioni sospette. Non cancellare i log. Presenta querela entro 90 giorni.",
        'prevenzione': "Usa password diverse per ogni servizio e un Password Manager."
    },
    '615-aggravato': {
        'titolo': "Accesso abusivo da parte di Pubblico Ufficiale",
        'tags': ["pubblico ufficiale", "polizia", "comune", "abuso potere", "database statale"],
        'pena': "Pena aumentata (Art. 615-ter comma 2)",
        'soluzione': ["Segnala l'abuso all'ente di appartenenza del soggetto"],
        'denuncia': "Art. 615-ter c.p. (Aggravato). Specifica la qualifica del colpevole nella querela.",
        'azione_legale': "Oltre alla querela, richiedi un audit interno all'ente di appartenenza del Pubblico Ufficiale. Identifica il database specifico che è stato violato indebitamente.",
        'prevenzione': "Monitoraggio degli accessi (audit log) nei sistemi della PA."
    },
    '635-bis': {
        'titolo': "Danneggiamento di dati, informazioni o programmi",
        'tags': ["virus", "malware", "file cancellati", "ransomware", "criptati", "dati persi"],
        'pena': "Reclusione da 2 a 6 anni",
        'soluzione': ["Isola il dispositivo", "Tenta ripristino da backup offline", "Non pagare riscatti"],
        'denuncia': "Art. 635-bis c.p. - Il reato sussiste anche se i dati sono recuperabili.",
        'azione_legale': "Non formattare il dispositivo. Salva i file danneggiati su un supporto esterno come prova. Se possibile, ottieni una perizia informatica che attesti l'alterazione dei dati.",
        'prevenzione': "Effettua backup periodici su dischi non collegati alla rete."
    },
    '635-ter': {
        'titolo': "Danneggiamento di sistemi di Pubblica Utilità",
        'tags': ["ospedale", "energia", "trasporti", "infrastruttura", "servizi pubblici"],
        'pena': "Reclusione da 3 a 8 anni",
        'soluzione': ["Attiva piani di emergenza e continuità operativa"],
        'denuncia': "Art. 635-ter c.p. - Segnalazione immediata al CNAIPIC.",
        'azione_legale': "Segnala immediatamente l'incidente al CNAIPIC (Polizia Postale) e coordina l'azione legale con l'ufficio legale dell'ente colpito.",
        'prevenzione': "Protezione delle infrastrutture critiche con sistemi ridondanti."
    },
    '635-quater': {
        'titolo': "Danneggiamento di sistemi informatici o telematici",
        'tags': ["rete bloccata", "server down", "dos", "ddos", "rallentamento"],
        'pena': "Reclusione da 2 a 6 anni",
        'soluzione': ["Analisi del traffico per filtrare attacchi DDoS", "Potenziamento firewall"],
        'denuncia': "Art. 635-quater c.p. - Raccogli prove dell'interruzione del servizio.",
        'azione_legale': "Documenta il periodo di inattività (downtime) tramite log del server o testimonianze. Raccogli prove degli indirizzi IP sorgente dell'attacco per la denuncia.",
        'prevenzione': "Sistemi di filtraggio del traffico e bilanciamento del carico."
    },
    '640': {
        'titolo': "Truffa online",
        'tags': ["finto annuncio", "truffa", "inganno", "venditore falso", "raggiro"],
        'pena': "Reclusione da 6 mesi a 3 anni + multa",
        'soluzione': ["Blocca ogni comunicazione col truffatore", "Segnala il sito/profilo"],
        'denuncia': "Art. 640 c.p. - Conserva chat, ricevute e URL del sito truffaldino.",
        'azione_legale': "Salva tutte le conversazioni (WhatsApp, email), l'annuncio di vendita e la prova del pagamento. Non cancellare il profilo del venditore anche se scompare.",
        'prevenzione': "Verifica recensioni e usa metodi di pagamento protetti."
    },
    '640-bis': {
        'titolo': "Truffa aggravata per erogazioni pubbliche",
        'tags': ["bonus", "finanziamento", "stato", "inps", "agevolazioni", "indebito"],
        'soluzione': ["Rettifica immediata presso l'ente erogatore."],
        'azione_legale': "Prepara tutta la documentazione inviata per ottenere il bonus. Se l'errore è involontario, procedi con un ravvedimento operoso prima dell'azione penale.",
        'prevenzione': "Verifica scrupolosa dei requisiti prima di inoltrare istanze telematiche."
    },
    '640-ter': {
        'titolo': "Frode informatica",
        'tags': ["soldi rubati", "conto svuotato", "banca", "bonifico falso", "phishing"],
        'pena': "Reclusione da 2 a 6 anni + multa",
        'soluzione': ["Blocca conti e carte immediatamente", "Disconosci le operazioni"],
        'denuncia': "Art. 640-ter c.p. - Fondamentale per tentare il rimborso bancario.",
        'azione_legale': "Stampa l'estratto conto evidenziando le transazioni illecite. Recati in banca per il disconoscimento formale e allega copia della denuncia per il rimborso.",
        'prevenzione': "Non cliccare mai su link in SMS o email che chiedono dati bancari."
    },
    '648-bis': {
        'titolo': "Riciclaggio di beni informatici",
        'tags': ["pulizia soldi", "denaro sporco", "prestanome", "crypto sospette"],
        'pena': "Reclusione da 4 a 12 anni",
        'soluzione': ["Segnala transazioni sospette al responsabile antiriciclaggio"],
        'denuncia': "Art. 648-bis c.p. - Reato perseguibile d'ufficio.",
        'azione_legale': "Identifica l'origine dei fondi. Se sei stato usato come 'prestanome' a tua insaputa, collabora immediatamente con le autorità per dimostrare il raggiro subito.",
        'prevenzione': "Procedure KYC (Know Your Customer) stringenti."
    },
    '491-bis': {
        'titolo': "Falsità in un documento informatico",
        'tags': ["firma rubata", "documento falso", "pec falsa", "alterazione atto"],
        'pena': "Equiparata al falso in atto pubblico",
        'soluzione': ["Revoca certificati di firma digitale", "Segnala al provider"],
        'denuncia': "Art. 491-bis c.p. - Il documento digitale ha valore legale pari al cartaceo.",
        'azione_legale': "Revoca immediatamente il certificato di firma. Richiedi al gestore (Aruba/InfoCert) i log di utilizzo della firma per dimostrare l'uso abusivo.",
        'prevenzione': "Proteggi i token di firma con PIN sicuri."
    },
    'AI-insidioso': {
        'titolo': "Reato commesso tramite IA (AI Act)",
        'tags': ["deepfake", "ia", "intelligenza artificiale", "bot", "malware ai"],
        'pena': "Aggravante Art. 61 n. 11-undecies",
        'soluzione': ["Analisi forense per provare la generazione sintetica del file"],
        'denuncia': "Aggravante specifica prevista per l'uso insidioso di tecnologie IA.",
        'azione_legale': "Documenta la natura 'sintetica' della prova (Deepfake). Indica nella denuncia che il reato è stato facilitato da strumenti di Intelligenza Artificiale.",
        'prevenzione': "Formazione su come riconoscere contenuti manipolati da IA."
    }
}

# --- SIDEBAR: CALCOLATORE DELLA GRAVITÀ ---
with st.sidebar:
    st.title("📊 Security Health Check")
    st.markdown("Verifica quanto è protetta la tua situazione attuale:")
    
    c1 = st.checkbox("Ho cambiato le password")
    c2 = st.checkbox("Ho attivato la 2FA (SMS/App)")
    c3 = st.checkbox("Ho sporto denuncia")
    c4 = st.checkbox("Ho isolato i dispositivi infetti")
    
    # Calcolo punteggio
    score = sum([c1, c2, c3, c4])
    st.markdown("---")
    st.subheader("Livello di Sicurezza:")
    
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

# --- MAIN: RICERCA E RISULTATI ---
st.title("🚨 Cybercrime Incident Advisor")
st.markdown("Identifica il reato subito e ricevi istruzioni immediate su come agire.")

# Barra di ricerca intelligente
st.subheader("🔍 Cosa è successo? Descrivi il problema")
search_query = st.text_input("Esempio: 'mi hanno svuotato il conto' oppure 'hacker su instagram'").lower()

codice_trovato = None

if query:
    # Ricerca intelligente nel database
    for cod, info in database_reati.items():
        if query in info['titolo'].lower() or any(tag in query for tag in info['tags']):
            codice_identificato = cod
            break

    if codice_identificato:
        res = database_reati[codice_identificato]
        st.success(f"### Reato Riconosciuto: {res['titolo']}")
        
        tab1, tab2, tab3 = st.tabs(["🛠️ Azioni Immediate", "👮 Procedura Legale", "🛡️ Prevenzione"])
        
        with tab1:
            st.markdown("#### Cosa fare nei prossimi 5 minuti:")
            for s in res['soluzione']:
                st.write(f"- {s}")
        
        with tab2:
            st.markdown("#### Iter di Denuncia (Cosa deve fare il soggetto):")
            st.info(res['azione_legale'])
            st.warning("⚠️ Ricorda: Hai 90 giorni di tempo dalla scoperta del fatto per presentare querela.")
            
            if st.button("📝 Genera Bozza Denuncia"):
                bozza = f"AL RESPONSABILE DELLA POLIZIA POSTALE\n\nIl sottoscritto espone quanto segue: in data odierna ho riscontrato anomalie riconducibili al reato di {res['titolo']}.\nAzioni di contenimento già effettuate: {res['soluzione'][0]}.\nSi richiede l'identificazione dei responsabili e si resta a disposizione per fornire le prove digitali raccolte."
                st.code(bozza, language="text")
        
        with tab3:
            st.markdown("#### Consigli per il futuro:")
            st.success(res['prevenzione'])
            
    else:
        st.error("❌ Nessun reato specifico identificato. Prova termini come 'banca', 'hacker', 'virus' o 'soldi'.")
else:
    st.info("Digita il problema riscontrato nella barra di ricerca sopra per ricevere assistenza.")

st.markdown("---")
st.caption("Nota: Questo applicativo ha scopo informativo. In caso di reato, consulta sempre un avvocato o la Polizia Postale.")
