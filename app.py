import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import streamlit as st

# កំណត់ Layout ទំព័រ
st.set_page_config(
    page_title="AI Smart Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== MODERN ULTRA UI CSS ====================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Kantumruy Pro', sans-serif !important;
    }

    /* កំណត់ពណ៌ផ្ទៃក្រោយឱ្យបែប Modern Off-White */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }

    /* Gradient Header Banner ទំនើប */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 35px 25px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
        text-align: center;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .hero-subtitle {
        font-size: 16px;
        opacity: 0.92;
        font-weight: 400;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* កែលម្អ Tabs Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        color: #64748b;
        padding: 0 20px;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #eff6ff !important;
        color: #2563eb !important;
    }

    /* ប្រអប់ Card សម្រាប់ផ្នែកខាងឆ្វេង និងស្ដាំ */
    .content-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .card-header {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 10px;
    }

    /* ប៊ូតុងចុចទំនើប */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        border: none;
        width: 100%;
        margin-top: 15px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }

    /* កែសម្រួលកន្លែង Upload មិនឱ្យជាន់អក្សរ */
    [data-testid="stFileUploader"] {
        background: #f8fafc;
        border: 2px dashed #cbd5e1;
        border-radius: 14px;
        padding: 15px;
    }

    /* ប្រអប់លទ្ធផល */
    .result-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ផ្ទៀងផ្ទាត់ API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
  st.warning("⚠️ សូមកំណត់ GEMINI_API_KEY នៅក្នុង Streamlit Secrets ជាមុនសិន!")
  st.stop()

client = genai.Client(api_key=api_key)

# ==================== BANNER ====================
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚡ ប្រព័ន្ធជំនួយការឆ្លាតវៃ AI Workspace</div>
        <div class="hero-subtitle">ជំនួយការរដ្ឋបាល និងបច្ចេកទេសកម្រិតខ្ពស់ សម្រួលការងារបម្លែងសំឡេង សម្រាយឯកសារ និងវិភាគទិន្នន័យ</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ សំឡេង ➜ របាយការណ៍",
    "📄 សម្រាយ & សង្ខេបឯកសារ",
    "🖼️ អានក្រដាស Scan / OCR",
    "💬 AI ពិគ្រោះ & ព្រាងលិខិត",
])

# ----------------- TAB 1: VOICE -----------------
with tab1:
  col_left, col_right = st.columns([1, 1], gap="large")
  with col_left:
    st.markdown(
        '<div class="content-card"><div class="card-header">🎙️ បញ្ចូលសំឡេងការងារ</div>',
        unsafe_allow_html=True,
    )
    audio_file = st.file_uploader(
        "ជ្រើសរើស File សំឡេង (MP3, WAV, OGG, M4A)៖",
        type=["mp3", "wav", "ogg", "m4a"],
        key="aud_up",
    )
    report_type = st.selectbox(
        "ជ្រើសរើសទម្រង់របាយការណ៍៖",
        [
            "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ",
            "🏛️ របាយការណ៍ចុះមូលដ្ឋាន",
            "🛠️ របាយការណ៍បច្ចេកទេស & ដោះស្រាយបញ្ហា",
            "📝 កំណត់ហេតុអង្គប្រជុំ (Minutes of Meeting)",
        ],
    )
    btn_audio = st.button("🚀 រៀបចំរបាយការណ៍ស្វ័យប្រវត្ត", key="btn_run_audio")
    st.markdown("</div>", unsafe_allow_html=True)

  with col_right:
    st.markdown(
        '<div class="content-card"><div class="card-header">📋'
        ' លទ្ធផលរបាយការណ៍សម្រេច</div>',
        unsafe_allow_html=True,
    )
    if audio_file and btn_audio:
      with st.spinner("AI កំពុងស្ដាប់ និងរៀបចំជារបាយការណ៍ផ្លូវការ..."):
        ext = audio_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{ext}"
        ) as tmp:
          tmp.write(audio_file.read())
          tmp_path = tmp.name

        try:
          uploaded = client.files.upload(
              file=tmp_path, mime_type=audio_file.type
          )
          prompt = f"""
                    សូមស្ដាប់សំឡេងនេះ ហើយរៀបចំចេញជា {report_type} ជាភាសាខ្មែរផ្លូវការ ស្អាតបាត។
                    បែងចែកជាចំណុចច្បាស់ៗ៖
                    ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីតាំង សមាសភាព)
                    ២. សកម្មភាពស្នូល
                    ៣. លទ្ធផលសម្រេចបាន
                    ៤. បញ្ហាប្រឈម & ដំណោះស្រាយ
                    ៥. ផែនការអនុវត្តបន្ត
                    """
          resp = client.models.generate_content(
              model="gemini-2.5-flash", contents=[uploaded, prompt]
          )
          client.files.delete(name=uploaded.name)
          st.success("✅ រៀបចំរបាយការណ៍ជោគជ័យ!")
          st.markdown(
              f'<div class="result-box">{resp.text}</div>',
              unsafe_allow_html=True,
          )
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
    else:
      st.info(
          "👉 សូមជ្រើសរើស File សំឡេងនៅប្រអប់ខាងឆ្វេង រួចចុចប៊ូតុងដើម្បីមើលលទ្ធផល"
      )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 2: DOCUMENTS -----------------
