from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

OUTPUT = r"D:\Profiles\Documents\Claude\docs\TSA_Cesar_Curado_Call_Prep.pdf"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# ── Colors ──────────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#0D1B2A")
MID_BLUE    = colors.HexColor("#1B3A5C")
ACCENT_BLUE = colors.HexColor("#2E6DA4")
LIGHT_BLUE  = colors.HexColor("#D6E8F7")
WHITE       = colors.white
GRAY        = colors.HexColor("#555555")
LIGHT_GRAY  = colors.HexColor("#F2F6FA")
GREEN       = colors.HexColor("#1A7A4A")
RED         = colors.HexColor("#B02020")

# ── Page setup ───────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

def footer_content(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, PAGE_W, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(PAGE_W / 2, 3.5 * mm,
        "Bruno Alexandre  |  Shaingan  |  hello@shaingan.com")
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=14 * mm, bottomMargin=18 * mm,
    onFirstPage=footer_content,
    onLaterPages=footer_content,
)

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

heading1 = S("H1", fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,
              leading=26, alignment=TA_CENTER)
heading2 = S("H2", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE,
              leading=15, spaceAfter=0, spaceBefore=0)
heading3 = S("H3", fontName="Helvetica-Bold", fontSize=9.5, textColor=ACCENT_BLUE,
              leading=13, spaceAfter=2, spaceBefore=6)
body     = S("Body", fontName="Helvetica", fontSize=8.5, textColor=DARK_BLUE,
              leading=13, spaceAfter=2)
body_sm  = S("BodySm", fontName="Helvetica", fontSize=8, textColor=GRAY,
              leading=12, spaceAfter=1)
bold_sm  = S("BoldSm", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK_BLUE,
              leading=13, spaceAfter=2)
label    = S("Label", fontName="Helvetica-Bold", fontSize=7.5, textColor=ACCENT_BLUE,
              leading=11)
qa_q     = S("QQ", fontName="Helvetica-Bold", fontSize=8.5, textColor=MID_BLUE,
              leading=13, spaceAfter=1)
qa_a     = S("QA", fontName="Helvetica", fontSize=8.5, textColor=DARK_BLUE,
              leading=13, spaceAfter=6, leftIndent=8)
num_item = S("Num", fontName="Helvetica", fontSize=8.5, textColor=DARK_BLUE,
              leading=13, spaceAfter=2, leftIndent=4)
italic_sm = S("Italic", fontName="Helvetica-Oblique", fontSize=8, textColor=GRAY,
              leading=12)

story = []

# ═══════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════
header_data = [[
    Paragraph("César Curado / TSA Mudanças", heading1),
]]
header_table = Table(header_data, colWidths=[PAGE_W - 2 * MARGIN])
header_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
    ("TOPPADDING",    (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ("ROUNDEDCORNERS", [4]),
]))
story.append(header_table)

sub_data = [[
    Paragraph("Client Call Prep Sheet", S("Sub", fontName="Helvetica",
        fontSize=10, textColor=LIGHT_BLUE, leading=14, alignment=TA_CENTER))
]]
sub_table = Table(sub_data, colWidths=[PAGE_W - 2 * MARGIN])
sub_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(sub_table)
story.append(Spacer(1, 5 * mm))

