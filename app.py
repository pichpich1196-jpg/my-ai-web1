import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import streamlit as st

st.set_page_config(
    page_title="AI Smart Assistant - ប្រព័ន្ធជំនួយការឆ្លាតវៃ",
    page_icon="⚡",
    layout="wide",
)

# ⚠️ ដាក់ GEMINI API KEY របស់អ្នកនៅទីនេះ
# ប្រើប្រព័ន្ធ Secrets របស់ Streamlit ដើម្បីសុវត្ថិភាព
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

st.title("⚡ ប្រព័ន្ធជំនួយការឆ្លាតវៃ AI (All-in-One)")
st.caption(
    "ប្រព័ន្ធគ្រប់គ្រងការងារឆ្លាតវៃ៖ ធ្វើរបាយការណ៍ សម្រាយឯកសារ អានរូបភាព និងជជែកពិគ្រោះយោបល់"
)

# បង្កើត ៥ ផ្ទាំងការងារ
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎙️ សំឡេង ➜ របាយការណ៍",
    "📄 សម្រាយឯកសារ",
    "🖼️ អានរូបភាព/Scan (OCR)",
    "💬 ជជែកសួរឆ្លើយ AI",
    "🌐 បកប្រែឯកសារ",
])

# ==================== TAB 1: សំឡេង ====================
with tab1:
  st.subheader("បម្លែងសំឡេងទៅជារបាយការណ៍ការងារ")
  col1, col2 = st.columns([1, 1])
  with col1:
    audio_file = st.file_uploader(
        "បញ្ចូល File សំឡេង (MP3, WAV, OGG, M4A)៖",
        type=["mp3", "wav", "ogg", "m4a"],
    )
    report_type = st.selectbox("ជ្រើសរើសទម្រង់របាយការណ៍៖", [
        "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ",
        "🏛️ របាយការណ៍ចុះមូលដ្ឋាន",
        "🛠️ របាយការណ៍បច្ចេកទេស & ដោះស្រាយបញ្ហា",
        "📝 កំណត់ហេតុអង្គប្រជុំ (Minutes of Meeting)",
    ])
    btn_audio = st.button("🚀 រៀបចំរបាយការណ៍", key="btn_aud")

  with col2:
    if audio_file and btn_audio:
      with st.spinner("Gemini កំពុងស្ដាប់ និងរៀបចំជារបាយការណ៍..."):
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
                    សូមស្ដាប់សំឡេងនេះ ហើយរៀបចំចេញជា {report_type} ជាភាសាខ្មែរឱ្យមានទម្រង់ច្បាស់លាស់ ស្អាតបាត និងផ្លូវការ។
                    បែងចែកជាកថាខណ្ឌ៖
                    ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីតាំង សមាសភាពចូលរួម)
                    ២. ខ្លឹមសារលម្អិត និងសកម្មភាពស្នូល
                    ៣. លទ្ធផលសម្រេចបាន
                    ៤. បញ្ហាប្រឈម និងសំណូមពរ
                    ៥. ផែនការអនុវត្តបន្ត
                    """
          resp = client.models.generate_content(
              model="gemini-2.5-flash", contents=[uploaded, prompt]
          )
          client.files.delete(name=uploaded.name)
          st.success("✅ រៀបចំរួចរាល់!")
          st.markdown(resp.text)
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)

# ==================== TAB 2: ឯកសារ ====================
with tab2:
  st.subheader("សម្រាយ និងសង្ខេបឯកសារចម្បងៗ")
  doc_file = st.file_uploader(
      "បញ្ចូល File ឯកសារ (PDF, Word, PPT)៖", type=["pdf", "docx", "pptx"]
  )
  doc_detail = st.radio(
      "ទម្រង់សម្រាយ៖",
      ["សង្ខេបខ្លីខ្លឹម ៣-៥ ចំណុច", "សម្រាយលម្អិតតាមជំពូកនីមួយៗ"],
      horizontal=True,
  )

  if doc_file and st.button("🚀 សម្រាយឯកសារ", key="btn_doc"):
    with st.spinner("Gemini កំពុងអានឯកសារ..."):
      ext = doc_file.name.split(".")[-1].lower()
      with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(doc_file.read())
        tmp_path = tmp.name

      try:
        p_doc = f"សូមសម្រាយខ្លឹមសារនេះជាភាសាខ្មែរតាមទម្រង់ '{doc_detail}' ដោយប្រើពាក្យបច្ចេកទេសត្រឹមត្រូវ និងងាយយល់។"
        if ext == "pdf":
          up = client.files.upload(file=tmp_path, mime_type="application/pdf")
          res = client.models.generate_content(
              model="gemini-2.5-flash", contents=[up, p_doc]
          )
          client.files.delete(name=up.name)
          st.markdown(res.text)
        elif ext == "docx":
          d = docx.Document(tmp_path)
          txt = "\n".join([p.text for p in d.paragraphs if p.text.strip()])
          res = client.models.generate_content(
              model="gemini-2.5-flash", contents=f"{p_doc}\n\n{txt}"
          )
          st.markdown(res.text)
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
          st.markdown(res.text)
      except Exception as e:
        st.error(f"កំហុស៖ {e}")
      finally:
        if os.path.exists(tmp_path):
          os.remove(tmp_path)

# ==================== TAB 3: រូបភាព OCR ====================
with tab3:
  st.subheader("ស្រង់អត្ថបទ និងបកស្រាយរូបភាព / ក្រដាស Scan")
  img_file = st.file_uploader(
      "បញ្ចូលរូបភាព (JPG, PNG)៖", type=["jpg", "jpeg", "png"]
  )
  img_action = st.selectbox("តម្រូវការ៖", [
      "ស្រង់អក្សរទាំងអស់ចេញជារូបរាងដើម (Extract Text/OCR)",
      "បកប្រែអត្ថបទក្នុងរូបភាពជាភាសាខ្មែរ",
      "វិភាគ និងសង្ខេបខ្លឹមសារក្នុងរូបភាព",
  ])

  if img_file and st.button("🚀 ដំណើរការរូបភាព", key="btn_img"):
    with st.spinner("Gemini កំពុងស្កេនរូបភាព..."):
      ext = img_file.name.split(".")[-1]
      with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(img_file.read())
        tmp_path = tmp.name

      try:
        up = client.files.upload(file=tmp_path, mime_type=img_file.type)
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[up, f"ធ្វើសកម្មភាព៖ {img_action}"],
        )
        client.files.delete(name=up.name)
        st.markdown(res.text)
      except Exception as e:
        st.error(f"កំហុស៖ {e}")
      finally:
        if os.path.exists(tmp_path):
          os.remove(tmp_path)

# ==================== TAB 4: CHAT ASSISTANT ====================
with tab4:
  st.subheader("ជំនួយការសួរឆ្លើយ & ព្រាងលិខិត")
  user_query = st.text_area(
      "បញ្ចូលសំណួរ ឬប្រធានបទដែលចង់ឱ្យ AI រៀបចំ (ឧទាហរណ៍៖ សេចក្តីជូនដំណឹង, លិខិតស្នើសុំ, ឬបញ្ហាបច្ចេកទេស)៖"
  )
  if st.button("🚀 ឆ្លើយតប", key="btn_chat") and user_query:
    with st.spinner("AI កំពុងរៀបចំចម្លើយ..."):
      res = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=(
              "អ្នកគឺជាជំនួយការបច្ចេកទេស និងរដ្ឋបាលដ៏ជំនាញ។ ឆ្លើយជាភាសាខ្មែរផ្លូវការ"
              f" និងជាក់ច្បាស់៖ {user_query}"
          ),
      )
      st.markdown(res.text)

# ==================== TAB 5: បកប្រែ ====================
with tab5:
  st.subheader("បកប្រែអត្ថបទរហ័ស")
  target_lang = st.selectbox(
      "បកប្រែទៅជាភាសា៖", ["ភាសាខ្មែរ", "ភាសាអង់គ្លេស", "ភាសាចិន"]
  )
  source_text = st.text_area(
      "បញ្ចូលអត្ថបទដើមនៅទីនេះ៖", height=150, key="txt_trans"
  )
  if st.button("🚀 បកប្រែឥឡូវនេះ", key="btn_trans") and source_text:
    with st.spinner("កំពុងបកប្រែ..."):
      res = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=(
              f"សូមបកប្រែអត្ថបទនេះទៅជា {target_lang} ឱ្យមានន័យត្រឹមត្រូវតាមក្បួនខ្នាត៖\n\n{source_text}"
          ),
      )
      st.markdown(res.text)
import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import streamlit as st

# កំណត់ Layout
st.set_page_config(
    page_title="AI Smart Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== MODERN CUSTOM CSS ====================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Kantumruy Pro', sans-serif !important;
    }

    /* Gradient Header Banner */
    .hero-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        text-align: center;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    .hero-subtitle {
        font-size: 16px;
        opacity: 0.9;
        font-weight: 300;
    }

    /* Card Box */
    .stCard {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    /* Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0062E0 0%, #1976D2 100%);
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(25, 118, 210, 0.3);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(25, 118, 210, 0.4);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        gap: 8px;
        font-weight: 600;
        font-size: 15px;
        padding: 0 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f0fe !important;
        color: #1967d2 !important;
        border-bottom: 3px solid #1967d2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ⚠️ សូមដាក់ GEMINI API KEY របស់អ្នកនៅទីនេះ
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
client = genai.Client(api_key=GEMINI_API_KEY)

# ==================== HEADER ====================
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚡ ប្រព័ន្ធជំនួយការឆ្លាតវៃ AI Workspace</div>
        <div class="hero-subtitle">ជំនួយការបច្ចេកទេស និងរដ្ឋបាលស្វ័យប្រវត្តិកម្រិតខ្ពស់ (សំឡេង ឯកសារ រូបភាព និងពិគ្រោះយោបល់)</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ សំឡេង ➜ របាយការណ៍",
    "📄 សម្រាយ & សង្ខេបឯកសារ",
    "🖼️ អានក្រដាស Scan / OCR",
    "💬 AI ពិគ្រោះ & ព្រាងលិខិត",
])

# ----------------- TAB 1: VOICE REPORT -----------------
with tab1:
  col_left, col_right = st.columns([1, 1], gap="medium")
  with col_left:
    st.markdown("### 🎙️ បញ្ចូលសំឡេង")
    audio_file = st.file_uploader(
        "ជ្រើសរើស File សំឡេង (MP3, WAV, OGG, M4A)៖",
        type=["mp3", "wav", "ogg", "m4a"],
        key="aud_up",
    )
    report_type = st.selectbox(
        "ជ្រើសរើសទម្រង់របាយការណ៍ដែលត្រូវការ៖",
        [
            "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ",
            "🏛️ របាយការណ៍ចុះមូលដ្ឋាន",
            "🛠️ របាយការណ៍បច្ចេកទេស & ដោះស្រាយបញ្ហា",
            "📝 កំណត់ហេតុអង្គប្រជុំ (Minutes of Meeting)",
        ],
    )
    btn_audio = st.button("✨ រៀបចំរបាយការណ៍ដោយ AI", key="btn_run_audio")

  with col_right:
    st.markdown("### 📋 លទ្ធផលរបាយការណ៍")
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
          st.success("✅ រៀបចំរបាយការណ៍រួចរាល់!")
          st.markdown(resp.text)
        except Exception as e:
          st.error(f"កំហុស៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
    else:
      st.info("👈 សូមជ្រើសរើស File សំឡេងនៅខាងឆ្វេង រួចចុចប៊ូតុងដើម្បីមើលលទ្ធផល")

# ----------------- TAB 2: DOCUMENT SUMMARY -----------------
with tab2:
  col_doc1, col_doc2 = st.columns([1, 1], gap="medium")
  with col_doc1:
    st.markdown("### 📄 ជ្រើសរើសឯកសារ")
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
    btn_doc = st.button("✨ សម្រាយឯកសារឥឡូវនេះ", key="btn_run_doc")

  with col_doc2:
    st.markdown("### 📑 ខ្លឹមសារសង្ខេប")
    if doc_file and btn_doc:
      with st.spinner("AI កំពុងអាន និងសម្រាយខ្លឹមសារ..."):
        ext = doc_file.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
          tmp.write(doc_file.read())
          tmp_path = tmp.name

        try:
          p_doc = f"សូមសម្រាយខ្លឹមសារនេះជាភាសាខ្មែរតាមទម្រង់ '{doc_mode}' ដោយប្រើភាសាបច្ចេកទេសត្រឹមត្រូវ និងងាយយល់។
          
