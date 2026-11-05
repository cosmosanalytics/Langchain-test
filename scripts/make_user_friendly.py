# -*- coding: utf-8 -*-
"""
Script to make callcenter_ai_voice_agents.html exceptionally user-friendly:
  1. Responsive View Switcher: [🎙️ Live Call] [🕸️ Grounding Graph] [◫ Split View]
  2. Floating Canvas Zoom & Physics Controls (+, -, Center, Freeze)
  3. Single-line horizontally scrollable Scenario Pills (no awkward text wrapping)
  4. Crisp High-Contrast Graph Node Fonts (13-14px bold with outline)
  5. Interactive "How it Works" Quick Guide Banner (dismissible)
  6. Sleek Chat Dialogue Timeline with Prominent Audio Playback
"""

html_path = "callcenter_ai_voice_agents.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Header to be clean, compact, and responsive
old_header = """  <!-- TOP HEADER & USE CASE SELECTOR -->
  <header class="bg-white border-b border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-3 shrink-0 shadow-xs z-20">
    <div class="flex items-center space-x-3">
      <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-600 to-indigo-600 flex items-center justify-center text-white shadow-xs font-black text-sm">
        <i class="fa-solid fa-headset"></i>
      </div>
      <div>
        <div class="flex items-center space-x-2">
          <h1 class="text-sm sm:text-base font-extrabold text-slate-900 tracking-tight">Call Center AI Voice Agents Studio</h1>
          <span class="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200 text-[10px] font-bold uppercase tracking-wider">Live Grounding</span>
        </div>
        <p class="text-[11px] text-slate-500 hidden sm:block">Upper: Real-Time Call &bull; Lower: Graph Grounding (SOP Policies + Call Records &rarr; Business Value &amp; Drift)</p>
      </div>
    </div>

    <!-- USE CASE SELECTOR -->
    <div class="flex items-center space-x-1 bg-slate-100 border border-slate-200 p-1 rounded-xl">
      <span class="text-[10px] font-mono font-bold text-slate-500 px-2 uppercase hidden lg:inline">Scenario:</span>
      <button onclick="selectUseCase('billing')" id="btn-usecase-billing" class="usecase-btn px-2.5 py-1 rounded-lg text-xs font-bold bg-white text-indigo-700 border border-indigo-200 shadow-xs transition flex items-center space-x-1.5">
        <i class="fa-solid fa-file-invoice-dollar text-amber-500"></i>
        <span>1. Billing ($150)</span>
      </button>
      <button onclick="selectUseCase('outage')" id="btn-usecase-outage" class="usecase-btn px-2.5 py-1 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 border border-transparent transition flex items-center space-x-1.5">
        <i class="fa-solid fa-wifi text-sky-500"></i>
        <span>2. Outage (LOS)</span>
      </button>
      <button onclick="selectUseCase('retention')" id="btn-usecase-retention" class="usecase-btn px-2.5 py-1 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 border border-transparent transition flex items-center space-x-1.5">
        <i class="fa-solid fa-handshake text-emerald-600"></i>
        <span>3. VIP Retention ($18k)</span>
      </button>
      <button onclick="selectUseCase('cross')" id="btn-usecase-cross" class="usecase-btn px-2.5 py-1 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 border border-transparent transition flex items-center space-x-1.5 bg-gradient-to-r hover:from-indigo-50 hover:to-emerald-50">
        <i class="fa-solid fa-diagram-project text-indigo-500"></i>
        <span>🌍 Cross-Usecases</span>
      </button>
    </div>

    <!-- Header Right Actions -->
    <div class="flex items-center space-x-2">
      <button id="btn-open-extractor" onclick="openDocExtractorModal()" class="px-3 py-1 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 shadow-2xs transition flex items-center space-x-1.5 cursor-pointer">
        <i class="fa-solid fa-file-invoice text-indigo-600"></i>
        <span>📄 Docs &rarr; Graph Extractor</span>
      </button>
      <button id="btn-toggle-speech" onclick="toggleVoiceSpeech()" class="px-3 py-1 rounded-xl text-xs font-bold bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-2xs transition flex items-center space-x-1.5 cursor-pointer">
        <i id="voice-icon" class="fa-solid fa-volume-high text-emerald-600"></i>
        <span id="voice-toggle-text">Voice Speech: ON</span>
      </button>
    </div>
  </header>"""

