import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import streamlit as st

# កំណត់ទម្រង់ទំព័រ Web
st.set_page_config(
    page_title="AI Assistant - សម្រាយឯកសារ & របាយការណ៍",
    page_icon="📑",
    layout="centered",
)

# ⚠️ សូមដាក់ GEMINI API KEY របស់អ្នកនៅចន្លោះសញ្ញាសម្រង់ "" ខាងក្រោមនេះ៖
GEMINI_API_KEY = "AQ.Ab8RN6I39GWR3-YnsMR0R6CocmWoEEOVrwXX5ghjv6H7xYsFzQE"

client = genai.Client(api_key=GEMINI_API_KEY)

st.title("📑 ប្រព័ន្ធសម្រាយឯកសារ & របាយការណ៍ AI")
st.write(
    "ជំនួយការឆ្លាតវៃសម្រាប់បម្លែងសំឡេងជារបាយការណ៍ និងសម្រាយឯកសារ (PDF, Word, PPT) ជាភាសាខ្មែរ"
)

tab1, tab2 = st.tabs(
    ["🎙️ សំឡេង ➜ របាយការណ៍", "📄 សម្រាយឯកសារ (PDF/Word/PPT)"]
)

# --- TAB 1: សំឡេង ➜ របាយការណ៍ ---
with tab1:
  st.subheader("បម្លែងសំឡេងទៅជារបាយការណ៍ការងារ")
  audio_file = st.file_uploader(
      "បញ្ចូល File សំឡេង (MP3, WAV, OGG, M4A)៖",
      type=["mp3", "wav", "ogg", "m4a"],
  )

  report_type = st.selectbox(
      "ជ្រើសរើសទម្រង់របាយការណ៍៖",
      [
          "📊 របាយការណ៍វឌ្ឍនភាពការងារទូទៅ",
          "🏛️ របាយការណ៍ចុះមូលដ្ឋានបក្ស",
      ],
  )

  if audio_file is not None:
    st.audio(audio_file)
    if st.button("🚀 រៀបចំរបាយការណ៍ឥឡូវនេះ", key="btn_audio"):
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

          if "មូលដ្ឋាន" in report_type:
            prompt = """
                        សូមស្ដាប់សំឡេងនេះ រួចរៀបចំជា 'របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន' ជាភាសាខ្មែរតាមទម្រង់៖
                        ━━━━━━━━━━━━━━━━━━━━━━━
                        🏛 របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន
                        ━━━━━━━━━━━━━━━━━━━━━━━
                        📌 ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីតាំង ក្រុមការងារ សមាសភាពចូលរួម)
                        🎯 ២. គោលបំណង និងសកម្មភាពស្នូល
                        📊 ៣. លទ្ធផលសម្រេចបាន
                        🗣 ៤. មតិសំណូមពរ និងបញ្ហាប្រឈម
                        🧭 ៥. វិធានការដោះស្រាយ និងទិសដៅបន្ត
                        ━━━━━━━━━━━━━━━━━━━━━━━
                        """
          else:
            prompt = """
                        សូមស្ដាប់សំឡេងនេះ រួចរៀបចំជា 'របាយការណ៍វឌ្ឍនភាពការងារ' ជាភាសាខ្មែរតាមទម្រង់៖
                        ━━━━━━━━━━━━━━━━━━━━
                        📊 របាយការណ៍វឌ្ឍនភាពការងារ
                        ━━━━━━━━━━━━━━━━━━━━
                        🗓 ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីតាំង អ្នកទទួលបន្ទុក)
                        ⚡ សកម្មភាព និងលទ្ធផលសម្រេចបាន (ជាចំណុចៗ)
                        ⚠️ បញ្ហាប្រឈម និងឧបសគ្គ
                        🎯 ផែនការអនុវត្តបន្ត
                        ━━━━━━━━━━━━━━━━━━━━
                        """

          response = client.models.generate_content(
              model="gemini-2.5-flash", contents=[uploaded, prompt]
          )
          client.files.delete(name=uploaded.name)
          st.success("✅ រៀបចំរបាយការណ៍ជោគជ័យ!")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"មានបញ្ហា៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)

# --- TAB 2: សម្រាយឯកសារ ---
with tab2:
  st.subheader("សម្រាយឯកសារឱ្យខ្លី ខ្លឹម ងាយយល់")
  doc_file = st.file_uploader(
      "បញ្ចូល File ឯកសារ (PDF, DOCX, PPTX)៖",
      type=["pdf", "docx", "pptx"],
  )

  if doc_file is not None:
    if st.button("🚀 សម្រាយឯកសារ", key="btn_doc"):
      with st.spinner("Gemini កំពុងអាន និងសម្រាយខ្លឹមសារ..."):
        ext = doc_file.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{ext}"
        ) as tmp:
          tmp.write(doc_file.read())
          tmp_path = tmp.name

        try:
          prompt_doc = "សូមសម្រាយខ្លឹមសារនេះជាភាសាខ្មែរឱ្យខ្លី ខ្លឹម ងាយយល់ ត្រឹម ៣ ទៅ ៥ ចំណុច ដោយចាប់ផ្ដើមដោយ 📌 ប្រធានបទសំខាន់៖"

          if ext == "pdf":
            uploaded = client.files.upload(
                file=tmp_path, mime_type="application/pdf"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=[uploaded, prompt_doc]
            )
            client.files.delete(name=uploaded.name)
            result = response.text
          elif ext == "docx":
            d = docx.Document(tmp_path)
            text = "\n".join([p.text for p in d.paragraphs if p.text.strip()])
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{prompt_doc}\n\n{text}"
            )
            result = response.text
          elif ext == "pptx":
            prs = Presentation(tmp_path)
            text = "\n".join([
                p.text
                for s in prs.slides
                for sh in s.shapes
                if sh.has_text_frame
                for p in sh.text_frame.paragraphs
                if p.text.strip()
            ])
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{prompt_doc}\n\n{text}"
            )
            result = response.text

          st.success("✅ សម្រាយខ្លឹមសាររួចរាល់!")
          st.markdown(result)
        except Exception as e:
          st.error(f"មានបញ្ហា៖ {e}")
        finally:
          if os.path.exists(tmp_path):
            os.remove(tmp_path)
