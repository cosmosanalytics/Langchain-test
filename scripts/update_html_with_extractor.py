# -*- coding: utf-8 -*-
"""
Script to inject Document-to-Graph Extractor into callcenter_ai_voice_agents.html
"""
import re

html_path = "callcenter_ai_voice_agents.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add "Docs -> Graph Extractor" button in Header
header_old = """    <!-- Audio Speech Toggle -->
    <div class="flex items-center space-x-2">
      <button id="btn-toggle-speech" onclick="toggleVoiceSpeech()" class="px-3 py-1 rounded-xl text-xs font-bold bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-2xs transition flex items-center space-x-1.5">
        <i id="voice-icon" class="fa-solid fa-volume-high text-emerald-600"></i>
        <span id="voice-toggle-text">Voice Speech: ON</span>
      </button>
    </div>"""

header_new = """    <!-- Header Right Actions -->
    <div class="flex items-center space-x-2">
      <button id="btn-open-extractor" onclick="openDocExtractorModal()" class="px-3 py-1 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 shadow-2xs transition flex items-center space-x-1.5 cursor-pointer">
        <i class="fa-solid fa-file-invoice text-indigo-600"></i>
        <span>📄 Docs &rarr; Graph Extractor</span>
      </button>
      <button id="btn-toggle-speech" onclick="toggleVoiceSpeech()" class="px-3 py-1 rounded-xl text-xs font-bold bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-2xs transition flex items-center space-x-1.5 cursor-pointer">
        <i id="voice-icon" class="fa-solid fa-volume-high text-emerald-600"></i>
        <span id="voice-toggle-text">Voice Speech: ON</span>
      </button>
    </div>"""

content = content.replace(header_old, header_new)