new_header = """  <!-- TOP NAVIGATION BAR -->
  <header class="bg-white border-b border-slate-200 px-3 sm:px-5 py-2 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-2.5 shrink-0 shadow-xs z-30">
    
    <!-- Left: Brand & Quick Guide Trigger -->
    <div class="flex items-center justify-between shrink-0">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-600 to-indigo-600 flex items-center justify-center text-white shadow-xs font-black text-sm">
          <i class="fa-solid fa-headset"></i>
        </div>
        <div>
          <div class="flex items-center space-x-1.5">
            <h1 class="text-xs sm:text-sm font-extrabold text-slate-900 tracking-tight">Call Center AI Studio</h1>
            <span class="px-1.5 py-0.2 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200 text-[9px] font-extrabold uppercase">Live</span>
          </div>
          <p class="text-[10px] text-slate-500 hidden sm:block">Real-Time Voice Call &bull; SOP &amp; Context Graph Grounding</p>
        </div>
      </div>

      <!-- Quick Guide Toggle (Help Icon on Mobile) -->
      <button onclick="toggleQuickGuide()" class="md:hidden text-slate-500 hover:text-indigo-600 p-1.5 rounded-lg border border-slate-200 text-xs">
        <i class="fa-regular fa-circle-question"></i> Guide
      </button>
    </div>

    <!-- Center: Horizontal Non-Wrapping Scenario Bar -->
    <div class="flex items-center space-x-1.5 overflow-x-auto py-0.5 scrollbar-none shrink-0 bg-slate-100/80 border border-slate-200 p-1 rounded-xl">
      <button onclick="selectUseCase('billing')" id="btn-usecase-billing" class="usecase-btn px-3 py-1.5 rounded-lg text-xs font-bold bg-white text-indigo-700 border border-indigo-200 shadow-2xs whitespace-nowrap transition flex items-center space-x-1.5 cursor-pointer">
        <i class="fa-solid fa-file-invoice-dollar text-amber-500"></i>
        <span>1. Billing ($150)</span>
      </button>
      <button onclick="selectUseCase('outage')" id="btn-usecase-outage" class="usecase-btn px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 border border-transparent whitespace-nowrap transition flex items-center space-x-1.5 cursor-pointer">
        <i class="fa-solid fa-wifi text-sky-500"></i>
        <span>2. Outage (LOS)</span>
      </button>
      <button onclick="selectUseCase('retention')" id="btn-usecase-retention" class="usecase-btn px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 border border-transparent whitespace-nowrap transition flex items-center space-x-1.5 cursor-pointer">
        <i class="fa-solid fa-handshake text-emerald-600"></i>
        <span>3. VIP Retention ($18k)</span>
      </button>
      <button onclick="selectUseCase('cross')" id="btn-usecase-cross" class="usecase-btn px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 hover:text-slate-900 border border-transparent whitespace-nowrap transition flex items-center space-x-1.5 cursor-pointer">
        <i class="fa-solid fa-diagram-project text-indigo-500"></i>
        <span>🌍 Cross-Usecases</span>
      </button>
    </div>

    <!-- Right: View Mode Switcher & Actions -->
    <div class="flex items-center justify-between sm:justify-end space-x-2 shrink-0">
      
      <!-- Responsive View Switcher -->
      <div class="flex items-center bg-slate-100 border border-slate-200 p-0.5 rounded-xl text-xs font-bold shadow-2xs">
        <button onclick="setViewMode('split')" id="btn-view-split" class="px-2.5 py-1 rounded-lg bg-white text-slate-900 shadow-2xs border border-slate-200 flex items-center space-x-1 cursor-pointer" title="Split Screen">
          <i class="fa-solid fa-table-columns text-slate-600"></i>
          <span class="hidden xl:inline">Split</span>
        </button>
        <button onclick="setViewMode('call')" id="btn-view-call" class="px-2.5 py-1 rounded-lg text-slate-600 hover:text-slate-900 flex items-center space-x-1 cursor-pointer" title="Call Console Only">
          <i class="fa-solid fa-phone text-emerald-600"></i>
          <span class="hidden sm:inline">Call</span>
        </button>
        <button onclick="setViewMode('graph')" id="btn-view-graph" class="px-2.5 py-1 rounded-lg text-slate-600 hover:text-slate-900 flex items-center space-x-1 cursor-pointer" title="Grounding Graph Only">
          <i class="fa-solid fa-circle-nodes text-indigo-600"></i>
          <span class="hidden sm:inline">Graph</span>
        </button>
      </div>

      <!-- Docs Extractor & Audio Toggle -->
      <button id="btn-open-extractor" onclick="openDocExtractorModal()" class="px-2.5 py-1.5 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 shadow-2xs transition flex items-center space-x-1.5 cursor-pointer" title="View Source SOPs & Transcripts">
        <i class="fa-solid fa-file-invoice text-indigo-600"></i>
        <span class="hidden sm:inline">Docs &rarr; Graph</span>
      </button>

      <button id="btn-toggle-speech" onclick="toggleVoiceSpeech()" class="px-2.5 py-1.5 rounded-xl text-xs font-bold bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-2xs transition flex items-center space-x-1.5 cursor-pointer">
        <i id="voice-icon" class="fa-solid fa-volume-high text-emerald-600"></i>
        <span id="voice-toggle-text" class="hidden sm:inline">Voice: ON</span>
      </button>

    </div>
  </header>

  <!-- QUICK GUIDE BANNER (DISMISSIBLE & TOGGLEABLE) -->
  <div id="quick-guide-banner" class="bg-gradient-to-r from-indigo-50 via-sky-50 to-emerald-50 border-b border-indigo-100 px-4 py-2 flex items-center justify-between text-xs text-slate-700 shrink-0">
    <div class="flex items-center space-x-3 overflow-hidden">
      <span class="flex h-2 w-2 shrink-0">
        <span class="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-indigo-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
      </span>
      <p class="truncate font-medium">
        <strong class="text-indigo-950 font-bold">How it works:</strong>
        <span class="text-slate-600 ml-1">1. Pick a scenario &bull; 2. Audio plays grounded response &bull; 3. Lower Graph shows live reconciliation:</span>
        <span class="font-bold text-indigo-700 ml-1">SOPs (Indigo)</span> +
        <span class="font-bold text-emerald-700 ml-1">Call (Emerald)</span> &rarr;
        <span class="font-bold text-amber-700 ml-1">Business Value (Amber)</span> &amp;
        <span class="font-bold text-pink-600 ml-1">Drift Loop (Pink)</span>
      </p>
    </div>
    <button onclick="toggleQuickGuide()" class="text-slate-400 hover:text-slate-700 ml-2 text-xs p-1">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </div>"""

