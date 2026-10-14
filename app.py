import sys
import os

# Ensure UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import os
import json
import tempfile
import io
import re
import time
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from google import genai
from google.genai import types
import docx
from pptx import Presentation
import pypdf
import openpyxl

class AuthError(Exception):
    pass

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
config = {
    "gemini_api_key": "AQ.Ab8RN6KzSUJONKyOlx5oy3ZjQVcYCOJ4_jtKaZFYXpBnUw8MJA",
    "default_model": "gemini-3.5-flash",
    "fallback_model": "gemini-3.5-flash-lite",
    "port": 5000
}

if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    except Exception as e:
        print(f"Error loading config: {e}")

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

def get_client(api_key=None):
    key = api_key or os.environ.get("GEMINI_API_KEY") or config.get("gemini_api_key")
    return genai.Client(api_key=key)

def call_gemini(client, contents, system_instruction=None, model=None):
    preferred_model = model or config.get("default_model", "gemini-3.5-flash")
    fallback_model = config.get("fallback_model", "gemini-3.5-flash-lite")
    
    config_params = {}
    if system_instruction:
        config_params["system_instruction"] = system_instruction

    for target_model in models_to_try:
        for attempt in range(max_retries):
            try:
                if config_params:
            return client.models.generate_content(
                model=preferred_model,
                        contents=contents,
                        config=config_params
            ).text
                else:
            return client.models.generate_content(
                model=preferred_model,
                        contents=contents
            ).text
            except Exception as e:
        print(f"Warning: Primary model {preferred_model} failed ({e}), attempting fallback {fallback_model}...")
        try:
            if config_params:
                return client.models.generate_content(
                    model=fallback_model,
                    contents=contents,
                    config=config_params
                ).text
                else:
                return client.models.generate_content(
                    model=fallback_model,
                    contents=contents
                ).text
        except Exception as e2:
            raise RuntimeError(f"Gemini API Error: {e2}")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    if request.method == "POST":
        data = request.json or {}
        new_key = data.get("gemini_api_key")
        new_model = data.get("default_model")
        if new_key:
            config["gemini_api_key"] = new_key.strip()
        if new_model:
            config["default_model"] = new_model.strip()
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        return jsonify({"status": "success", "message": "ការកំណត់ត្រូវបានរក្សាទុកជោគជ័យ!"})
    
    # GET: return masked key
    masked_key = ""
    if config.get("gemini_api_key"):
        k = config["gemini_api_key"]
        masked_key = k[:6] + "..." + k[-4:] if len(k) > 10 else "********"
    return jsonify({
        "status": "success",
        "masked_key": masked_key,
        "default_model": config.get("default_model"),
        "has_key": bool(config.get("gemini_api_key"))
    })

