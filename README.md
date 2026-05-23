# 🤖 Free Custom AI Builder with Image & Problem-Solving Capabilities

A Streamlit application that lets you create custom AI personalities and interact with them through chat, image analysis, and **problem-solving from images** (like Google Gemini).

## ✨ Features

### 🧠 **Custom AI Creation** 
Define any AI persona you want (fitness coach, teacher, developer, mentor, etc.)

### 💬 **Chat Interface** 
Talk to your custom AI with persistent conversation history and personality

### 🖼️ **Image Generation** 
Generate creative image prompts based on your AI's personality and style

### 🔍 **Image Analysis** 
Upload images for your AI to analyze and describe in its unique voice

### 📐 **Problem Solving** ⭐ NEW!
Upload images of problems and get step-by-step solutions:
- 🧮 **Mathematics**: Algebra, Calculus, Statistics, Trigonometry
- 🔶 **Geometry**: Shapes, Proofs, Spatial Reasoning, Diagrams
- ⚙️ **Physics**: Mechanics, Energy, Equations, Forces
- 🧪 **Chemistry**: Reactions, Compounds, Stoichiometry
- 🧩 **Logic Puzzles**: Sudoku, Riddles, Games, Brain Teasers
- 📊 **Other Problems**: Economics, Statistics, Programming Challenges

Each solution includes:
- Problem restatement & understanding
- Step-by-step work shown
- Verification & answer checking
- Alternative solution methods
- Concept explanations
- All delivered in your AI's personality!

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhraneel-sealguy/my-custom-ai-builder.git
   cd my-custom-ai-builder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Click "Get API Key"
   - Create a new API key
   - Copy it

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Paste your API key** when prompted in the app

## 📚 Usage Guide

### Creating Your Custom AI

1. Enter your Gemini API key
2. Describe what you want your AI to do:
   - "A sarcastic fitness coach who motivates through humor"
   - "A patient math tutor who explains concepts simply"
   - "A professional code reviewer who finds bugs and suggests improvements"
3. Click "✨ Build My Custom AI"
4. Your AI personality is created instantly!

### Using the 4 Tabs

#### 💬 **Chat Tab**
- Real-time conversation with your AI
- View the AI blueprint/system instructions
- Chat history is maintained
- Your AI responds in its unique personality

#### 🖼️ **Generate Images Tab**
- Describe an image you want to create
- Your AI generates a detailed prompt based on its personality
- Use with image generation APIs (DALL-E, Midjourney, Stable Diffusion, etc.)

#### 🔍 **Analyze Images Tab**
- Upload any image (JPG, PNG, GIF, WebP)
- Ask your AI to analyze it
- Get analysis in your AI's unique style
- Great for creative descriptions, technical reviews, etc.

#### 📐 **Solve Problems Tab** ⭐
- Upload clear image of any problem
- Select problem type (or leave as "Other")
- Add optional context (chapter, constraints, etc.)
- Click "🧠 Solve This Problem"
- Get comprehensive step-by-step solutions
- Download solution as text file

## 🎯 Problem-Solving Examples

### Math Problem
- Upload: Photo of equation "2x² + 5x - 3 = 0"
- Get: Complete solution with quadratic formula steps and verification

### Geometry Problem
- Upload: Photo of triangle diagram
- Get: Area calculation, properties identified, step-by-step solution

### Physics Problem
- Upload: Photo of "Calculate force for 5kg object with 2m/s² acceleration"
- Get: F=ma solution, units verification, concept explanation

### Sudoku Puzzle
- Upload: Photo of incomplete sudoku grid
- Get: Solution with logical steps explained

### Logic Puzzle
- Upload: Photo of puzzle description
- Get: Solution with reasoning explained

## 📦 Requirements

```
streamlit
google-genai
pillow
```

## 🔐 Security & Privacy

- ✅ API key is handled securely (password input field)
- ✅ No data storage - everything is session-based
- ✅ Images processed locally then sent to Google's API
- ✅ Open source - you can review the code

## 🛠️ Troubleshooting

### Vision/Image Features Not Working?
- ✓ Ensure your Gemini API key has vision capabilities (most free keys do)
- ✓ Try PNG or JPG format (most compatible)
- ✓ Check that the image is clear and readable
- ✓ Verify image file size is reasonable (< 20MB)
- ✓ Restart the app and try again

### Problem Solving Errors?
- ✓ Make sure the entire problem is fully visible in the image
- ✓ Use high-quality, well-lit images
- ✓ For multi-part problems, try solving one part at a time
- ✓ Check internet connection
- ✓ Verify API key hasn't reached quota

### API Key Issues?
- ✓ Double-check your key from Google AI Studio
- ✓ Make sure no extra spaces were copied
- ✓ Ensure the key is for Gemini API (not other Google APIs)
- ✓ Create a fresh API key if problems persist

### General Issues?
- ✓ Restart the app: `Ctrl+C` then `streamlit run app.py`
- ✓ Check your internet connection
- ✓ Try with a simpler problem or image first
- ✓ Clear browser cache if UI seems stuck

## 💡 Tips for Best Results

### For Problem Solving
1. **Use clear images**: Good lighting, sharp focus, no blur
2. **Whole problem visible**: Ensure the entire problem is in the image
3. **Add context**: Include curriculum level or specific constraints
4. **One problem at a time**: Multi-part problems work best separately
5. **Handwritten OK**: Photos of handwritten problems work well

### For Image Analysis
1. **Be specific**: Tell AI exactly what to analyze
2. **High quality images**: Clear, well-composed photos
3. **Use personality**: Leverage your AI's unique traits
4. **Ask follow-ups**: Build on the AI's responses

### For Custom AIs
1. **Be detailed**: Specific personality descriptions work better
2. **Test thoroughly**: Try different types of prompts
3. **Iterate**: Refine your AI's personality if needed
4. **Combine features**: Use all tabs with your AI

## 🌟 Example Custom AIs

```
🎓 Math Tutor
"A patient, encouraging math tutor who explains concepts in simple terms 
using real-world examples. You celebrate small victories and break down 
complex problems into manageable steps."

😂 Sarcastic Coach
"A fitness coach with a biting sense of humor who motivates through 
relentless teasing. You're knowledgeable but never let people take 
themselves too seriously."

🎨 Creative Writer
"A creative writing mentor who helps brainstorm stories, improve prose, 
and develop characters. You're enthusiastic and provide constructive 
feedback with encouragement."

👨‍💻 Code Reviewer
"A professional senior developer reviewing code. You're direct, spot 
security issues, suggest performance improvements, and explain why 
changes matter."
```

## 📄 License

This project is open source and available for educational and personal use.

## 🤝 Contributing

Found a bug? Want a feature? Create an issue on GitHub!

## ❤️ Built With

- [Streamlit](https://streamlit.io/) - Web app framework
- [Google Gemini API](https://ai.google.dev/) - Vision & language AI
- [Python](https://python.org/) - Programming language

---

**🚀 Get Started Now!**

Get your free API key: https://aistudio.google.com/app/apikey

**Made with ❤️ to help learners, educators, and builders**
