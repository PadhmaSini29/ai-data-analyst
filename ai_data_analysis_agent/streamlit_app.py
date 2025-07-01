import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from dotenv import load_dotenv

from utils.data_loader import load_csv_and_get_info
from agent import generate_answer_from_query, generate_insight_with_chart_instruction

# Load environment variables (for GROQ_API_KEY)
load_dotenv()

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("📊 AI Data Analyst (Insights + Charts)")

# Session state for Q&A history
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df_info = load_csv_and_get_info(df)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    query = st.text_input("❓ Ask a question about your data")

    if st.button("Generate Answer") and query:
        with st.spinner("Thinking..."):
            keywords = ["plot", "chart", "graph", "visualize"]
            is_chart_query = any(kw in query.lower() for kw in keywords)

            if is_chart_query:
                response = generate_insight_with_chart_instruction(query, df)
                plot_match = re.search(r"\[plot\](.*?)\[/plot\]", response, re.DOTALL)
                insight_text = re.sub(r"\[plot\].*?\[/plot\]", "", response, flags=re.DOTALL).strip()

                st.subheader("💡 Insight")
                st.write(insight_text)

                if plot_match:
                    try:
                        local_env = {"df": df.copy(), "pd": pd, "plt": plt}
                        exec(plot_match.group(1), {}, local_env)
                        st.subheader("📊 Chart")
                        st.pyplot(plt.gcf())
                        plt.clf()
                    except Exception as e:
                        st.error(f"⚠️ Failed to generate chart: {e}")

                # Store Q&A and chart code in session
                st.session_state.qa_history.append(
                    (query, insight_text, plot_match.group(1).strip() if plot_match else None)
                )

            else:
                answer = generate_answer_from_query(query, df)
                st.subheader("💬 Answer")
                st.write(answer)

                # Store Q&A without chart
                st.session_state.qa_history.append((query, answer, None))

    # Q&A History
    if st.session_state.qa_history:
        st.subheader("🕘 Q&A History")
        for i, (q, a, plot_code) in enumerate(st.session_state.qa_history[::-1], 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            if plot_code:
                try:
                    local_env = {"df": df.copy(), "pd": pd, "plt": plt}
                    exec(plot_code, {}, local_env)
                    st.pyplot(plt.gcf())
                    plt.clf()
                except Exception as e:
                    st.warning(f"⚠️ Failed to re-display chart: {e}")
