# 📊 AI Data Analyst (LLM-Powered CSV Insights)

This is an interactive AI-powered data analysis tool that lets you upload any CSV and ask questions in natural language. It uses the blazing fast **GROQ + LLaMA3** backend to deliver:

- 💬 Natural language insights
- 📈 Automatic chart generation (when requested)
- 🧠 Session-based Q&A history
- 🔍 Fuzzy query matching to correct typos or vague terms

---

## 🚀 Features

- ✅ Upload any CSV
- ✅ Ask free-form questions like:
- ✅ Visualizations when queries include "plot", "chart", "graph", etc.
- ✅ Fuzzy query matching to correct column names
- ✅ Session history of past questions and answers

---

## 🧠 Powered by

| LLM Engine         | Why?                               |
|--------------------|-------------------------------------|
| **GROQ + LLaMA3**  | Lightning-fast, OpenAI-compatible, FREE |

---

## 🖥️ Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/PadhmaSini29/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Install dependencies

Make sure Python 3.10+ is installed.

```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your-groq-api-key-here
```

(Refer to `.env.template`)

### 4. Launch the app

```bash
streamlit run streamlit_app.py
```

---

## 🌍 Sample Usage

Upload a CSV like this:

| date       | temp_max | temp_min | wind_speed |
|------------|----------|----------|------------|
| 2023-01-01 | 20.1     | 12.3     | 5.6        |

Then ask:
- "When was the coldest day?"
- "Plot temp_max over time"
- "Average wind speed?"

---

## 🛡️ Security

- ✅ `.env` is ignored by Git
- ✅ `.env.template` included for contributors
- 🚫 No secrets are stored or committed