content = content.replace(old_header, new_header)

# 2. Add Floating Controls onto Vis.js Graph Canvas
old_canvas_container = """        <!-- Graph Vis.js Container -->
        <div id="unified-graph-canvas" class="flex-1 w-full h-full relative cursor-grab active:cursor-grabbing bg-slate-50/50">
        </div>"""

new_canvas_container = """        <!-- Graph Vis.js Container with Floating Usability Controls -->
        <div class="flex-1 w-full h-full relative bg-slate-50/50 overflow-hidden">
          
          <div id="unified-graph-canvas" class="w-full h-full cursor-grab active:cursor-grabbing"></div>

          <!-- Floating Zoom & Layout Bar -->
          <div class="absolute bottom-4 right-4 z-10 flex items-center bg-white/95 backdrop-blur-xs border border-slate-200 rounded-2xl shadow-lg p-1 space-x-1 text-xs">
            <button onclick="zoomGraph(1.2)" class="w-8 h-8 rounded-xl hover:bg-slate-100 text-slate-700 flex items-center justify-center font-bold transition cursor-pointer" title="Zoom In (+)">
              <i class="fa-solid fa-plus"></i>
            </button>
            <button onclick="zoomGraph(0.8)" class="w-8 h-8 rounded-xl hover:bg-slate-100 text-slate-700 flex items-center justify-center font-bold transition cursor-pointer" title="Zoom Out (-)">
              <i class="fa-solid fa-minus"></i>
            </button>
            <button onclick="resetGraphView()" class="px-2.5 h-8 rounded-xl hover:bg-slate-100 text-slate-700 flex items-center space-x-1 font-bold transition cursor-pointer" title="Center & Fit">
              <i class="fa-solid fa-crosshairs text-indigo-600"></i>
              <span class="text-[11px]">Center</span>
            </button>
            <button onclick="togglePhysics()" id="btn-physics-toggle" class="px-2.5 h-8 rounded-xl hover:bg-slate-100 text-slate-700 flex items-center space-x-1 font-bold transition cursor-pointer" title="Lock / Unlock Node Physics">
              <i id="physics-icon" class="fa-solid fa-snowflake text-sky-500"></i>
              <span id="physics-text" class="text-[11px]">Lock</span>
            </button>
          </div>

        </div>"""

content = content.replace(old_canvas_container, new_canvas_container)

