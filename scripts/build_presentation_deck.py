# -*- coding: utf-8 -*-
"""
Generate a professional, executive-ready 16:9 PowerPoint Presentation (.pptx)
for the Call Center AI Voice Agents Studio.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette
    C_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50
    C_BG_CARD = RGBColor(255, 255, 255)        # Pure White
    C_TEXT_DARK = RGBColor(15, 23, 42)         # Slate 900
    C_TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500
    C_INDIGO = RGBColor(67, 56, 202)           # SOPs / KG
    C_INDIGO_LIGHT = RGBColor(238, 242, 255)   # Indigo 50
    C_EMERALD = RGBColor(5, 150, 105)          # Calls / CG
    C_EMERALD_LIGHT = RGBColor(236, 253, 245)  # Emerald 50
    C_AMBER = RGBColor(217, 119, 6)            # Reconciliation / BG
    C_AMBER_LIGHT = RGBColor(254, 243, 199)    # Amber 50
    C_PINK = RGBColor(219, 39, 119)            # Policy Drift
    C_BORDER = RGBColor(226, 232, 240)         # Slate 200

    assets_dir = os.path.abspath("docs/presentation_assets")

    def add_header(slide, title, category, subtitle=""):
        # Category Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.5), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_INDIGO_LIGHT
        pill.line.color.rgb = C_INDIGO
        pill.line.width = Pt(1)
        tf_pill = pill.text_frame
        tf_pill.word_wrap = True
        p_p = tf_pill.paragraphs[0]
        p_p.text = category.upper()
        p_p.font.size = Pt(9)
        p_p.font.bold = True
        p_p.font.color.rgb = C_INDIGO
        p_p.alignment = PP_ALIGN.CENTER

        # Title
        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.5))
        tf_t = tx_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_DARK

        if subtitle:
            p_sub = tf_t.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Executive Dark Accent)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(15, 23, 42) # Dark navy
    bg1.line.fill.background()

    # Title Box
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "ENTERPRISE CALL CENTER AI ARCHITECTURE"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(52, 211, 153) # Emerald 400
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Call Center AI Voice Agents Studio"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Closing the Enterprise Execution Gap with Deterministic Graph Grounding:\nReconciling SOP Rulebooks (KG) with Real-Time Call Realities (CG) to Drive Net ROI & Prevent Policy Drift"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Core Engine: Triad Spatial Graph (KG • CG • BG)  |  LLM Pipeline: Groq LPU (Llama-3.3-70B) & AWS Bedrock (us-east-2)"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: THE EXECUTIVE PROBLEM & THE EXECUTION GAP
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Enterprise Execution Gap: Why Traditional Voice AI Fails", "The Problem & Opportunity", "Static policy manuals never survive contact with frontline customer calls.")

    cols = [
        {
            "num": "01",
            "title": "Naive RAG Hallucinations",
            "desc": "Standard vector embeddings match semantic similarity but completely fail at strict constraint verification (e.g. max $50 vs $250 concession caps). Agents give unauthorized credits or recite outdated handbooks.",
            "color": RGBColor(239, 68, 68),
            "bg": RGBColor(254, 242, 242)
        },
        {
            "num": "02",
            "title": "Frontline Policy Drift Blindspot",
            "desc": "When customers push back, human agents routinely bypass baseline rules (67% exception rate). Management has zero visibility into this operational drift until quarterly financial audits.",
            "color": RGBColor(217, 119, 6),
            "bg": RGBColor(254, 243, 199)
        },
        {
            "num": "03",
            "title": "Supervisory Wait Bottlenecks",
            "desc": "Because frontline agents lack grounded autonomy, customers sit in 15-minute transfer queues waiting for Tier-2 supervisor sign-offs, inflating AHT and crushing CSAT scorecards.",
            "color": RGBColor(99, 102, 241),
            "bg": RGBColor(238, 242, 255)
        }
    ]

    for i, c in enumerate(cols):
        x = Inches(0.8 + i * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = c["bg"]
        card.line.color.rgb = c["color"]
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.4)

        pn = tf.paragraphs[0]
        pn.text = c["num"]
        pn.font.size = Pt(28)
        pn.font.bold = True
        pn.font.color.rgb = c["color"]
        pn.space_after = Pt(12)

        pt = tf.add_paragraph()
        pt.text = c["title"]
        pt.font.size = Pt(16)
        pt.font.bold = True
        pt.font.color.rgb = C_TEXT_DARK
        pt.space_after = Pt(14)

        pd = tf.add_paragraph()
        pd.text = c["desc"]
        pd.font.size = Pt(12)
        pd.font.color.rgb = RGBColor(51, 65, 85)
        pd.line_spacing = 1.25

    # =========================================================================
    # SLIDE 3: THE CORE ARCHITECTURE - THE SPATIAL TRIAD (USER'S DIAGRAM)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Core Architecture: The Spatial Triad Framework", "System Core", "Grounding voice autonomy across Knowledge Graph, Context Graph, and Business Graph.")

    # Left: Embed User's uploaded diagram
    diag_path = os.path.join(assets_dir, "architecture_spatial_triad.png")
    if os.path.exists(diag_path):
        s3.shapes.add_picture(diag_path, Inches(0.8), Inches(1.8), width=Inches(6.8))

    # Right: Narrative breakdown cards
    right_x = Inches(8.0)
    cards_data = [
        ("Knowledge Graph (KG) — Upper Left", "What SHOULD Happen (SOPs)", "Extracts and encodes approved business policies, authority tiers, dollar concession ceilings, and escalation matrices into formal RDF/OWL triples.", C_INDIGO),
        ("Context Graph (CG) — Upper Right", "What ACTUALLY Happened (Calls)", "Ingests live ASR streaming speech, customer CRM history, LTV accounts, and real-time agent actions into temporal session subgraphs.", C_EMERALD),
        ("Business Graph (BG) — Center Middle", "Reconciliation Engine", "Compares SHOULD vs ACTUALLY in real time. Evaluates policy drift, verifies compliance, calculates net ROI, and eliminates supervisor bottlenecks.", C_AMBER),
        ("Policy Drift Loop — Closed Loop", "Continuous SOP Self-Healing", "A dashed feedback arrow automatically signals policy teams when frontline calls repeatedly deviate, transforming static SOPs into living assets.", C_PINK)
    ]

    for j, (title, tag, desc, col) in enumerate(cards_data):
        y = Inches(1.8 + j * 1.25)
        cd = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, y, Inches(4.5), Inches(1.15))
        cd.fill.solid()
        cd.fill.fore_color.rgb = C_BG_CARD
        cd.line.color.rgb = col
        cd.line.width = Pt(1.5)

        tf = cd.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.12)

        p = tf.paragraphs[0]
        p.text = f"{title} • {tag}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 4: END-TO-END OPERATIONAL FLOW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "End-to-End Operational Flow: Document to Decision to Loop", "Execution Flow", "How unstructured text documents become computable graphs and real-time voice intelligence.")

    flow_steps = [
        ("1. Ingestion", "Raw SOP manuals & exception clauses ingested via Groq LPU (Llama 3.3 70B) & AWS Bedrock.", C_INDIGO),
        ("2. Graph Build", "Constructs formal Knowledge Graph: SOP-04, $50 Base Cap, Clause 4.2 VIP exception ($250).", C_INDIGO),
        ("3. Inbound Call", "Customer dials in; streaming ASR transcribes voice into real-time Context Graph (CG).", C_EMERALD),
        ("4. Reconciliation", "Business Graph (BG) checks: Base $50 exceeded? Yes. Customer LTV > $1,500? Yes. Concession Validated.", C_AMBER),
        ("5. Agent Speech", "Autonomous AI speaks grounded answer via Web Speech API; balance zeroed in 42 seconds.", C_EMERALD),
        ("6. Drift Loop", "Policy Drift logged (67% exception frequency) & triggers feedback arrow to update SOP-04.", C_PINK)
    ]

    for k, (step_t, step_d, step_c) in enumerate(flow_steps):
        col_idx = k % 3
        row_idx = k // 3
        x = Inches(0.8 + col_idx * 4.0)
        y = Inches(1.8 + row_idx * 2.5)

        fcard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(2.2))
        fcard.fill.solid()
        fcard.fill.fore_color.rgb = C_BG_CARD
        fcard.line.color.rgb = step_c
        fcard.line.width = Pt(1.5)

        tf = fcard.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = step_t
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = step_c
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = step_d
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK
        p2.line_spacing = 1.2

    # =========================================================================
    # SLIDE 5: VALUE STORY 1 - BILLING DISPUTE ($150 ROAMING FEE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Value Story 1: Billing Dispute ($150 International Roaming)", "Use Case 1 • Customer Retention", "Caller: Sarah Jenkins (CID: #48291) • LTV: $2,400 • Tenured 6 Years")

    img1_path = os.path.join(assets_dir, "story1_billing_dispute.png")
    if os.path.exists(img1_path):
        s5.shapes.add_picture(img1_path, Inches(0.8), Inches(1.8), width=Inches(7.6))

    # Right Side: Annotated Value Story Takeaways
    x_ann = Inches(8.7)
    ann1 = [
        ("The Customer Trigger", "Sarah received an unexpected $150 roaming fee on her bill and threatened churn if not waived immediately (Churn Risk: 82%).", C_TEXT_DARK),
        ("KG Grounded Rule", "SOP-04 Section 2 limits Tier-1 reps to $50. However, Section 4.2 authorizes up to $250 for customers with LTV > $1,500 and clean history.", C_INDIGO),
        ("Autonomous Action", "Agent applies Section 4.2 instantly in voice dialog without supervisor transfer. 100% First Contact Resolution.", C_EMERALD),
        ("Net ROI Preserved", "+$2,250 Net Value ($2,400 customer LTV protected vs $150 concession). 42s handle time.", C_AMBER),
        ("Policy Drift Alert", "67% of billing concessions rely on Clause 4.2 -> Triggers dashed feedback loop to update baseline SOP-04 from $50 to $150.", C_PINK)
    ]

    for m, (atitle, adesc, acol) in enumerate(ann1):
        y = Inches(1.8 + m * 1.0)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_ann, y, Inches(3.8), Inches(0.92))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BG_CARD
        box.line.color.rgb = acol
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.08)

        p = tf.paragraphs[0]
        p.text = atitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = acol

        p2 = tf.add_paragraph()
        p2.text = adesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 6: VALUE STORY 2 - BROADBAND OUTAGE (LOS TELEMETRY)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Value Story 2: Broadband Outage & Telemetry Preemption", "Use Case 2 • Technical Operations", "Caller: Marcus Vance • Plan: 1Gbps Fiber • Status: Red Optical Alarm (LOS)")

    img2_path = os.path.join(assets_dir, "story2_broadband_outage.png")
    if os.path.exists(img2_path):
        s6.shapes.add_picture(img2_path, Inches(0.8), Inches(1.8), width=Inches(7.6))

    ann2 = [
        ("The Customer Trigger", "Marcus's fiber ONT router blinks red. He already rebooted 3 times and demands an immediate emergency truck roll.", C_TEXT_DARK),
        ("Telemetry Preemption", "Agent automatically queries Upstream Hub Telemetry: confirms Red Optical Signal Loss (LOS) at neighborhood feeder splice.", C_INDIGO),
        ("Autonomous Action", "Under SOP-12 Clause 6.1, agent completely bypasses repetitive reboot scripts and books priority field engineer in 2 hours.", C_EMERALD),
        ("Net ROI Created", "+$340 Avoided Cost by preventing false dispatches and saving 18 minutes of frustrating repetitive troubleshooting.", C_AMBER),
        ("Policy Drift Alert", "84% of LOS calls skip remote diagnostics -> Updates SOP-12 triage trees to require telemetry query prior to customer interaction.", C_PINK)
    ]

    for m, (atitle, adesc, acol) in enumerate(ann2):
        y = Inches(1.8 + m * 1.0)
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_ann, y, Inches(3.8), Inches(0.92))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BG_CARD
        box.line.color.rgb = acol
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.08)

        p = tf.paragraphs[0]
        p.text = atitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = acol

        p2 = tf.add_paragraph()
        p2.text = adesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 7: VALUE STORY 3 - VIP ENTERPRISE RETENTION ($18K CHURN RISK)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Value Story 3: VIP Enterprise Retention ($18k Contract Churn)", "Use Case 3 • Revenue Protection", "Caller: Elena Rostova (Apex Global Logistics) • Account ARR: $18,000 USD")

    img3_path = os.path.join(assets_dir, "story3_vip_retention.png")
    if os.path.exists(img3_path):
        s7.shapes.add_picture(img3_path, Inches(0.8), Inches(1.8), width=Inches(7.6))

    ann3 = [
        ("The Customer Trigger", "Elena presents a competitor proposal matching fiber connectivity at a 15% discount. Demands rate match or full termination.", C_TEXT_DARK),
        ("Commercial Guardrail", "Standard reps capped at 5% discount. But SOP-28 Executive Clause 3.1 allows 15% for enterprise ARR > $15k with 24-month lock.", C_INDIGO),
        ("Autonomous Action", "Voice agent applies 15% reduction ($18k -> $15,300) bound to 2-year contract amendment and routes DocuSign immediately.", C_EMERALD),
        ("Net ARR Protected", "+$15,300 Net Retained ARR ($18k ARR saved - $2.7k discount). Prevents $36k multi-year customer loss.", C_AMBER),
        ("Bottleneck Crushed", "Eliminated a 4-day sales director pricing approval chain; customer signed and retained during the call.", C_PINK)
    ]

    for m, (atitle, adesc, acol) in enumerate(ann3):
        y = Inches(1.8 + m * 1.0)
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_ann, y, Inches(3.8), Inches(0.92))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BG_CARD
        box.line.color.rgb = acol
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.08)

        p = tf.paragraphs[0]
        p.text = atitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = acol

        p2 = tf.add_paragraph()
        p2.text = adesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 8: DOCUMENT-TO-GRAPH EXTRACTION PIPELINE (GROQ LPU)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Document-to-Graph Extraction Pipeline: Groq LPU Engine", "Technical Ingestion", "Extracting Knowledge Graphs and Context Graphs from raw text documents with sub-second inference.")

    img_ext = os.path.join(assets_dir, "extractor_pipeline.png")
    if os.path.exists(img_ext):
        s8.shapes.add_picture(img_ext, Inches(0.8), Inches(1.8), width=Inches(7.6))

    ext_notes = [
        ("Raw Text Ingestion", "Ingests 3 unformatted SOP policy manuals and 3 real-world timestamped call transcripts directly from the repository.", C_TEXT_DARK),
        ("Default Groq Cloud LPU", "Powered by Llama-3.3-70B running on Groq LPUs at 340+ tokens/sec with sub-400ms round-trip latency.", C_AMBER),
        ("Knowledge Graph Triples", "Extracts explicit policy nodes and predicates: (SOP-04) -[:governs]-> ($50 Cap), (SOP-04) -[:allows_exception]-> (Clause 4.2).", C_INDIGO),
        ("Context Graph Triples", "Extracts runtime event nodes and customer states: (Sarah Jenkins) -[:disputed]-> ($150 Roaming), (Sarah) -[:LTV]-> ($2,400).", C_EMERALD),
        ("Real-Time Synchronization", "One click on 'Apply Extracted Graph' maps the LLM-derived triples straight onto the live Vis.js canvas.", C_PINK)
    ]

    for m, (atitle, adesc, acol) in enumerate(ext_notes):
        y = Inches(1.8 + m * 1.0)
        box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_ann, y, Inches(3.8), Inches(0.92))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BG_CARD
        box.line.color.rgb = acol
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.08)

        p = tf.paragraphs[0]
        p.text = atitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = acol

        p2 = tf.add_paragraph()
        p2.text = adesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 9: BUSINESS IMPACT & ROI SCORECARD
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Enterprise Business Impact & Operational Scorecard", "Business Value & ROI", "Quantified business results across compliance, handle time, and net revenue.")

    metrics = [
        {"metric": "92%", "label": "First Contact Resolution", "sub": "Up from 61% baseline; eliminates repetitive escalations", "col": C_EMERALD},
        {"metric": "42 sec", "label": "Average Handle Time (AHT)", "sub": "Down from 4.8 min average; zero supervisor transfer wait", "col": C_INDIGO},
        {"metric": "100%", "label": "Audit Compliance", "sub": "Every concession mapped directly to verified SOP exception clauses", "col": C_AMBER},
        {"metric": "+$2,250", "label": "Net Value Per Dispute", "sub": "High-LTV customer accounts preserved at fractional concession cost", "col": C_PINK}
    ]

    for idx, m in enumerate(metrics):
        x = Inches(0.8 + idx * 2.95)
        mcard = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(4.8))
        mcard.fill.solid()
        mcard.fill.fore_color.rgb = C_BG_CARD
        mcard.line.color.rgb = m["col"]
        mcard.line.width = Pt(1.5)

        tf = mcard.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.4)

        pm = tf.paragraphs[0]
        pm.text = m["metric"]
        pm.font.size = Pt(36)
        pm.font.bold = True
        pm.font.color.rgb = m["col"]
        pm.space_after = Pt(14)

        pl = tf.add_paragraph()
        pl.text = m["label"]
        pl.font.size = Pt(15)
        pl.font.bold = True
        pl.font.color.rgb = C_TEXT_DARK
        pl.space_after = Pt(14)

        ps = tf.add_paragraph()
        ps.text = m["sub"]
        ps.font.size = Pt(11)
        ps.font.color.rgb = C_TEXT_MUTED
        ps.line_spacing = 1.25

    # =========================================================================
    # SLIDE 10: ARCHITECTURE BLUEPRINT & LIVE DEMO ACCESS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Production Architecture Blueprint & Live Interactive Demo", "Production Roadmap", "Ready for deployment in AWS project 'For Each and Every' (region us-east-2).")

    # Left: AWS Production Blueprint
    card_aws = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card_aws.fill.solid()
    card_aws.fill.fore_color.rgb = C_BG_CARD
    card_aws.line.color.rgb = C_INDIGO
    card_aws.line.width = Pt(1.5)

    tf_aws = card_aws.text_frame
    tf_aws.word_wrap = True
    tf_aws.margin_left = Inches(0.3)
    tf_aws.margin_top = Inches(0.3)

    p = tf_aws.paragraphs[0]
    p.text = "AWS Enterprise Cloud Blueprint (us-east-2)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p.space_after = Pt(14)

    aws_bullets = [
        "Region: us-east-2 (Project: 'For Each and Every')",
        "Document Ingestion: Amazon Bedrock (anthropic.claude-3-5-sonnet) extracts SOP PDFs into OWL/RDF ontologies.",
        "Graph Storage: Amazon Neptune (Serverless OpenCypher/SPARQL) stores Knowledge Graph and temporal Context Graph.",
        "Runtime Voice Agent: Amazon Bedrock (Nova-Lite / Llama-3.3-70B) or Groq Cloud LPU for sub-250ms streaming voice.",
        "Telephony Integration: Amazon Connect / SIP Trunk with real-time audio ASR transcription."
    ]

    for b in aws_bullets:
        pb = tf_aws.add_paragraph()
        pb.text = f"• {b}"
        pb.font.size = Pt(11)
        pb.font.color.rgb = C_TEXT_DARK
        pb.space_after = Pt(8)
        pb.line_spacing = 1.2

    # Right: Live Demo Links
    card_demo = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card_demo.fill.solid()
    card_demo.fill.fore_color.rgb = C_BG_CARD
    card_demo.line.color.rgb = C_EMERALD
    card_demo.line.width = Pt(1.5)

    tf_demo = card_demo.text_frame
    tf_demo.word_wrap = True
    tf_demo.margin_left = Inches(0.3)
    tf_demo.margin_top = Inches(0.3)

    p = tf_demo.paragraphs[0]
    p.text = "Live Interactive Links & Source Repositories"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(14)

    demo_bullets = [
        "Live Interactive Web Studio:\nhttps://cosmosanalytics.github.io/uat-copilot-local/callcenter_ai_voice_agents.html",
        "Mirror Live Studio:\nhttps://cosmosanalytics.github.io/Langchain-test/callcenter_ai_voice_agents.html",
        "GitHub Repository (Code & Pipeline):\nhttps://github.com/cosmosanalytics/uat-copilot-local",
        "Raw SOP Policy Documents:\nhttps://github.com/cosmosanalytics/uat-copilot-local/tree/main/docs/sops",
        "Raw Call Scripts:\nhttps://github.com/cosmosanalytics/uat-copilot-local/tree/main/docs/transcripts"
    ]

    for b in demo_bullets:
        pb = tf_demo.add_paragraph()
        pb.text = f"• {b}"
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = C_TEXT_DARK
        pb.space_after = Pt(8)
        pb.line_spacing = 1.15

    # Save presentation
    output_pptx = os.path.abspath("Call_Center_AI_Voice_Agents_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Successfully generated PowerPoint presentation at: {output_pptx}")

if __name__ == "__main__":
    create_deck()
