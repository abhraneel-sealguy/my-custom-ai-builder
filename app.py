import streamlit as st
from google import genai

# 1. Setup the Webpage Title and Style
st.set_page_config(page_title="Free Custom AI Builder", page_icon="🤖", layout="centered")

st.title("🤖 Free Custom AI Generator")
st.write("Describe what kind of AI expert you need, and our background AI will build it for you instantly!")

# 2. Securely Ask the User for their Gemini API Key
user_api_key = st.text_input("Step 1: Enter your Google Gemini API Key", type="password",
                             help="Get a free key from Google AI Studio")

if not user_api_key:
    st.info("Please enter your API key to activate the background AI builder.", icon="🔑")
else:
    # Initialize the Google GenAI client with the user's key
    try:
        client = genai.Client(api_key=user_api_key)

        st.divider()

        # 3. Get the Custom AI Requirements
        st.subheader("Step 2: Define your Custom AI")
        ai_purpose = st.text_area(
            "What should your custom AI do?",
            placeholder="Example: A sarcastic fitness coach who gives short workout tips and makes fun of lazy habits."
        )

        # 4. Generate the Persona using Background AI
        if st.button("✨ Build My Custom AI", type="primary"):
            if ai_purpose.strip() == "":
                st.error("Please describe what you want your AI to do first!")
            else:
                with st.spinner("Background AI is formatting and training your custom persona..."):
                    # We instruct the background AI to generate system instructions
                    meta_prompt = f"You are a master AI engineer. Create a highly detailed system prompt/persona for an AI whose job is: '{ai_purpose}'. Return only the rules, tone, constraints, and instructions for this AI persona. Do not include introductory text."

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=meta_prompt
                    )

                    # Store the generated custom persona in the app's memory
                    st.session_state['custom_persona'] = response.text
                    st.session_state['chat_history'] = []
                    st.success("🎉 Your Custom AI has been successfully created below!")

        # 5. Interact with the Newly Created Custom AI
        if 'custom_persona' in st.session_state:
            st.divider()
            st.subheader("Step 3: Chat with your Custom AI")

            # Show the user what the background AI built for them
            with st.expander("View Blueprint / System Instructions of your AI"):
                st.write(st.session_state['custom_persona'])

            # User chat input
            user_message = st.chat_input("Talk to your custom AI here...")

            if user_message:
                # Add user message to history
                st.session_state['chat_history'].append({"role": "user", "text": user_message})

                # Combine Persona + Chat History to send to Gemini
                full_context = f"SYSTEM INSTRUCTIONS:\n{st.session_state['custom_persona']}\n\nCHAT HISTORY:\n"
                for msg in st.session_state['chat_history']:
                    full_context += f"{msg['role']}: {msg['text']}\n"

                # Get response from the custom AI configuration
                with st.spinner("Custom AI is thinking..."):
                    ai_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_context
                    )

                # Add AI response to history
                st.session_state['chat_history'].append({"role": "model", "text": ai_response.text})

            # Display the conversation
            for msg in st.session_state['chat_history']:
                if msg['role'] == "user":
                    with st.chat_message("user"):
                        st.write(msg['text'])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(msg['text'])

    except Exception as e:
        st.error(f"An error occurred. Check your API key or connection. Details: {e}")
