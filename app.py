import streamlit as st
from google import genai
import base64

# 1. Setup the Webpage Title and Style
st.set_page_config(page_title="Free Custom AI Builder", page_icon="🤖", layout="wide")

st.title("🤖 Free Custom AI Generator with Image Capabilities")
st.write("Describe what kind of AI expert you need, and our background AI will build it for you instantly! Plus, generate and analyze images.")

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
                    meta_prompt = f"You are a master AI engineer. Create a highly detailed system prompt/persona for an AI whose job is: '{ai_purpose}'. Return only the rules, tone, constraints, and key behaviors. Be specific and creative."

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
            
            # Create tabs for different interaction modes
            tab1, tab2, tab3 = st.tabs(["💬 Chat", "🖼️ Generate Images", "🔍 Analyze Images"])
            
            with tab1:
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

            with tab2:
                st.subheader("Generate Images with Your Custom AI")
                st.write("Describe an image you'd like to generate, and the AI will create a detailed prompt based on its personality.")
                
                image_description = st.text_area(
                    "Describe the image you want to generate:",
                    placeholder="Example: A futuristic city at sunset with flying cars and neon signs",
                    key="image_gen_input"
                )
                
                if st.button("🎨 Generate Image", type="primary"):
                    if not image_description.strip():
                        st.error("Please describe the image you want to generate!")
                    else:
                        with st.spinner("Your AI is crafting the perfect image prompt..."):
                            # First, have the custom AI create a detailed prompt based on its personality
                            prompt_creation = f"SYSTEM INSTRUCTIONS:\n{st.session_state['custom_persona']}\n\nYou are being asked to create a detailed image generation prompt. The user wants: {image_description}\n\nCreate a vivid, detailed prompt that matches your personality and the user's request. Return ONLY the image prompt, nothing else."
                            
                            prompt_response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=prompt_creation
                            )
                            
                            detailed_prompt = prompt_response.text
                            
                            st.info(f"**AI-Generated Prompt:** {detailed_prompt}")
                            st.success("✅ Image prompt generated successfully! (Note: Image generation requires additional image generation API)")

            with tab3:
                st.subheader("Analyze Images with Your Custom AI")
                st.write("Upload an image and your custom AI will analyze it based on its personality.")
                
                uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "webp"])
                
                analysis_prompt_input = st.text_area(
                    "What would you like your AI to analyze about this image?",
                    placeholder="Example: Describe what you see and give your opinion in your unique style",
                    key="image_analysis_input"
                )
                
                if uploaded_file and st.button("🔍 Analyze Image", type="primary"):
                    if not analysis_prompt_input.strip():
                        st.error("Please provide instructions for what to analyze!")
                    else:
                        with st.spinner("Your AI is analyzing the image..."):
                            try:
                                # Read the uploaded image
                                image_data = uploaded_file.read()
                                
                                # Display the uploaded image
                                st.image(image_data, caption="Uploaded Image", use_column_width=True)
                                
                                # Encode image to base64
                                image_base64 = base64.standard_b64encode(image_data).decode("utf-8")
                                
                                # Determine the media type
                                file_extension = uploaded_file.name.split('.')[-1].lower()
                                media_type_map = {
                                    'jpg': 'image/jpeg',
                                    'jpeg': 'image/jpeg',
                                    'png': 'image/png',
                                    'gif': 'image/gif',
                                    'webp': 'image/webp'
                                }
                                media_type = media_type_map.get(file_extension, 'image/jpeg')
                                
                                # Create system context with persona
                                system_context = f"SYSTEM INSTRUCTIONS:\n{st.session_state['custom_persona']}\n\nUser request: {analysis_prompt_input}"
                                
                                # Use genai.Part to properly structure the request
                                image_part = genai.Part(
                                    inline_data=genai.types.BlobData(
                                        mime_type=media_type,
                                        data=image_base64
                                    )
                                )
                                
                                # Send to Gemini with image
                                response = client.models.generate_content(
                                    model='gemini-2.5-flash',
                                    contents=[
                                        system_context,
                                        image_part
                                    ]
                                )
                                
                                st.success("✅ Analysis complete!")
                                st.write("**AI Analysis:**")
                                st.write(response.text)
                                
                            except Exception as image_error:
                                st.error(f"Error analyzing image: {str(image_error)}")
                                st.info("💡 Troubleshooting tips:\n1. Make sure your Gemini API key has vision capabilities\n2. Try with a different image format (PNG or JPG)\n3. Check that your API account has Vision API access enabled")

    except Exception as e:
        st.error(f"An error occurred. Check your API key or connection. Details: {e}")