# 2. Add Modal HTML before </body>
modal_html = """
  <!-- ================================================================= -->
  <!-- MODAL: DOCUMENT-TO-GRAPH EXTRACTION PIPELINE                      -->
  <!-- ================================================================= -->
  <div id="modal-doc-extractor" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-3 sm:p-6 hidden">
    <div class="bg-white rounded-3xl shadow-2xl border border-slate-200 w-full max-w-6xl max-h-[92vh] flex flex-col overflow-hidden animate-fade-in">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 shrink-0">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 to-emerald-600 flex items-center justify-center text-white shadow-sm font-bold text-base">
            <i class="fa-solid fa-network-wired"></i>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h2 class="text-base sm:text-lg font-black text-slate-900">Document-to-Graph Extraction Pipeline</h2>
              <span class="px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-800 text-[10px] font-bold border border-indigo-200 uppercase">Text &rarr; Triples &rarr; Graphs</span>
            </div>
            <p class="text-xs text-slate-500">Ingest raw SOP policy documents &amp; call transcripts &rarr; Extract Knowledge Graph &amp; Context Graph &rarr; Reconcile into Business Graph</p>
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <!-- Quick Switcher Inside Modal -->
          <div class="flex items-center bg-white border border-slate-200 p-0.5 rounded-xl shadow-2xs text-xs font-bold">
            <button onclick="setExtractorScenario('billing')" id="ext-tab-billing" class="px-2.5 py-1 rounded-lg text-indigo-700 bg-indigo-50 border border-indigo-200">1. Billing (SOP-04)</button>
            <button onclick="setExtractorScenario('outage')" id="ext-tab-outage" class="px-2.5 py-1 rounded-lg text-slate-600 hover:text-slate-900">2. Outage (SOP-12)</button>
            <button onclick="setExtractorScenario('retention')" id="ext-tab-retention" class="px-2.5 py-1 rounded-lg text-slate-600 hover:text-slate-900">3. VIP Retention (SOP-28)</button>
          </div>

          <button onclick="closeDocExtractorModal()" class="w-8 h-8 rounded-xl bg-white hover:bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500 hover:text-slate-800 transition shadow-2xs">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>

      <!-- Modal Body (Split: Raw Inputs vs Extracted Graphs) -->
      <div class="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-12 overflow-hidden">
        
        <!-- Left Column: Raw Source Documents (5 cols) -->
        <div class="lg:col-span-5 border-r border-slate-200 bg-slate-50/70 p-4 flex flex-col min-h-0 overflow-hidden">
          <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-200 shrink-0">
            <div class="flex items-center space-x-2">
              <span class="text-xs font-extrabold uppercase tracking-wider text-slate-700">Raw Text Documents</span>
            </div>
            <!-- Doc Sub-tab -->
            <div class="flex items-center bg-white border border-slate-200 p-0.5 rounded-lg text-[11px] font-bold">
              <button onclick="switchDocTab('sop')" id="doc-subtab-sop" class="px-2 py-0.5 rounded-md bg-indigo-600 text-white shadow-2xs">SOP Rulebook</button>
              <button onclick="switchDocTab('call')" id="doc-subtab-call" class="px-2 py-0.5 rounded-md text-slate-600 hover:text-slate-900">Call Transcript</button>
            </div>
          </div>

          <!-- Document Viewer Box -->
          <div class="flex-1 min-h-0 bg-white border border-slate-200 rounded-2xl p-3.5 overflow-y-auto font-mono text-[11px] leading-relaxed shadow-inner" id="raw-document-viewer">
            <!-- Injected via JavaScript -->
          </div>

          <!-- Extraction Controls -->
          <div class="pt-3 shrink-0 flex items-center justify-between gap-2">
            <span class="text-[11px] text-slate-500 font-medium">Pipeline: LLM Entity &amp; Relation Extraction</span>
            <button onclick="runExtractionDemo()" id="btn-run-extract" class="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-sm transition flex items-center space-x-2 cursor-pointer">
              <i class="fa-solid fa-bolt"></i>
              <span>Extract Graphs From Text</span>
            </button>
          </div>
        </div>

        <!-- Right Column: Extracted Triples & Graph Representation (7 cols) -->
        <div class="lg:col-span-7 p-4 flex flex-col min-h-0 overflow-y-auto bg-white space-y-4">
          
          <!-- STAGE 1: KNOWLEDGE GRAPH (WHAT SHOULD HAPPEN) -->
          <div class="border border-indigo-100 rounded-2xl p-3.5 bg-indigo-50/30">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded-full bg-indigo-600"></span>
                <span class="text-xs font-extrabold uppercase text-indigo-950">1. Knowledge Graph (Extracted from SOP Document)</span>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 border border-indigo-200">What SHOULD happen</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono" id="extracted-kg-triples">
              <!-- Triples Injected via JS -->
            </div>
          </div>

          <!-- STAGE 2: CONTEXT GRAPH (WHAT ACTUALLY HAPPENED) -->
          <div class="border border-emerald-100 rounded-2xl p-3.5 bg-emerald-50/30">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded-full bg-emerald-600"></span>
                <span class="text-xs font-extrabold uppercase text-emerald-950">2. Context Graph (Extracted from Call Transcript)</span>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 border border-emerald-200">What ACTUALLY happened</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono" id="extracted-cg-triples">
              <!-- Triples Injected via JS -->
            </div>
          </div>

          <!-- STAGE 3: BUSINESS GRAPH (RECONCILIATION ENGINE) -->
          <div class="border border-amber-100 rounded-2xl p-3.5 bg-amber-50/30">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded-full bg-amber-500"></span>
                <span class="text-xs font-extrabold uppercase text-amber-950">3. Business Graph (Reconciliation: SHOULD vs ACTUALLY)</span>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-200">Compares Should vs Actual</span>
            </div>
            <div class="space-y-2 text-xs" id="extracted-bg-reconciliation">
              <!-- Reconciliation Injected via JS -->
            </div>
          </div>

        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-3 bg-slate-50 border-t border-slate-200 flex flex-wrap items-center justify-between gap-3 shrink-0">
        <div class="flex items-center space-x-2 text-xs text-slate-600">
          <i class="fa-solid fa-circle-check text-emerald-600"></i>
          <span>Schema verified against Domain Ontology (RDF/OWL classes &amp; property constraints)</span>
        </div>
        <div class="flex items-center space-x-3">
          <button onclick="closeDocExtractorModal()" class="px-4 py-1.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold shadow-2xs transition">
            Close
          </button>
          <button onclick="applyExtractedToStudio()" class="px-4 py-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-700 hover:to-emerald-700 text-white text-xs font-bold shadow-sm transition flex items-center space-x-1.5 cursor-pointer">
            <i class="fa-solid fa-arrows-rotate"></i>
            <span>Apply Extracted Graph to Visual Studio</span>
          </button>
        </div>
      </div>

    </div>
  </div>
"""