# ── Helper: section header ────────────────────────────────────────────────
def section_header(title):
    t = Table([[Paragraph(title, heading2)]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    return t

def info_row(label_text, value_text):
    return [
        Paragraph(label_text, label),
        Paragraph(value_text, body),
    ]

def card(rows_data, col_widths=None):
    if col_widths is None:
        col_widths = [45 * mm, PAGE_W - 2 * MARGIN - 45 * mm]
    t = Table(rows_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════════════
# 1. CLIENT OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("1. CLIENT OVERVIEW"))
story.append(Spacer(1, 2))
overview_rows = [
    info_row("Company",   "Transportes Senhora da Agonia, Lda (TSA Mudanças)"),
    info_row("Contact",   "César Curado"),
    info_row("Email",     "mudatudo@gmail.com"),
    info_row("Phone",     "+351 965 653 025  /  +34 603 503 656"),
    info_row("Websites",  "mudatudo.com  ·  mudancas.pt  ·  removalstoportugal.com  ·  international-removals.es"),
    info_row("Since",     "1986 — over 35 years in the removals business"),
    info_row("Platform",  "WordPress (all 4 sites)"),
]
story.append(card(overview_rows))
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 2. WEBSITE TRAFFIC REPORT
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("2. WEBSITE TRAFFIC REPORT"))
story.append(Spacer(1, 2))

traffic_header = [
    Paragraph("Website", bold_sm),
    Paragraph("Monthly Visits", bold_sm),
    Paragraph("Trend", bold_sm),
    Paragraph("Market", bold_sm),
    Paragraph("Auto Quote?", bold_sm),
]
traffic_rows = [
    traffic_header,
    [Paragraph("mudatudo.com", body), Paragraph("~1,600", body),
     Paragraph("-22.6%", S("Red", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13)),
     Paragraph("Portugal", body), Paragraph("NO", S("Red", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13))],
    [Paragraph("mudancas.pt", body), Paragraph("~163", body),
     Paragraph("-78.75%", S("Red2", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13)),
     Paragraph("Portugal", body), Paragraph("NO", S("Red3", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13))],
    [Paragraph("removalstoportugal.com", body), Paragraph("~108", body),
     Paragraph("-73.27%", S("Red4", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13)),
     Paragraph("UK", body), Paragraph("NO", S("Red5", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13))],
    [Paragraph("international-removals.es", body_sm), Paragraph("—", body),
     Paragraph("—", body), Paragraph("Spain", body),
     Paragraph("NO", S("Red6", fontName="Helvetica-Bold", fontSize=8.5, textColor=RED, leading=13))],
]
col_w = [(PAGE_W - 2 * MARGIN) / 5] * 5
traffic_table = Table(traffic_rows, colWidths=col_w)
traffic_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), MID_BLUE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("BACKGROUND",    (0, 1), (-1, -1), LIGHT_GRAY),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(traffic_table)
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 3. THE OPPORTUNITY
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("3. THE OPPORTUNITY"))
story.append(Spacer(1, 2))

opp_items = [
    ("None of the 4 websites have automated quote systems", "Every quote requires manual phone/email — losing speed to competitors."),
    ("All sites losing traffic", "When visits drop, every single lead becomes MORE valuable. Can't afford to lose any."),
    ("1,600 visits/mo on main site × 5% conversion", "= 80 potential leads/month. Missing just 20% = ~16 lost leads."),
    ("Average moving job value ~€500", "16 lost leads/month × €500 = ~€8,000 lost revenue monthly."),
    ("WordPress platform", "= Easy 30-minute embed. No rebuild, no developer needed."),
]

opp_rows = []
for title, detail in opp_items:
    opp_rows.append([
        Paragraph("→", S("Arrow", fontName="Helvetica-Bold", fontSize=9, textColor=ACCENT_BLUE, leading=13)),
        [Paragraph(title, bold_sm), Paragraph(detail, body_sm)],
    ])

opp_table = Table(opp_rows, colWidths=[8 * mm, PAGE_W - 2 * MARGIN - 8 * mm])
opp_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]))
story.append(opp_table)
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 4. PRICING
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("4. YOUR PRICING"))
story.append(Spacer(1, 2))

