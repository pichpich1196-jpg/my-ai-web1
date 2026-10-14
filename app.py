import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import streamlit as st

# កំណត់ទម្រង់ទំព័រ
st.set_page_config(
    page_title="KhemaraAI WorkSuite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== KHEMARAAI DARK SAAS CSS ====================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Kantumruy Pro', sans-serif !important;
        background-color: #0b0e17 !important;
        color: #e2e8f0 !important;
    }

    /* Navbar Header */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0 20px 0;
        border-bottom: 1px solid #1e2436;
        margin-bottom: 25px;
    }
    .brand-box {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-logo {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    .brand-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .brand-subtitle {
        font-size: 13px;
        color: #94a3b8;
    }
    .status-badge {
        background-color: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #131722;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #1e2433;
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        font-weight: 500;
        font-size: 14px;
        color: #94a3b8;
        padding: 0 18px;
        border: none !important;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }

    /* Container Cards */
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .card-header-title {
        font-size: 18px;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .tag-badge {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Primary Action Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.35) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5) !important;
    }

    /* Upload Box Styling */
    [data-testid="stFileUploader"] {
        background-color: #0f121d;
        border: 1.5px dashed #2d3748;
        border-radius: 14px;
        padding: 12px;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
    }

    /* Empty Result Placeholder Box */
    .empty-result-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 480px;
        border: 1px solid #1a202c;
        border-radius: 14px;
        background: #0f131f;
        text-align: center;
        padding: 30px;
    }
    .empty-icon {
        font-size: 45px;
        margin-bottom: 15px;
        opacity: 0.6;
    }
    .empty-title {
        font-size: 16px;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 8px;
    }
    .empty-desc {
        font-size: 13px;
        color: #64748b;
        max-width: 320px;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ផ្ទៀងផ្ទាត់ API Key ពី Streamlit Secrets (សុវត្ថិភាពខ្ពស់)
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
  st.warning("⚠️ សូមកំណត់ GEMINI_API_KEY នៅក្នុង Streamlit Secrets ជាមុនសិន!")
  st.stop()

client = genai.Client(api_key=api_key)

# ==================== TOP NAVIGATION BAR ====================
st.markdown(
    """
    <div class="top-nav">
        <div class="brand-box">
            <div class="brand-logo">⚡</div>
            <div>
                <div class="brand-title">KhemaraAI WorkSuite</div>
                <div class="brand-subtitle">ប្រព័ន្ធជំនួយការរដ្ឋបាល និងការិយាល័យឆ្លាតវៃ AI</div>
            </div>
        </div>
        <div class="status-badge">
            <span style="height: 8px; width: 8px; background-color: #10b981; border-radius: 50%; display: inline-block;"></span>
            Gemini Flash (ល្បឿនលឿនបំផុត)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================== TABS BAR ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ សំឡេង ➜ របាយការណ៍",
    "📄 សម្រាយ & សង្ខេបឯកសារ",
    "🌐 បកប្រែភាសាការងារ",
    "💬 ជំនួយការឆ្លាតវៃ (AI Chat)",
])

# ----------------- TAB 1: VOICE REPORT -----------------
with tab1:
  col_left, col_right = st.columns([1, 1], gap="large")

  with col_left:
    st.markdown(
        """
        <div class="card-top">
            <div class="card-header-title">🎙️ បម្លែងសំឡេងជារបាយការណ៍</div>
            <div class="tag-badge">AI Audio Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    source_type = st.radio(
        "ជ្រើសរើសប្រភពសំឡេង៖",
        ["📁 បញ្ចូល File សំឡេង", "🔴 ថតសំឡេងផ្ទាល់"],
        horizontal=True,
    )

    audio_file = None
    if "បញ្ចូល File" in source_type:
      audio_file = st.file_uploader(
          "ចុចទីនេះ ឬទម្លាក់ File សំឡេងចូល (MP3, WAV, M4A, OGG, WebM)៖",
          type=["mp3", "wav", "ogg", "m4a", "webm"],
      )
    else:
      audio_file = st.audio_input("ចុចប៊ូតុងក្រហមដើម្បីចាប់ផ្ដើមថតសំឡេង៖")

    st.markdown("<br>", unsafe_allow_html=True)
    report_format = st.radio(
        "ជ្រើសរើសទម្រង់របាយការណ៍ដែលត្រូវការ៖",
        [
            "📊 វឌ្ឍនភាពការងារ (របាយការណ៍ការងារទូទៅ សកម្មភាព លទ្ធផល"
            " និងបញ្ហាប្រឈម)",
            "🏛️ ការងារចុះមូលដ្ឋាន (របាយការណ៍ចុះជួបប្រជាពលរដ្ឋ សំណូមពរ"
            " និងដំណោះស្រាយ)",
            "📝 កំណត់ហេតុប្រជុំ (ខ្លឹមសារអង្គប្រជុំ មតិពិភាក្សា និងសេចក្ដីសម្រេច)",
            (
                "⚡ សង្ខេបបន្ទាន់ (Brief) (ខ្លឹមសារស្នូលខ្លីៗ ចំណុចសំខាន់ៗ"
                " និងសកម្មភាពបន្ទាន់)"
            ),
        ],
    )

    custom_notes = st.text_input(
        "ចំណាំបន្ថែម ឬការណែនាំពិសេស (បើមាន)៖",
        placeholder="ឧទាហរណ៍៖ សូមសង្កត់ធ្ងន់លើលទ្ធផលការងារ និងកាលបរិច្ឆេទ...",
    )

    btn_audio = st.button("✏️ រៀបចំរបាយការណ៍ដោយ AI", key="btn_run_voice")

  with col_right:
    st.markdown(
        """
        <div class="card-top">
            <div class="card-header-title">📋 លទ្ធផលរបាយការណ៍</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if audio_file and btn_audio:
      with st.spinner("AI កំពុងស្ដាប់ និងរៀបចំជារបាយការណ៍ផ្លូវការ..."):
        ext = audio_file.name.split(".")[-1] if hasattr(audio_file, "name") else "wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
          tmp.write(audio_file.read())
          tmp_path = tmp.name

        try:
          mime = (
              audio_file.type
              if hasattr(audio_file, "type")
              else f"audio/{ext}"
          )
          uploaded = client.files.upload(file=tmp_path, mime_type=mime)
          prompt = f"""
                    សូមស្ដាប់សំឡេងនេះ ហើយរៀបចំចេញជា '{report_format}' ជាភាសាខ្មែរផ្លូវការ ស្អាតបាត និងមានលំដាប់លំដោយ។
                    កំណត់សម្គាល់បន្ថែមពីអ្នកប្រើប្រាស់៖ {custom_notes if custom_notes else 'គ្មាន'}
                    
                    ទម្រង់រៀបចំ៖
                    - ចំណងជើងរបាយការណ៍
                    - ព័ត៌មានទូទៅ
                    - ខ្លឹមសារលម្អិត
                    - លទ្ធផលសម្រេចបាន
                    - បញ្ហា និងដំណោះស្រាយ/ទិសដៅបន្ត
                    """
          resp = client.models.generate_content(
              model="gemini-2.5-flash", contents=[uploaded, prompt]
          )
          client.files.delete(name=uploaded.name)

          st.success("✅ រៀបចំរបាយការណ៍ជោគជ័យ!")
          st.markdown(resp.text)
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
    else:
      st.markdown(
          """
            <div class="empty-result-box">
                <div class="empty-icon">📄</div>
                <div class="empty-title">រង់ចាំការបម្លែងសំឡេង</div>
                <div class="empty-desc">សូមបញ្ចូល File សំឡេង ឬចុចថតសំឡេង រួចចុចប៊ូតុងខាងឆ្វេង ដើម្បីឱ្យ AI រៀបចំរបាយការណ៍ជូនលោកអ្នក។</div>
            </div>
            """,
            unsafe_allow_html=True,
      )

# ----------------- TAB 2: DOCUMENTS -----------------
with tab2:
  c_doc1, c_doc2 = st.columns([1, 1], gap="large")
  with c_doc1:
    st.markdown("### 📄 ជ្រើសរើសឯកសារ")
    doc_file = st.file_uploader(
        "បញ្ចូល File (PDF, Word, PPT)៖", type=["pdf", "docx", "pptx"]
    )
    doc_style = st.radio(
        "កម្រិតនៃការសង្ខេប៖",
        ["សង្ខេបខ្លឹមសារស្នូល ៣-៥ ចំណុច", "សម្រាយលម្អិតតាមជំពូក"],
        horizontal=True,
    )
    btn_doc = st.button("🚀 សម្រាយឯកសារ", key="btn_doc_action")
  with c_doc2:
    st.markdown("### 📑 ខ្លឹមសារសម្រាយ")
    if doc_file and btn_doc:
      with st.spinner("AI កំពុងអានឯកសារ..."):
        ext = doc_file.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
          tmp.write(doc_file.read())
          tmp_path = tmp.name
        try:
          p = f"សូមសម្រាយខ្លឹមសារនេះជាភាសាខ្មែរតាមទម្រង់ '{doc_style}'៖"
          if ext == "pdf":
            up = client.files.upload(file=tmp_path, mime_type="application/pdf")
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=[up, p]
            )
            client.files.delete(name=up.name)
            st.markdown(res.text)
          elif ext == "docx":
            d = docx.Document(tmp_path)
            txt = "\n".join([pr.text for pr in d.paragraphs if pr.text.strip()])
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{p}\n\n{txt}"
            )
            st.markdown(res.text)
          elif ext == "pptx":
            prs = Presentation(tmp_path)
            txt = "\n".join([
                pr.text
                for s in prs.slides
                for sh in s.shapes
                if sh.has_text_frame
                for pr in sh.text_frame.paragraphs
                if pr.text.strip()
            ])
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{p}\n\n{txt}"
            )
            st.markdown(res.text)
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
    else:
      st.info("👈 បញ្ចូលឯកសារដើម្បីឱ្យ AI ជួយសម្រាយ")

# ----------------- TAB 3: TRANSLATION -----------------
with tab3:
  st.markdown("### 🌐 បកប្រែភាសាការងារផ្លូវការ")
  lang = st.selectbox(
      "បកប្រែទៅជា៖", ["ភាសាខ្មែរ", "ភាសាអង់គ្លេស", "ភាសាចិន"]
  )
  raw_text = st.text_area("បញ្ចូលអត្ថបទដើមនៅទីនេះ៖", height=150)
  if st.button("🚀 បកប្រែឥឡូវនេះ", key="btn_trans_action") and raw_text:
    with st.spinner("AI កំពុងបកប្រែ..."):
      res = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=(
              f"សូមបកប្រែអត្ថបទនេះទៅជា {lang} ឱ្យត្រឹមត្រូវតាមក្បួនខ្នាតរដ្ឋបាលផ្លូវការ៖\n\n{raw_text}"
          ),
      )
      st.markdown(res.text)

# ----------------- TAB 4: CHAT ASSISTANT -----------------
with tab4:
  st.markdown("### 💬 ជំនួយការឆ្លាតវៃ AI Chat")
  q = st.text_area("សួរសំណួរ ឬឱ្យជួយព្រាងលិខិតផ្លូវការផ្សេងៗ៖", height=130)
  if st.button("🚀 ឆ្លើយតប", key="btn_chat_action") and q:
    with st.spinner("AI កំពុងរៀបចំខ្លឹមសារ..."):
      res = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=(
              "អ្នកគឺជាជំនួយការបច្ចេកទេស និងរដ្ឋបាលដ៏ជំនាញ។ ឆ្លើយជាភាសាខ្មែរផ្លូវការ"
              f" និងជាក់ច្បាស់៖ {q}"
          ),
      )
      st.markdown(res.text)