with tab2:
  col_doc1, col_doc2 = st.columns([1, 1], gap="large")
  with col_doc1:
    st.markdown(
        '<div class="content-card"><div class="card-header">📄'
        " ជ្រើសរើសឯកសារត្រូវសម្រាយ</div>",
        unsafe_allow_html=True,
    )
    doc_file = st.file_uploader(
        "បញ្ចូល File (PDF, Word, PowerPoint)៖",
        type=["pdf", "docx", "pptx"],
        key="doc_up",
    )
    doc_mode = st.radio(
        "កម្រិតនៃការសម្រាយ៖",
        ["សង្ខេបចំណុចស្នូល ៣ ទៅ ៥ ចំណុច", "សម្រាយខ្លឹមសារលម្អិតតាមជំពូក"],
        horizontal=True,
    )
    btn_doc = st.button("🚀 សម្រាយឯកសារឥឡូវនេះ", key="btn_run_doc")
    st.markdown("</div>", unsafe_allow_html=True)

  with col_doc2:
    st.markdown(
        '<div class="content-card"><div class="card-header">📑'
        " ខ្លឹមសារសង្ខេប និងការសម្រាយ</div>",
        unsafe_allow_html=True,
    )
    if doc_file and btn_doc:
      with st.spinner("AI កំពុងអាន និងសម្រាយខ្លឹមសារ..."):
        ext = doc_file.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
          tmp.write(doc_file.read())
          tmp_path = tmp.name

        try:
          p_doc = (
              "សូមសម្រាយខ្លឹមសារនេះជាភាសាខ្មែរតាមទម្រង់ '"
              + str(doc_mode)
              + "' ដោយប្រើភាសាបច្ចេកទេសត្រឹមត្រូវ និងងាយយល់។"
          )
          if ext == "pdf":
            up = client.files.upload(file=tmp_path, mime_type="application/pdf")
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=[up, p_doc]
            )
            client.files.delete(name=up.name)
            result_text = res.text
          elif ext == "docx":
            d = docx.Document(tmp_path)
            txt = "\n".join([p.text for p in d.paragraphs if p.text.strip()])
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{p_doc}\n\n{txt}"
            )
            result_text = res.text
          elif ext == "pptx":
            prs = Presentation(tmp_path)
            txt = "\n".join([
                p.text
                for s in prs.slides
                for sh in s.shapes
                if sh.has_text_frame
                for p in sh.text_frame.paragraphs
                if p.text.strip()
            ])
            res = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{p_doc}\n\n{txt}"
            )
            result_text = res.text

          st.success("✅ សម្រាយខ្លឹមសាររួចរាល់!")
          st.markdown(
              f'<div class="result-box">{result_text}</div>',
              unsafe_allow_html=True,
          )
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
    else:
      st.info("👉 បញ្ចូលឯកសារដើម្បីឱ្យ AI ជួយសម្រាយជាចំណុចៗងាយយល់")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 3: IMAGE OCR -----------------
