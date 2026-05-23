import streamlit as st
from google import genai
import base64
from datetime import datetime
import pytz

# 1. Setup the Webpage Title and Style
st.set_page_config(page_title="Free Custom AI Builder", page_icon="🤖", layout="wide")

st.title("🤖 Free Custom AI Generator with Image Capabilities")
st.write("Describe what kind of AI expert you need, and our background AI will build it for you instantly! Plus, generate, analyze images, and solve problems from pictures.")

# Display Digital Clock with Timezones in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("⏰ Global Time Zones")

# Common timezones
timezones = {
    "🌍 UTC": "UTC",
    "🇺🇸 Eastern (ET)": "America/New_York",
    "🇺🇸 Central (CT)": "America/Chicago",
    "🇺🇸 Mountain (MT)": "America/Denver",
    "🇺🇸 Pacific (PT)": "America/Los_Angeles",
    "🇬🇧 London (GMT)": "Europe/London",
    "🇪🇺 Paris (CET)": "Europe/Paris",
    "🇮🇳 India (IST)": "Asia/Kolkata",
    "🇨🇳 Beijing (CST)": "Asia/Shanghai",
    "🇯🇵 Tokyo (JST)": "Asia/Tokyo",
    "🇦🇺 Sydney (AEDT)": "Australia/Sydney",
    "🇧🇷 São Paulo (BRT)": "America/Sao_Paulo",
    "🇦🇪 Dubai (GST)": "Asia/Dubai",
    "🇸🇬 Singapore (SGT)": "Asia/Singapore",
}

# Allow user to select which timezones to display
selected_timezones = st.sidebar.multiselect(
    "Select timezones to display:",
    list(timezones.keys()),
    default=["🌍 UTC", "🇺🇸 Eastern (ET)", "🇯🇵 Tokyo (JST)"]
)

# Allow user to add custom timezones
st.sidebar.markdown("**Add Custom Timezone:**")
custom_tz_input = st.sidebar.text_input("Enter timezone (e.g., America/New_York):", "")
custom_timezones = {}
if custom_tz_input:
    try:
        pytz.timezone(custom_tz_input)
        custom_timezones = {custom_tz_input: custom_tz_input}
    except pytz.exceptions.UnknownTimeZoneError:
        st.sidebar.error(f"Invalid timezone: {custom_tz_input}")

# Create a placeholder for the clock display
clock_placeholder = st.sidebar.empty()

# Function to update clock
def update_clock():
    current_time = datetime.now()
    
    clock_html = '<div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; font-family: monospace; color: #00ff00; font-size: 12px;">'
    
    # Display selected timezones
    for label in selected_timezones:
        if label in timezones:
            tz_name = timezones[label]
            try:
                tz = pytz.timezone(tz_name)
                time_in_tz = current_time.astimezone(tz)
                time_str = time_in_tz.strftime("%H:%M:%S")
                date_str = time_in_tz.strftime("%a, %b %d, %Y")
                utc_offset = time_in_tz.strftime("%z")
                offset_formatted = f"{utc_offset[:3]}:{utc_offset[3:]}"
                clock_html += f'<div style="margin: 10px 0; padding: 8px; border: 1px solid #00ff00; border-radius: 5px;"><strong>{label}</strong><br><span style="font-size: 16px; font-weight: bold;">{time_str}</span><br><span style="font-size: 11px; color: #888;">{date_str} ({offset_formatted})</span></div>'
            except:
                pass
    
    # Display custom timezone if added
    for tz_name in custom_timezones.keys():
        try:
            tz = pytz.timezone(tz_name)
            time_in_tz = current_time.astimezone(tz)
            time_str = time_in_tz.strftime("%H:%M:%S")
            date_str = time_in_tz.strftime("%a, %b %d, %Y")
            utc_offset = time_in_tz.strftime("%z")
            offset_formatted = f"{utc_offset[:3]}:{utc_offset[3:]}"
            clock_html += f'<div style="margin: 10px 0; padding: 8px; border: 2px solid #ffff00; border-radius: 5px;"><strong>✨ {tz_name}</strong><br><span style="font-size: 16px; font-weight: bold;">{time_str}</span><br><span style="font-size: 11px; color: #888;">{date_str} ({offset_formatted})</span></div>'
        except:
            pass
    
    clock_html += '</div>'
    clock_placeholder.markdown(clock_html, unsafe_allow_html=True)