pricing_rows = [
    [Paragraph("Option", bold_sm), Paragraph("Setup", bold_sm),
     Paragraph("Monthly", bold_sm), Paragraph("Tools Cost", bold_sm), Paragraph("Your Profit/mo", bold_sm)],
    [Paragraph("1 website", body), Paragraph("€400", body),
     Paragraph("€50", body), Paragraph("€26.13 (Zapier Pro)", body_sm),
     Paragraph("€23.87+", S("Green", fontName="Helvetica-Bold", fontSize=8.5, textColor=GREEN, leading=13))],
    [Paragraph("4 websites package", S("BoldOpt", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=ACCENT_BLUE, leading=13)),
     Paragraph("€1,000", S("BoldGreen", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=GREEN, leading=13)),
     Paragraph("€150", S("BoldGreen2", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=GREEN, leading=13)),
     Paragraph("€26.13 (Zapier Pro)", body_sm),
     Paragraph("€123.87+", S("Green2", fontName="Helvetica-Bold", fontSize=8.5, textColor=GREEN, leading=13))],
]
pricing_cw = [50*mm, 28*mm, 28*mm, 48*mm, (PAGE_W - 2*MARGIN - 154*mm)]
pricing_table = Table(pricing_rows, colWidths=pricing_cw)
pricing_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), MID_BLUE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("BACKGROUND",    (0, 1), (-1, 1), LIGHT_GRAY),
    ("BACKGROUND",    (0, 2), (-1, 2), colors.HexColor("#EAF4EE")),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(pricing_table)
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 5. CALL STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("5. CALL STRUCTURE  (15 minutes)"))
story.append(Spacer(1, 2))

call_rows = [
    [Paragraph("0–2 min", bold_sm),   Paragraph("Quick introduction — who you are, what Shaingan does in one line.", body)],
    [Paragraph("2–8 min", bold_sm),   Paragraph("Ask your questions (see Section 6). Listen more than you talk.", body)],
    [Paragraph("8–12 min", bold_sm),  Paragraph("Show LIVE DEMO — share screen, open quick-move-quote-pro.lovable.app and walk through it.", body)],
    [Paragraph("12–15 min", bold_sm), Paragraph("Answer their questions (see Section 7) and close with the pilot offer.", body)],
]
story.append(card(call_rows, col_widths=[30 * mm, PAGE_W - 2 * MARGIN - 30 * mm]))
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 6. QUESTIONS TO ASK
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("6. QUESTIONS TO ASK CÉSAR"))
story.append(Spacer(1, 2))

questions_pt = [
    "Quantos pedidos de orçamento recebem por semana aproximadamente?",
    "Como respondem atualmente aos pedidos de orçamento — por telefone, email?",
    "Quanto tempo demora normalmente a responder a um pedido?",
    "Têm uma tabela de preços definida ou cada orçamento é calculado manualmente?",
    "Quais são os serviços principais que querem incluir no formulário?",
    "Qual dos websites é o principal — mudatudo.com ou mudancas.pt?",
    "Têm acesso ao painel WordPress (admin) dos websites?",
    "Quem gere os websites atualmente?",
    "Preferem o formulário num website específico ou em todos?",
    "Qual é a vossa maior dificuldade com os pedidos de orçamento agora?",
    "Já tentaram alguma solução automática antes?",
    "Qual seria o resultado ideal para vocês?",
]

q_rows = []
for i, q in enumerate(questions_pt, 1):
    q_rows.append([
        Paragraph(str(i), S(f"QN{i}", fontName="Helvetica-Bold", fontSize=8.5,
                             textColor=WHITE, leading=13, alignment=TA_CENTER)),
        Paragraph(q, body),
        Paragraph("_" * 35, italic_sm),
    ])

q_table = Table(q_rows, colWidths=[7*mm, 85*mm, PAGE_W - 2*MARGIN - 92*mm])
q_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (0, -1), ACCENT_BLUE),
    ("BACKGROUND",    (1, 0), (-1, -1), LIGHT_GRAY),
    ("ROWBACKGROUNDS", (1, 0), (-1, -1), [LIGHT_GRAY, WHITE]),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]))
story.append(q_table)
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 7. Q&A — QUESTIONS HE WILL ASK
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("7. Q&A — QUESTIONS HE WILL ASK YOU"))
story.append(Spacer(1, 2))

