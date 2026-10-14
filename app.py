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

    /* Result & Empty Placeholder */
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

# ផ្ទៀងផ្ទាត់ API Key ពី Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
  st.warning("⚠️ សូមកំណត់ GEMINI_API_KEY នៅក្នុង Streamlit Secrets ជាមុនសិន!")
  st.stop()

client = genai.Client(api_key=api_key)

# បញ្ជីភាសាពេញនិយម
LANG_OPTIONS = [
    "ភាសាខ្មែរ (Khmer)",
    "ភាសាអង់គ្លេស (English)",
    "ភាសាចិន (Chinese)",
    "ភាសាថៃ (Thai)",
    "ភាសាវៀតណាម (Vietnamese)",
    "ភាសាបារាំង (French)",
    "ភាសាជប៉ុន (Japanese)",
    "ភាសាកូរ៉េ (Korean)",
    "ភាសាអេស្ប៉ាញ (Spanish)",
    "ភាសាអាល្លឺម៉ង់ (German)",
    "ភាសាផ្សេងទៀត (Other)",
]

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
    "🎙️ សំឡេង ➜ របាយការណ៍/អក្សរ",
    "📄 សម្រាយ & សង្ខេបឯកសារ",
    "🌐 បកប្រែគ្រប់ភាសា (Universal)",
    "💬 ជំនួយការឆ្លាតវៃ (AI Chat)",
])