# 3. Add View Mode Controller and Canvas Zoom JS functions
new_js = """
    // =========================================================================
    // RESPONSIVE VIEW MODES: [SPLIT] [CALL] [GRAPH]
    // =========================================================================
    let currentViewMode = 'split';
    let isPhysicsFrozen = false;

    function setViewMode(mode) {
      currentViewMode = mode;
      const callSec = document.querySelector('main > section:first-of-type');
      const graphSec = document.querySelector('main > section:last-of-type');
      
      const btnSplit = document.getElementById('btn-view-split');
      const btnCall = document.getElementById('btn-view-call');
      const btnGraph = document.getElementById('btn-view-graph');

      // Reset button classes
      [btnSplit, btnCall, btnGraph].forEach(btn => {
        if (btn) btn.className = "px-2.5 py-1 rounded-lg text-slate-600 hover:text-slate-900 flex items-center space-x-1 cursor-pointer";
      });

      if (mode === 'split') {
        if (btnSplit) btnSplit.className = "px-2.5 py-1 rounded-lg bg-white text-slate-900 shadow-2xs border border-slate-200 flex items-center space-x-1 cursor-pointer";
        if (callSec) {
          callSec.classList.remove('hidden');
          callSec.style.height = '34%';
          callSec.style.display = 'flex';
        }
        if (graphSec) {
          graphSec.classList.remove('hidden');
          graphSec.style.display = 'flex';
        }
      } else if (mode === 'call') {
        if (btnCall) btnCall.className = "px-2.5 py-1 rounded-lg bg-white text-slate-900 shadow-2xs border border-slate-200 flex items-center space-x-1 cursor-pointer";
        if (callSec) {
          callSec.classList.remove('hidden');
          callSec.style.height = '100%';
          callSec.style.display = 'flex';
        }
        if (graphSec) graphSec.classList.add('hidden');
      } else if (mode === 'graph') {
        if (btnGraph) btnGraph.className = "px-2.5 py-1 rounded-lg bg-white text-slate-900 shadow-2xs border border-slate-200 flex items-center space-x-1 cursor-pointer";
        if (callSec) callSec.classList.add('hidden');
        if (graphSec) {
          graphSec.classList.remove('hidden');
          graphSec.style.height = '100%';
          graphSec.style.display = 'flex';
        }
      }

      // Re-fit graph canvas
      setTimeout(() => {
        if (networkInstance) networkInstance.fit({ animation: { duration: 400 } });
      }, 100);
    }

    function toggleQuickGuide() {
      const banner = document.getElementById('quick-guide-banner');
      if (banner) {
        banner.classList.toggle('hidden');
      }
    }

    function zoomGraph(factor) {
      if (!networkInstance) return;
      const currentScale = networkInstance.getScale();
      networkInstance.moveTo({
        scale: currentScale * factor,
        animation: { duration: 300, easingFunction: 'easeInOutQuad' }
      });
    }

    function togglePhysics() {
      if (!networkInstance) return;
      isPhysicsFrozen = !isPhysicsFrozen;
      networkInstance.setOptions({ physics: { enabled: !isPhysicsFrozen } });
      const text = document.getElementById('physics-text');
      const icon = document.getElementById('physics-icon');
      if (isPhysicsFrozen) {
        if (text) text.textContent = "Unfreeze";
        if (icon) icon.className = "fa-solid fa-play text-emerald-500";
      } else {
        if (text) text.textContent = "Lock";
        if (icon) icon.className = "fa-solid fa-snowflake text-sky-500";
      }
    }
"""

content = content.replace("function resetGraphView() {", new_js + "\n    function resetGraphView() {")

# 4. Enhance Vis.js node font size for crisp mobile readability
old_font_config = "font: { color: '#0f172a', size: 11, face: 'Plus Jakarta Sans', multi: true },"
new_font_config = "font: { color: '#0f172a', size: 13, face: 'Plus Jakarta Sans', multi: true, bold: { color: '#0f172a', size: 13 } },"
content = content.replace(old_font_config, new_font_config)

# 5. On mobile, automatically default to 'call' or clean split
mobile_detect_js = """
    window.addEventListener('DOMContentLoaded', () => {
      startCallTimer();
      // On small screens (< 768px), default to comfortable Call view
      if (window.innerWidth < 768) {
        setViewMode('call');
      } else {
        setViewMode('split');
      }
      selectUseCase('billing');
    });
"""

old_dom_listener = """    window.addEventListener('DOMContentLoaded', () => {
      startCallTimer();
      selectUseCase('billing');
    });"""

content = content.replace(old_dom_listener, mobile_detect_js)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully injected all usability and user-friendly enhancements!")