qa_pairs = [
    ("Já fez este tipo de trabalho antes?",
     "Sim, desenvolvi recentemente um sistema completo de orçamentos automáticos para uma empresa de mudanças. Podem ver aqui: quick-move-quote-pro.lovable.app. O sistema envia orçamentos automáticos em menos de 2 minutos."),
    ("Quanto custa?",
     "A implementação inicial num website custa €400 e inclui tudo — o formulário, a automação, os emails automáticos e o registo em folha de cálculo. A manutenção mensal é €50. Para os 4 websites posso fazer um pacote especial de €1,000 setup + €150/mês."),
    ("Quanto tempo demora?",
     "Para um website, consigo entregar em 2–3 dias úteis após termos todos os detalhes definidos."),
    ("Como funciona exatamente?",
     "O cliente preenche o formulário no vosso website. Em menos de 2 minutos recebe um email automático com uma estimativa de preço. Ao mesmo tempo, vocês recebem uma notificação com todos os dados do cliente, e o pedido fica registado automaticamente numa folha de cálculo."),
    ("Precisam de alterar o nosso website?",
     "Não é necessário alterar nada no design atual. Adicionamos apenas um formulário numa página existente ou nova — o resto do website fica exatamente igual."),
    ("Os dados dos clientes ficam seguros?",
     "Sim. Os dados são processados através do Zapier, utilizado por mais de 2 milhões de empresas mundialmente e cumpre todas as normas de segurança e RGPD."),
    ("Têm custos mensais?",
     "Sim, €50/mês que inclui Zapier (plataforma de automação), suporte e manutenção, e pequenos ajustes quando necessário. Podem cancelar a qualquer altura."),
    ("E se o sistema deixar de funcionar?",
     "Estou disponível para resolver qualquer problema rapidamente. O €50/mês inclui suporte contínuo."),
    ("Podem implementar nos 4 websites?",
     "Sim. Para os 4 websites ofereço €1,000 setup (em vez de €1,600) e €150/mês para todos. Começamos por um para garantir que está perfeito, depois expandimos."),
]

qa_rows = []
for q, a in qa_pairs:
    qa_rows.append([
        Paragraph(f"Q: {q}", qa_q),
        Paragraph(f"A: {a}", qa_a),
    ])

qa_table = Table(qa_rows, colWidths=[(PAGE_W - 2*MARGIN)/2, (PAGE_W - 2*MARGIN)/2])
qa_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GRAY, WHITE]),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 7),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]))
story.append(qa_table)
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 8. THE CLOSE
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("8. THE CLOSE"))
story.append(Spacer(1, 2))

close_text = (
    '"Com base no que discutimos, consigo implementar isto no mudatudo.com em 2–3 dias. '
    'Quer que avancemos com um projeto piloto num website para ver os resultados?"'
)
close_table = Table(
    [[Paragraph(close_text, S("Close", fontName="Helvetica-BoldOblique", fontSize=10,
                               textColor=DARK_BLUE, leading=16, alignment=TA_CENTER))]],
    colWidths=[PAGE_W - 2 * MARGIN]
)
close_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#EAF4EE")),
    ("TOPPADDING",    (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LEFTPADDING",   (0, 0), (-1, -1), 12),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ("BOX",           (0, 0), (-1, -1), 1.5, GREEN),
]))
story.append(close_table)
story.append(Spacer(1, 4 * mm))

# ═══════════════════════════════════════════════════════════════════════════
# 9. PRE-CALL CHECKLIST
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("9. BEFORE THE CALL CHECKLIST"))
story.append(Spacer(1, 2))

checklist = [
    "Demo link working: quick-move-quote-pro.lovable.app",
    "Screen share ready to show demo live",
    "Price list ready: €400 + €50/mo per site  |  4-site package: €1,000 + €150/mo",
    "This prep sheet open for reference",
    "Notebook ready to take notes",
]

check_rows = []
for item in checklist:
    check_rows.append([
        Paragraph("☐", S("CB", fontName="Helvetica", fontSize=11, textColor=ACCENT_BLUE, leading=13)),
        Paragraph(item, body),
    ])

check_table = Table(check_rows, colWidths=[8 * mm, PAGE_W - 2 * MARGIN - 8 * mm])
check_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GRAY, WHITE]),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 7),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ("LINEBELOW",     (0, 0), (-1, -2), 0.3, colors.HexColor("#C8D8E8")),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(check_table)

# ── Build ─────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF created: {OUTPUT}")
