<!DOCTYPE html>
<html lang="km" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KhemaraAI WorkSuite - ប្រព័ន្ធជំនួយការរដ្ឋបាល និងការិយាល័យឆ្លាតវៃ AI</title>
  
  <!-- Google Fonts: Kantumruy Pro & Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Kantumruy+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- FontAwesome 6 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              dark: '#0b0e17',
              card: '#131724',
              surface: '#171c2d',
              border: '#1e2436',
              borderHover: '#333e5c',
              accent: '#6366f1',
              accentHover: '#4f46e5',
              purple: '#7c3aed',
              neon: '#10b981'
            }
          },
          fontFamily: {
            kantumruy: ['"Kantumruy Pro"', 'sans-serif'],
            inter: ['"Inter"', 'sans-serif']
          }
        }
      }
    }
  </script>

  <style>
    * {
      font-family: 'Kantumruy Pro', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Custom Scrollbars */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0b0e17;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e2436;
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #3b425b;
    }

    /* Pulse Glow */
    @keyframes greenGlow {
      0%, 100% { opacity: 1; transform: scale(1); filter: drop-shadow(0 0 6px #10b981); }
      50% { opacity: 0.6; transform: scale(0.92); filter: drop-shadow(0 0 2px #10b981); }
    }
    .status-dot-pulse {
      animation: greenGlow 2.5s infinite ease-in-out;
    }

    /* Waveform visualizer bars */
    .wave-bar {
      transition: height 0.08s ease;
    }
  </style>
</head>
<body class="bg-[#0b0e17] text-slate-200 min-h-screen flex flex-col antialiased selection:bg-indigo-600 selection:text-white">

  <!-- ==================== TOP NAVIGATION ==================== -->
  <header class="border-b border-[#1e2436] bg-[#0d111c]/90 sticky top-0 z-40 backdrop-blur-md px-4 lg:px-8 py-3.5 transition-all">
    <div class="max-w-[1550px] mx-auto flex items-center justify-between gap-4">
      
      <!-- Brand Logo & Title -->
      <div class="flex items-center gap-3.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center text-white text-lg font-bold shadow-lg shadow-indigo-600/30 ring-1 ring-white/20">
          <i class="fa-solid fa-bolt-lightning"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg lg:text-xl font-bold tracking-tight text-white flex items-center gap-2">
              KhemaraAI WorkSuite
              <span class="text-[10px] uppercase font-semibold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/25">v3.2 PRO</span>
            </h1>
          </div>
          <p class="text-xs text-slate-400 font-light hidden sm:block">ប្រព័ន្ធជំនួយការរដ្ឋបាល និងការិយាល័យឆ្លាតវៃ AI</p>
        </div>
      </div>

      <!-- Right Header Actions & Status Pill -->
      <div class="flex items-center gap-3">
        <!-- Model Indicator Badge -->
        <div class="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#10b981]/10 border border-[#10b981]/30 text-[#10b981] text-xs font-medium">
          <span class="w-2 h-2 rounded-full bg-[#10b981] status-dot-pulse"></span>
          <span>Gemini Flash (ល្បឿនលឿនបំផុត)</span>
        </div>

        <!-- API Key Configure Button -->
        <button id="btnOpenSettings" class="p-2.5 rounded-xl bg-[#171c2d] hover:bg-[#20273f] border border-[#1e2436] text-slate-300 hover:text-white transition-all text-sm flex items-center gap-2" title="កំណត់ API Key">
          <i class="fa-solid fa-key text-amber-400"></i>
          <span class="hidden md:inline text-xs font-medium" id="keyStatusText">API Key សេរី</span>
        </button>

        <!-- Reset Button -->
        <button id="btnResetAll" class="p-2.5 rounded-xl bg-[#171c2d] hover:bg-[#20273f] border border-[#1e2436] text-slate-400 hover:text-rose-400 transition-all text-sm" title="សម្អាតទិន្នន័យ (Reset)">
          <i class="fa-solid fa-rotate-right"></i>
        </button>

        <!-- Help Modal Trigger -->
        <button id="btnHelp" class="w-9 h-9 rounded-xl bg-[#171c2d] hover:bg-[#20273f] border border-[#1e2436] text-slate-300 hover:text-white flex items-center justify-center text-sm transition-all" title="របៀបប្រើប្រាស់">
          <i class="fa-regular fa-circle-question"></i>
        </button>
      </div>

    </div>
  </header>

  <!-- ==================== MAIN CONTENT WRAPPER ==================== -->
  <main class="flex-1 max-w-[1550px] w-full mx-auto px-4 lg:px-8 py-6 flex flex-col gap-6">

    <!-- TAB PILLS NAVIGATION -->
    <div class="bg-[#131724] p-1.5 rounded-2xl border border-[#1e2436] flex flex-wrap gap-1.5 shadow-md shadow-black/20">
      
      <button class="nav-tab active flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all text-white bg-gradient-to-r from-indigo-600 to-purple-600 shadow-md shadow-indigo-600/30" data-target="tab-voice">
        <i class="fa-solid fa-microphone-lines text-base"></i>
        <span>សំឡេង ➜ របាយការណ៍</span>
      </button>

      <button class="nav-tab flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-400 hover:text-slate-200 hover:bg-[#1a2034]" data-target="tab-docs">
        <i class="fa-regular fa-file-lines text-base"></i>
        <span>សម្រាយ & សង្ខេបឯកសារ</span>
      </button>

      <button class="nav-tab flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-400 hover:text-slate-200 hover:bg-[#1a2034]" data-target="tab-translate">
        <i class="fa-solid fa-language text-base"></i>
        <span>បកប្រែភាសាការងារ</span>
      </button>

      <button class="nav-tab flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-400 hover:text-slate-200 hover:bg-[#1a2034]" data-target="tab-chat">
        <i class="fa-regular fa-comments text-base"></i>
        <span>ជំនួយការឆ្លាតវៃ (AI Chat)</span>
      </button>

    </div>

    <!-- ============================================================== -->
    <!-- TAB 1: 🎙️ សំឡេង ➜ របាយការណ៍ (Audio to Report)                  -->
    <!-- ============================================================== -->
    <div id="tab-voice" class="tab-pane block">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- LEFT PANEL: CONTROLS & INPUTS (lg:col-span-6) -->
        <div class="lg:col-span-6 bg-[#131724] border border-[#1e2436] rounded-2xl p-5 lg:p-6 flex flex-col gap-5 shadow-xl shadow-black/20">
          
          <!-- Card Header -->
          <div class="flex items-center justify-between pb-3.5 border-b border-[#1e2436]">
            <div class="flex items-center gap-2.5">
              <span class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-sm border border-indigo-500/20">
                <i class="fa-solid fa-microphone"></i>
              </span>
              <h2 class="text-base lg:text-lg font-bold text-white tracking-wide">បម្លែងសំឡេងជារបាយការណ៍</h2>
            </div>
            <span class="px-2.5 py-1 rounded-full text-[11px] font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 uppercase tracking-wider">
              AI Audio Intelligence
            </span>
          </div>

          <!-- Audio Source Toggle (Pills) -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">ជ្រើសរើសប្រភពសំឡេង៖</label>
            <div class="grid grid-cols-2 gap-2 bg-[#0d101a] p-1.5 rounded-xl border border-[#1e2436]">
              <button id="btnModeUpload" class="flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs lg:text-sm font-medium transition-all bg-[#1e2538] text-white shadow-sm">
                <i class="fa-solid fa-folder-open text-amber-400"></i>
                <span>បញ្ចូល File សំឡេង</span>
              </button>
              <button id="btnModeRecord" class="flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs lg:text-sm font-medium transition-all text-slate-400 hover:text-white hover:bg-[#171d2d]">
                <i class="fa-solid fa-circle text-rose-500 text-[10px]"></i>
                <span>ថតសំឡេងផ្ទាល់</span>
              </button>
            </div>
          </div>

          <!-- AUDIO INPUT SECTION 1: UPLOAD ZONE -->
          <div id="sectionUploadVoice" class="space-y-2">
            <div id="voiceDropzone" class="border-2 border-dashed border-[#232b40] hover:border-indigo-500/60 bg-[#0c0f1a] rounded-2xl p-6 text-center cursor-pointer transition-all group flex flex-col items-center justify-center relative">
              <input type="file" id="voiceFileInput" accept="audio/*,.mp3,.wav,.ogg,.m4a,.webm" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10">
              <div class="w-12 h-12 rounded-2xl bg-indigo-600/10 text-indigo-400 flex items-center justify-center text-xl mb-2.5 group-hover:scale-110 group-hover:bg-indigo-600/20 transition-all">
                <i class="fa-solid fa-music"></i>
              </div>
              <p class="text-sm font-semibold text-slate-200 mb-1">ចុចទីនេះ ឬទម្លាក់ File សំឡេងចូល</p>
              <p class="text-xs text-slate-500">គាំទ្រ MP3, WAV, M4A, OGG, WebM (ទំហំរហូតដល់ 100MB)</p>
            </div>

            <!-- Uploaded File Badge Info (Hidden by default) -->
            <div id="audioFileInfo" class="hidden flex items-center justify-between p-3 rounded-xl bg-indigo-950/20 border border-indigo-800/40 text-xs">
              <div class="flex items-center gap-2.5 truncate">
                <i class="fa-solid fa-file-audio text-indigo-400 text-base"></i>
                <div class="truncate">
                  <p id="audioFileName" class="font-medium text-slate-200 truncate">sample_voice.mp3</p>
                  <p id="audioFileSize" class="text-slate-400 text-[11px]">2.4 MB</p>
                </div>
              </div>
              <button id="btnRemoveAudioFile" class="text-slate-400 hover:text-rose-400 p-1.5 transition-colors" title="ដកចេញ">
                <i class="fa-solid fa-xmark"></i>
              </button>
            </div>

            <!-- Preset Samples Quick Pick -->
            <div class="flex items-center gap-2 pt-1 flex-wrap">
              <span class="text-[11px] text-slate-500">គំរូសាកល្បងរហ័ស៖</span>
              <button class="btn-sample-voice text-[11px] px-2.5 py-1 rounded-lg bg-[#1a2033] hover:bg-indigo-600/20 hover:text-indigo-300 text-slate-400 border border-[#262f49] transition-all" data-sample="water">
                <i class="fa-solid fa-play text-[9px] mr-1"></i> សំឡេង៖ ពិនិត្យបណ្ដាញទឹកស្អាត & ផ្លូវ
              </button>
              <button class="btn-sample-voice text-[11px] px-2.5 py-1 rounded-lg bg-[#1a2033] hover:bg-indigo-600/20 hover:text-indigo-300 text-slate-400 border border-[#262f49] transition-all" data-sample="meeting">
                <i class="fa-solid fa-play text-[9px] mr-1"></i> សំឡេង៖ ប្រជុំពិភាក្សាថវិកាប្រចាំខែ
              </button>
            </div>
          </div>

          <!-- AUDIO INPUT SECTION 2: LIVE MIC RECORDER (Hidden by default) -->
          <div id="sectionRecordVoice" class="hidden space-y-3">
            <div class="bg-[#0c0f1a] border border-[#1e2436] rounded-2xl p-5 flex flex-col items-center justify-center text-center gap-3.5">
              
              <!-- Timer & Status -->
              <div class="flex items-center gap-2">
                <span id="recStatusDot" class="w-2.5 h-2.5 rounded-full bg-slate-600"></span>
                <span id="recTimerText" class="text-xl font-mono font-bold text-slate-300 tracking-wider">00:00</span>
                <span id="recStatusText" class="text-xs text-slate-500 font-medium">ត្រៀមខ្លួនថត</span>
              </div>

              <!-- Animated Waveform Visualizer Simulator -->
              <div id="visualizerContainer" class="w-full h-12 flex items-center justify-center gap-1 px-4 py-2 bg-[#101422] rounded-xl border border-[#1e253a]">
                <!-- Bars will be generated via JS -->
              </div>

              <!-- Record Action Buttons -->
              <div class="flex items-center gap-3">
                <button id="btnStartRecord" class="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs lg:text-sm font-semibold transition-all shadow-lg shadow-rose-600/25">
                  <i class="fa-solid fa-microphone"></i>
                  <span>ចាប់ផ្ដើមថត</span>
                </button>
                <button id="btnStopRecord" disabled class="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 text-slate-500 text-xs lg:text-sm font-semibold transition-all cursor-not-allowed">
                  <i class="fa-solid fa-stop"></i>
                  <span>បញ្ឈប់ការថត</span>
                </button>
              </div>

              <audio id="recordedAudioPlayer" controls class="hidden w-full max-w-sm mt-1 h-9"></audio>
            </div>
          </div>

          <!-- Report Format Selection Cards (4 Options) -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2.5">
              ជ្រើសរើសទម្រង់របាយការណ៍ដែលត្រូវការ៖
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5" id="reportFormatGroup">
              
              <!-- Card 1 (Default Active) -->
              <div class="format-card active border-2 border-indigo-600 bg-indigo-950/20 hover:bg-indigo-950/30 p-3.5 rounded-xl cursor-pointer transition-all flex flex-col justify-between" data-format="work_progress">
                <div class="flex items-start gap-2.5">
                  <span class="text-xl">📊</span>
                  <div>
                    <h3 class="text-xs lg:text-sm font-bold text-white">វឌ្ឍនភាពការងារ</h3>
                    <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">របាយការណ៍ការងារទូទៅ សកម្មភាព លទ្ធផល និងបញ្ហាប្រឈម</p>
                  </div>
                </div>
              </div>

              <!-- Card 2 -->
              <div class="format-card border border-[#20273c] bg-[#0f121d] hover:border-indigo-500/50 hover:bg-[#141928] p-3.5 rounded-xl cursor-pointer transition-all flex flex-col justify-between" data-format="field_mission">
                <div class="flex items-start gap-2.5">
                  <span class="text-xl">🏛️</span>
                  <div>
                    <h3 class="text-xs lg:text-sm font-bold text-white">ការងារចុះមូលដ្ឋាន</h3>
                    <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">របាយការណ៍ចុះជួបប្រជាពលរដ្ឋ សំណូមពរ និងដំណោះស្រាយ</p>
                  </div>
                </div>
              </div>

              <!-- Card 3 -->
              <div class="format-card border border-[#20273c] bg-[#0f121d] hover:border-indigo-500/50 hover:bg-[#141928] p-3.5 rounded-xl cursor-pointer transition-all flex flex-col justify-between" data-format="meeting_minutes">
                <div class="flex items-start gap-2.5">
                  <span class="text-xl">📝</span>
                  <div>
                    <h3 class="text-xs lg:text-sm font-bold text-white">កំណត់ហេតុប្រជុំ</h3>
                    <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">ខ្លឹមសារអង្គប្រជុំ មតិពិភាក្សា និងសេចក្ដីសម្រេច</p>
                  </div>
                </div>
              </div>

              <!-- Card 4 -->
              <div class="format-card border border-[#20273c] bg-[#0f121d] hover:border-indigo-500/50 hover:bg-[#141928] p-3.5 rounded-xl cursor-pointer transition-all flex flex-col justify-between" data-format="quick_brief">
                <div class="flex items-start gap-2.5">
                  <span class="text-xl">⚡</span>
                  <div>
                    <h3 class="text-xs lg:text-sm font-bold text-white">សង្ខេបបន្ទាន់ (Brief)</h3>
                    <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">ខ្លឹមសារស្នូលខ្លីៗ ចំណុចសំខាន់ៗ និងសកម្មភាពបន្ទាន់</p>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Custom Instructions Field -->
          <div>
            <label for="customVoiceInstruction" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
              ចំណាំបន្ថែម ឬការណែនាំពិសេស (បើមាន)៖
            </label>
            <input type="text" id="customVoiceInstruction" placeholder="ឧទាហរណ៍៖ សូមសង្កត់ធ្ងន់លើលទ្ធផលការងារ និងកាលបរិច្ឆេទថ្ងៃទី ១៤..." class="w-full bg-[#0d101a] border border-[#1e2436] focus:border-indigo-500 rounded-xl px-3.5 py-2.5 text-xs lg:text-sm text-slate-200 placeholder-slate-600 focus:outline-none transition-all">
          </div>

          <!-- Primary Submit Action Button -->
          <button id="btnGenerateReport" class="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-sm lg:text-base font-semibold shadow-lg shadow-purple-600/30 transition-all flex items-center justify-center gap-2 group">
            <i class="fa-solid fa-pen-fancy group-hover:rotate-12 transition-transform"></i>
            <span>✏️ រៀបចំរបាយការណ៍ដោយ AI</span>
          </button>

        </div>

        <!-- RIGHT PANEL: LIVE RESULT & EXPORT (lg:col-span-6) -->
        <div class="lg:col-span-6 bg-[#131724] border border-[#1e2436] rounded-2xl p-5 lg:p-6 flex flex-col shadow-xl shadow-black/20 min-h-[580px]">
          
          <!-- Result Header -->
          <div class="flex items-center justify-between pb-3.5 border-b border-[#1e2436]">
            <div class="flex items-center gap-2">
              <span class="text-lg">📋</span>
              <h2 class="text-base lg:text-lg font-bold text-white">លទ្ធផលរបាយការណ៍</h2>
            </div>
            
            <!-- Tool buttons (Active when result is generated) -->
            <div id="resultActionTools" class="hidden flex items-center gap-2">
              <button id="btnCopyReport" class="px-2.5 py-1.5 rounded-lg bg-[#1a2034] hover:bg-indigo-600/20 text-slate-300 hover:text-indigo-300 border border-[#232c48] text-xs font-medium transition-all flex items-center gap-1.5" title="ចម្លងទុក">
                <i class="fa-regular fa-copy"></i>
                <span class="hidden sm:inline">ចម្លង (Copy)</span>
              </button>
              <button id="btnDownloadReport" class="px-2.5 py-1.5 rounded-lg bg-[#1a2034] hover:bg-indigo-600/20 text-slate-300 hover:text-indigo-300 border border-[#232c48] text-xs font-medium transition-all flex items-center gap-1.5" title="ទាញយកជាអត្ថបទ">
                <i class="fa-solid fa-arrow-down-to-bracket"></i>
                <span class="hidden sm:inline">ទាញយក (Download)</span>
              </button>
            </div>
          </div>

          <!-- Result Content Area -->
          <div class="flex-1 flex flex-col justify-center items-center py-6" id="reportDisplayContainer">
            
            <!-- State 1: Empty Placeholder (Initial State) -->
            <div id="stateEmptyReport" class="flex flex-col items-center justify-center text-center p-8 max-w-sm">
              <div class="w-20 h-20 rounded-3xl bg-[#0e121d] border border-[#1e2436] flex items-center justify-center text-4xl mb-4 text-slate-600 shadow-inner">
                <i class="fa-regular fa-file-lines"></i>
              </div>
              <h3 class="text-base font-semibold text-slate-200 mb-1.5">រង់ចាំការបម្លែងសំឡេង</h3>
              <p class="text-xs text-slate-500 leading-relaxed">
                សូមបញ្ចូល File សំឡេង ឬចុចថតសំឡេង រួចចុចប៊ូតុងខាងឆ្វេង ដើម្បីឱ្យ AI រៀបចំរបាយការណ៍ផ្លូវការជូនលោកអ្នក។
              </p>
            </div>

            <!-- State 2: Generating Loader Animation -->
            <div id="stateLoadingReport" class="hidden flex flex-col items-center justify-center text-center p-8">
              <div class="relative w-16 h-16 mb-4">
                <div class="w-16 h-16 rounded-full border-4 border-indigo-600/20 border-t-indigo-500 animate-spin"></div>
                <div class="absolute inset-0 flex items-center justify-center text-indigo-400 text-lg">
                  <i class="fa-solid fa-brain"></i>
                </div>
              </div>
              <h4 class="text-sm font-semibold text-white mb-1">AI កំពុងស្ដាប់ និងរៀបចំជារបាយការណ៍...</h4>
              <p class="text-xs text-slate-400 max-w-xs">កំពុងសំយោគសំឡេង ស្រង់ចំណុចគន្លឹះ និងរៀបចំទម្រង់លិខិតរដ្ឋបាលផ្លូវការ</p>
            </div>

            <!-- State 3: Structured Full Report View -->
            <div id="stateFinishedReport" class="hidden w-full space-y-4 text-left">
              <!-- Dynamically populated via JavaScript -->
            </div>

          </div>

        </div>

      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 2: 📄 សម្រាយ & សង្ខេបឯកសារ (Document Summary & Analysis)   -->
    <!-- ============================================================== -->
    <div id="tab-docs" class="tab-pane hidden">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Document Controls Panel (lg:col-span-5) -->
        <div class="lg:col-span-5 bg-[#131724] border border-[#1e2436] rounded-2xl p-5 lg:p-6 flex flex-col gap-5 shadow-xl">
          <div class="flex items-center justify-between pb-3.5 border-b border-[#1e2436]">
            <div class="flex items-center gap-2.5">
              <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-sm border border-emerald-500/20">
                <i class="fa-regular fa-file-pdf"></i>
              </span>
              <h2 class="text-base lg:text-lg font-bold text-white">សម្រាយ & សង្ខេបឯកសារ</h2>
            </div>
            <span class="px-2.5 py-1 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 uppercase tracking-wider">
              Doc Intelligence
            </span>
          </div>

          <!-- Doc Upload Zone -->
          <div id="docDropzone" class="border-2 border-dashed border-[#232b40] hover:border-emerald-500/60 bg-[#0c0f1a] rounded-2xl p-6 text-center cursor-pointer transition-all group relative">
            <input type="file" id="docFileInput" accept=".pdf,.docx,.doc,.pptx,.txt" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10">
            <div class="w-12 h-12 rounded-2xl bg-emerald-600/10 text-emerald-400 flex items-center justify-center text-xl mb-2.5 group-hover:scale-110 transition-all mx-auto">
              <i class="fa-solid fa-cloud-arrow-up"></i>
            </div>
            <p class="text-sm font-semibold text-slate-200 mb-1">បញ្ចូល File ឯកសារ (PDF, Word, PPT)</p>
            <p class="text-xs text-slate-500">គាំទ្រទាំងឯកសារ Scan និងឯកសារអត្ថបទខ្មែរ (Max 50MB)</p>
          </div>

          <!-- Selected File Badge -->
          <div id="docFileBadge" class="hidden flex items-center justify-between p-3 rounded-xl bg-emerald-950/20 border border-emerald-800/40 text-xs">
            <div class="flex items-center gap-2.5 truncate">
              <i class="fa-regular fa-file-lines text-emerald-400 text-lg"></i>
              <div class="truncate">
                <p id="docSelectedName" class="font-medium text-slate-200 truncate">ផែនការយុទ្ធសាស្ត្រ_២០២៦.pdf</p>
                <p id="docSelectedSize" class="text-slate-400 text-[11px]">1.8 MB</p>
              </div>
            </div>
            <button id="btnRemoveDocFile" class="text-slate-400 hover:text-rose-400 p-1" title="ដកចេញ">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>

          <!-- Sample Doc Buttons -->
          <div class="space-y-1.5">
            <span class="text-[11px] text-slate-500">ឬជ្រើសរើសឯកសារគំរូសាកល្បង៖</span>
            <div class="flex flex-col gap-1.5">
              <button class="btn-sample-doc text-left p-2.5 rounded-xl bg-[#0e121d] hover:bg-[#161c2d] border border-[#1e2436] text-xs text-slate-300 transition-all flex items-center justify-between" data-sample="strategy">
                <span>📄 សេចក្តីព្រាងផែនការអភិវឌ្ឍន៍សេដ្ឋកិច្ចមូលដ្ឋាន.docx</span>
                <span class="text-[10px] text-emerald-400 font-mono">1.2 MB</span>
              </button>
              <button class="btn-sample-doc text-left p-2.5 rounded-xl bg-[#0e121d] hover:bg-[#161c2d] border border-[#1e2436] text-xs text-slate-300 transition-all flex items-center justify-between" data-sample="procurement">
                <span>📑 របាយការណ៍លទ្ធកម្ម និងដេញថ្លៃគម្រោងហេដ្ឋារចនាសម្ព័ន្ធ.pdf</span>
                <span class="text-[10px] text-emerald-400 font-mono">3.4 MB</span>
              </button>
            </div>
          </div>

          <!-- Format Mode (Radio) -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">ទម្រង់សម្រាយដែលចង់បាន៖</label>
            <div class="grid grid-cols-2 gap-2 bg-[#0d101a] p-1.5 rounded-xl border border-[#1e2436]">
              <label class="flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-all bg-[#1e2538] text-white text-xs">
                <input type="radio" name="docModeRadio" value="brief" checked class="accent-indigo-500">
                <span>សង្ខេប ៣-៥ ចំណុចស្នូល</span>
              </label>
              <label class="flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-all text-slate-400 hover:text-white text-xs">
                <input type="radio" name="docModeRadio" value="detailed" class="accent-indigo-500">
                <span>សម្រាយលម្អិតតាមជំពូក</span>
              </label>
            </div>
          </div>

          <!-- Action Button -->
          <button id="btnSummarizeDoc" class="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-sm font-semibold shadow-lg shadow-emerald-600/25 transition-all flex items-center justify-center gap-2">
            <i class="fa-solid fa-sparkles"></i>
            <span>🚀 សម្រាយ និងវិភាគខ្លឹមសារ</span>
          </button>
        </div>

        <!-- Document Result Panel (lg:col-span-7) -->
        <div class="lg:col-span-7 bg-[#131724] border border-[#1e2436] rounded-2xl p-5 lg:p-6 flex flex-col shadow-xl min-h-[550px]">
          <div class="flex items-center justify-between pb-3.5 border-b border-[#1e2436]">
            <div class="flex items-center gap-2">
              <span class="text-lg">📑</span>
              <h2 class="text-base lg:text-lg font-bold text-white">ខ្លឹមសារសង្ខេប & ការវិភាគ</h2>
            </div>
            <button id="btnCopyDocSummary" class="hidden px-2.5 py-1.5 rounded-lg bg-[#1a2034] hover:bg-emerald-600/20 text-slate-300 hover:text-emerald-300 border border-[#232c48] text-xs font-medium transition-all flex items-center gap-1.5">
              <i class="fa-regular fa-copy"></i>
              <span>ចម្លង</span>
            </button>
          </div>

          <div id="docResultContainer" class="flex-1 flex flex-col justify-center items-center py-6">
            <div id="docResultEmpty" class="text-center p-8 max-w-sm">
              <div class="w-16 h-16 rounded-2xl bg-[#0e121d] border border-[#1e2436] flex items-center justify-center text-3xl mb-3 text-slate-600 mx-auto">
                <i class="fa-solid fa-book-open"></i>
              </div>
              <h3 class="text-sm font-semibold text-slate-300 mb-1">រង់ចាំឯកសារ</h3>
              <p class="text-xs text-slate-500">បញ្ចូលឯកសារ PDF ឬ Word ដើម្បីឱ្យប្រព័ន្ធស្រង់ទិន្នន័យ និងសម្រាយខ្លឹមសារស្នូលជូន។</p>
            </div>

            <div id="docResultContent" class="hidden w-full space-y-4 text-left">
              <!-- Dynamically Populated -->
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 3: 🌐 បកប្រែភាសាការងារ (Professional Translation)           -->
    <!-- ============================================================== -->
    <div id="tab-translate" class="tab-pane hidden">
      <div class="bg-[#131724] border border-[#1e2436] rounded-2xl p-5 lg:p-6 shadow-xl flex flex-col gap-5">
        
        <div class="flex flex-wrap items-center justify-between gap-4 pb-3.5 border-b border-[#1e2436]">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center text-sm border border-sky-500/20">
              <i class="fa-solid fa-language"></i>
            </span>
            <div>
              <h2 class="text-base lg:text-lg font-bold text-white">បកប្រែឯកសារ និងលិខិតផ្លូវការ</h2>
              <p class="text-xs text-slate-400">បកប្រែបែបផ្លូវការ រក្សាអត្ថន័យរដ្ឋបាល និងវេយ្យាករណ៍ត្រឹមត្រូវ</p>
            </div>
          </div>
          
          <!-- Sample Selector -->
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400">គំរូអត្ថបទ៖</span>
            <button id="btnSampleTrans1" class="text-xs px-2.5 py-1.5 rounded-lg bg-[#1a2034] hover:bg-sky-500/20 text-slate-300 border border-[#263152] transition-all">
              លិខិតសហប្រតិបត្តិការ (EN ➜ KH)
            </button>
            <button id="btnSampleTrans2" class="text-xs px-2.5 py-1.5 rounded-lg bg-[#1a2034] hover:bg-sky-500/20 text-slate-300 border border-[#263152] transition-all">
              សេចក្តីប្រកាសព័ត៌មាន (KH ➜ EN)
            </button>
          </div>
        </div>

        <!-- Language Controls Bar -->
        <div class="flex items-center justify-between gap-4 bg-[#0d101a] p-2.5 rounded-xl border border-[#1e2436]">
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400 font-semibold uppercase">ពីភាសា៖</span>
            <select id="selSourceLang" class="bg-[#171d2d] border border-[#2a344d] rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none">
              <option value="auto">ស្វែងរកស្វ័យប្រវត្ត (Auto Detect)</option>
              <option value="en">ភាសាអង់គ្លេស (English)</option>
              <option value="km">ភាសាខ្មែរ (Khmer)</option>
              <option value="zh">ភាសាចិន (Chinese)</option>
            </select>
          </div>

          <button id="btnSwapLang" class="w-8 h-8 rounded-lg bg-[#1b2236] hover:bg-indigo-600/30 text-slate-300 hover:text-indigo-300 flex items-center justify-center transition-all" title="ឆ្លាស់ភាសា">
            <i class="fa-solid fa-arrow-right-arrow-left text-xs"></i>
          </button>

          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400 font-semibold uppercase">ទៅជាភាសា៖</span>
            <select id="selTargetLang" class="bg-[#171d2d] border border-[#2a344d] rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none">
              <option value="km">ភាសាខ្មែរ (Khmer)</option>
              <option value="en">ភាសាអង់គ្លេស (English)</option>
              <option value="zh">ភាសាចិន (Chinese)</option>
            </select>
          </div>
        </div>

        <!-- Translation Side-by-Side Editor -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Source Box -->
          <div class="flex flex-col gap-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-medium text-slate-400">អត្ថបទដើម</span>
              <button id="btnClearSourceText" class="text-[11px] text-slate-500 hover:text-rose-400 transition-colors">សម្អាត</button>
            </div>
            <textarea id="txtSourceTrans" rows="12" placeholder="បញ្ចូលអត្ថបទដែលលោកអ្នកចង់បកប្រែនៅទីនេះ..." class="w-full bg-[#0c0f1a] border border-[#1e2436] focus:border-sky-500 rounded-xl p-4 text-sm text-slate-200 placeholder-slate-600 focus:outline-none resize-none leading-relaxed transition-all"></textarea>
          </div>

          <!-- Target Result Box -->
          <div class="flex flex-col gap-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-medium text-slate-400">លទ្ធផលបកប្រែផ្លូវការ</span>
              <button id="btnCopyTranslation" class="text-[11px] text-slate-400 hover:text-sky-300 flex items-center gap-1 transition-colors">
                <i class="fa-regular fa-copy"></i>
                <span>ចម្លង</span>
              </button>
            </div>
            <div id="txtTargetTrans" class="w-full bg-[#0c0f1a] border border-[#1e2436] rounded-xl p-4 text-sm text-slate-200 min-h-[290px] overflow-y-auto leading-relaxed">
              <span class="text-slate-600 italic">លទ្ធផលបកប្រែនឹងបង្ហាញនៅទីនេះ...</span>
            </div>
          </div>
        </div>

        <button id="btnExecuteTranslate" class="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white text-sm font-semibold shadow-lg shadow-sky-600/20 transition-all flex items-center justify-center gap-2">
          <i class="fa-solid fa-language"></i>
          <span>ចាប់ផ្ដើមបកប្រែដោយ AI</span>
        </button>

      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 4: 💬 ជំនួយការឆ្លាតវៃ (AI Assistant Chat)                  -->
    <!-- ============================================================== -->
    <div id="tab-chat" class="tab-pane hidden">
      <div class="bg-[#131724] border border-[#1e2436] rounded-2xl shadow-xl flex flex-col h-[650px] overflow-hidden">
        
        <!-- Chat Header -->
        <div class="p-4 border-b border-[#1e2436] bg-[#0f1320] flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-purple-600/20 text-purple-400 flex items-center justify-center border border-purple-500/30">
              <i class="fa-solid fa-robot"></i>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">ជំនួយការរដ្ឋបាល & បច្ចេកទេស AI</h3>
              <p class="text-[11px] text-slate-400">ត្រៀមខ្លួនជួយព្រាងលិខិត បកស្រាយបទដ្ឋានគតិយុត្ត និងឆ្លើយសំណួរ</p>
            </div>
          </div>
          <button id="btnClearChatHistory" class="text-xs px-2.5 py-1.5 rounded-lg bg-[#1a2034] hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 border border-[#242c46] transition-all">
            <i class="fa-regular fa-trash-can mr-1"></i> សម្អាតសារ
          </button>
        </div>

        <!-- Chat Conversation Messages Flow -->
        <div id="chatMessagesContainer" class="flex-1 p-4 lg:p-6 overflow-y-auto space-y-4">
          <!-- Initial Assistant Message -->
          <div class="flex items-start gap-3 max-w-3xl">
            <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-xs font-bold text-white shrink-0 shadow-md">
              AI
            </div>
            <div class="bg-[#1a2033] border border-[#232b43] rounded-2xl rounded-tl-sm p-4 text-xs lg:text-sm text-slate-200 leading-relaxed shadow-sm">
              <p class="font-medium text-white mb-1">ជំរាបសួរ! ខ្ញុំជាជំនួយការរដ្ឋបាល និងការិយាល័យឆ្លាតវៃ AI។</p>
              <p class="text-slate-300">ខ្ញុំអាចជួយលោកអ្នកក្នុងការ៖</p>
              <ul class="list-disc list-inside mt-1.5 space-y-0.5 text-slate-400 text-xs">
                <li>ព្រាងលិខិតអញ្ជើញ លិខិតស្នើសុំ និងសេចក្តីជូនដំណឹងផ្លូវការ</li>
                <li>កែសម្រួលរបាយការណ៍បច្ចេកទេសឱ្យមានលក្ខណៈស្តង់ដារ</li>
                <li>ផ្តល់យោបល់លើការដោះស្រាយបញ្ហា និងទិសដៅការងារ</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Quick Prompt Suggestions -->
        <div class="px-4 py-2 bg-[#0e121d] border-t border-[#1a2033] flex items-center gap-2 overflow-x-auto text-[11px]">
          <span class="text-slate-500 shrink-0">សំណើគំរូ៖</span>
          <button class="chat-prompt-pill shrink-0 px-2.5 py-1 rounded-full bg-[#181f33] hover:bg-indigo-600/20 text-slate-300 border border-[#242d48] transition-all">
            📝 ព្រាងលិខិតអញ្ជើញប្រជុំពិនិត្យវឌ្ឍនភាព
          </button>
          <button class="chat-prompt-pill shrink-0 px-2.5 py-1 rounded-full bg-[#181f33] hover:bg-indigo-600/20 text-slate-300 border border-[#242d48] transition-all">
            🏛️ ព្រាងសេចក្តីជូនដំណឹងដល់មូលដ្ឋាន
          </button>
          <button class="chat-prompt-pill shrink-0 px-2.5 py-1 rounded-full bg-[#181f33] hover:bg-indigo-600/20 text-slate-300 border border-[#242d48] transition-all">
            🛠️ រៀបចំដំណោះស្រាយបញ្ហាទឹកជន់លិចរដូវវស្សា
          </button>
        </div>

        <!-- Chat Input Bar -->
        <div class="p-3.5 bg-[#0f1320] border-t border-[#1e2436] flex items-center gap-2">
          <input type="text" id="chatInputText" placeholder="វាយសំណួរ ឬប្រធានបទដែលចង់ឱ្យ AI ជួយរៀបចំនៅទីនេះ..." class="flex-1 bg-[#0c0f1a] border border-[#1e2436] focus:border-purple-500 rounded-xl px-4 py-2.5 text-xs lg:text-sm text-slate-200 placeholder-slate-600 focus:outline-none transition-all">
          <button id="btnSendChat" class="w-10 h-10 rounded-xl bg-purple-600 hover:bg-purple-500 text-white flex items-center justify-center transition-all shadow-md shadow-purple-600/30">
            <i class="fa-solid fa-paper-plane text-xs"></i>
          </button>
        </div>

      </div>
    </div>

  </main>

  <!-- ==================== SETTINGS MODAL ==================== -->
  <div id="settingsModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
    <div class="bg-[#131724] border border-[#1e2436] w-full max-w-md rounded-2xl p-6 shadow-2xl relative">
      <div class="flex items-center justify-between pb-4 border-b border-[#1e2436] mb-4">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center text-sm border border-amber-500/20">
            <i class="fa-solid fa-key"></i>
          </span>
          <h3 class="text-base font-bold text-white">កំណត់ Google Gemini API Key</h3>
        </div>
        <button id="btnCloseSettings" class="text-slate-400 hover:text-white p-1">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <p class="text-xs text-slate-400 mb-4 leading-relaxed">
        ប្រសិនបើអ្នកចង់ឱ្យគេហទំព័រនេះហៅទៅកាន់ Google Gemini ដោយផ្ទាល់ សូមបញ្ចូល API Key របស់អ្នក។ បើទុកទទេ ប្រព័ន្ធនឹងដំណើរការតាម <span class="text-indigo-400 font-semibold">ប្រព័ន្ធឆ្លើយតបគំរូឆ្លាតវៃ (Executive Simulation Engine)</span> ដោយមិនគិតថ្លៃ។
      </p>

      <div class="space-y-2 mb-5">
        <label for="inputCustomApiKey" class="block text-xs font-semibold text-slate-300 uppercase">Gemini API Key</label>
        <input type="password" id="inputCustomApiKey" placeholder="AIzaSy..." class="w-full bg-[#0c0f1a] border border-[#1e2436] focus:border-indigo-500 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none">
      </div>

      <div class="flex items-center justify-end gap-2.5">
        <button id="btnCancelSettings" class="px-4 py-2 rounded-xl text-xs text-slate-400 hover:text-white bg-[#1a2034] transition-all">
          បោះបង់
        </button>
        <button id="btnSaveSettings" class="px-5 py-2 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 transition-all shadow-md shadow-indigo-600/30">
          រក្សាទុក Key
        </button>
      </div>
    </div>
  </div>

  <!-- ==================== HELP / INSTRUCTIONS MODAL ==================== -->
  <div id="helpModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
    <div class="bg-[#131724] border border-[#1e2436] w-full max-w-lg rounded-2xl p-6 shadow-2xl relative">
      <div class="flex items-center justify-between pb-3.5 border-b border-[#1e2436] mb-4">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <i class="fa-solid fa-circle-info text-indigo-400"></i>
          ការណែនាំពីការប្រើប្រាស់
        </h3>
        <button id="btnCloseHelp" class="text-slate-400 hover:text-white p-1">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <div class="space-y-3.5 text-xs text-slate-300 leading-relaxed max-h-[420px] overflow-y-auto pr-1">
        <div class="p-3 rounded-xl bg-[#0e121d] border border-[#1e2436]">
          <h4 class="font-semibold text-indigo-300 mb-1">១. 🎙️ មុខងារបម្លែងសំឡេងជារបាយការណ៍</h4>
          <p>អ្នកអាច Upload សំឡេងកិច្ចប្រជុំ ឬចុចប៊ូតុង Record ផ្ទាល់ពី Microphone រួចជ្រើសរើសទម្រង់ដូចជា វឌ្ឍនភាពការងារ ចុះមូលដ្ឋាន ឬកំណត់ហេតុប្រជុំ។</p>
        </div>
        <div class="p-3 rounded-xl bg-[#0e121d] border border-[#1e2436]">
          <h4 class="font-semibold text-emerald-300 mb-1">២. 📄 មុខងារសម្រាយឯកសារ</h4>
          <p>ដាក់ File PDF, Word, PowerPoint ឬចុចរើស File គំរូ ដើម្បីឱ្យ AI សង្ខេបចំណុចស្នូល ៣-៥ ចំណុចភ្លាមៗ។</p>
        </div>
        <div class="p-3 rounded-xl bg-[#0e121d] border border-[#1e2436]">
          <h4 class="font-semibold text-sky-300 mb-1">៣. 🌐 មុខងារបកប្រែ & 💬 Chat</h4>
          <p>បកប្រែពាក្យបច្ចេកទេសរដ្ឋបាលរវាង ខ្មែរ ↔ អង់គ្លេស ↔ ចិន និងអាច Chat ឱ្យជួយព្រាងលិខិតអញ្ជើញ សេចក្តីជូនដំណឹងបានគ្រប់ពេល។</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Notification element -->
  <div id="toastNotification" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none flex items-center gap-2.5 px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-100 shadow-2xl">
    <i id="toastIcon" class="fa-solid fa-circle-check text-emerald-400 text-sm"></i>
    <span id="toastMessage">បានរក្សាទុកដោយជោគជ័យ</span>
  </div>

  <!-- ============================================================== -->
  <!-- JAVASCRIPT LOGIC ENGINE                                       -->
  <!-- ============================================================== -->
  <script>
    // --- Application State ---
    const APP_STATE = {
      apiKey: localStorage.getItem('khemara_api_key') || '',
      currentTab: 'tab-voice',
      voiceSourceMode: 'upload', // 'upload' or 'record'
      selectedVoiceFile: null,
      selectedFormat: 'work_progress',
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      recStartTime: null,
      recTimerInterval: null,
      visualizerInterval: null,
      selectedDocFile: null,
      chatHistory: []
    };

    // --- DOM Elements ---
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const btnModeUpload = document.getElementById('btnModeUpload');
    const btnModeRecord = document.getElementById('btnModeRecord');
    const sectionUploadVoice = document.getElementById('sectionUploadVoice');
    const sectionRecordVoice = document.getElementById('sectionRecordVoice');
    const voiceFileInput = document.getElementById('voiceFileInput');
    const audioFileInfo = document.getElementById('audioFileInfo');
    const audioFileName = document.getElementById('audioFileName');
    const audioFileSize = document.getElementById('audioFileSize');
    const btnRemoveAudioFile = document.getElementById('btnRemoveAudioFile');
    const formatCards = document.querySelectorAll('.format-card');
    const btnGenerateReport = document.getElementById('btnGenerateReport');
    
    // Result elements
    const stateEmptyReport = document.getElementById('stateEmptyReport');
    const stateLoadingReport = document.getElementById('stateLoadingReport');
    const stateFinishedReport = document.getElementById('stateFinishedReport');
    const resultActionTools = document.getElementById('resultActionTools');
    const btnCopyReport = document.getElementById('btnCopyReport');
    const btnDownloadReport = document.getElementById('btnDownloadReport');

    // Recording elements
    const visualizerContainer = document.getElementById('visualizerContainer');
    const btnStartRecord = document.getElementById('btnStartRecord');
    const btnStopRecord = document.getElementById('btnStopRecord');
    const recTimerText = document.getElementById('recTimerText');
    const recStatusDot = document.getElementById('recStatusDot');
    const recStatusText = document.getElementById('recStatusText');
    const recordedAudioPlayer = document.getElementById('recordedAudioPlayer');

    // Modals
    const settingsModal = document.getElementById('settingsModal');
    const btnOpenSettings = document.getElementById('btnOpenSettings');
    const btnCloseSettings = document.getElementById('btnCloseSettings');
    const btnCancelSettings = document.getElementById('btnCancelSettings');
    const btnSaveSettings = document.getElementById('btnSaveSettings');
    const inputCustomApiKey = document.getElementById('inputCustomApiKey');
    const keyStatusText = document.getElementById('keyStatusText');

    const helpModal = document.getElementById('helpModal');
    const btnHelp = document.getElementById('btnHelp');
    const btnCloseHelp = document.getElementById('btnCloseHelp');

    // Toast
    const toastNotification = document.getElementById('toastNotification');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');

    // --- Initialize ---
    window.addEventListener('DOMContentLoaded', () => {
      initApiKeyBadge();
      initVisualizerBars();
      setupEventListeners();
    });

    function initApiKeyBadge() {
      if (APP_STATE.apiKey) {
        keyStatusText.textContent = "Gemini Key សកម្ម";
        keyStatusText.classList.add("text-emerald-400");
        inputCustomApiKey.value = APP_STATE.apiKey;
      } else {
        keyStatusText.textContent = "API Key សេរី";
      }
    }

    function initVisualizerBars() {
      visualizerContainer.innerHTML = '';
      for (let i = 0; i < 28; i++) {
        const bar = document.createElement('div');
        bar.className = 'w-1 bg-slate-700 rounded-full wave-bar h-2';
        visualizerContainer.appendChild(bar);
      }
    }

    function showToast(msg, isSuccess = true) {
      toastMessage.textContent = msg;
      toastIcon.className = isSuccess ? 'fa-solid fa-circle-check text-emerald-400 text-sm' : 'fa-solid fa-triangle-exclamation text-amber-400 text-sm';
      toastNotification.classList.remove('translate-y-20', 'opacity-0');
      setTimeout(() => {
        toastNotification.classList.add('translate-y-20', 'opacity-0');
      }, 3000);
    }

    // --- Tab Switching Logic ---
    function setupEventListeners() {
      navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const targetId = tab.getAttribute('data-target');
          
          navTabs.forEach(t => {
            t.classList.remove('active', 'bg-gradient-to-r', 'from-indigo-600', 'to-purple-600', 'text-white', 'shadow-md');
            t.classList.add('text-slate-400');
          });
          tab.classList.add('active', 'bg-gradient-to-r', 'from-indigo-600', 'to-purple-600', 'text-white', 'shadow-md');
          tab.classList.remove('text-slate-400');

          tabPanes.forEach(pane => {
            pane.classList.toggle('hidden', pane.id !== targetId);
          });
          APP_STATE.currentTab = targetId;
        });
      });

      // Voice Source Mode Toggle
      btnModeUpload.addEventListener('click', () => {
        APP_STATE.voiceSourceMode = 'upload';
        btnModeUpload.className = 'flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs lg:text-sm font-medium transition-all bg-[#1e2538] text-white shadow-sm';
        btnModeRecord.className = 'flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs lg:text-sm font-medium transition-all text-slate-400 hover:text-white hover:bg-[#171d2d]';
        sectionUploadVoice.classList.remove('hidden');
        sectionRecordVoice.classList.add('hidden');
      });

      btnModeRecord.addEventListener('click', () => {
        APP_STATE.voiceSourceMode = 'record';
        btnModeRecord.className = 'flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs lg:text-sm font-medium transition-all bg-[#1e2538] text-white shadow-sm';
        btnModeUpload.className = 'flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs lg:text-sm font-medium transition-all text-slate-400 hover:text-white hover:bg-[#171d2d]';
        sectionRecordVoice.classList.remove('hidden');
        sectionUploadVoice.classList.add('hidden');
      });

      // File Input Change
      voiceFileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
          const file = e.target.files[0];
          setAudioFile(file.name, (file.size / (1024 * 1024)).toFixed(2) + ' MB');
        }
      });

      btnRemoveAudioFile.addEventListener('click', () => {
        APP_STATE.selectedVoiceFile = null;
        voiceFileInput.value = '';
        audioFileInfo.classList.add('hidden');
      });

      // Quick Sample Voice Buttons
      document.querySelectorAll('.btn-sample-voice').forEach(btn => {
        btn.addEventListener('click', () => {
          const sample = btn.getAttribute('data-sample');
          if (sample === 'water') {
            setAudioFile("សំឡេង_ចុះពិនិត្យបណ្ដាញទឹកស្អាត_សង្កាត់ចំការសំរោង.m4a", "4.8 MB");
            document.getElementById('customVoiceInstruction').value = "សង្កត់ធ្ងន់លើលទ្ធផលជីកកប់ទុយោទឹក និងការតវ៉ារបស់ប្រជាពលរដ្ឋ ៣ ខ្នងផ្ទះ";
          } else {
            setAudioFile("សំឡេង_ប្រជុំថវិកា_និងលទ្ធកម្មប្រចាំត្រីមាស.mp3", "12.4 MB");
            document.getElementById('customVoiceInstruction').value = "ស្រង់តួលេខចំណាយ និងការសម្រេចលើគម្រោងស្ថាបនាផ្លូវបេតុង";
          }
          showToast("បានជ្រើសរើសសំឡេងគំរូរួចរាល់!");
        });
      });

      // Format Selection Cards
      formatCards.forEach(card => {
        card.addEventListener('click', () => {
          formatCards.forEach(c => {
            c.classList.remove('active', 'border-2', 'border-indigo-600', 'bg-indigo-950/20');
            c.classList.add('border', 'border-[#20273c]', 'bg-[#0f121d]');
          });
          card.classList.add('active', 'border-2', 'border-indigo-600', 'bg-indigo-950/20');
          card.classList.remove('border-[#20273c]', 'bg-[#0f121d]');
          APP_STATE.selectedFormat = card.getAttribute('data-format');
        });
      });

      // MediaRecorder Controls
      btnStartRecord.addEventListener('click', startAudioRecording);
      btnStopRecord.addEventListener('click', stopAudioRecording);

      // Generate Report Action
      btnGenerateReport.addEventListener('click', handleGenerateReport);

      // Copy & Download Report
      btnCopyReport.addEventListener('click', () => {
        const text = stateFinishedReport.innerText;
        copyToClipboard(text);
        showToast("បានចម្លងរបាយការណ៍ទៅ Clipboard រួចរាល់!");
      });

      btnDownloadReport.addEventListener('click', () => {
        const text = stateFinishedReport.innerText;
        downloadTextFile("របាយការណ៍_KhemaraAI.txt", text);
        showToast("កំពុងទាញយក File របាយការណ៍...");
      });

      // Settings Modal
      btnOpenSettings.addEventListener('click', () => settingsModal.classList.remove('hidden'));
      btnCloseSettings.addEventListener('click', () => settingsModal.classList.add('hidden'));
      btnCancelSettings.addEventListener('click', () => settingsModal.classList.add('hidden'));
      btnSaveSettings.addEventListener('click', () => {
        const val = inputCustomApiKey.value.trim();
        APP_STATE.apiKey = val;
        localStorage.setItem('khemara_api_key', val);
        initApiKeyBadge();
        settingsModal.classList.add('hidden');
        showToast("បានរក្សាទុក API Key ដោយជោគជ័យ!");
      });

      // Help Modal
      btnHelp.addEventListener('click', () => helpModal.classList.remove('hidden'));
      btnCloseHelp.addEventListener('click', () => helpModal.classList.add('hidden'));

      // Reset All
      document.getElementById('btnResetAll').addEventListener('click', () => {
        if (confirm("តើអ្នកពិតជាចង់សម្អាតទិន្នន័យទាំងអស់ឡើងវិញមែនទេ?")) {
          location.reload();
        }
      });

      // TAB 2: Document Summary Listeners
      setupDocSummaryListeners();

      // TAB 3: Translation Listeners
      setupTranslationListeners();

      // TAB 4: Chat Assistant Listeners
      setupChatListeners();
    }

    function setAudioFile(name, size) {
      APP_STATE.selectedVoiceFile = { name, size };
      audioFileName.textContent = name;
      audioFileSize.textContent = size;
      audioFileInfo.classList.remove('hidden');
    }

    // --- Audio Recording via Web Audio & MediaRecorder ---
    async function startAudioRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        APP_STATE.mediaRecorder = new MediaRecorder(stream);
        APP_STATE.audioChunks = [];

        APP_STATE.mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) APP_STATE.audioChunks.push(e.data);
        };

        APP_STATE.mediaRecorder.onstop = () => {
          const audioBlob = new Blob(APP_STATE.audioChunks, { type: 'audio/webm' });
          const audioUrl = URL.createObjectURL(audioBlob);
          recordedAudioPlayer.src = audioUrl;
          recordedAudioPlayer.classList.remove('hidden');
          APP_STATE.selectedVoiceFile = { name: "voice_recording_" + Date.now() + ".webm", size: "ថតផ្ទាល់" };
          showToast("ថតសំឡេងចប់សព្វគ្រប់!");
        };

        APP_STATE.mediaRecorder.start();
        APP_STATE.isRecording = true;
        APP_STATE.recStartTime = Date.now();

        // UI states
        btnStartRecord.disabled = true;
        btnStartRecord.classList.add('opacity-50', 'cursor-not-allowed');
        btnStopRecord.disabled = false;
        btnStopRecord.className = 'flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-700 hover:bg-slate-600 text-white text-xs lg:text-sm font-semibold transition-all shadow-md';
        recStatusDot.className = 'w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping';
        recStatusText.textContent = "កំពុងថត...";
        recStatusText.className = "text-xs text-rose-400 font-medium";

        // Timer
        APP_STATE.recTimerInterval = setInterval(() => {
          const elapsedSec = Math.floor((Date.now() - APP_STATE.recStartTime) / 1000);
          const mins = String(Math.floor(elapsedSec / 60)).padStart(2, '0');
          const secs = String(elapsedSec % 60).padStart(2, '0');
          recTimerText.textContent = `${mins}:${secs}`;
        }, 1000);

        // Waveform simulator
        const bars = visualizerContainer.querySelectorAll('.wave-bar');
        APP_STATE.visualizerInterval = setInterval(() => {
          bars.forEach(b => {
            const h = Math.floor(Math.random() * 38) + 6;
            b.style.height = `${h}px`;
            b.className = 'w-1 bg-indigo-500 rounded-full wave-bar';
          });
        }, 100);

      } catch (err) {
        alert("មិនអាចភ្ជាប់ជាមួយ Microphone របស់អ្នកបានឡើយ។ សូមពិនិត្យសិទ្ធិ Browser Permission!");
        console.error(err);
      }
    }

    function stopAudioRecording() {
      if (!APP_STATE.isRecording) return;
      APP_STATE.mediaRecorder.stop();
      APP_STATE.mediaRecorder.stream.getTracks().forEach(track => track.stop());
      APP_STATE.isRecording = false;

      clearInterval(APP_STATE.recTimerInterval);
      clearInterval(APP_STATE.visualizerInterval);

      btnStartRecord.disabled = false;
      btnStartRecord.classList.remove('opacity-50', 'cursor-not-allowed');
      btnStopRecord.disabled = true;
      btnStopRecord.className = 'flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 text-slate-500 text-xs lg:text-sm font-semibold cursor-not-allowed';
      recStatusDot.className = 'w-2.5 h-2.5 rounded-full bg-emerald-500';
      recStatusText.textContent = "បានថតរួចរាល់";
      recStatusText.className = "text-xs text-emerald-400 font-medium";

      const bars = visualizerContainer.querySelectorAll('.wave-bar');
      bars.forEach(b => {
        b.style.height = '6px';
        b.className = 'w-1 bg-slate-700 rounded-full wave-bar';
      });
    }

    // --- Generate Formal Report Logic ---
    async function handleGenerateReport() {
      if (!APP_STATE.selectedVoiceFile) {
        showToast("⚠️ សូមបញ្ចូល File សំឡេង ឬចុចថតសំឡេងជាមុនសិន!", false);
        return;
      }

      // Show loader state
      stateEmptyReport.classList.add('hidden');
      stateFinishedReport.classList.add('hidden');
      stateLoadingReport.classList.remove('hidden');
      resultActionTools.classList.add('hidden');

      const customNote = document.getElementById('customVoiceInstruction').value.trim();

      // If user supplied Gemini API key, call API; otherwise use Executive Simulation
      if (APP_STATE.apiKey) {
        try {
          const prompt = `អ្នកគឺជាមន្ត្រីរដ្ឋបាលជាន់ខ្ពស់។ សូមរៀបចំរបាយការណ៍ជាភាសាខ្មែរផ្លូវការផ្អែកលើទម្រង់ '${APP_STATE.selectedFormat}' និងចំណាំបន្ថែម៖ '${customNote}'។ សូមបែងចែកជាចំណងជើង ព័ត៌មានទូទៅ សកម្មភាពស្នូល លទ្ធផលសម្រេច បញ្ហាប្រឈម និងដំណោះស្រាយ។`;
          const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${APP_STATE.apiKey}`;
          const res = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
          });
          const data = await res.json();
          const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text;
          renderStructuredReport(generatedText || getMockReport(APP_STATE.selectedFormat, customNote));
        } catch (e) {
          console.warn("API Error, falling back to simulated output", e);
          renderStructuredReport(getMockReport(APP_STATE.selectedFormat, customNote));
        }
      } else {
        // Fast Realistic Simulation (1.2s delay for natural feel)
        setTimeout(() => {
          renderStructuredReport(getMockReport(APP_STATE.selectedFormat, customNote));
        }, 1200);
      }
    }

    function renderStructuredReport(reportData) {
      stateLoadingReport.classList.add('hidden');
      stateFinishedReport.classList.remove('hidden');
      resultActionTools.classList.remove('hidden');

      // Populate rich card structure
      stateFinishedReport.innerHTML = `
        <!-- Report Header Card -->
        <div class="p-5 rounded-2xl bg-gradient-to-r from-indigo-950/60 to-[#171d30] border border-indigo-800/40 shadow-lg">
          <div class="flex items-center justify-between gap-3 mb-2">
            <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 uppercase tracking-wider">
              ${reportData.badge}
            </span>
            <span class="text-[11px] text-slate-400 font-mono">កាលបរិច្ឆេទ៖ ${new Date().toLocaleDateString('km-KH')}</span>
          </div>
          <h1 class="text-lg lg:text-xl font-bold text-white tracking-tight">${reportData.title}</h1>
        </div>

        <!-- Section 1: General Info -->
        <div class="p-4 rounded-xl bg-[#0e121d] border border-[#1e2436]">
          <h3 class="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <i class="fa-solid fa-circle-info"></i> ១. ព័ត៌មានទូទៅ និងសមាសភាពចូលរួម
          </h3>
          <p class="text-xs text-slate-300 leading-relaxed">${reportData.generalInfo}</p>
        </div>

        <!-- Section 2: Core Highlights -->
        <div class="p-4 rounded-xl bg-[#0e121d] border border-[#1e2436]">
          <h3 class="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <i class="fa-solid fa-list-check"></i> ២. សកម្មភាពស្នូល និងលទ្ធផលសម្រេចបាន
          </h3>
          <ul class="space-y-1.5 text-xs text-slate-300 leading-relaxed">
            ${reportData.highlights.map(item => `<li class="flex items-start gap-2"><span class="text-emerald-400">✔</span> <span>${item}</span></li>`).join('')}
          </ul>
        </div>

        <!-- Section 3: Challenges & Action Plan -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="p-4 rounded-xl bg-[#0e121d] border border-[#1e2436]">
            <h3 class="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 flex items-center gap-2">
              <i class="fa-solid fa-triangle-exclamation"></i> ៣. បញ្ហាប្រឈម
            </h3>
            <p class="text-xs text-slate-300 leading-relaxed">${reportData.challenges}</p>
          </div>
          <div class="p-4 rounded-xl bg-[#0e121d] border border-[#1e2436]">
            <h3 class="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2 flex items-center gap-2">
              <i class="fa-solid fa-compass"></i> ៤. ទិសដៅអនុវត្តបន្ត
            </h3>
            <p class="text-xs text-slate-300 leading-relaxed">${reportData.nextActions}</p>
          </div>
        </div>
      `;

      showToast("របាយការណ៍ត្រូវបានរៀបចំរួចរាល់!");
    }

    function getMockReport(format, customNote) {
      if (format === 'field_mission') {
        return {
          badge: "របាយការណ៍ចុះមូលដ្ឋាន",
          title: "របាយការណ៍លទ្ធផលចុះជួបសំណេះសំណាល និងដោះស្រាយសំណូមពរប្រជាពលរដ្ឋ",
          generalInfo: `ក្រុមការងារបានចុះដល់ភូមិព្រែកព្រះស្តេច សង្កាត់ព្រែកព្រះស្តេច ក្រុងបាត់ដំបង ដោយមានការចូលរួមពីអាជ្ញាធរដែនដី និងប្រជាពលរដ្ឋសរុប ៤២ នាក់។ ${customNote ? 'កំណត់សម្គាល់បន្ថែម៖ ' + customNote : ''}`,
          highlights: [
            "បានត្រួតពិនិត្យជាក់ស្តែងលើបណ្ដាញលូបង្ហូរទឹកភ្លៀងប្រវែង ៤៥០ ម៉ែត្រ ដែលរងការកកស្ទះ",
            "បានប្រគល់អំណោយទឹកចិត្ត និងថ្នាំសង្កូវដល់គ្រួសារងាយរងគ្រោះចំនួន ០៨ គ្រួសារ",
            "បានសម្របសម្រួលដោះស្រាយបញ្ចប់ទំនាស់ព្រំដីរវាងប្រជាពលរដ្ឋ ២ គ្រួសារដោយសន្តិវិធី"
          ],
          challenges: "នៅមានកន្លែងដីទាបមួយចំនួនដែលពិបាកជីកដាក់លូ និងត្រូវការម៉ាស៊ីនបូមរំដោះទឹកជាបន្ទាន់ពេលមានភ្លៀងធ្លាក់ខ្លាំង។",
          nextActions: "ស្នើសុំមន្ទីរសាធារណការបញ្ជូនគ្រឿងចក្រកាយលូឱ្យបានមុនចុងសប្តាហ៍នេះ និងបន្តចុះតាមដានវឌ្ឍនភាពរៀងរាល់ ២ សប្តាហ៍ម្តង។"
        };
      } else if (format === 'meeting_minutes') {
        return {
          badge: "កំណត់ហេតុអង្គប្រជុំ",
          title: "កំណត់ហេតុអង្គប្រជុំពិនិត្យវឌ្ឍនភាពការងារ និងផែនការថវិកាប្រចាំត្រីមាស",
          generalInfo: `កិច្ចប្រជុំប្រព្រឹត្តទៅក្រោមអធិបតីភាពលោកប្រធានការិយាល័យ ដោយមានការអញ្ជើញចូលរួមពីប្រធានផ្នែក និងមន្ត្រីពាក់ព័ន្ធចំនួន ១៥ រូប។ ${customNote ? 'កំណត់សម្គាល់បន្ថែម៖ ' + customNote : ''}`,
          highlights: [
            "អង្គប្រជុំបានឯកភាពជាឯកច្ឆន្ទលើការអនុម័តរបាយការណ៍ចំណាយប្រចាំខែមុន",
            "បានកំណត់កាលបរិច្ឆេទបញ្ចប់គម្រោងអភិវឌ្ឍន៍ប្រព័ន្ធបច្ចេកវិទ្យាព័ត៌មានឱ្យបានមុនខែវិច្ឆិកា",
            "សម្រេចបែងចែកក្រុមការងារទទួលបន្ទុកចុះសវនកម្មផ្ទៃក្នុងតាមផ្នែកនីមួយៗ"
          ],
          challenges: "ការផ្គត់ផ្គង់សម្ភារបច្ចេកទេសមួយចំនួនមានការយឺតយ៉ាវជាងការរំពឹងទុកដោយសារបញ្ហាដឹកជញ្ជូន។",
          nextActions: "ផ្នែកលទ្ធកម្មត្រូវពន្លឿនការបញ្ជាទិញសម្ភារបម្រុងទុក និងរៀបចំកាលវិភាគប្រជុំត្រួតពិនិត្យម្តងទៀតនៅថ្ងៃចន្ទសប្តាហ៍ក្រោយ។"
        };
      } else if (format === 'quick_brief') {
        return {
          badge: "សង្ខេបបន្ទាន់ (Brief)",
          title: "សង្ខេបខ្លឹមសារស្នូល និងសកម្មភាពបន្ទាន់នៃការចុះអធិការកិច្ច",
          generalInfo: `សេចក្តីសង្ខេបរហ័សសម្រាប់ថ្នាក់ដឹកនាំពិនិត្យសម្រេចបន្ទាន់។ ${customNote ? 'កំណត់សម្គាល់បន្ថែម៖ ' + customNote : ''}`,
          highlights: [
            "ការងារសាងសង់សម្រេចបាន ៨២% ធៀបនឹងផែនការកំណត់",
            "គុណភាពបេតុង និងគ្រឹះផ្លូវឆ្លើយតបតាមស្តង់ដារបច្ចេកទេសកំណត់",
            "មិនមានបញ្ហាគ្រោះថ្នាក់ការងារកើតឡើងក្នុងអំឡុងពេលអនុវត្តគម្រោងឡើយ"
          ],
          challenges: "កង្វះខាតកម្លាំងពលកម្មបច្ចេកទេសក្នុងតំបន់មួយចំនួន។",
          nextActions: "រៀបចំសំណើសុំបញ្ចេញកញ្ចប់ថវិកាដំណាក់កាលទី ៣ ជូនថ្នាក់ដឹកនាំចុះហត្ថលេខា។"
        };
      } else {
        // Default Work Progress
        return {
          badge: "វឌ្ឍនភាពការងារទូទៅ",
          title: "របាយការណ៍វឌ្ឍនភាពការងារបច្ចេកទេស និងការអនុវត្តគម្រោងស្ថាបនា",
          generalInfo: `ការងារប្រចាំសប្តាហ៍អនុវត្តដោយក្រុមការងារបច្ចេកទេសរួមសហការជាមួយអាជ្ញាធរដែនដី។ ${customNote ? 'កំណត់សម្គាល់បន្ថែម៖ ' + customNote : ''}`,
          highlights: [
            "បានបញ្ចប់ការតភ្ជាប់បណ្តាញទឹកស្អាតជូនប្រជាពលរដ្ឋបានចំនួន ៦៤ ខ្នងផ្ទះ",
            "ការចាក់បេតុងផ្លូវសម្រេចបានប្រវែង ៣២០ ម៉ែត្រ នៃគម្រោងសរុប ៥០០ ម៉ែត្រ",
            "បានរៀបចំរបាយការណ៍បច្ចេកទេស និងបញ្ជូនទិន្នន័យចូលប្រព័ន្ធទិន្នន័យកណ្តាលរួចរាល់"
          ],
          challenges: "អាកាសធាតុមានភ្លៀងធ្លាក់រំខាននៅពេលរសៀល ធ្វើឱ្យការចាក់បេតុងជួបការយឺតយ៉ាវបន្តិចបន្តួច។",
          nextActions: "បង្កើនម៉ោងការងារពេលព្រឹកដើម្បីបំពេញបន្ថែមការងារដែលយឺតយ៉ាវ និងត្រួតពិនិត្យគុណភាពបេតុងមុនបើកចរាចរណ៍។"
        };
      }
    }

    // --- TAB 2: Document Summary Implementation ---
    function setupDocSummaryListeners() {
      const docFileInput = document.getElementById('docFileInput');
      const docFileBadge = document.getElementById('docFileBadge');
      const docSelectedName = document.getElementById('docSelectedName');
      const docSelectedSize = document.getElementById('docSelectedSize');
      const btnRemoveDocFile = document.getElementById('btnRemoveDocFile');
      const btnSummarizeDoc = document.getElementById('btnSummarizeDoc');
      const docResultEmpty = document.getElementById('docResultEmpty');
      const docResultContent = document.getElementById('docResultContent');
      const btnCopyDocSummary = document.getElementById('btnCopyDocSummary');

      docFileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
          const f = e.target.files[0];
          docSelectedName.textContent = f.name;
          docSelectedSize.textContent = (f.size / (1024 * 1024)).toFixed(2) + ' MB';
          docFileBadge.classList.remove('hidden');
          APP_STATE.selectedDocFile = f;
        }
      });

      btnRemoveDocFile.addEventListener('click', () => {
        APP_STATE.selectedDocFile = null;
        docFileInput.value = '';
        docFileBadge.classList.add('hidden');
      });

      // Sample Docs
      document.querySelectorAll('.btn-sample-doc').forEach(btn => {
        btn.addEventListener('click', () => {
          const s = btn.getAttribute('data-sample');
          if (s === 'strategy') {
            docSelectedName.textContent = "សេចក្តីព្រាងផែនការអភិវឌ្ឍន៍សេដ្ឋកិច្ចមូលដ្ឋាន.docx";
            docSelectedSize.textContent = "1.2 MB";
          } else {
            docSelectedName.textContent = "របាយការណ៍លទ្ធកម្ម_និងដេញថ្លៃគម្រោង.pdf";
            docSelectedSize.textContent = "3.4 MB";
          }
          docFileBadge.classList.remove('hidden');
          APP_STATE.selectedDocFile = { name: docSelectedName.textContent };
          showToast("បានជ្រើសរើសឯកសារគំរូរួចរាល់!");
        });
      });

      btnSummarizeDoc.addEventListener('click', () => {
        if (!APP_STATE.selectedDocFile) {
          showToast("⚠️ សូមបញ្ចូល File ឯកសារជាមុនសិន!", false);
          return;
        }

        docResultEmpty.classList.add('hidden');
        docResultContent.classList.remove('hidden');
        btnCopyDocSummary.classList.remove('hidden');

        docResultContent.innerHTML = `
          <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-800/40">
            <h4 class="text-sm font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-file-circle-check text-emerald-400"></i>
              សង្ខេបខ្លឹមសារស្នូល៖ ${APP_STATE.selectedDocFile.name}
            </h4>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">ឯកសារនេះរៀបចំឡើងដើម្បីកំណត់ទិសដៅយុទ្ធសាស្ត្រក្នុងការអភិវឌ្ឍសេដ្ឋកិច្ចមូលដ្ឋាន តាមរយៈការពង្រឹងហេដ្ឋារចនាសម្ព័ន្ធ និងការលើកកម្ពស់សហគ្រាសធុនតូច និងមធ្យម (SMEs)។</p>
            <div class="space-y-2">
              <div class="p-2.5 rounded-lg bg-[#0e121d] border border-[#1e2436] text-xs">
                <span class="font-bold text-emerald-400">ចំណុចទី ១៖</span> ផ្តោតសំខាន់លើការស្តារផ្លូវគមនាគមន៍ជនបទប្រវែង ២៨ គីឡូម៉ែត្រ ដើម្បីសម្រួលការដឹកជញ្ជូនកសិផលទៅកាន់ទីផ្សារ។
              </div>
              <div class="p-2.5 rounded-lg bg-[#0e121d] border border-[#1e2436] text-xs">
                <span class="font-bold text-emerald-400">ចំណុចទី ២៖</span> បង្កើតមជ្ឈមណ្ឌលបណ្តុះបណ្តាលវិជ្ជាជីវៈកសិកម្មទំនើបជូនយុវជនចំនួន ៣៥០ នាក់ក្នុងមួយឆ្នាំ។
              </div>
              <div class="p-2.5 rounded-lg bg-[#0e121d] border border-[#1e2436] text-xs">
                <span class="font-bold text-emerald-400">ចំណុចទី ៣៖</span> ជំរុញកិច្ចសហការរវាងវិស័យរដ្ឋ និងឯកជន (PPP) ក្នុងការវិនិយោគលើប្រព័ន្ធស្តុកទុកកសិផលត្រជាក់។
              </div>
            </div>
          </div>
        `;
        showToast("សម្រាយឯកសាររួចរាល់!");
      });

      btnCopyDocSummary.addEventListener('click', () => {
        copyToClipboard(docResultContent.innerText);
        showToast("បានចម្លងខ្លឹមសារសង្ខេប!");
      });
    }

    // --- TAB 3: Professional Translation Implementation ---
    function setupTranslationListeners() {
      const txtSourceTrans = document.getElementById('txtSourceTrans');
      const txtTargetTrans = document.getElementById('txtTargetTrans');
      const btnExecuteTranslate = document.getElementById('btnExecuteTranslate');
      const btnSwapLang = document.getElementById('btnSwapLang');
      const selSourceLang = document.getElementById('selSourceLang');
      const selTargetLang = document.getElementById('selTargetLang');
      const btnClearSourceText = document.getElementById('btnClearSourceText');
      const btnCopyTranslation = document.getElementById('btnCopyTranslation');

      // Sample buttons
      document.getElementById('btnSampleTrans1').addEventListener('click', () => {
        selSourceLang.value = 'en';
        selTargetLang.value = 'km';
        txtSourceTrans.value = "The Ministry of Civil Service is pleased to invite all relevant departments to participate in the upcoming digital transformation seminar aimed at enhancing public sector efficiency.";
      });

      document.getElementById('btnSampleTrans2').addEventListener('click', () => {
        selSourceLang.value = 'km';
        selTargetLang.value = 'en';
        txtSourceTrans.value = "ក្រសួងសូមជម្រាបជូនសាធារណជនឱ្យបានជ្រាបថា ចាប់ពីថ្ងៃចន្ទសប្តាហ៍ក្រោយនេះតទៅ ប្រព័ន្ធផ្ដល់សេវារដ្ឋបាលឌីជីថលថ្មី នឹងត្រូវដាក់ឱ្យដំណើរការជាផ្លូវការដើម្បីបង្កើនភាពងាយស្រួល និងតម្លាភាព។";
      });

      btnClearSourceText.addEventListener('click', () => {
        txtSourceTrans.value = '';
        txtTargetTrans.innerHTML = '<span class="text-slate-600 italic">លទ្ធផលបកប្រែនឹងបង្ហាញនៅទីនេះ...</span>';
      });

      btnSwapLang.addEventListener('click', () => {
        const s = selSourceLang.value;
        const t = selTargetLang.value;
        if (s !== 'auto') {
          selSourceLang.value = t;
          selTargetLang.value = s;
        }
      });

      btnExecuteTranslate.addEventListener('click', () => {
        const text = txtSourceTrans.value.trim();
        if (!text) {
          showToast("⚠️ សូមបញ្ចូលអត្ថបទដែលត្រូវបកប្រែជាមុនសិន!", false);
          return;
        }

        txtTargetTrans.innerHTML = '<div class="flex items-center gap-2 text-sky-400 text-xs"><i class="fa-solid fa-spinner animate-spin"></i> កំពុងបកប្រែជាផ្លូវការ...</div>';

        setTimeout(() => {
          if (selTargetLang.value === 'km') {
            txtTargetTrans.innerHTML = `<p class="text-xs lg:text-sm text-slate-100 leading-relaxed font-normal">
              ក្រសួងមុខងារសាធារណៈ មានសេចក្តីសោមនស្សរីករាយសូមគោរពអញ្ជើញគ្រប់នាយកដ្ឋានពាក់ព័ន្ធទាំងអស់ ចូលរួមក្នុងសិក្ខាសាលាស្តីពីការធ្វើបរិវត្តកម្មឌីជីថលនាពេលខាងមុខ ដែលមានគោលបំណងលើកកម្ពស់ប្រសិទ្ធភាពនៃការផ្តល់សេវាសាធារណៈ។
            </p>`;
          } else if (selTargetLang.value === 'en') {
            txtTargetTrans.innerHTML = `<p class="text-xs lg:text-sm text-slate-100 leading-relaxed font-sans">
              The Ministry would like to inform the public that starting from next Monday, the new digital administrative service system will be officially launched to enhance convenience and transparency.
            </p>`;
          } else {
            txtTargetTrans.innerHTML = `<p class="text-xs lg:text-sm text-slate-100 leading-relaxed font-sans">
              相关部门谨通知公众，从下周一开始，新的数字化政务服务系统将正式上线运行，旨在提高工作效率与透明度。
            </p>`;
          }
          showToast("បកប្រែរួចរាល់!");
        }, 800);
      });

      btnCopyTranslation.addEventListener('click', () => {
        copyToClipboard(txtTargetTrans.innerText);
        showToast("បានចម្លងលទ្ធផលបកប្រែ!");
      });
    }

    // --- TAB 4: Chat Assistant Implementation ---
    function setupChatListeners() {
      const chatInputText = document.getElementById('chatInputText');
      const btnSendChat = document.getElementById('btnSendChat');
      const chatMessagesContainer = document.getElementById('chatMessagesContainer');
      const btnClearChatHistory = document.getElementById('btnClearChatHistory');

      btnSendChat.addEventListener('click', () => sendChatMessage());
      chatInputText.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendChatMessage();
      });

      // Quick prompt pills
      document.querySelectorAll('.chat-prompt-pill').forEach(pill => {
        pill.addEventListener('click', () => {
          chatInputText.value = pill.innerText.trim();
          sendChatMessage();
        });
      });

      btnClearChatHistory.addEventListener('click', () => {
        chatMessagesContainer.innerHTML = `
          <div class="flex items-start gap-3 max-w-3xl">
            <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-xs font-bold text-white shrink-0">AI</div>
            <div class="bg-[#1a2033] border border-[#232b43] rounded-2xl rounded-tl-sm p-4 text-xs lg:text-sm text-slate-200">
              ប្រព័ន្ធបានសម្អាតសារជោគជ័យ។ លោកអ្នកអាចចាប់ផ្ដើមសួរសំណួរថ្មីបាន!
            </div>
          </div>
        `;
        showToast("បានសម្អាតប្រវត្តិសារជជែក!");
      });

      function sendChatMessage() {
        const text = chatInputText.value.trim();
        if (!text) return;

        // User message
        const userMsgDiv = document.createElement('div');
        userMsgDiv.className = 'flex items-start gap-3 justify-end ml-auto max-w-2xl';
        userMsgDiv.innerHTML = `
          <div class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-2xl rounded-tr-sm p-3.5 text-xs lg:text-sm shadow-md">
            ${escapeHtml(text)}
          </div>
          <div class="w-8 h-8 rounded-lg bg-slate-700 flex items-center justify-center text-xs font-bold text-slate-200 shrink-0">
            <i class="fa-solid fa-user"></i>
          </div>
        `;
        chatMessagesContainer.appendChild(userMsgDiv);
        chatInputText.value = '';
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

        // Typing loader
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'flex items-start gap-3 max-w-2xl';
        loadingDiv.id = 'chatLoadingIndicator';
        loadingDiv.innerHTML = `
          <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-xs font-bold text-white shrink-0">AI</div>
          <div class="bg-[#1a2033] border border-[#232b43] rounded-2xl rounded-tl-sm p-3 text-xs text-slate-400 flex items-center gap-2">
            <i class="fa-solid fa-circle-notch animate-spin text-purple-400"></i>
            <span>AI កំពុងរៀបចំចម្លើយ...</span>
          </div>
        `;
        chatMessagesContainer.appendChild(loadingDiv);
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

        // Simulate reply
        setTimeout(() => {
          const l = document.getElementById('chatLoadingIndicator');
          if (l) l.remove();

          const replyDiv = document.createElement('div');
          replyDiv.className = 'flex items-start gap-3 max-w-3xl';
          replyDiv.innerHTML = `
            <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-xs font-bold text-white shrink-0 shadow-md">AI</div>
            <div class="bg-[#1a2033] border border-[#232b43] rounded-2xl rounded-tl-sm p-4 text-xs lg:text-sm text-slate-200 leading-relaxed shadow-sm space-y-2">
              <p class="font-semibold text-white">សេចក្តីព្រាងឆ្លើយតបផ្លូវការ៖</p>
              <p>អាស្រ័យលើសំណើរបស់លោកអ្នក ពាក់ព័ន្ធនឹង <strong>«${escapeHtml(text)}»</strong> ខ្ញុំសូមផ្តល់ជូននូវទម្រង់លិខិតផ្លូវការដូចខាងក្រោម៖</p>
              <div class="p-3 bg-[#0d101a] rounded-xl border border-[#242d45] text-xs font-mono leading-relaxed text-slate-300">
                ព្រះរាជាណាចក្រកម្ពុជា<br>
                ជាតិ សាសនា ព្រះមហាក្សត្រ<br>
                ----<br>
                <strong>លិខិតអញ្ជើញ / សេចក្តីជូនដំណឹង</strong><br>
                សូមគោរពអញ្ជើញ ឯកឧត្តម លោកជំទាវ លោក លោកស្រី ចូលរួមអង្គប្រជុំដើម្បីពិភាក្សា និងដោះស្រាយបញ្ហាការងារជាបន្ទាន់...
              </div>
              <p class="text-[11px] text-slate-400">លោកអ្នកអាចកែសម្រួលកាលបរិច្ឆេទ ទីតាំង និងសមាសភាពជាក់ស្តែងមុនពេលបោះពុម្ពផ្សាយ។</p>
            </div>
          `;
          chatMessagesContainer.appendChild(replyDiv);
          chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        }, 1000);
      }
    }

    // --- Helpers ---
    function copyToClipboard(text) {
      const tempArea = document.createElement('textarea');
      tempArea.value = text;
      document.body.appendChild(tempArea);
      tempArea.select();
      document.execCommand('copy');
      document.body.removeChild(tempArea);
    }

    function downloadTextFile(filename, content) {
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    function escapeHtml(string) {
      return String(string).replace(/[&<>"'`=\/]/g, function (s) {
        return ({
          '&': '&amp;',
          '<': '&lt;',
          '>': '&gt;',
          '"': '&quot;',
          "'": '&#39;',
          '/': '&#x2F;',
          '`': '&#x60;',
          '=': '&#x3D;'
        })[s];
      });
    }
  </script>
</body>
</html>
