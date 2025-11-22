import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 頁面設定 (必須是第一行) ---
st.set_page_config(
    page_title="VM Smart Eye",
    page_icon="👁️",
    layout="centered"
)

# --- 2. 自定義 CSS (讓介面更漂亮) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: white;
        border-radius: 5px;
    }
    .report-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 標題與介紹 ---
st.title("👁️ VM Smart Eye")
st.caption("您的 AI 陳列合規助手 | Powered by Gemini 2.0 Flash")

with st.expander("ℹ️ 關於這個 App (About)"):
    st.write("""
    這個應用程式由一位擁有 15 年經驗的 VM 經理開發。
    它使用 AI 來模擬專業的巡店視角，幫助您即時檢查陳列是否符合指引。
    """)

# --- 4. 側邊欄：設定 API Key ---
with st.sidebar:
    st.header("⚙️ 設定")
    # 嘗試從 Secrets 讀取，如果沒有則讓用戶輸入
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("API Key 已從系統讀取 ✅")
    else:
        api_key = st.text_input("請輸入 Google API Key", type="password")
        if not api_key:
            st.warning("請輸入 API Key 才能開始使用")
            st.stop()

# --- 5. 主畫面：輸入指引與圖片 ---

# 指引輸入區 (預設填入範本)
default_guideline = """【2025 Spring Collection Guidelines】
1. Color: Focus on Sage Green & Pistachio.
2. Styling: Mannequins must use 'Relaxed Logic' poses.
3. Housekeeping: Floor must be clear, rails leveled.
"""
guideline_text = st.text_area("📋 本季陳列指引 (Current Guidelines)", value=default_guideline, height=150)

# 圖片上傳區
uploaded_file = st.file_uploader("📸 上傳店鋪照片 (Upload Photo)", type=["jpg", "jpeg", "png"])

# --- 6. 核心邏輯 (AI 分析) ---
if uploaded_file and st.button("🚀 開始智能分析 (Analyze)"):
    if not api_key:
        st.error("請先設定 API Key！")
    else:
        try:
            # 設定模型
            genai.configure(api_key=api_key)
            
            # 顯示載入動畫
            with st.spinner('VM Smart Eye 正在仔細觀察您的照片...'):
                image = Image.open(uploaded_file)
                
                # 顯示圖片
                st.image(image, caption='上傳的照片', use_column_width=True)

                # Prompt (沿用我們優化過的版本)
                prompt = f"""
                你是一位資深的 Visual Merchandising Manager (VM Smart Eye)。
                
                ---
                📋 本季陳列指引:
                {guideline_text}
                ---

                請分析圖片並生成繁體中文報告。
                思維步驟:
                1. 視覺識別 (顏色、模特、整潔度)。
                2. 合規對比 (與指引比對)。
                3. 生成 Markdown 報告。

                格式要求:
                ## 👁️ VM Smart Eye 智能巡店報告
                **📊 合規評分:** [0-10]/10
                **✅ 亮點:**
                **⚠️ 違規與改進:** (指出具體違規點並提供改進方案)
                **💡 專家洞察:**
                """
                
                # 呼叫 Gemini 2.0 Flash
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content([prompt, image])
                
                # 顯示結果
                st.markdown("---")
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                st.success("分析完成！")

        except Exception as e:
            st.error(f"發生錯誤: {str(e)}")