# 1. VOICE TO STRUCTURED REPORT
@app.route("/api/voice-to-report", methods=["POST"])
def voice_to_report():
    if "audio" not in request.files:
        return jsonify({"error": "សូមបញ្ចូល File សំឡេង"}), 400
    
    audio_file = request.files["audio"]
    report_type = request.form.get("report_type", "general")
    custom_instructions = request.form.get("custom_instructions", "").strip()
    client_api_key = request.headers.get("X-Gemini-Key") or request.form.get("api_key")

    filename = audio_file.filename or "recording.webm"
    ext = os.path.splitext(filename)[1].lower() or ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        client = get_client(client_api_key)

    mime_types = {
        ".mp3": "audio/mp3",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".webm": "audio/webm",
        ".aac": "audio/aac",
        ".mp4": "audio/mp4"
    }
    mime = mime_types.get(ext, "audio/webm")

        uploaded = client.files.upload(file=tmp_path, mime_type=mime)

    template_prompts = {
        "general": """
សូមស្តាប់សំឡេងនេះដោយយកចិត្តទុកដាក់បំផុត ហើយរៀបចំជា «របាយការណ៍វឌ្ឍនភាពការងារទូទៅ» ជាភាសាខ្មែរផ្លូវការ ត្រឹមត្រូវតាមក្បួនខ្នាតរដ្ឋបាល ដោយមានទម្រង់៖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 របាយការណ៍វឌ្ឍនភាពការងារ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🗓 ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីកន្លែង សមាសភាពចូលរួម/អ្នកទទួលបន្ទុក)
⚡ ២. សកម្មភាព និងការងារសំខាន់ៗដែលបានអនុវត្ត
🏆 ៣. លទ្ធផលសម្រេចបាន (ចំណុចលេចធ្លោ និងបរិមាណការងារ)
⚠️ ៤. បញ្ហាប្រឈម និងឧបសគ្គដែលបានជួបប្រទះ
🎯 ៥. ដំណោះស្រាយ និងទិសដៅអនុវត្តបន្ត
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
សូមសរសេរឱ្យមានរបៀប រៀបចំជាចំណុចៗងាយស្រួលអាន និងច្បាស់លាស់។
""",
        "field": """
សូមស្តាប់សំឡេងនេះដោយយកចិត្តទុកដាក់ ហើយរៀបចំជា «របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន» ជាភាសាខ្មែរផ្លូវការ ដោយមានទម្រង់៖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛 របាយការណ៍លទ្ធផលការងារចុះមូលដ្ឋាន
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ១. ព័ត៌មានទូទៅ (កាលបរិច្ឆេទ ទីតាំងចុះមូលដ្ឋាន ក្រុមការងារ និងសមាសភាពចូលរួម)
🎯 ២. គោលបំណង និងសកម្មភាពស្នូលនៃការចុះជួប
🤝 ៣. សភាពការណ៍ទូទៅ និងមតិសាទរ/មនោសញ្ចេតនាប្រជាពលរដ្ឋ
🗣 ៤. មតិសំណូមពរ កង្វល់ និងបញ្ហាប្រឈមជាក់ស្តែង
🧭 ៥. វិធានការដោះស្រាយចំពោះមុខ និងសំណើទិសដៅបន្ត
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
សូមសរសេរប្រកបដោយភាពកក់ក្តៅ និងផ្លូវការច្បាស់លាស់។
""",
        "meeting": """
សូមស្តាប់សំឡេងនេះ ហើយរៀបចំជា «កំណត់ហេតុអង្គប្រជុំផ្លូវការ» ជាភាសាខ្មែរតាមទម្រង់៖
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
        "executive": """
សូមស្តាប់សំឡេងនេះ ហើយរៀបចំជា «របាយការណ៍សង្ខេបបន្ទាន់ (Executive Brief)» ជាភាសាខ្មែរខ្លី ខ្លឹម ចំគោលដៅ៖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ របាយការណ៍សង្ខេបបន្ទាន់ (EXECUTIVE BRIEF)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 សេចក្តីសង្ខេបខ្លឹមសារស្នូល (១-២ កថាខណ្ឌខ្លី)
🔥 ចំណុចគន្លឹះសំខាន់ៗត្រូវដឹងភ្លាមៗ (Bullet Points)
⚠️ ហានិភ័យ ឬបញ្ហាប្រឈមបន្ទាន់
🚀 សកម្មភាពដែលត្រូវចាត់ចែងភ្លាមៗ (Action Items & Person in charge)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    }

    selected_prompt = template_prompts.get(report_type, template_prompts["general"])
    if custom_instructions:
        selected_prompt += f"\n\nចំណាំបន្ថែមពីអ្នកប្រើប្រាស់៖ {custom_instructions}"

    uploaded_ref = None
    tmp_path = None

    try:
        client = get_client(client_api_key)

        if len(audio_bytes) <= 20 * 1024 * 1024:
            audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime)
            result_text = call_gemini(
                client=client,
                contents=[audio_part, selected_prompt],
                system_instruction="អ្នកគឺជាជំនួយការផ្នែករដ្ឋបាល និងរៀបចំរបាយការណ៍ការងារជាន់ខ្ពស់ដែលមានជំនាញភាសាខ្មែររដ្ឋបាលខ្ពស់បំផុត។"
            )
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            uploaded_ref = client.files.upload(file=tmp_path, config={"mime_type": mime})
            result_text = call_gemini(
                client=client,
            contents=[uploaded, selected_prompt],
                system_instruction="អ្នកគឺជាជំនួយការផ្នែករដ្ឋបាល និងរៀបចំរបាយការណ៍ការងារជាន់ខ្ពស់ដែលមានជំនាញភាសាខ្មែររដ្ឋបាលខ្ពស់បំផុត។"
            )

        try:
            client.files.delete(name=uploaded.name)
        except Exception:
            pass

        return jsonify({"status": "success", "report": result_text})

    except AuthError as e:
        return jsonify({"status": "error", "auth_error": True, "message": str(e)}), 401
    except Exception as e:
        safe_print(f"voice_to_report error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if os.path.exists(tmp_path):
                os.remove(tmp_path)
            except Exception:
                pass

# 2. DOCUMENT SUMMARIZATION & ANALYSIS
def extract_document_text(file_path, ext):
    ext = ext.lower()
    text = ""
    if ext == ".pdf":
        try:
            reader = pypdf.PdfReader(file_path)
            pages_text = []
            for i, page in enumerate(reader.pages):
                try:
                    pt = page.extract_text()
                if pt:
                    pages_text.append(f"--- ទំព័រទី {i+1} ---\n" + pt)
            text = "\n\n".join(pages_text)
        except Exception as e:
            print(f"pypdf extraction error: {e}")
    elif ext == ".docx":
        try:
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            # Also extract tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
                    if row_text:
                        text += f"\n| {row_text} |"
        except Exception as e:
            print(f"docx extraction error: {e}")
    elif ext == ".pptx":
        try:
            prs = Presentation(file_path)
            slides_text = []
            for i, slide in enumerate(prs.slides):
                s_lines = []
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for p in shape.text_frame.paragraphs:
                            if p.text.strip():
                                s_lines.append(p.text.strip())
                    elif shape.has_table:
                        for row in shape.table.rows:
                            r_cells = [c.text.strip() for c in row.cells if c.text.strip()]
                            if r_cells:
                                s_lines.append(" | ".join(r_cells))
                if s_lines:
                    slides_text.append(f"--- ស្លាយទី {i+1} ---\n" + "\n".join(s_lines))
            text = "\n\n".join(slides_text)
        except Exception as e:
            print(f"pptx extraction error: {e}")
    elif ext in [".xlsx", ".xls"]:
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheets_text = []
            for sheetname in wb.sheetnames[:5]:  # first 5 sheets
                ws = wb[sheetname]
                rows_text = []
                for row in list(ws.iter_rows(values_only=True))[:100]:
                    valid_cells = [str(c).strip() for c in row if c is not None and str(c).strip()]
                    if valid_cells:
                        rows_text.append(" | ".join(valid_cells))
                if rows_text:
                    sheets_text.append(f"--- Sheet: {sheetname} ---\n" + "\n".join(rows_text))
            text = "\n\n".join(sheets_text)
        except Exception as e:
            safe_print(f"openpyxl extraction error: {e}")
    elif ext in [".txt", ".md", ".csv", ".json"]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            safe_print(f"text reading error: {e}")
    return text.strip()

@app.route("/api/summarize-doc", methods=["POST"])
def summarize_document():
    if "document" not in request.files:
        return jsonify({"status": "error", "message": "សូមបញ្ចូល File ឯកសារ"}), 400
    
    doc_file = request.files["document"]
    mode = request.form.get("mode", "key_points")
    custom_question = request.form.get("custom_question", "").strip()
    client_api_key = request.headers.get("X-Gemini-Key") or request.form.get("api_key")

    filename = doc_file.filename or "document.pdf"
    ext = os.path.splitext(filename)[1].lower()

    file_bytes = doc_file.read()
    if not file_bytes:
        return jsonify({"status": "error", "message": "File ឯកសារទទេ សូមពិនិត្យឡើងវិញ"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    uploaded_ref = None

    try:
        client = get_client(client_api_key)
        extracted_text = extract_document_text(tmp_path, ext)

        mode_prompts = {
            "key_points": """
សូមអាន និងសម្រាយខ្លឹមសារឯកសារនេះជាភាសាខ្មែរឱ្យខ្លី ខ្លឹម ងាយយល់បំផុត ដោយចែកចេញជា៖
📌 ១. ប្រធានបទសំខាន់ និងគោលបំណងនៃឯកសារ
🎯 ២. ចំណុចស្នូលគន្លឹះ (Key Takeaways) ៣ ទៅ ៥ ចំណុចសំខាន់បំផុត
💡 ៣. អត្ថន័យ និងផលប៉ះពាល់ជាក់ស្តែង
""",
            "detailed": """
សូមធ្វើការវិភាគ និងសម្រាយលម្អិតខ្លឹមសារឯកសារនេះជាភាសាខ្មែរ៖
📖 ១. សេចក្តីផ្តើម និងបរិបទនៃឯកសារ
📑 ២. ការសម្រាយខ្លឹមសារលម្អិតតាមផ្នែក/ជំពូក ឬចំណុចនីមួយៗ
📊 ៣. ទិន្នន័យ ស្ថិតិ ឬអង្គហេតុសំខាន់ៗដែលត្រូវបានលើកឡើង
🔍 ៤. ការវាយតម្លៃរួម
""",
            "action_items": """
សូមស្រង់ទិន្នន័យពីឯកសារនេះជាភាសាខ្មែរដោយផ្តោតលើការអនុវត្ត៖
⚖️ ១. សេចក្តីសម្រេច ឬគោលការណ៍ដែលបានកំណត់
📋 ២. បញ្ជីការងារដែលត្រូវចាត់ចែងអនុវត្ត (Action Items)
👤 ៣. បុគ្គល ឬអង្គភាពទទួលបន្ទុកជាក់លាក់
⏰ ៤. កាលបរិច្ឆេទកំណត់ ឬកាលវិភាគអនុវត្ត (Deadlines)
""",
            "qa": f"""
សូមឆ្លើយសំណួរជាក់លាក់ខាងក្រោមនេះ ដោយយោងទៅតាមខ្លឹមសារនៃឯកសារ៖
❓ សំណួររបស់អ្នកប្រើប្រាស់៖ {custom_question}
សូមឆ្លើយឱ្យចំគោលដៅ ច្បាស់លាស់ និងមានយោងទឡ្ហីករណ៍ពីឯកសារ។
"""
        }

        prompt = mode_prompts.get(mode, mode_prompts["key_points"])
        if custom_question and mode != "qa":
            prompt += f"\n\nសំណួរ ឬចំណាំបន្ថែម៖ {custom_question}"

        # If extracted text is substantial, pass text directly
        if len(extracted_text) > 50:
            prompt_content = f"{prompt}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nខ្លឹមសារឯកសារ៖\n{extracted_text[:35000]}"
            result_text = call_gemini(
                client=client,
                contents=prompt_content,
                system_instruction="អ្នកគឺជាអ្នកវិភាគ និងសង្ខេបឯកសារអាជីព មានសមត្ថភាពទាញយកខ្លឹមសារសំខាន់ៗជាភាសាខ្មែរបានយ៉ាងត្រឹមត្រូវ និងទាក់ទាញ។"
            )
        else:
            # Scanned / Image document fallback: Use inline bytes if <= 20MB or files API
            mime_map = {
                ".pdf": "application/pdf",
                ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg"
            }
            mime = mime_map.get(ext, "application/pdf")
            
            if len(file_bytes) <= 20 * 1024 * 1024:
                file_part = types.Part.from_bytes(data=file_bytes, mime_type=mime)
                result_text = call_gemini(
                    client=client,
                    contents=[file_part, prompt],
                    system_instruction="អ្នកគឺជាអ្នកវិភាគ និងសង្ខេបឯកសារអាជីព មានសមត្ថភាពទាញយកខ្លឹមសារសំខាន់ៗជាភាសាខ្មែរបានយ៉ាងត្រឹមត្រូវ។"
                )
            else:
                uploaded_ref = client.files.upload(file=tmp_path, config={"mime_type": mime})
                result_text = call_gemini(
                    client=client,
                contents=[uploaded, prompt],
                    system_instruction="អ្នកគឺជាអ្នកវិភាគ និងសង្ខេបឯកសារអាជីព មានសមត្ថភាពទាញយកខ្លឹមសារសំខាន់ៗជាភាសាខ្មែរបានយ៉ាងត្រឹមត្រូវ។"
                )
            try:
                client.files.delete(name=uploaded.name)
            except Exception:
                pass

        return jsonify({
            "status": "success",
            "filename": filename,
            "text_length": len(extracted_text),
            "summary": result_text
        })

    except AuthError as e:
        return jsonify({"status": "error", "auth_error": True, "message": str(e)}), 401
    except Exception as e:
        safe_print(f"summarize_document error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if uploaded_ref:
            try:
                client.files.delete(name=uploaded_ref.name)
            except Exception:
                pass
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

# 3. SMART MULTILINGUAL TRANSLATOR
@app.route("/api/translate", methods=["POST"])
def translate_text():
    data = request.json or {}
    text = data.get("text", "").strip()
    source_lang = data.get("source_lang", "auto")
    target_lang = data.get("target_lang", "km")
    tone = data.get("tone", "formal") # formal, natural, technical
    client_api_key = request.headers.get("X-Gemini-Key") or data.get("api_key")

    if not text:
        return jsonify({"status": "error", "message": "សូមបញ្ចូលអត្ថបទដែលត្រូវបកប្រែ"}), 400

    lang_names = {
        "km": "ភាសាខ្មែរ (Khmer)",
        "en": "English",
        "zh": "中文 (Chinese)",
        "vi": "Tiếng Việt (Vietnamese)",
        "th": "ภาษาไทย (Thai)",
        "fr": "Français (French)",
        "ja": "日本語 (Japanese)",
        "ko": "한국어 (Korean)",
        "auto": "ស្វ័យប្រវត្តិ (Auto-Detect)"
    }

    tone_instructions = {
        "formal": "ប្រើប្រាស់រចនាបថផ្លូវការ រដ្ឋបាល សុភាពរាបសារ និងត្រឹមត្រូវតាមក្បួនខ្នាតវេយ្យាករណ៍ខ្ពស់បំផុត (Official & Administrative)",
        "natural": "ប្រើប្រាស់ពាក្យពេចន៍ទូទៅ ងាយយល់ រលូនតាមបែបសន្ទនាប្រចាំថ្ងៃ (Natural & Conversational)",
        "technical": "រក្សាពាក្យបច្ចេកទេសឱ្យបានច្បាស់លាស់ ត្រឹមត្រូវតាមក្បួនខ្នាតវិជ្ជាជីវៈ (Technical & Professional)"
    }

    target_name = lang_names.get(target_lang, target_lang)
    source_name = lang_names.get(source_lang, "Auto-detect")
    tone_desc = tone_instructions.get(tone, tone_instructions["formal"])

    prompt = f"""
សូមបកប្រែអត្ថបទខាងក្រោមពី {source_name} ទៅជា {target_name}។
លក្ខខណ្ឌតម្រូវ៖
- រចនាបថបកប្រែ៖ {tone_desc}
- រក្សាទម្រង់អត្ថបទដើម (កថាខណ្ឌ ចំណុច bullet points លេខរៀង)
- បកប្រែឱ្យមានអត្ថន័យជ្រាលជ្រៅ មិនមែនបកប្រែពាក្យទល់ពាក្យ (Word-by-word) នោះទេ
- បញ្ចេញតែលទ្ធផលបកប្រែសុទ្ធ ដោយមិនបាច់សរសេរសេចក្តីផ្តើម ឬការពន្យល់បន្ថែមឡើយ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
អត្ថបទដើម៖
{text}
"""

    try:
        client = get_client(client_api_key)
        translated = call_gemini(
            client=client,
            contents=prompt,
            system_instruction="អ្នកគឺជាអ្នកបកប្រែភាសាអាជីពកម្រិតខ្ពស់ដែលមានជំនាញជ្រៅជ្រះទាំងភាសាខ្មែរ និងភាសាអន្តរជាតិ។"
        )
        return jsonify({
            "status": "success",
            "translated_text": translated.strip(),
            "target_lang": target_lang
        })
    except AuthError as e:
        return jsonify({"status": "error", "auth_error": True, "message": str(e)}), 401
    except Exception as e:
        safe_print(f"translate error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 4. AI WORK CHAT ASSISTANT
@app.route("/api/chat", methods=["POST"])
def chat_assistant():
    data = request.json or {}
    message = data.get("message", "").strip()
    history = data.get("history", [])
    client_api_key = request.headers.get("X-Gemini-Key") or data.get("api_key")

    if not message:
        return jsonify({"error": "សូមបញ្ចូលសារ"}), 400

    system_instruction = """
អ្នកគឺជា «KhemaraAI WorkSuite Assistant» ជំនួយការឆ្លាតវៃផ្នែកការងារ ការិយាល័យ និងរដ្ឋបាល។
អ្នកមានសមត្ថភាពខ្ពស់ក្នុងការ៖
១. ជួយព្រាងលិខិតផ្លូវការ លិខិតអញ្ជើញ លិខិតថ្លែងអំណរគុណ និងលិខិតរដ្ឋបាល
២. កែសម្រួលអក្ខរាវិរុទ្ធ វេយ្យាករណ៍ និងពាក្យពេចន៍ភាសាខ្មែរឱ្យត្រឹមត្រូវ និងទាក់ទាញ
៣. ជួយរៀបចំរបៀបវារៈ គម្រោងការងារ ផែនការសកម្មភាព និងសំណើផ្សេងៗ
៤. ផ្តល់យោបល់ និងដោះស្រាយបញ្ហាការងារប្រកបដោយវិជ្ជាជីវៈ
៥. ឆ្លើយតបដោយសុភាពរាបសារ រៀបចំជាទម្រង់ Markdown ច្បាស់លាស់ ងាយស្រួលអាន។
"""

    # Build conversation contents
    contents = []
    # Include up to last 6 messages of history for context
    for turn in history[-6:]:
        role = turn.get("role", "user")
        text = turn.get("text", "")
        if text:
            # Map role
            gemini_role = "user" if role == "user" else "model"
            contents.append({"role": gemini_role, "parts": [{"text": text}]})

    contents.append({"role": "user", "parts": [{"text": message}]})

    try:
        client = get_client(client_api_key)
        preferred_model = config.get("default_model", "gemini-3.5-flash")
        
        response = client.models.generate_content(
            model=preferred_model,
            contents=contents,
            config={"system_instruction": system_instruction}
        )
        return jsonify({"status": "success", "reply": response.text})
    except Exception as e:
        # Retry with direct prompt fallback
        try:
            client = get_client(client_api_key)
            reply = call_gemini(
                client=client,
                contents=f"System: {system_instruction}\n\nUser: {message}",
                system_instruction=system_instruction
            )
            return jsonify({"status": "success", "reply": reply})
        except AuthError as ae:
            return jsonify({"status": "error", "auth_error": True, "message": str(ae)}), 401
        except Exception as e2:
            return jsonify({"status": "error", "message": str(e2)}), 500

# 5. EXPORT AS DOCX (Word Document)
@app.route("/api/export-docx", methods=["POST"])
def export_docx():
    data = request.json or {}
    title = data.get("title", "របាយការណ៍ការងារ")
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "គ្មានខ្លឹមសារសម្រាប់ Export ទេ"}), 400

    doc = docx.Document()

    # Set document title
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(title)
    title_run.font.name = "Khmer OS Siemreap"
    title_run.font.size = docx.shared.Pt(18)
    title_run.bold = True
    title_p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

    # Add divider
    doc.add_paragraph("―" * 30).alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check headings
        if stripped.startswith("# "):
            h = doc.add_heading(level=1)
            r = h.add_run(stripped.replace("# ", ""))
            r.font.name = "Khmer OS Siemreap"
            r.bold = True
        elif stripped.startswith("## "):
            h = doc.add_heading(level=2)
            r = h.add_run(stripped.replace("## ", ""))
            r.font.name = "Khmer OS Siemreap"
            r.bold = True
        elif stripped.startswith("### "):
            h = doc.add_heading(level=3)
            r = h.add_run(stripped.replace("### ", ""))
            r.font.name = "Khmer OS Siemreap"
            r.bold = True
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', stripped[2:])
            try:
                p = doc.add_paragraph(style='List Bullet')
                r = p.add_run(clean_text)
            except Exception:
                p = doc.add_paragraph()
                r = p.add_run("• " + clean_text)
            r.font.name = "Khmer OS Siemreap"
            r.font.size = docx.shared.Pt(11.5)
        elif stripped.startswith("━━━━") or stripped.startswith("----"):
            p = doc.add_paragraph("―" * 25)
            p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        else:
            p = doc.add_paragraph()
            clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', stripped)
            r = p.add_run(clean_text)
            r.font.name = "Khmer OS Siemreap"
            r.font.size = docx.shared.Pt(11.5)

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)

    safe_title = re.sub(r'[^a-zA-Z0-9_\u1780-\u17FF]', '_', title)
    return send_file(
        bio,
        as_attachment=True,
        download_name=f"{safe_title}.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if __name__ == "__main__":
    port = int(config.get("port", 5000))
    print(f">> KhemaraAI WorkSuite is running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
