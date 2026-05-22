import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot using Custom Endpoint")
st.write(
    "This is a simple chatbot that uses an external API to generate responses."
)

# Base URL is now the main requirement. API key is completely optional.
openai_api_url = st.text_input("API Base URL (Required)", placeholder="http://localhost:8000/v1")
openai_api_key = st.text_input("API Key (Optional)", type="password", placeholder="Leave blank if not required")

if not openai_api_url:
    st.info("Please add your custom API URL to continue.", icon="🌐")
else:
    # Initialize the client. If no key is provided, pass a dummy string to satisfy the library.
    try:
        client = OpenAI(
            api_key=openai_api_key if openai_api_key else "not-needed",
            base_url=openai_api_url
        )
    except Exception as e:
        st.error(f"Error initializing the client: {e}")
        client = None

    if client:
        # Create a session state variable to store the chat messages.
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display the existing chat messages via `st.chat_message`.
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Create a chat input field to allow the user to enter a message.
        if prompt := st.chat_input("What is up?"):

            # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                # Generate a response using the custom endpoint.
                stream = client.chat.completions.create(
                    model="/root/.cache/huggingface/hub/models--TrevorJS--gemma-4-E2B-it-uncensored-GGUF/snapshots/4345c0c77cde7da43084c94b1deac23c09bccfc1/gemma-4-E2B-it-uncensored-Q4_K_M.gguf",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                # Stream the response to the chat using `st.write_stream`, then store it.
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Failed to generate response. Check your local server terminal. Error: {e}")