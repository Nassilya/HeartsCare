import streamlit as st
import ollama

# Parie 1
#Configuration de la page et du style
st.set_page_config(page_title="Hearts & Care AI", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    h1 { color: #D53F8C !important; font-family: 'Helvetica Neue', sans-serif; }
    .subtitle { color: #4A5568; font-size: 1.2rem; font-weight: 500; margin-bottom: 2rem; }
    
    /* Rend le texte des messages ultra lisible et bien espacé */
    .stChatMessage p, .stChatMessage li { 
        color: #1A202C !important; 
        font-weight: 500 !important;
        line-height: 1.6 !important; /* Donne de l'espace entre les lignes */
        margin-bottom: 10px !important; /* Espace entre les paragraphes */
    }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.8) !important; border: 1px solid #FED7D7; }
    </style>
""", unsafe_allow_html=True)

st.title("💖 Hearts & Care")
st.markdown('<p class="subtitle">Your AI confidante for hormonal health & wellness (Powered by Llama 3)</p>', unsafe_allow_html=True)

# Parie 2
# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am Hearts & Care, your advanced health companion. How can I help you today?"}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Parie 3
# Zone de saisie utilisateur
if user_query := st.chat_input("Ask me anything about your cycle or symptoms..."):
    # Affichage du message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # Parie 4
    # Génération de la réponse avec Llama 3 en mode Streaming Propre
    with st.chat_message("assistant"):
        try:
            system_prompt = (
                "You are Hearts & Care, a helpful, specialized medical AI assistant for women's hormonal health. "
                "Provide a direct, kind, and scientific answer. Do not confuse symptoms with causes. "
                "Use clear paragraphs and clean bullet points for readability."
            )
            
            full_prompt = f"{system_prompt}\n\nQuestion: {user_query}\n\nAnswer:"
            
            stream = ollama.generate(
                model='llama3',
                prompt=full_prompt,
                stream=True
            )
            
            # 1) créeation d'un espace vide (un placeholder) pour afficher le txt
            message_placeholder = st.empty()
            full_response = ""
            
            # 2) pour accumuler les mots en direct
            for chunk in stream:
                full_response += chunk['response']
                # On ajoute un curseur visuel (┃) pendant que ça écrit pour faire plus pro
                message_placeholder.markdown(full_response + "┃")
            
            # 3) une fois DONE -> affiche la réponse finale sans le curseur (nettoie tout le Markdown d'un coup)
            message_placeholder.markdown(full_response)
            
            # Sauvegarde de la réponse dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Make sure the Ollama application is running on your Mac!")