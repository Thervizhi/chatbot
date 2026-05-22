import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot using Custom Endpoint")
st.write(
    f"This is a simple chatbot that uses an external API to generate responses. "
    f"It is configured to use the base URL: `{CUSTOM_API_BASE_URL}`."
)

# Ask user for their API key (if your custom service requires one, otherwise this might be optional)
openai_api_key = st.text_input("API Key (if required by custom service)", type="password")

if not openai_api_key:
    st.info("Please add your API key to continue.", icon="🗝️")
else:

    # --- CHANGE HERE: Initialize the client with the base URL ---
    try:
        client = OpenAI(
            api_key=openai_api_key,
            base_url=CUSTOM_API_BASE_URL  # <-- This is the key change for custom endpoints
        )
    except Exception as e:
        st.error(f"Error initializing the client: {e}")
        client = None
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="/root/.cache/huggingface/hub/models--TrevorJS--gemma-4-E2B-it-uncensored-GGUF/snapshots/4345c0c77cde7da43084c94b1deac23c09bccfc1/gemma-4-E2B-it-uncensored-Q4_K_M.gguf",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