# Update clock on page load
update_clock()

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
                    meta_prompt = f"You are a master AI engineer. Create a highly detailed system prompt/persona for an AI whose job is: '{ai_purpose}'. Return only the rules, tone, constraints, and behavioral guidelines. Be specific and detailed."

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
            tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🖼️ Generate Images", "🔍 Analyze Images", "📐 Solve Problems"])
            
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
                            prompt_creation = f"SYSTEM INSTRUCTIONS:\n{st.session_state['custom_persona']}\n\nYou are being asked to create a detailed image generation prompt. The user wants: {image_description}. Create a vivid, detailed prompt that captures the essence of what they want while incorporating your personality and style."
                            
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
                                st.info("💡 Troubleshooting tips:\n1. Make sure your Gemini API key has vision capabilities\n2. Try with a different image format (PNG or JPG)\n3. Check your internet connection")

            with tab4:
                st.subheader("📐 Solve Problems from Pictures")
                st.write("Upload an image containing a problem (math, physics, logic puzzles, etc.) and your custom AI will solve it step-by-step!")
                
                # Problem type selector
                problem_type = st.selectbox(
                    "What type of problem is this?",
                    [
                        "Mathematics (Algebra, Calculus, Statistics)",
                        "Geometry (Shapes, proofs, diagrams)",
                        "Physics (Equations, mechanics, energy)",
                        "Chemistry (Reactions, compounds)",
                        "Logic Puzzles & Games",
                        "Sudoku & Number Puzzles",
                        "Other"
                    ],
                    key="problem_type"
                )
                
                # File uploader for problem image
                problem_file = st.file_uploader("Upload the image with the problem:", type=["jpg", "jpeg", "png", "gif", "webp"], key="problem_upload")
                
                # Additional context
                additional_context = st.text_area(
                    "Any additional information about the problem? (optional)",
                    placeholder="Example: This is from Chapter 5 on quadratic equations, or provide any constraints",
                    key="problem_context"
                )
                
                if problem_file and st.button("🧠 Solve This Problem", type="primary"):
                    with st.spinner("Your AI is solving the problem..."):
                        try:
                            # Read the problem image
                            problem_data = problem_file.read()
                            
                            # Display the problem image
                            st.image(problem_data, caption="Problem Image", use_column_width=True)
                            
                            # Encode to base64
                            problem_base64 = base64.standard_b64encode(problem_data).decode("utf-8")
                            
                            # Determine media type
                            file_ext = problem_file.name.split('.')[-1].lower()
                            media_types = {
                                'jpg': 'image/jpeg',
                                'jpeg': 'image/jpeg',
                                'png': 'image/png',
                                'gif': 'image/gif',
                                'webp': 'image/webp'
                            }
                            media_type = media_types.get(file_ext, 'image/jpeg')
                            
                            # Create the problem-solving prompt with custom AI persona
                            solving_prompt = f"""SYSTEM INSTRUCTIONS:
{st.session_state['custom_persona']}

TASK: Solve the problem shown in the image. This is a {problem_type} problem.
{f'Additional context: {additional_context}' if additional_context else ''}

Please provide:
1. **Problem Statement**: Extract and restate the problem clearly
2. **Understanding**: Explain what the problem is asking
3. **Solution Steps**: Show detailed step-by-step work
4. **Calculations/Logic**: Show all mathematical or logical reasoning
5. **Answer**: State the final answer clearly
6. **Verification**: Double-check the answer and explain why it's correct
7. **Alternative Methods**: If applicable, show alternative approaches
8. **Concepts Used**: Explain the key concepts or formulas applied

Be thorough, clear, and educational in your explanation while maintaining your AI's unique personality and style."""
                            
                            # Create image part
                            problem_image_part = genai.Part(
                                inline_data=genai.types.BlobData(
                                    mime_type=media_type,
                                    data=problem_base64
                                )
                            )
                            
                            # Send to Gemini for solving
                            solution_response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=[
                                    solving_prompt,
                                    problem_image_part
                                ]
                            )
                            
                            st.success("✅ Problem solved!")
                            st.write("**Solution:**")
                            st.write(solution_response.text)
                            
                            # Option to download solution
                            if st.button("📥 Download Solution as Text"):
                                solution_text = f"PROBLEM TYPE: {problem_type}\n\nCONTEXT: {additional_context if additional_context else 'None provided'}\n\nSOLUTION:\n\n{solution_response.text}"
                                st.download_button(
                                    label="Click to download",
                                    data=solution_text,
                                    file_name="problem_solution.txt",
                                    mime="text/plain"
                                )
                            
                        except Exception as problem_error:
                            st.error(f"Error solving problem: {str(problem_error)}")
                            st.info("💡 Troubleshooting tips:\n1. Make sure the image is clear and readable\n2. Ensure your API key supports vision\n3. Try with a different image format (PNG or JPG recommended)\n4. Make sure the problem is fully visible in the image")

    except Exception as e:
        st.error(f"An error occurred. Check your API key or connection. Details: {e}")
