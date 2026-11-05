# -*- coding: utf-8 -*-
"""
Generate an interactive web presentation slide deck (presentation_deck.html)
with keyboard navigation, fullscreen mode, 16:9 responsive aspect ratio,
and download link for the PPTX file.
"""

import os

html_content = """<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-950">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation: Call Center AI Voice Agents Studio</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- FontAwesome 6 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
    .slide { display: none; }
    .slide.active { display: flex; }
  </style>
</head>
<body class="h-full flex flex-col justify-between overflow-hidden text-slate-800 select-none">

  <!-- TOP DECK CONTROL BAR -->
  <nav class="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-4 py-2.5 flex items-center justify-between text-white z-50 shrink-0">
    <div class="flex items-center space-x-3">
      <div class="w-7 h-7 rounded-lg bg-gradient-to-tr from-emerald-500 to-indigo-600 flex items-center justify-center text-xs font-black shadow-sm">
        <i class="fa-solid fa-headset"></i>
      </div>
      <div>
        <span class="text-xs sm:text-sm font-extrabold tracking-tight">Call Center AI Voice Agents Studio</span>
        <span class="text-[10px] text-slate-400 ml-2 hidden sm:inline">Executive Presentation Deck</span>
      </div>
    </div>

    <!-- Slide Indicators & Controls -->
    <div class="flex items-center space-x-2">
      <button onclick="prevSlide()" class="p-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-bold transition flex items-center space-x-1 cursor-pointer">
        <i class="fa-solid fa-chevron-left"></i>
        <span class="hidden sm:inline">Prev</span>
      </button>
      
      <div class="text-xs font-mono font-bold px-2.5 py-1 rounded-md bg-slate-800/80 text-emerald-400 border border-slate-700">
        Slide <span id="current-slide-num">1</span> / <span id="total-slides-num">10</span>
      </div>

      <button onclick="nextSlide()" class="p-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-bold transition flex items-center space-x-1 cursor-pointer">
        <span class="hidden sm:inline">Next</span>
        <i class="fa-solid fa-chevron-right"></i>
      </button>

      <a href="Call_Center_AI_Voice_Agents_Presentation.pptx" download class="p-1.5 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition flex items-center space-x-1 ml-2 shadow-sm cursor-pointer" title="Download .pptx PowerPoint File">
        <i class="fa-solid fa-file-powerpoint"></i>
        <span>Download PPTX</span>
      </a>

      <button onclick="toggleFullScreen()" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 ml-1 cursor-pointer" title="Toggle Fullscreen">
        <i class="fa-solid fa-expand"></i>
      </button>
    </div>
  </nav>

  <!-- MAIN SLIDES VIEWPORT (16:9 CONTAINER) -->
  <main class="flex-1 min-h-0 flex items-center justify-center p-2 sm:p-4 bg-slate-950">
    <div class="w-full max-w-6xl aspect-[16/9] max-h-[85vh] bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col relative" id="presentation-viewport">

      <!-- ============================================================= -->
      <!-- SLIDE 1: TITLE SLIDE (Executive Dark)                         -->
      <!-- ============================================================= -->
      <section class="slide active w-full h-full bg-slate-900 text-white p-8 sm:p-14 flex-col justify-between">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-400">Executive Architecture &amp; Value Showcase</span>
          <span class="text-xs text-slate-400 font-mono">Region: us-east-2 &bull; Project: For Each and Every</span>
        </div>
        <div class="space-y-4 my-auto">
          <span class="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider">Deterministic Graph Grounding</span>
          <h1 class="text-3xl sm:text-5xl font-black tracking-tight leading-tight">Call Center AI Voice Agents Studio</h1>
          <p class="text-lg sm:text-xl text-slate-300 font-medium max-w-3xl leading-relaxed">
            Closing the Enterprise Execution Gap with Graph Grounding: Reconciling SOP Rulebooks (KG) with Real-Time Call Realities (CG) to Drive Net ROI &amp; Prevent Policy Drift.
          </p>
          <div class="flex flex-wrap items-center gap-3 pt-3 text-xs font-mono text-slate-400">
            <span class="bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">Triad Spatial Graph (KG &bull; CG &bull; BG)</span>
            <span class="bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">Groq LPU (Llama 3.3 70B Versatile)</span>
            <span class="bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">Sub-second Voice Reasoning</span>
          </div>
        </div>
        <div class="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800 pt-4">
          <span>Confidential &bull; Enterprise Strategy Presentation</span>
          <span>Use Keyboard &larr; / &rarr; or click Next</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 2: THE PROBLEM (EXECUTION GAP)                          -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full border border-rose-200">The Problem &amp; Opportunity</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">The Enterprise Execution Gap: Why Traditional Voice AI Fails</h2>
          <p class="text-xs sm:text-sm text-slate-500">Static policy manuals never survive contact with frontline customer calls.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-auto">
          <div class="bg-white border-2 border-rose-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-2xl font-black text-rose-500 font-mono">01</span>
            <h3 class="text-base font-extrabold text-slate-900">Naive RAG Hallucinations</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Standard vector search matches semantic similarity but completely fails at rigid constraint checking ($50 vs $250 limits). Agents recite outdated handbooks or grant unauthorized credits.
            </p>
          </div>

          <div class="bg-white border-2 border-amber-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-2xl font-black text-amber-500 font-mono">02</span>
            <h3 class="text-base font-extrabold text-slate-900">Policy Drift Blindspot</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              When customers push back, human agents routinely bypass base SOPs (67% exception rate). Management has zero visibility into this operational drift until quarterly financial audits.
            </p>
          </div>

          <div class="bg-white border-2 border-indigo-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-2xl font-black text-indigo-500 font-mono">03</span>
            <h3 class="text-base font-extrabold text-slate-900">Escalation Bottlenecks</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Because frontline agents lack grounded autonomy, customers sit in 15-minute transfer queues waiting for Tier-2 supervisor sign-offs, inflating AHT and crushing CSAT scorecards.
            </p>
          </div>
        </div>

        <div class="bg-indigo-50 border border-indigo-200 rounded-xl p-3 flex items-center justify-between text-xs text-indigo-950 font-medium">
          <span><strong>The Solution:</strong> Replace naive vector search with a 3-way Deterministic Spatial Graph that reconciles policies against reality in real time.</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 3: CORE ARCHITECTURE (THE SPATIAL TRIAD)                -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full border border-indigo-200">System Core Architecture</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">The Spatial Triad: Knowledge, Context, and Business Graphs</h2>
          <p class="text-xs sm:text-sm text-slate-500">The exact spatial hierarchy grounding live call center decisions.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto items-center">
          <div class="md:col-span-7 bg-white p-3 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-center">
            <img src="docs/presentation_assets/architecture_spatial_triad.png" alt="Spatial Triad Architecture" class="max-h-[320px] object-contain rounded-xl">
          </div>
          <div class="md:col-span-5 space-y-2.5 text-xs">
            <div class="p-2.5 rounded-xl bg-indigo-50 border border-indigo-200">
              <strong class="text-indigo-950 block font-extrabold text-[11px]">Upper-Left: Knowledge Graph (KG)</strong>
              <span class="text-indigo-800">What SHOULD happen. Encodes approved SOPs, base limits, role authorities, and exception thresholds.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200">
              <strong class="text-emerald-950 block font-extrabold text-[11px]">Upper-Right: Context Graph (CG)</strong>
              <span class="text-emerald-800">What ACTUALLY happened. Ingests caller identity, LTV tenure, real-time telemetry, and agent actions.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200">
              <strong class="text-amber-950 block font-extrabold text-[11px]">Center: Business Graph (BG)</strong>
              <span class="text-amber-800">Reconciliation Engine. Evaluates rule vs reality, calculates net ROI, and verifies compliance.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-pink-50 border border-pink-200">
              <strong class="text-pink-950 block font-extrabold text-[11px]">Bottom: Policy Drift Feedback Loop</strong>
              <span class="text-pink-800">Dashed feedback loop alerts management when exceptions outpace baseline rules, self-healing the SOP.</span>
            </div>
          </div>
        </div>

        <div class="text-[11px] text-slate-400 font-mono flex items-center justify-between border-t border-slate-200 pt-2">
          <span>Triad Layout: KG (Upper-Left) &bull; CG (Upper-Right) &bull; BG (Center) &bull; 4 Outcomes (Bottom)</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 4: END-TO-END OPERATIONAL FLOW                          -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">Operational Flow</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">End-to-End Operational Pipeline: Document &rarr; Decision &rarr; Loop</h2>
          <p class="text-xs sm:text-sm text-slate-500">How unstructured text documents transform into sub-second voice intelligence.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 my-auto text-xs">
          <div class="bg-white border border-indigo-200 rounded-2xl p-4 shadow-sm space-y-1.5">
            <span class="text-indigo-600 font-black font-mono text-sm">STEP 1</span>
            <h4 class="font-extrabold text-slate-900">SOP Document Ingestion</h4>
            <p class="text-slate-600 text-[11px]">Raw SOP PDF manuals &amp; exception clauses parsed into formal OWL/RDF knowledge graph triples.</p>
          </div>
          <div class="bg-white border border-indigo-200 rounded-2xl p-4 shadow-sm space-y-1.5">
            <span class="text-indigo-600 font-black font-mono text-sm">STEP 2</span>
            <h4 class="font-extrabold text-slate-900">Knowledge Graph Build</h4>
            <p class="text-slate-600 text-[11px]">Encodes Tier-1 $50 limit, Section 4.2 VIP exception ($250), and minimum LTV threshold ($1,500).</p>
          </div>
          <div class="bg-white border border-emerald-200 rounded-2xl p-4 shadow-sm space-y-1.5">
            <span class="text-emerald-600 font-black font-mono text-sm">STEP 3</span>
            <h4 class="font-extrabold text-slate-900">Live Inbound Call Stream</h4>
            <p class="text-slate-600 text-[11px]">Customer dials in; ASR transcribes voice in real-time, building session Context Graph.</p>
          </div>
          <div class="bg-white border border-amber-200 rounded-2xl p-4 shadow-sm space-y-1.5">
            <span class="text-amber-600 font-black font-mono text-sm">STEP 4</span>
            <h4 class="font-extrabold text-slate-900">Reconciliation Engine</h4>
            <p class="text-slate-600 text-[11px]">Checks: Base $50 exceeded? Yes. Customer LTV > $1,500? Yes ($2,400). Action 100% compliant.</p>
          </div>
          <div class="bg-white border border-emerald-200 rounded-2xl p-4 shadow-sm space-y-1.5">
            <span class="text-emerald-600 font-black font-mono text-sm">STEP 5</span>
            <h4 class="font-extrabold text-slate-900">Grounded Agent Speech</h4>
            <p class="text-slate-600 text-[11px]">Voice Agent speaks grounded resolution; balance zeroed in 42 seconds with zero supervisor hold.</p>
          </div>
          <div class="bg-white border border-pink-200 rounded-2xl p-4 shadow-sm space-y-1.5">
            <span class="text-pink-600 font-black font-mono text-sm">STEP 6</span>
            <h4 class="font-extrabold text-slate-900">Closed-Loop Drift Alert</h4>
            <p class="text-slate-600 text-[11px]">Policy Drift detected (67% exception rate) &rarr; triggers feedback arrow to update base SOP-04.</p>
          </div>
        </div>

        <div class="bg-slate-100 rounded-xl p-2.5 text-[11px] text-slate-600 flex items-center justify-between font-mono">
          <span>Latency: Sub-400ms &bull; AHT: 42s &bull; First Contact Resolution: 92%</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 5: VALUE STORY 1 - BILLING DISPUTE                      -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-300">Value Story 1 &bull; Customer Retention</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">Billing Dispute: $150 International Roaming Waiver</h2>
          <p class="text-xs sm:text-sm text-slate-500">Caller: Sarah Jenkins (CID #48291) &bull; Account LTV: $2,400 &bull; Tenured 6 Years</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto items-center">
          <div class="md:col-span-8 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
            <img src="docs/presentation_assets/story1_billing_dispute.png" alt="Story 1 Billing Screenshot" class="max-h-[320px] w-full object-contain rounded-xl">
          </div>
          <div class="md:col-span-4 space-y-2 text-xs">
            <div class="p-2.5 rounded-xl bg-white border border-slate-200 shadow-2xs">
              <strong class="text-slate-900 block font-bold text-[11px]">1. Inbound Trigger:</strong>
              <span class="text-slate-600">Disputed $150 unauthorized roaming fee; churn risk flagged at 82%.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-indigo-50 border border-indigo-200 shadow-2xs">
              <strong class="text-indigo-950 block font-bold text-[11px]">2. Knowledge Graph Rule:</strong>
              <span class="text-indigo-800">Base limit is $50. Section 4.2 allows $250 for accounts with LTV > $1,500.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 shadow-2xs">
              <strong class="text-emerald-950 block font-bold text-[11px]">3. Grounded Action:</strong>
              <span class="text-emerald-800">Agent autonomously waives $150 with zero supervisor transfer.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 shadow-2xs">
              <strong class="text-amber-950 block font-bold text-[11px]">4. Net ROI Preserved:</strong>
              <span class="text-amber-800 font-bold">+$2,250 Net Value ($2,400 LTV saved vs $150 concession).</span>
            </div>
            <div class="p-2.5 rounded-xl bg-pink-50 border border-pink-200 shadow-2xs">
              <strong class="text-pink-950 block font-bold text-[11px]">5. Policy Drift Loop:</strong>
              <span class="text-pink-800">67% exception rate triggers feedback arrow to update SOP-04 base rules.</span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-500 border-t border-slate-200 pt-2 font-mono">
          <span>First Contact Resolution: 100% &bull; Handle Time: 42s &bull; Supervisor Wait: 0s</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 6: VALUE STORY 2 - BROADBAND OUTAGE                     -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-sky-700 bg-sky-50 px-2.5 py-1 rounded-full border border-sky-300">Value Story 2 &bull; Technical Operations</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">Broadband Residential Outage: Telemetry Preemption</h2>
          <p class="text-xs sm:text-sm text-slate-500">Caller: Marcus Vance &bull; Plan: 1Gbps Fiber &bull; Status: Red Optical Alarm (Loss of Signal)</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto items-center">
          <div class="md:col-span-8 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
            <img src="docs/presentation_assets/story2_broadband_outage.png" alt="Story 2 Outage Screenshot" class="max-h-[320px] w-full object-contain rounded-xl">
          </div>
          <div class="md:col-span-4 space-y-2 text-xs">
            <div class="p-2.5 rounded-xl bg-white border border-slate-200 shadow-2xs">
              <strong class="text-slate-900 block font-bold text-[11px]">1. Inbound Trigger:</strong>
              <span class="text-slate-600">Marcus's ONT router blinks red. Already rebooted 3x, demands tech.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-indigo-50 border border-indigo-200 shadow-2xs">
              <strong class="text-indigo-950 block font-bold text-[11px]">2. Telemetry Verification:</strong>
              <span class="text-indigo-800">Telemetry confirms upstream feeder splice break. Reboots counter-indicated.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 shadow-2xs">
              <strong class="text-emerald-950 block font-bold text-[11px]">3. Clause 6.1 Waiver:</strong>
              <span class="text-emerald-800">Waives $120 dispatch fee and schedules priority field crew in 2 hours.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 shadow-2xs">
              <strong class="text-amber-950 block font-bold text-[11px]">4. Net Value Created:</strong>
              <span class="text-amber-800 font-bold">+$340 Avoided Cost (prevents false truck rolls &amp; repeat calls).</span>
            </div>
            <div class="p-2.5 rounded-xl bg-pink-50 border border-pink-200 shadow-2xs">
              <strong class="text-pink-950 block font-bold text-[11px]">5. Bottlenecks Crushed:</strong>
              <span class="text-pink-800">Saved 18 min repetitive customer troubleshooting sequences.</span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-500 border-t border-slate-200 pt-2 font-mono">
          <span>Dispatch Fee: $0 ($120 Waived) &bull; Dispatch ETA: 2h &bull; Redundant Diagnostic: Bypassed</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 7: VALUE STORY 3 - VIP RETENTION                        -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-300">Value Story 3 &bull; Revenue Protection</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">VIP Enterprise Retention: $18k ARR Churn Prevention</h2>
          <p class="text-xs sm:text-sm text-slate-500">Caller: Elena Rostova (Apex Global Logistics) &bull; Enterprise Account ARR: $18,000 USD</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto items-center">
          <div class="md:col-span-8 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
            <img src="docs/presentation_assets/story3_vip_retention.png" alt="Story 3 Retention Screenshot" class="max-h-[320px] w-full object-contain rounded-xl">
          </div>
          <div class="md:col-span-4 space-y-2 text-xs">
            <div class="p-2.5 rounded-xl bg-white border border-slate-200 shadow-2xs">
              <strong class="text-slate-900 block font-bold text-[11px]">1. Inbound Trigger:</strong>
              <span class="text-slate-600">Competitor offered 15% discount; demands rate match or cancels $18k contract.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-indigo-50 border border-indigo-200 shadow-2xs">
              <strong class="text-indigo-950 block font-bold text-[11px]">2. Executive Clause 3.1:</strong>
              <span class="text-indigo-800">Authorizes up to 15% concession for ARR > $15k bound to 24-month lock.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 shadow-2xs">
              <strong class="text-emerald-950 block font-bold text-[11px]">3. Immediate Execution:</strong>
              <span class="text-emerald-800">Applies 15% rate reduction ($18k &rarr; $15,300) &amp; routes DocuSign amendment.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 shadow-2xs">
              <strong class="text-amber-950 block font-bold text-[11px]">4. Net Retained ARR:</strong>
              <span class="text-amber-800 font-bold">+$15,300 Net Retained ARR (Prevents $36k multi-year churn).</span>
            </div>
            <div class="p-2.5 rounded-xl bg-pink-50 border border-pink-200 shadow-2xs">
              <strong class="text-pink-950 block font-bold text-[11px]">5. Latency Crushed:</strong>
              <span class="text-pink-800">Eliminated 4-day sales director pricing approval chain.</span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-500 border-t border-slate-200 pt-2 font-mono">
          <span>Churn Prevented: 100% &bull; Contract Term: 24 Months Locked &bull; Approval Latency: 0 Days</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 8: DOCUMENT-TO-GRAPH EXTRACTION PIPELINE                -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-full border border-indigo-300">Technical Ingestion Pipeline</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">Document-to-Graph Extraction via Groq LPU Engine</h2>
          <p class="text-xs sm:text-sm text-slate-500">Transforming unstructured policy documents and live transcripts into computable triples.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto items-center">
          <div class="md:col-span-8 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
            <img src="docs/presentation_assets/extractor_pipeline.png" alt="Extractor Pipeline Screenshot" class="max-h-[320px] w-full object-contain rounded-xl">
          </div>
          <div class="md:col-span-4 space-y-2.5 text-xs">
            <div class="p-2.5 rounded-xl bg-white border border-slate-200 shadow-2xs">
              <strong class="text-slate-900 block font-bold text-[11px]">1. 3 Source Documents:</strong>
              <span class="text-slate-600">Ingests raw SOP-04, SOP-12, and SOP-28 policy manuals &amp; matching transcripts.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 shadow-2xs">
              <strong class="text-amber-950 block font-bold text-[11px]">2. Default Groq Cloud LPU:</strong>
              <span class="text-amber-800">Powered by <strong>llama-3.3-70b-versatile</strong> with sub-400ms latency and 340 tok/s throughput.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-indigo-50 border border-indigo-200 shadow-2xs">
              <strong class="text-indigo-950 block font-bold text-[11px]">3. Schema Validation:</strong>
              <span class="text-indigo-800">Guarantees structured RDF triples conforming to domain ontology constraints.</span>
            </div>
            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 shadow-2xs">
              <strong class="text-emerald-950 block font-bold text-[11px]">4. Studio Sync:</strong>
              <span class="text-emerald-800">One-click projection maps extracted triples straight onto the visual studio canvas.</span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-500 border-t border-slate-200 pt-2 font-mono">
          <span>Engine: Groq Cloud LPU &bull; Model: llama-3.3-70b-versatile &bull; Format: json_object</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 9: BUSINESS IMPACT & ROI SCORECARD                      -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-50 p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-300">Executive ROI Scorecard</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2">Enterprise Business Impact &amp; Operational Scorecard</h2>
          <p class="text-xs sm:text-sm text-slate-500">Measurable efficiency, compliance, and revenue protection metrics.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 my-auto">
          <div class="bg-white border-2 border-emerald-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-3xl sm:text-4xl font-black text-emerald-600 font-mono">92%</span>
            <h4 class="text-sm font-extrabold text-slate-900">First Contact Resolution</h4>
            <p class="text-xs text-slate-500">Up from 61% baseline. Eliminates repetitive callbacks and frustrated customer churn.</p>
          </div>
          <div class="bg-white border-2 border-indigo-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-3xl sm:text-4xl font-black text-indigo-600 font-mono">42 sec</span>
            <h4 class="text-sm font-extrabold text-slate-900">Average Handle Time</h4>
            <p class="text-xs text-slate-500">Down from 4.8 min average. Zero supervisor transfer queues or lengthy hold times.</p>
          </div>
          <div class="bg-white border-2 border-amber-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-3xl sm:text-4xl font-black text-amber-600 font-mono">100%</span>
            <h4 class="text-sm font-extrabold text-slate-900">Audit Compliance</h4>
            <p class="text-xs text-slate-500">Every single fee concession and dispatch fee is tied to explicit SOP exception clauses.</p>
          </div>
          <div class="bg-white border-2 border-pink-200 rounded-2xl p-5 shadow-sm space-y-2">
            <span class="text-3xl sm:text-4xl font-black text-pink-600 font-mono">+$2,250</span>
            <h4 class="text-sm font-extrabold text-slate-900">Net Value Saved</h4>
            <p class="text-xs text-slate-500">Per high-LTV billing dispute, preserving valuable customer equity at fractional cost.</p>
          </div>
        </div>

        <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-3 flex items-center justify-between text-xs text-emerald-950 font-medium">
          <span><strong>Executive Summary:</strong> Self-healing SOPs eliminate policy drift and empower autonomous voice agents to act decisively within compliant boundaries.</span>
        </div>
      </section>

      <!-- ============================================================= -->
      <!-- SLIDE 10: ARCHITECTURE BLUEPRINT & ACCESS                     -->
      <!-- ============================================================= -->
      <section class="slide w-full h-full bg-slate-900 text-white p-6 sm:p-10 flex-col justify-between">
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">Roadmap &amp; Access</span>
          <h2 class="text-xl sm:text-2xl font-black text-white mt-2">Production Architecture Blueprint &amp; Live Studio Access</h2>
          <p class="text-xs sm:text-sm text-slate-400">Ready for enterprise deployment in AWS project "For Each and Every" (region us-east-2).</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 my-auto text-xs">
          <!-- AWS Architecture Blueprint -->
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-5 space-y-3">
            <div class="flex items-center space-x-2 text-indigo-400">
              <i class="fa-brands fa-aws text-xl"></i>
              <h4 class="font-extrabold text-sm text-white">AWS Enterprise Blueprint (us-east-2)</h4>
            </div>
            <ul class="space-y-2 text-slate-300 text-[11px] leading-relaxed">
              <li>&bull; <strong>Region:</strong> us-east-2 (Project: <em>For Each and Every</em>)</li>
              <li>&bull; <strong>Document Ingestion:</strong> Amazon Bedrock (<code>anthropic.claude-3-5-sonnet</code>) extracts SOP PDFs into OWL/RDF ontologies.</li>
              <li>&bull; <strong>Graph Database:</strong> Amazon Neptune (OpenCypher/SPARQL) stores Knowledge Graph and temporal Context Graph.</li>
              <li>&bull; <strong>Runtime Voice Agent:</strong> Bedrock Nova-Lite / Llama-3.3-70B or Groq LPU for sub-250ms streaming voice reasoning.</li>
              <li>&bull; <strong>Telephony Bridge:</strong> Amazon Connect / SIP Trunk with live ASR transcription.</li>
            </ul>
          </div>

          <!-- Live Links -->
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-5 space-y-3">
            <div class="flex items-center space-x-2 text-emerald-400">
              <i class="fa-solid fa-link text-lg"></i>
              <h4 class="font-extrabold text-sm text-white">Live Interactive Links</h4>
            </div>
            <ul class="space-y-2 text-slate-300 text-[11px] leading-relaxed">
              <li>&bull; <strong>Live Web Studio:</strong><br><a href="https://cosmosanalytics.github.io/uat-copilot-local/callcenter_ai_voice_agents.html" target="_blank" class="text-emerald-400 hover:underline">cosmosanalytics.github.io/uat-copilot-local/callcenter_ai_voice_agents.html</a></li>
              <li>&bull; <strong>Mirror Live Studio:</strong><br><a href="https://cosmosanalytics.github.io/Langchain-test/callcenter_ai_voice_agents.html" target="_blank" class="text-emerald-400 hover:underline">cosmosanalytics.github.io/Langchain-test/callcenter_ai_voice_agents.html</a></li>
              <li>&bull; <strong>GitHub Repository:</strong><br><a href="https://github.com/cosmosanalytics/uat-copilot-local" target="_blank" class="text-emerald-400 hover:underline">github.com/cosmosanalytics/uat-copilot-local</a></li>
              <li>&bull; <strong>PowerPoint Deck:</strong><br><a href="Call_Center_AI_Voice_Agents_Presentation.pptx" download class="text-amber-400 font-bold hover:underline">Download Call_Center_AI_Voice_Agents_Presentation.pptx</a></li>
            </ul>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800 pt-2 font-mono">
          <span>Thank You &bull; Questions &amp; Discussion</span>
          <span>Press [Esc] to exit Fullscreen</span>
        </div>
      </section>

    </div>
  </main>

  <!-- BOTTOM PROGRESS STRIP -->
  <footer class="bg-slate-900 border-t border-slate-800 px-6 py-2 flex items-center justify-between text-xs text-slate-400 shrink-0">
    <div class="flex items-center space-x-2">
      <span class="text-slate-500">Navigation:</span>
      <kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono text-[10px]">&larr;</kbd>
      <kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono text-[10px]">&rarr;</kbd>
      <span class="text-slate-500 ml-2">or Space / Backspace</span>
    </div>

    <!-- Progress dots -->
    <div class="flex items-center space-x-1.5" id="slide-dots">
      <!-- Injected via JS -->
    </div>
  </footer>

  <script>
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 0;

    function updateSlide() {
      slides.forEach((s, idx) => {
        s.classList.toggle('active', idx === currentSlide);
      });
      document.getElementById('current-slide-num').textContent = currentSlide + 1;
      document.getElementById('total-slides-num').textContent = totalSlides;

      // Update dots
      const dotsContainer = document.getElementById('slide-dots');
      if (dotsContainer) {
        dotsContainer.innerHTML = Array.from({ length: totalSlides }).map((_, i) => `
          <button onclick="goToSlide(${i})" class="w-2.5 h-2.5 rounded-full transition ${i === currentSlide ? 'bg-emerald-400 scale-125' : 'bg-slate-700 hover:bg-slate-500'}"></button>
        `).join('');
      }
    }

    function nextSlide() {
      if (currentSlide < totalSlides - 1) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 0) {
        currentSlide--;
        updateSlide();
      }
    }

    function goToSlide(idx) {
      if (idx >= 0 && idx < totalSlides) {
        currentSlide = idx;
        updateSlide();
      }
    }

    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => console.log(err));
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'Backspace' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToSlide(totalSlides - 1);
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullScreen();
      }
    });

    // Touch swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    document.addEventListener('touchstart', e => {
      touchStartX = e.changedTouches[0].screenX;
    });
    document.addEventListener('touchend', e => {
      touchEndX = e.changedTouches[0].screenX;
      if (touchEndX < touchStartX - 50) nextSlide();
      if (touchEndX > touchStartX + 50) prevSlide();
    });

    updateSlide();
  </script>
</body>
</html>
"""

with open("presentation_deck.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully generated interactive presentation_deck.html!")
