import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import pypdf
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

    /* Container Header */
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

    /* Empty Placeholder Box */
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
MODEL_NAME = "gemini-2.0-flash"

LANG_OPTIONS = [
    "ភាសាខ្មែរ (Khmer)",
    "English",
    "中文 (Chinese)",
    "ภาษาไทย (Thai)",
    "Tiếng Việt (Vietnamese)",
    "Français (French)",
    "日本語 (Japanese)",
    "한국어 (Korean)",
    "Español (Spanish)",
    "Deutsch (German)",
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
            Gemini 2.0 Flash (Online & High-Speed)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================== TABS BAR ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ សំឡេង ➜ របាយការណ៍/អក្សរ",
    "📄 សម្រាយ & សង្ខេបឯកសារ",
    "🌐 បកប្រែភាសាការងារ (Universal)",
    "💬 ជំនួយការឆ្លាតវៃ (AI Chat)",
])

# ----------------- TAB 1: VOICE TO REPORT & TEXT -----------------
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="card-top">
                <div class="card-header-title">🎙️ បម្លែងសំឡេងជារបាយការណ៍ & អក្សរ</div>
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

        audio_mode = st.radio(
            "តម្រូវការបម្លែង៖",
            ["📊 រៀបចំជារបាយការណ៍ការងារផ្លូវការ", "📝 បម្លែងជាអត្ថបទសុទ្ធ (Transcribe)"],
            horizontal=True,
        )

        target_lang = st.selectbox(
            "ភាសាលទ្ធផលដែលចង់បាន (បម្លែង/បកប្រែចេញពីសំឡេង)៖",
            LANG_OPTIONS,
            index=0,
        )

        report_type = "general"
        if "របាយការណ៍" in audio_mode:
            report_type = st.selectbox(
                "ជ្រើសរើសទម្រង់របាយការណ៍ដែលត្រូវការ៖",
                [
                    "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ",
                    "🏛️ របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន",
                    "📝 កំណត់ហេតុអង្គប្រជុំផ្លូវការ",
                    "⚡ របាយការណ៍សង្ខេបបន្ទាន់ (Executive Brief)",
                ],
            )

        custom_instructions = st.text_input(
            "ចំណាំបន្ថែម ឬការណែនាំពិសេស (បើមាន)៖",
            placeholder="ឧទាហរណ៍៖ សំឡេងដើមជាភាសាអង់គ្លេស សូមសង្កត់ធ្ងន់លើកាលបរិច្ឆេទ...",
        )

        btn_audio = st.button("🚀 រៀបចំរបាយការណ៍ដោយ AI", key="btn_run_voice")

    with col_right:
        st.markdown(
            """
            <div class="card-top">
                <div class="card-header-title">📋 លទ្ធផលសម្រេច</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if audio_file and btn_audio:
            with st.spinner("AI កំពុងស្ដាប់ និងដំណើរការរៀបចំ..."):
                ext = audio_file.name.split(".")[-1] if hasattr(audio_file, "name") else "wav"
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
                    tmp.write(audio_file.read())
                    tmp_path = tmp.name

                try:
                    mime = audio_file.type if hasattr(audio_file, "type") else f"audio/{ext}"
                    uploaded = client.files.upload(file=tmp_path, mime_type=mime)

                    if "អត្ថបទសុទ្ធ" in audio_mode:
                        prompt = f"""
                        សូមស្ដាប់សំឡេងនេះ (ទោះជាភាសាអ្វីក៏ដោយ) ហើយបម្លែងទៅជាអត្ថបទសរសេរជា '{target_lang}' ឱ្យបានសុក្រឹត និងត្រឹមត្រូវបំផុតតាមពាក្យសម្ដីដើម។
                        ចំណាំបន្ថែមពីអ្នកប្រើប្រាស់៖ {custom_instructions if custom_instructions else 'គ្មាន'}
                        """
                    else:
                        template_prompts = {
                            "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ": """
                            សូមរៀបចំជា «របាយការណ៍វឌ្ឍនភាពការងារទូទៅ» ជាភាសា {target_lang} តាមទម្រង់៖
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            📊 របាយការណ៍វឌ្ឍនភាពការងារ
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            🗓 ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីកន្លែង សមាសភាពចូលរួម/អ្នកទទួលបន្ទុក)
                            ⚡ ២. សកម្មភាព និងការងារសំខាន់ៗដែលបានអនុវត្ត
                            🏆 ៣. លទ្ធផលសម្រេចបាន (ចំណុចលេចធ្លោ និងបរិមាណការងារ)
                            ⚠️ ៤. បញ្ហាប្រឈម និងឧបសគ្គដែលបានជួបប្រទះ
                            🎯 ៥. ដំណោះស្រាយ និងទិសដៅអនុវត្តបន្ត
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            """,
                            "🏛️ របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន": """
                            សូមរៀបចំជា «របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន» ជាភាសា {target_lang} តាមទម្រង់៖
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            🏛 របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            📌 ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីតាំងចុះមូលដ្ឋាន ក្រុមការងារ និងសមាសភាពចូលរួម)
                            🎯 ២. គោលបំណង និងសកម្មភាពស្នូលនៃការចុះជួប
                            🤝 ៣. សភាពការណ៍ទូទៅ និងមតិសាទរ/មនោសញ្ចេតនាប្រជាពលរដ្ឋ
                            🗣 ៤. មតិសំណូមពរ កង្វល់ និងបញ្ហាប្រឈមជាក់ស្តែង
                            🧭 ៥. វិធានការដោះស្រាយចំពោះមុខ និងសំណើទិសដៅបន្ត
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            """,
                            "📝 កំណត់ហេតុអង្គប្រជុំផ្លូវការ": """
                            សូមរៀបចំជា «កំណត់ហេតុអង្គប្រជុំផ្លូវការ» ជាភាសា {target_lang} តាមទម្រង់៖
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            📝 កំណត់ហេតុអង្គប្រជុំ
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            🕒 ១. កាលបរិច្ឆេទ ពេលវេលា ទីកន្លែង និងអធិបតីភាពដឹកនាំកិច្ចប្រជុំ
                            👥 ២. សមាសភាពចូលរួម និងអវត្តមាន
                            📋 ៣. របៀបវារៈនៃកិច្ចប្រជុំ
                            💬 ៤. ខ្លឹមសារពិភាក្សា និងមតិយោបល់សំខាន់ៗ
                            ⚖️ ៥. សេចក្តីសន្និដ្ឋាន និងសេចក្តីសម្រេចរបស់អង្គប្រជុំ
                            📌 ៦. ការចាត់តាំងការងារ និងកាលបរិច្ឆេទតាមដានបន្ទាប់
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            """,
                            "⚡ របាយការណ៍សង្ខេបបន្ទាន់ (Executive Brief)": """
                            សូមរៀបចំជា «របាយការណ៍សង្ខេបបន្ទាន់ (Executive Brief)» ជាភាសា {target_lang} ខ្លី ខ្លឹម ចំគោលដៅ៖
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            ⚡ របាយការណ៍សង្ខេបបន្ទាន់ (EXECUTIVE BRIEF)
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            🎯 សេចក្តីសង្ខេបខ្លឹមសារស្នូល (១-២ កថាខណ្ឌខ្លី)
                            🔥 ចំណុចគន្លឹះសំខាន់ៗត្រូវដឹងភ្លាមៗ (Bullet Points)
                            ⚠️ ហានិភ័យ ឬបញ្ហាប្រឈមបន្ទាន់
                            🚀 សកម្មភាពដែលត្រូវចាត់ចែងភ្លាមៗ (Action Items & Person in charge)
                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            """,
                        }
                        prompt = template_prompts.get(report_type, template_prompts["📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ"])
                        prompt = prompt.replace("{target_lang}", target_lang)
                        if custom_instructions:
                            prompt += f"\n\nចំណាំបន្ថែម៖ {custom_instructions}"

                    resp = client.models.generate_content(
                        model=MODEL_NAME, contents=[uploaded, prompt]
                    )
                    client.files.delete(name=uploaded.name)

                    st.success("✅ ដំណើរការជោគជ័យ!")
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
                    <div class="empty-title">រង់ចាំការបម្លែងសំឡេង</div>
                    <div class="empty-desc">សូមបញ្ចូល File សំឡេង ឬចុចថតសំឡេង រួចចុចប៊ូតុងខាងឆ្វេង ដើម្បីឱ្យ AI រៀបចំរបាយការណ៍ ឬបម្លែងជាអក្សរជូនលោកអ្នក។</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------- TAB 2: DOCUMENTS -----------------
with tab2:
    c_doc1, c_doc2 = st.columns([1, 1], gap="large")
    with c_doc1:
        st.markdown("### 📄 ជ្រើសរើសឯកសារត្រូវសម្រាយ")
        doc_file = st.file_uploader(
            "បញ្ចូល File ឯកសារ (PDF, Word, PPT)៖", type=["pdf", "docx", "pptx"]
        )
        doc_mode = st.radio(
            "ទម្រង់សម្រាយ៖",
            [
                "📌 ចំណុចស្នូលគន្លឹះ ៣-៥ ចំណុច (Key Takeaways)",
                "📑 វិភាគ និងសម្រាយលម្អិតតាមជំពូក",
                "📋 ស្រង់បញ្ជីការងារត្រូវអនុវត្ត (Action Items)",
            ],
        )
        doc_target_lang = st.selectbox(
            "ភាសានៃការសម្រាយ៖", LANG_OPTIONS, index=0, key="doc_lang_select"
        )
        btn_doc = st.button("🚀 សម្រាយឯកសារឥឡូវនេះ", key="btn_doc_action")

    with c_doc2:
        st.markdown("### 📑 ខ្លឹមសារសម្រាយ")
        if doc_file and btn_doc:
            with st.spinner("AI កំពុងអាន និងសម្រាយខ្លឹមសារ..."):
                ext = doc_file.name.split(".")[-1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
                    tmp.write(doc_file.read())
                    tmp_path = tmp.name

                try:
                    p = f"សូមអាន និងសម្រាយខ្លឹមសារឯកសារនេះជា '{doc_target_lang}' តាមទម្រង់ '{doc_mode}' ដោយប្រើពាក្យបច្ចេកទេសត្រឹមត្រូវតាមក្បួនខ្នាតរដ្ឋបាលផ្លូវការ។"
                    if ext == "pdf":
                        up = client.files.upload(file=tmp_path, mime_type="application/pdf")
                        res = client.models.generate_content(model=MODEL_NAME, contents=[up, p])
                        client.files.delete(name=up.name)
                        st.markdown(res.text)
                    elif ext == "docx":
                        d = docx.Document(tmp_path)
                        txt = "\n".join([pr.text for pr in d.paragraphs if pr.text.strip()])
                        res = client.models.generate_content(model=MODEL_NAME, contents=f"{p}\n\n{txt}")
                        st.markdown(res.text)
                    elif ext == "pptx":
                        prs = Presentation(tmp_path)
                        txt = "\n".join([pr.text for s in prs.slides for sh in s.shapes if sh.has_text_frame for pr in sh.text_frame.paragraphs if pr.text.strip()])
                        res = client.models.generate_content(model=MODEL_NAME, contents=f"{p}\n\n{txt}")
                        st.markdown(res.text)
                except Exception as e:
                    st.error(f"កំហុសក្នុងការសម្រាយឯកសារ៖ {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
        else:
            st.info("👈 បញ្ចូលឯកសារដើម្បីឱ្យ AI ជួយសម្រាយ")

# ----------------- TAB 3: UNIVERSAL TRANSLATION -----------------
with tab3:
    st.markdown("### 🌐 ប្រព័ន្ធបកប្រែភាសាការងារផ្លូវការ (Universal Translator)")
    st.caption("បកប្រែឆ្លាស់គ្នាគ្រប់ភាសាលើពិភពលោក (ខ្មែរ ⇄ គ្រប់ភាសា) ប្រកបដោយកម្រិតរដ្ឋបាលខ្ពស់")

    t_col1, t_col2 = st.columns([1, 1], gap="medium")
    with t_col1:
        source_lang = st.selectbox(
            "ភាសាដើម (Source Language)៖",
            ["ស្វែងរកដោយស្វ័យប្រវត្តិ (Auto-Detect)"] + LANG_OPTIONS,
            index=0,
        )
    with t_col2:
        target_trans_lang = st.selectbox(
            "បកប្រែទៅជាភាសា (Target Language)៖",
            LANG_OPTIONS,
            index=0,
            key="target_lang_select_box",
        )

    raw_text = st.text_area(
        "បញ្ចូលអត្ថបទដែលត្រូវបកប្រែនៅទីនេះ៖",
        height=180,
        placeholder="វាយ ឬ Paste អត្ថបទជាភាសាខ្មែរ អង់គ្លេស ចិន ថៃ ឬភាសាផ្សេងៗទៀតនៅទីនេះ...",
    )

    if st.button("🚀 បកប្រែឥឡូវនេះ", key="btn_trans_action") and raw_text:
        with st.spinner("AI កំពុងបកប្រែ..."):
            try:
                prompt_trans = f"""
                អ្នកគឺជាអ្នកបកប្រែភាសាអាជីពកម្រិតខ្ពស់ដែលមានជំនាញជ្រៅជ្រះទាំងភាសាខ្មែរ និងភាសាអន្តរជាតិ។
                សូមបកប្រែអត្ថបទខាងក្រោមពី '{source_lang}' ទៅជា '{target_trans_lang}'។
                លក្ខខណ្ឌតម្រូវ៖
                - រចនាបថបកប្រែ៖ ផ្លូវការ រដ្ឋបាល សុភាពរាបសារ និងត្រឹមត្រូវតាមក្បួនខ្នាតវេយ្យាករណ៍ខ្ពស់បំផុត
                - រក្សាទម្រង់អត្ថបទដើម (កថាខណ្ឌ ចំណុច bullet points លេខរៀង)
                - បកប្រែឱ្យមានអត្ថន័យជ្រាលជ្រៅ មិនមែនបកប្រែពាក្យទល់ពាក្យនោះទេ
                
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                អត្ថបទដើម៖
                {raw_text}
                """
                res = client.models.generate_content(model=MODEL_NAME, contents=prompt_trans)
                st.markdown("#### 📝 លទ្ធផលបកប្រែ៖")
                st.success("✅ បកប្រែរួចរាល់!")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"កំហុសក្នុងការបកប្រែ៖ {e}")

# ----------------- TAB 4: CHAT ASSISTANT -----------------
with tab4:
    st.markdown("### 💬 ជំនួយការឆ្លាតវៃ AI Work Chat Assistant")
    st.caption("ជួយព្រាងលិខិតផ្លូវការ លិខិតរដ្ឋបាល កែសម្រួលអក្ខរាវិរុទ្ធ និងប្រឹក្សាការងារ")

    q = st.text_area(
        "បញ្ចូលសំណើ ឬសេចក្តីព្រាងរបស់អ្នកនៅទីនេះ៖",
        height=130,
        placeholder="ឧទាហរណ៍៖ ព្រាងលិខិតអញ្ជើញចូលរួមប្រជុំ, លិខិតបុណ្យសព, ឬដំណោះស្រាយបច្ចេកទេស...",
    )
    if st.button("🚀 ឆ្លើយតប / រៀបចំខ្លឹមសារ", key="btn_chat_action") and q:
        with st.spinner("AI កំពុងរៀបចំខ្លឹមសារ..."):
            try:
                system_instruction = """
                អ្នកគឺជា «KhemaraAI WorkSuite Assistant» ជំនួយការឆ្លាតវៃផ្នែកការងារ ការិយាល័យ និងរដ្ឋបាល។
                អ្នកមានសមត្ថភាពខ្ពស់ក្នុងការ៖
                ១. ជួយព្រាងលិខិតផ្លូវការ លិខិតអញ្ជើញ លិខិតថ្លែងអំណរគុណ និងលិខិតរដ្ឋបាល
                ២. កែសម្រួលអក្ខរាវិរុទ្ធ វេយ្យាករណ៍ និងពាក្យពេចន៍ភាសាខ្មែរឱ្យត្រឹមត្រូវ និងទាក់ទាញ
                ៣. ជួយរៀបចំរបៀបវារៈ គម្រោងការងារ ផែនការសកម្មភាព និងសំណើផ្សេងៗ
                ៤. ផ្តល់យោបល់ និងដោះស្រាយបញ្ហាការងារប្រកបដោយវិជ្ជាជីវៈ
                ៥. ឆ្លើយតបដោយសុភាពរាបសារ រៀបចំជាទម្រង់ Markdown ច្បាស់លាស់ ងាយស្រួលអាន។
                """
                res = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=f"System: {system_instruction}\n\nUser: {q}",
                )
                st.markdown("#### 📄 ខ្លឹមសារដែលបានរៀបចំ៖")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"កំហុសក្នុងការបង្កើតខ្លឹមសារ៖ {e}")