content = content.replace("</body>", modal_html + "\n</body>")

# 3. Add Raw Documents and JavaScript Controller Functions
js_code = """
    // =========================================================================
    // DOCUMENT-TO-GRAPH EXTRACTION PIPELINE CONTROLLER
    // =========================================================================
    const RAW_DOCS = {
      billing: {
        sop: {
          title: "SOP-04 (REV. 8.2): Telecom Billing Disputes & Roaming Waivers",
          text: `STANDARD OPERATING PROCEDURE: SOP-04 (REV. 8.2)
TITLE: TELECOM BILLING DISPUTES & INTERNATIONAL ROAMING WAIVERS
CLASSIFICATION: INTERNAL COMPLIANCE - LEVEL 2
GOVERNANCE: CONSUMER OPERATIONS POLICY COMMITTEE

1. PURPOSE & SCOPE
Mandated operational parameters for Customer Service Representatives (CSRs)
regarding billing fee disputes and international data/voice roaming.

2. STANDARD AUTHORIZATION THRESHOLDS
2.1 Tier-1 Customer Care Representatives:
    - Empowered to grant billing concessions up to a hard ceiling of $50.00 USD per cycle.
    - Concessions between $50.01 and $200.00 USD strictly require Supervisory escalation.

3. SECTION 4.2: VIP CUSTOMER HARDSHIP & RETENTION CLAUSE (EXCEPTION PROVISION)
3.1 Qualifications:
    - Customer must hold an active account lifetime value (LTV) exceeding $1,500.00 USD.
    - Zero prior roaming fee concessions in the preceding 12 months.
    - Account status must be in Good Standing.
3.2 Authority Grant:
    - Tier-1 CSRs are granted expanded discretionary authority up to $250.00 USD waiver limit
      WITHOUT requiring supervisor escalation, provided the objective is immediate First
      Contact Resolution (FCR) and customer retention.`
        },
        transcript: {
          title: "CALL-0842: Inbound Dispute - Sarah Jenkins (LTV $2,400)",
          text: `CALL RECORD & ASR TRANSCRIPT: CALL-0842
CALLER ID: +1 (312) 555-0192 | CUSTOMER: Sarah Jenkins (CID: 948102)
ACCOUNT METRICS: Tenured 6 Years | LTV: $2,400.00 USD | Status: Good Standing

[00:02] AGENT: Thank you for calling Apex Telecom priority support. My name is Alex.
[00:07] CUSTOMER (Sarah Jenkins): "I was charged a $150 international roaming fee on my last bill that I didn't authorize. Can you waive it?"
[00:23] AGENT: Let me review your billing ledger and travel pass provisioning right now.
[00:31] [SYSTEM AUDIT: Roaming charge: $150.00. Account LTV: $2,400.00, Prior dispute count: 0.]
[00:35] AGENT: "Because you have been a valued customer for 6 years with $2,400 LTV, I am applying our VIP Hardship Exception under SOP-04 Section 4.2 to waive the full $150 right now. Your balance is adjusted to $0, and no supervisor transfer is required."
[00:54] CUSTOMER (Sarah Jenkins): "Wow, that was fast and painless! Thank you so much Alex."
[01:05] [RESOLUTION: FCR = 100% | Concession: $150.00 | Account Retained: $2,400.00 LTV]`
        },
        kgTriples: [
          { s: "SOP-04", p: "[:governs]", o: "Tier-1 Base Limit: $50", type: "rule" },
          { s: "SOP-04", p: "[:allows_exception]", o: "VIP Clause 4.2: $250 Limit", type: "exception" },
          { s: "VIP Clause 4.2", p: "[:requires_min_ltv]", o: "Min LTV > $1,500", type: "constraint" },
          { s: "SOP-04", p: "[:assigned_to]", o: "Role: Tier-1 Agent", type: "role" }
        ],
        cgTriples: [
          { s: "Sarah Jenkins", p: "[:disputed]", o: "Event: Disputed $150 Roaming", type: "event" },
          { s: "Sarah Jenkins", p: "[:received]", o: "Decision: Waived $150", type: "decision" },
          { s: "Sarah Jenkins", p: "[:profile_ltv]", o: "Account LTV: $2,400", type: "profile" },
          { s: "Sarah Jenkins", p: "[:prior_claims]", o: "Diary: 0 prior concessions", type: "profile" }
        ],
        reconciliation: {
          eval: "Base SOP-04 Limit ($50) was exceeded by $100 &rarr; Triggered VIP Hardship Exception Clause 4.2 ($250 ceiling).",
          check: "Sarah Jenkins Account LTV ($2,400) &gt; Minimum Threshold ($1,500) &rarr; <span class='text-emerald-700 font-bold'>VALIDATED</span>.",
          outcomes: [
            { label: "Policy Drift", val: "67% Exception Frequency &rarr; Triggers Feedback Arrow back to SOP-04", badge: "bg-amber-100 text-amber-800 border-amber-200" },
            { label: "Compliance Gap", val: "100% Validated (Clause 4.2 audit logged in CRM ledger)", badge: "bg-emerald-100 text-emerald-800 border-emerald-200" },
            { label: "Net Value", val: "+$2,250 Net Value ($2,400 LTV preserved - $150 waiver concession)", badge: "bg-emerald-100 text-emerald-800 border-emerald-200" },
            { label: "Bottlenecks", val: "0 min Supervisor Escalation Wait &rarr; 100% First Contact Resolution", badge: "bg-slate-100 text-slate-800 border-slate-200" }
          ]
        }
      },
      outage: {
        sop: {
          title: "SOP-12 (REV. 5.1): Broadband Outage Triage & Truck Roll Protocol",
          text: `STANDARD OPERATING PROCEDURE: SOP-12 (REV. 5.1)
TITLE: BROADBAND RESIDENTIAL OUTAGE TRIAGE & TRUCK ROLL PROTOCOL
CLASSIFICATION: TECHNICAL OPERATIONS MANUAL
GOVERNANCE: NETWORK INFRASTRUCTURE OPERATIONS

1. MANDATORY DIAGNOSTIC SEQUENCE
2.1 Telemetry Verification:
    - Agent must query Area Optical Loop Telemetry.
    - If Red Optical Alarm (Loss of Signal / LOS) is confirmed on the neighborhood hub,
      remote reboot sequences are strictly counter-indicated.
2.2 Step-by-Step Diagnostic Verification:
    - Step 1: Query Hub Telemetry (Verify upstream attenuation).
    - Step 2: Hardware Dispatch Decision:
      * Standard truck roll fee: $120.00 USD.
      * Clause 6.1 (Hardware Defect Waiver): If LOS is confirmed on upstream telemetry,
        dispatch fee is 100% waived, and priority field tech is scheduled within 4 hours.`
        },
        transcript: {
          title: "CALL-1109: Fiber Optical LOS - Marcus Vance (1Gbps Fiber)",
          text: `CALL RECORD & ASR TRANSCRIPT: CALL-1109
CALLER ID: +1 (512) 555-0481 | CUSTOMER: Marcus Vance (CID: 819203)
PLAN: 1Gbps Fiber Residential | STATUS: Degraded / LOS Alarm

[00:02] AGENT: Hello, Apex Fiber technical assistance.
[00:06] CUSTOMER (Marcus Vance): "My optical ONT router is blinking red, and my internet is dead. I already rebooted 3 times. Please dispatch a tech."
[00:25] [SYSTEM AUDIT: Telemetry Query... Upstream Hub 4-B reports Optical Signal Loss (LOS) alarm at feeder splice. Physical break confirmed.]
[00:28] AGENT: "I have confirmed a physical optical loss on your neighborhood hub. Under SOP-12 Clause 6.1, I am waiving the standard $120 technician fee and have dispatched field engineering for 1:00 PM today."
[00:46] CUSTOMER: "Awesome, appreciate you not making me do repetitive reboot steps."
[00:58] [RESOLUTION: Redundant reboot avoided | Dispatch Fee: $0 ($120 waived) | ETA: 2h]`
        },
        kgTriples: [
          { s: "SOP-12", p: "[:governs]", o: "Telemetry Protocol: Verify LOS", type: "rule" },
          { s: "SOP-12", p: "[:allows_exception]", o: "Clause 6.1: Fiber Break Waiver ($120)", type: "exception" },
          { s: "Clause 6.1", p: "[:requires_telemetry]", o: "Telemetry == Hub Red Optical Alarm", type: "constraint" },
          { s: "SOP-12", p: "[:assigned_to]", o: "Role: Autonomous Triage", type: "role" }
        ],
        cgTriples: [
          { s: "Marcus Vance", p: "[:reported_event]", o: "Event: Optical Alarm (Blinking Red)", type: "event" },
          { s: "Marcus Vance", p: "[:received]", o: "Decision: Tech Dispatched (Fee Waived)", type: "decision" },
          { s: "Marcus Vance", p: "[:telemetry_state]", o: "Hub Telemetry: Optical Signal Loss", type: "profile" },
          { s: "Marcus Vance", p: "[:redundant_test]", o: "Diagnostic: Bypassed 3x Reboot", type: "profile" }
        ],
        reconciliation: {
          eval: "Telemetry confirmed physical line break &rarr; Bypassed standard repetitive reset script.",
          check: "Upstream feeder splice LOS confirmed &rarr; <span class='text-emerald-700 font-bold'>VALIDATED</span>.",
          outcomes: [
            { label: "Policy Drift", val: "84% Automated Dispatch without manual agent transfer", badge: "bg-amber-100 text-amber-800 border-amber-200" },
            { label: "Compliance Gap", val: "100% Validated (Clause 6.1 Telemetry bypass criteria met)", badge: "bg-emerald-100 text-emerald-800 border-emerald-200" },
            { label: "Net Value", val: "+$340 Avoided Roll Cost (Avoided repeated false dispatches)", badge: "bg-emerald-100 text-emerald-800 border-emerald-200" },
            { label: "Bottlenecks", val: "Saved 18 min repetitive customer diagnostic scripts", badge: "bg-slate-100 text-slate-800 border-slate-200" }
          ]
        }
      },
      retention: {
        sop: {
          title: "SOP-28 (REV. 4.0): Enterprise & High-LTV Retention Governance",
          text: `STANDARD OPERATING PROCEDURE: SOP-28 (REV. 4.0)
TITLE: ENTERPRISE & HIGH-LTV RETENTION GOVERNANCE
CLASSIFICATION: COMMERCIAL SALES & ACCOUNTS OPERATIONS
GOVERNANCE: ENTERPRISE REVENUE PROTECTION COMMITTEE

1. RETENTION CEILINGS
2.1 Standard Account Representatives:
    - Maximum allowable discount on renewal: 5.0% without director sign-off.
2.2 Executive Clause 3.1: High-Value Retention Allowance:
    - Applicable only to accounts with verified ARR > $15,000.00 USD.
    - Tier-1 Enterprise Specialists authorized to offer up to 15.0% discount
      contingent on executing a 24-month contract lock.
    - Justification: Retaining $18,000 ARR with $2,700 concession yields +$15,300 net
      annual retained value, preventing churn.`
        },
        transcript: {
          title: "CALL-2204: Enterprise Churn Risk - Elena Rostova ($18,000 ARR)",
          text: `CALL RECORD & ASR TRANSCRIPT: CALL-2204
CALLER ID: +1 (212) 555-0819 | CUSTOMER: Elena Rostova (CID: 704192)
COMPANY: Apex Global Logistics | ARR: $18,000.00 USD

[00:03] AGENT: Hello Elena, thank you for reaching out to Enterprise Dedicated Support.
[00:09] CUSTOMER (Elena Rostova): "A competitor offered us equivalent fiber at 15% discount. Match it or cancel our $18,000 annual account."
[00:36] [SYSTEM AUDIT: ARR: $18,000. Account Tenure: 4 Years. Risk Level: Critical Churn.]
[00:41] AGENT: "Under SOP-28 Executive Clause 3.1, because your ARR exceeds $15,000, I am authorized to apply a 15% rate reduction ($18k to $15,300), bound to a renewed 24-month term lock. Executing amendment now."
[01:05] CUSTOMER (Elena): "That matches their proposal without the migration friction. Please execute that amendment."
[01:20] [RESOLUTION: Churn Prevented | Retained ARR: $15,300 Net | Term: 24mo lock]`
        },
        kgTriples: [
          { s: "SOP-28", p: "[:governs]", o: "Standard Rep Ceiling: 5% Discount", type: "rule" },
          { s: "SOP-28", p: "[:allows_exception]", o: "Clause 3.1: 15% VIP Discount", type: "exception" },
          { s: "Clause 3.1", p: "[:requires_contract]", o: "Min ARR > $15k & 24mo Lock", type: "constraint" },
          { s: "SOP-28", p: "[:assigned_to]", o: "Role: Enterprise Specialist", type: "role" }
        ],
        cgTriples: [
          { s: "Elena Rostova", p: "[:threatened_event]", o: "Event: Competitor 15% Match or Churn", type: "event" },
          { s: "Elena Rostova", p: "[:received]", o: "Decision: 15% Rate Discount Applied", type: "decision" },
          { s: "Elena Rostova", p: "[:enterprise_arr]", o: "Account ARR: $18,000", type: "profile" },
          { s: "Elena Rostova", p: "[:contract_lock]", o: "Term Lock: 24 Months Renewed", type: "profile" }
        ],
        reconciliation: {
          eval: "5% Standard Renewal ceiling was insufficient &rarr; Invoked Executive Clause 3.1 (15% concession).",
          check: "Enterprise ARR ($18,000) &gt; Minimum Threshold ($15,000) with 24mo commitment &rarr; <span class='text-emerald-700 font-bold'>VALIDATED</span>.",
          outcomes: [
            { label: "Policy Drift", val: "42% of Enterprise accounts require Tier-3 commercial matching", badge: "bg-amber-100 text-amber-800 border-amber-200" },
            { label: "Compliance Gap", val: "100% Validated (24-month lock clause executed via DocuSign)", badge: "bg-emerald-100 text-emerald-800 border-emerald-200" },
            { label: "Net Value", val: "+$15,300 Net Retained ARR ($18k saved - $2.7k discount)", badge: "bg-emerald-100 text-emerald-800 border-emerald-200" },
            { label: "Bottlenecks", val: "Eliminated 4-day sales director pricing approval loop", badge: "bg-slate-100 text-slate-800 border-slate-200" }
          ]
        }
      }
    };

    let activeExtractorScenario = 'billing';
    let activeDocSubTab = 'sop';

    function openDocExtractorModal() {
      const modal = document.getElementById('modal-doc-extractor');
      if (modal) {
        modal.classList.remove('hidden');
        renderExtractorView();
      }
    }

    function closeDocExtractorModal() {
      const modal = document.getElementById('modal-doc-extractor');
      if (modal) modal.classList.add('hidden');
    }

    function setExtractorScenario(key) {
      activeExtractorScenario = key;
      ['billing', 'outage', 'retention'].forEach(k => {
        const btn = document.getElementById(`ext-tab-${k}`);
        if (!btn) return;
        if (k === key) {
          btn.className = "px-2.5 py-1 rounded-lg text-indigo-700 bg-indigo-50 border border-indigo-200";
        } else {
          btn.className = "px-2.5 py-1 rounded-lg text-slate-600 hover:text-slate-900";
        }
      });
      renderExtractorView();
    }

    function switchDocTab(tab) {
      activeDocSubTab = tab;
      const btnSop = document.getElementById('doc-subtab-sop');
      const btnCall = document.getElementById('doc-subtab-call');
      if (tab === 'sop') {
        btnSop.className = "px-2 py-0.5 rounded-md bg-indigo-600 text-white shadow-2xs";
        btnCall.className = "px-2 py-0.5 rounded-md text-slate-600 hover:text-slate-900";
      } else {
        btnCall.className = "px-2 py-0.5 rounded-md bg-emerald-600 text-white shadow-2xs";
        btnSop.className = "px-2 py-0.5 rounded-md text-slate-600 hover:text-slate-900";
      }
      renderDocText();
    }

    function renderDocText() {
      const viewer = document.getElementById('raw-document-viewer');
      if (!viewer) return;
      const data = RAW_DOCS[activeExtractorScenario];
      if (activeDocSubTab === 'sop') {
        viewer.innerHTML = `
          <div class="text-xs font-bold text-indigo-900 pb-2 mb-2 border-b border-slate-200 flex items-center justify-between">
            <span>📄 ${data.sop.title}</span>
            <span class="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">Source Policy Document</span>
          </div>
          <pre class="whitespace-pre-wrap text-slate-700 leading-relaxed">${data.sop.text}</pre>
        `;
      } else {
        viewer.innerHTML = `
          <div class="text-xs font-bold text-emerald-900 pb-2 mb-2 border-b border-slate-200 flex items-center justify-between">
            <span>🎙️ ${data.transcript.title}</span>
            <span class="text-[10px] bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">Raw Call Recording</span>
          </div>
          <pre class="whitespace-pre-wrap text-slate-700 leading-relaxed">${data.transcript.text}</pre>
        `;
      }
    }

    function renderExtractorView() {
      renderDocText();
      const data = RAW_DOCS[activeExtractorScenario];

      // Render Knowledge Graph Triples
      const kgContainer = document.getElementById('extracted-kg-triples');
      if (kgContainer) {
        kgContainer.innerHTML = data.kgTriples.map(t => `
          <div class="p-2 rounded-xl bg-white border border-indigo-200 shadow-2xs flex items-center space-x-1.5 overflow-hidden">
            <span class="font-bold text-indigo-950 truncate">${t.s}</span>
            <span class="text-indigo-500 font-extrabold text-[10px] shrink-0">${t.p}</span>
            <span class="text-indigo-800 truncate">${t.o}</span>
          </div>
        `).join('');
      }

      // Render Context Graph Triples
      const cgContainer = document.getElementById('extracted-cg-triples');
      if (cgContainer) {
        cgContainer.innerHTML = data.cgTriples.map(t => `
          <div class="p-2 rounded-xl bg-white border border-emerald-200 shadow-2xs flex items-center space-x-1.5 overflow-hidden">
            <span class="font-bold text-emerald-950 truncate">${t.s}</span>
            <span class="text-emerald-600 font-extrabold text-[10px] shrink-0">${t.p}</span>
            <span class="text-emerald-800 truncate">${t.o}</span>
          </div>
        `).join('');
      }

      // Render Business Graph Reconciliation
      const bgContainer = document.getElementById('extracted-bg-reconciliation');
      if (bgContainer) {
        bgContainer.innerHTML = `
          <div class="p-2.5 rounded-xl bg-white border border-amber-200 shadow-2xs space-y-1.5 mb-2">
            <div class="flex items-center space-x-2">
              <span class="font-bold text-slate-800">Rule Evaluation:</span>
              <span class="text-slate-600">${data.reconciliation.eval}</span>
            </div>
            <div class="flex items-center space-x-2">
              <span class="font-bold text-slate-800">Criteria Check:</span>
              <span>${data.reconciliation.check}</span>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            ${data.reconciliation.outcomes.map(o => `
              <div class="p-2 rounded-xl border ${o.badge} text-[11px] font-medium flex flex-col justify-between">
                <span class="font-extrabold uppercase text-[10px] tracking-wider mb-0.5">${o.label}</span>
                <span>${o.val}</span>
              </div>
            `).join('')}
          </div>
        `;
      }
    }

    function runExtractionDemo() {
      const btn = document.getElementById('btn-run-extract');
      if (!btn) return;
      btn.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i><span>Extracting Triples...</span>`;
      setTimeout(() => {
        btn.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-300"></i><span>Extraction Complete!</span>`;
        renderExtractorView();
        setTimeout(() => {
          btn.innerHTML = `<i class="fa-solid fa-bolt"></i><span>Extract Graphs From Text</span>`;
        }, 1500);
      }, 500);
    }

    function applyExtractedToStudio() {
      closeDocExtractorModal();
      selectUseCase(activeExtractorScenario);
    }
"""

content = content.replace("function initUnifiedGraph() {", js_code + "\n    function initUnifiedGraph() {")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully injected Document-to-Graph Extraction Pipeline into callcenter_ai_voice_agents.html!")
