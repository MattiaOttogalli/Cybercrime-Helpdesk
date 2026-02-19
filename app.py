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
        'prevenzione': "Usa password diverse per ogni servizio e un Password Manager."
    },
    '615-aggravato': {
        'titolo': "Accesso abusivo da parte di Pubblico Ufficiale",
        'tags': ["pubblico ufficiale", "polizia", "comune", "abuso potere", "database statale"],
        'pena': "Pena aumentata (Art. 615-ter comma 2)",
        'soluzione': ["Segnala l'abuso all'ente di appartenenza del soggetto"],
        'denuncia': "Art. 615-ter c.p. (Aggravato). Specifica la qualifica del colpevole nella querela.",
        'prevenzione': "Monitoraggio degli accessi (audit log) nei sistemi della PA."
    },
    '635-bis': {
        'titolo': "Danneggiamento di dati, informazioni o programmi",
        'tags': ["virus", "malware", "file cancellati", "ransomware", "criptati", "dati persi"],
        'pena': "Reclusione da 2 a 6 anni",
        'soluzione': ["Isola il dispositivo", "Tenta ripristino da backup offline", "Non pagare riscatti"],
        'denuncia': "Art. 635-bis c.p. - Il reato sussiste anche se i dati sono recuperabili.",
        'prevenzione': "Effettua backup periodici su dischi non collegati alla rete."
    },
    '635-ter': {
        'titolo': "Danneggiamento di sistemi di Pubblica Utilità",
        'tags': ["ospedale", "energia", "trasporti", "infrastruttura", "servizi pubblici"],
        'pena': "Reclusione da 3 a 8 anni",
        'soluzione': ["Attiva piani di emergenza e continuità operativa"],
        'denuncia': "Art. 635-ter c.p. - Segnalazione immediata al CNAIPIC.",
        'prevenzione': "Protezione delle infrastrutture critiche con sistemi ridondanti."
    },
    '635-quater': {
        'titolo': "Danneggiamento di sistemi informatici o telematici",
        'tags': ["rete bloccata", "server down", "dos", "ddos", "rallentamento"],
        'pena': "Reclusione da 2 a 6 anni",
        'soluzione': ["Analisi del traffico per filtrare attacchi DDoS", "Potenziamento firewall"],
        'denuncia': "Art. 635-quater c.p. - Raccogli prove dell'interruzione del servizio.",
        'prevenzione': "Sistemi di filtraggio del traffico e bilanciamento del carico."
    },
    '640': {
        'titolo': "Truffa online",
        'tags': ["finto annuncio", "truffa", "inganno", "venditore falso", "raggiro"],
        'pena': "Reclusione da 6 mesi a 3 anni + multa",
        'soluzione': ["Blocca ogni comunicazione col truffatore", "Segnala il sito/profilo"],
        'denuncia': "Art. 640 c.p. - Conserva chat, ricevute e URL del sito truffaldino.",
        'prevenzione': "Verifica recensioni e usa metodi di pagamento protetti."
    },
    '640-ter': {
        'titolo': "Frode informatica",
        'tags': ["soldi rubati", "conto svuotato", "banca", "bonifico falso", "phishing"],
        'pena': "Reclusione da 2 a 6 anni + multa",
        'soluzione': ["Blocca conti e carte immediatamente", "Disconosci le operazioni"],
        'denuncia': "Art. 640-ter c.p. - Fondamentale per tentare il rimborso bancario.",
        'prevenzione': "Non cliccare mai su link in SMS o email che chiedono dati bancari."
    },
    '648-bis': {
        'titolo': "Riciclaggio di beni informatici",
        'tags': ["pulizia soldi", "denaro sporco", "prestanome", "crypto sospette"],
        'pena': "Reclusione da 4 a 12 anni",
        'soluzione': ["Segnala transazioni sospette al responsabile antiriciclaggio"],
        'denuncia': "Art. 648-bis c.p. - Reato perseguibile d'ufficio.",
        'prevenzione': "Procedure KYC (Know Your Customer) stringenti."
    },
    '491-bis': {
        'titolo': "Falsità in un documento informatico",
        'tags': ["firma rubata", "documento falso", "pec falsa", "alterazione atto"],
        'pena': "Equiparata al falso in atto pubblico",
        'soluzione': ["Revoca certificati di firma digitale", "Segnala al provider"],
        'denuncia': "Art. 491-bis c.p. - Il documento digitale ha valore legale pari al cartaceo.",
        'prevenzione': "Proteggi i token di firma con PIN sicuri."
    },
    'AI-insidioso': {
        'titolo': "Reato commesso tramite IA (AI Act)",
        'tags': ["deepfake", "ia", "intelligenza artificiale", "bot", "malware ai"],
        'pena': "Aggravante Art. 61 n. 11-undecies",
        'soluzione': ["Analisi forense per provare la generazione sintetica del file"],
        'denuncia': "Aggravante specifica prevista per l'uso insidioso di tecnologie IA.",
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

if search_query:
    # Cerca nei titoli o nei tags
    for codice, info in database_reati.items():
        if search_query in info['titolo'].lower() or any(tag in search_query for tag in info['tags']):
            codice_trovato = codice
            break

    if codice_trovato:
        dati = database_reati[codice_trovato]
        st.success(f"✅ Reato Identificato: **{dati['titolo']}**")
        
        # Layout a Tab per le soluzioni
        t1, t2, t3 = st.tabs(["🛠️ Azioni Immediate", "👮 Procedura Legale", "🛡️ Prevenzione"])
        
        with t1:
            st.markdown("### Protocollo di Risoluzione")
            for s in dati['soluzione']:
                st.write(f"- {s}")
        
       with t2:
            st.markdown("### Iter Legale: Cosa deve fare il soggetto")
            st.info(dati['azione_legale'])
            st.warning("⚠️ **Nota Bene:** La denuncia può essere presentata presso qualsiasi ufficio di Polizia o Carabinieri, ma la Polizia Postale è specializzata in questi reati.")
            
            if st.button("Genera Bozza per la Querela"):
                bozza = f"AL RESPONSABILE DELLA POLIZIA POSTALE\n\nIl sottoscritto espone quanto segue: in data odierna ho riscontrato anomalie riconducibili a {dati['titolo']}.\nAzioni intraprese: {dati['soluzione'][0]}.\nSi richiede l'identificazione dei responsabili e la punizione a norma di legge."
                st.code(bozza)
        
        with t3:
            st.markdown("### Come evitare che riaccada")
            st.success(dati['prevenzione'])
            
    else:
        st.error("❌ Nessun reato specifico trovato. Prova con parole diverse (es: banca, password, firma, virus).")
else:
    st.info("Digita una parola chiave nella barra sopra per analizzare il tuo caso.")

st.markdown("---")
st.caption("Nota: Questo strumento fornisce indicazioni generali. In caso di reato, si consiglia di consultare un legale o la Polizia Postale.")