# ----------------- TAB 1: AUDIO TRANSCRIPTION & REPORT -----------------
with tab1:
  col_left, col_right = st.columns([1, 1], gap="large")

  with col_left:
    st.markdown(
        """
        <div class="card-top">
            <div class="card-header-title">🎙️ បម្លែងសំឡេងទៅជាអក្សរ & របាយការណ៍</div>
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
          "បញ្ចូល File សំឡេង (MP3, WAV, M4A, OGG, WebM)៖",
          type=["mp3", "wav", "ogg", "m4a", "webm"],
      )
    else:
      audio_file = st.audio_input("ចុចប៊ូតុងក្រហមដើម្បីចាប់ផ្ដើមថតសំឡេង៖")

    # គោលបំណងនៃការបម្លែងសំឡេង
    audio_task = st.radio(
        "តម្រូវការបម្លែងសំឡេង៖",
        [
            "📝 បម្លែងសំឡេងជាអត្ថបទសុទ្ធ (Transcribe / Voice to Text)",
            "📊 រៀបចំចេញជារបាយការណ៍ការងារផ្លូវការ",
        ],
        horizontal=True,
    )

    # ជម្រើសភាសាលទ្ធផល
    target_audio_lang = st.selectbox(
        "ភាសាលទ្ធផលដែលចង់បាន (បកប្រែចេញពីសំឡេង)៖",
        LANG_OPTIONS,
        index=0,  # default ជាភាសាខ្មែរ
    )

    report_format = ""
    if "របាយការណ៍" in audio_task:
      report_format = st.selectbox(
          "ជ្រើសរើសទម្រង់របាយការណ៍៖",
          [
              "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ",
              "🏛️ របាយការណ៍ចុះមូលដ្ឋាន",
              "🛠️ របាយការណ៍បច្ចេកទេស & ដោះស្រាយបញ្ហា",
              "📝 កំណត់ហេតុអង្គប្រជុំ (Minutes of Meeting)",
              "⚡ សង្ខេបបន្ទាន់ (Brief ខ្លីខ្លឹម)",
          ],
      )

    custom_notes = st.text_input(
        "ចំណាំបន្ថែម ឬការណែនាំពិសេស (បើមាន)៖",
        placeholder="ឧទាហរណ៍៖ សំឡេងដើមជាភាសាអង់គ្លេស សូមបកប្រែជាខ្មែរ...",
    )

    btn_audio = st.button("🚀 ដំណើរការបម្លែងសំឡេង", key="btn_run_voice")

  with col_right:
    st.markdown(
        """
        <div class="card-top">
            <div class="card-header-title">📋 លទ្ធផលអត្ថបទ / របាយការណ៍</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if audio_file and btn_audio:
      with st.spinner("AI កំពុងស្ដាប់ និងបម្លែងសំឡេង..."):
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

          if "អត្ថបទសុទ្ធ" in audio_task:
            prompt = f"""
                        សូមស្ដាប់សំឡេងនេះ (ទោះជាភាសាអ្វីក៏ដោយ) ហើយបម្លែងទៅជាអត្ថបទសរសេរជា '{target_audio_lang}' ឱ្យបានសុក្រឹត និងត្រឹមត្រូវបំផុតតាមពាក្យសម្ដីដើម។
                        ចំណាំបន្ថែមពីអ្នកប្រើប្រាស់៖ {custom_notes if custom_notes else 'គ្មាន'}
                        """
          else:
            prompt = f"""
                        សូមស្ដាប់សំឡេងនេះ (ទោះជាភាសាអ្វីក៏ដោយ) ហើយរៀបចំចេញជា '{report_format}' ជា '{target_audio_lang}' ឱ្យមានទម្រង់ច្បាស់លាស់ ស្អាតបាត និងផ្លូវការ។
                        ចំណាំបន្ថែមពីអ្នកប្រើប្រាស់៖ {custom_notes if custom_notes else 'គ្មាន'}
                        
                        រចនាសម្ព័ន្ធរបាយការណ៍៖
                        - ចំណងជើង
                        - ព័ត៌មានទូទៅ
                        - ខ្លឹមសារលម្អិត
                        - លទ្ធផលសម្រេចបាន
                        - បញ្ហាប្រឈម & ដំណោះស្រាយ/ទិសដៅបន្ត
                        """

          resp = client.models.generate_content(
              model="gemini-2.5-flash", contents=[uploaded, prompt]
          )
          client.files.delete(name=uploaded.name)

          st.success("✅ ដំណើរការបម្លែងជោគជ័យ!")
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
                <div class="empty-icon">🎙️</div>
                <div class="empty-title">រង់ចាំការបញ្ចូលសំឡេង</div>
                <div class="empty-desc">អ្នកអាចបញ្ចូលសំឡេងជាភាសាខ្មែរ ឬភាសាដទៃ (អង់គ្លេស ចិន ថៃ...) ដើម្បីឱ្យ AI បម្លែងជាអក្សរខ្មែរ ឬបម្លែងពីខ្មែរទៅភាសាដទៃបានភ្លាមៗ។</div>
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
    doc_lang = st.selectbox(
        "ភាសានៃការសម្រាយ៖", LANG_OPTIONS, index=0, key="sel_doc_lang"
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
          p = f"សូមសម្រាយខ្លឹមសារនេះជា '{doc_lang}' តាមទម្រង់ '{doc_style}' ដោយប្រើពាក្យបច្ចេកទេសត្រឹមត្រូវ៖"
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

# ----------------- TAB 3: UNIVERSAL TRANSLATION (គ្រប់ភាសា) -----------------
with tab3:
  st.markdown("### 🌐 ប្រព័ន្ធបកប្រែពហុភាសា (Universal Translator)")
  st.caption("បកប្រែឆ្លាស់គ្នាគ្រប់ភាសាលើពិភពលោក (ខ្មែរ ⇄ គ្រប់ភាសា)")

  t_col1, t_col2 = st.columns([1, 1], gap="medium")
  with t_col1:
    source_lang = st.selectbox(
        "ភាសាដើម (Source Language)៖",
        ["ស្វែងរកដោយស្វ័យប្រវត្តិ (Auto Detect)"] + LANG_OPTIONS,
        index=0,
    )
  with t_col2:
    target_trans_lang = st.selectbox(
        "បកប្រែទៅជាភាសា (Target Language)៖",
        LANG_OPTIONS,
        index=0,  # default ខ្មែរ
        key="target_lang_select",
    )

  raw_text = st.text_area(
      "បញ្ចូលអត្ថបទដែលត្រូវបកប្រែនៅទីនេះ៖",
      height=180,
      placeholder=(
          "វាយ ឬ Paste អត្ថបទជាភាសាខ្មែរ អង់គ្លេស ចិន ថៃ"
          " ឬភាសាផ្សេងៗទៀតនៅទីនេះ..."
      ),
  )

  if st.button("🚀 បកប្រែឥឡូវនេះ", key="btn_trans_action") and raw_text:
    with st.spinner("AI កំពុងបកប្រែ..."):
      prompt_trans = f"""
            អ្នកគឺជាអ្នកបកប្រែជំនាញជាន់ខ្ពស់។
            សូមបកប្រែអត្ថបទខាងក្រោមពី '{source_lang}' ទៅជា '{target_trans_lang}' ដោយរក្សាអត្ថន័យដើមឱ្យបានសុក្រឹត ក្បួនវេយ្យាករណ៍ និងពាក្យបច្ចេកទេសឱ្យត្រឹមត្រូវតាមកម្រិតផ្លូវការ៖
            
            {raw_text}
            """
      res = client.models.generate_content(
          model="gemini-2.5-flash", contents=prompt_trans
      )
      st.markdown("#### 📝 លទ្ធផលបកប្រែ៖")
      st.success("✅ បកប្រែរួចរាល់!")
      st.markdown(res.text)

# ----------------- TAB 4: CHAT ASSISTANT -----------------
with tab4:
  st.markdown("### 💬 ជំនួយការឆ្លាតវៃ AI Chat")
  q = st.text_area(
      "សួរសំណួរ ពិគ្រោះយោបល់ ឬឱ្យជួយព្រាងលិខិតផ្លូវការផ្សេងៗ៖", height=130
  )
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
