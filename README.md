# 🤖 Free Custom AI Builder with Image & Problem-Solving Capabilities

A Streamlit application that lets you create custom AI personalities and interact with them through chat, image analysis, and **problem-solving from images** (like Google Gemini).

## Features

✨ **Custom AI Creation** - Define any AI persona you want (fitness coach, teacher, developer, etc.)

💬 **Chat Interface** - Talk to your custom AI with persistent conversation history

🖼️ **Image Generation** - Generate creative image prompts based on your AI's personality

🔍 **Image Analysis** - Upload images for your AI to analyze and describe

📐 **Problem Solving** - Upload images of problems (math, physics, geometry, etc.) and get step-by-step solutions
- Math problems (algebra, calculus, statistics)
- Geometry and spatial reasoning
- Physics problems
- Chemistry equations
- Logic puzzles and games
- And more!

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

Run the app:
```bash
streamlit run app.py
```

Then:
1. Enter your Gemini API key
2. Define your custom AI's personality and purpose
3. Click "Build My Custom AI"
4. Use any of the 4 tabs:
   - **Chat**: Conversation mode
   - **Generate Images**: Create image prompts
   - **Analyze Images**: Examine uploaded images
   - **Solve Problems**: Get solutions from problem photos

## Problem-Solving Example

Upload an image containing:
- A math equation (e.g., "2x + 5 = 15")
- A geometry problem with a diagram
- A physics equation
- A sudoku puzzle
- A logic puzzle

The AI will:
1. Extract the problem from the image
2. Break it down step-by-step
3. Solve it completely
4. Explain the reasoning
5. Verify the solution

## Requirements

- Python 3.8+
- Google Gemini API key (free tier available)
- Internet connection

## Dependencies

- `streamlit` - Web UI framework
- `google-genai` - Google Gemini API client
- `pillow` - Image processing

## API Key Setup

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key
4. Paste it into the app when prompted

## Features in Detail

### 📐 Problem Solver
- Analyzes images of problems
- Provides structured solutions
- Shows work and explanations
- Verifies answers
- Downloads solutions as text files

### 🤖 Custom AI Personalities
Create specialized AIs:
- Tutors (explains concepts)
- Code reviewers (analyzes code)
- Writers (creative assistance)
- Coaches (motivation & guidance)
- And anything else you imagine!

## Troubleshooting

**"Error analyzing image"**
- Ensure your API key has vision capabilities
- Try PNG or JPG format
- Make sure image is clear and readable
- Check file size (< 20MB)

**"API Key Invalid"**
- Double-check your key from Google AI Studio
- Ensure no extra spaces
- Make sure key hasn't expired

## Built With

- [Streamlit](https://streamlit.io/) - Python web app framework
- [Google Gemini API](https://ai.google.dev/) - Vision & language model
- [Python](https://python.org/) - Programming language

## License

This project is open source and available for educational use.

## Support

For issues with:
- **Gemini API**: Check [Google AI Documentation](https://ai.google.dev/docs)
- **Streamlit**: Visit [Streamlit Docs](https://docs.streamlit.io/)
- **This App**: Create an issue on GitHub

---

**Made with ❤️ to help learners and builders**