with tab3:
  col_img1, col_img2 = st.columns([1, 1], gap="large")
  with col_img1:
    st.markdown(
        '<div class="content-card"><div class="card-header">🖼️ រូបភាព ឬក្រដាស'
        " Scan</div>",
        unsafe_allow_html=True,
    )
    img_file = st.file_uploader(
        "បញ្ចូលរូបភាព (JPG, PNG)៖", type=["jpg", "jpeg", "png"], key="img_up"
    )
    img_action = st.selectbox("តម្រូវការអនុវត្ត៖", [
        "ស្រង់អក្សរចេញទាំងអស់ (Extract Text / OCR)",
        "បកប្រែខ្លឹមសារក្នុងរូបភាពជាភាសាខ្មែរ",
        "វិភាគទិន្នន័យ ឬតារាងក្នុងរូបភាព",
    ])
    btn_img = st.button("🚀 ដំណើរការរូបភាព", key="btn_run_img")
    st.markdown("</div>", unsafe_allow_html=True)

  with col_img2:
    st.markdown(
        '<div class="content-card"><div class="card-header">📝'
        " លទ្ធផលស្រង់ចេញ</div>",
        unsafe_allow_html=True,
    )
    if img_file and btn_img:
      with st.spinner("AI កំពុងវិភាគរូបភាព..."):
        ext = img_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
          tmp.write(img_file.read())
          tmp_path = tmp.name

        try:
          up = client.files.upload(file=tmp_path, mime_type=img_file.type)
          res = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=[up, f"ធ្វើសកម្មភាព៖ {img_action} ជាភាសាខ្មែរ"],
          )
          client.files.delete(name=up.name)
          st.success("✅ ដំណើរការរួចរាល់!")
          st.markdown(
              f'<div class="result-box">{res.text}</div>',
              unsafe_allow_html=True,
          )
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
    else:
      st.info("👉 បញ្ចូលរូបភាព Scan ឬឯកសារថតដើម្បីស្រង់ទិន្នន័យ")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 4: CHAT / DRAFT -----------------
with tab4:
  st.markdown(
      '<div class="content-card"><div class="card-header">💬'
      " ជំនួយការព្រាងលិខិត & ពិគ្រោះយោបល់</div>",
      unsafe_allow_html=True,
  )
  user_query = st.text_area(
      "សរសេរប្រធានបទ ឬសំណួររបស់អ្នកនៅទីនេះ (ឧ. សេចក្តីជូនដំណឹង, លិខិតផ្លូវការ,"
      " ដំណោះស្រាយបច្ចេកទេស)៖",
      height=120,
      placeholder="ឧទាហរណ៍៖ ជួយព្រាងលិខិតអញ្ជើញចូលរួមប្រជុំស្ដីពី...",
  )
  if st.button("🚀 បង្កើតខ្លឹមសារ", key="btn_run_chat") and user_query:
    with st.spinner("AI កំពុងរៀបចំខ្លឹមសារ..."):
      res = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=(
              "អ្នកគឺជាជំនួយការបច្ចេកទេស និងរដ្ឋបាលជាន់ខ្ពស់។"
              f" សូមឆ្លើយតបជាភាសាខ្មែរផ្លូវការ សុភាព និងមានលំដាប់លំដោយ៖ {user_query}"
          ),
      )
      st.markdown(
          f'<div class="result-box">{res.text}</div>', unsafe_allow_html=True
      )
  st.markdown("</div>", unsafe_allow_html=True)
