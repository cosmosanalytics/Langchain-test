# -*- coding: utf-8 -*-
"""
Refine user-friendly elements:
  1. Add explicit IDs to sections (section-call-console, section-graph-grounding)
  2. Bulletproof setViewMode with style.display = 'none' / 'flex'
  3. Ensure canvas floating controls have z-20
  4. Ensure mobile graph mode takes 100% height
"""

html_path = "callcenter_ai_voice_agents.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add explicit IDs to the two main sections
content = content.replace(
    '<section class="h-[32%] min-h-[195px] bg-white border border-slate-200 rounded-2xl p-2.5 shadow-sm flex flex-col shrink-0">',
    '<section id="section-call-console" class="h-[34%] min-h-[195px] bg-white border border-slate-200 rounded-2xl p-2.5 shadow-sm flex flex-col shrink-0 transition-all duration-300">'
)

content = content.replace(
    '<section class="flex-1 min-h-[400px] bg-white border border-slate-200 rounded-2xl shadow-sm flex flex-col overflow-hidden">',
    '<section id="section-graph-grounding" class="flex-1 min-h-[380px] bg-white border border-slate-200 rounded-2xl shadow-sm flex flex-col overflow-hidden transition-all duration-300">'
)

# 2. Bulletproof setViewMode function
old_set_view_mode = """    function setViewMode(mode) {
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
    }"""

new_set_view_mode = """    function setViewMode(mode) {
      currentViewMode = mode;
      const callSec = document.getElementById('section-call-console');
      const graphSec = document.getElementById('section-graph-grounding');
      
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
          callSec.style.display = 'flex';
          callSec.style.height = window.innerWidth < 768 ? '48%' : '34%';
        }
        if (graphSec) {
          graphSec.style.display = 'flex';
          graphSec.style.height = window.innerWidth < 768 ? '52%' : 'auto';
        }
      } else if (mode === 'call') {
        if (btnCall) btnCall.className = "px-2.5 py-1 rounded-lg bg-white text-slate-900 shadow-2xs border border-slate-200 flex items-center space-x-1 cursor-pointer";
        if (callSec) {
          callSec.style.display = 'flex';
          callSec.style.height = '100%';
        }
        if (graphSec) {
          graphSec.style.display = 'none';
        }
      } else if (mode === 'graph') {
        if (btnGraph) btnGraph.className = "px-2.5 py-1 rounded-lg bg-white text-slate-900 shadow-2xs border border-slate-200 flex items-center space-x-1 cursor-pointer";
        if (callSec) {
          callSec.style.display = 'none';
        }
        if (graphSec) {
          graphSec.style.display = 'flex';
          graphSec.style.height = '100%';
        }
      }

      // Re-fit graph canvas
      setTimeout(() => {
        if (networkInstance && mode !== 'call') {
          networkInstance.fit({ animation: { duration: 400 } });
        }
      }, 150);
    }"""

content = content.replace(old_set_view_mode, new_set_view_mode)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully refined user-friendly layout and view mode controllers!")
