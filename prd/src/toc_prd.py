import re, subprocess, sys, copy
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

D = "/home/claude/nivotime/prd/"
SOFF = "/root/.claude/skills/synced/5b175db4-abfe-46f2-a7e7-95413f494a7c_5fc3112e-28c3-4505-8ae9-7b97ecc16549/docx/scripts/office/soffice.py"
PURPLE = RGBColor(0x3B, 0x3A, 0x73); FONT = "Times New Roman"; TEXT_W = 6.27

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def headings(doc):
    out = []
    for p in doc.paragraphs:
        sn = p.style.name
        if sn in ("Heading 1", "Heading 2"):
            bm = p._p.find(qn("w:bookmarkStart"))
            out.append((1 if sn == "Heading 1" else 2, p.text.strip(), bm.get(qn("w:name")) if bm is not None else None))
    return out

def build(pages):
    doc = Document(D + "stage.docx")
    hs = headings(doc)
    marker = [p for p in doc.paragraphs if p.text == "[[TOC]]"][0]
    for i, (lvl, text, bm) in enumerate(hs):
        p = doc.add_paragraph()
        pf = p.paragraph_format; pf.line_spacing = 1.0
        section = text.startswith("SECTION ")
        pf.space_before = Pt(7 if (lvl == 1) else 0); pf.space_after = Pt(1.5)
        pf.left_indent = Inches(0 if lvl == 1 else 0.3)
        pf.tab_stops.add_tab_stop(Inches(TEXT_W), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        link = OxmlElement("w:hyperlink")
        if bm: link.set(qn("w:anchor"), bm)
        def run(t, bold=False, color=None, size=10.5):
            r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
            rf = OxmlElement("w:rFonts"); [rf.set(qn(a), FONT) for a in ("w:ascii", "w:hAnsi", "w:cs")]; rpr.append(rf)
            if bold: rpr.append(OxmlElement("w:b"))
            if color: c = OxmlElement("w:color"); c.set(qn("w:val"), color); rpr.append(c)
            sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size*2))); rpr.append(sz)
            r.append(rpr); tt = OxmlElement("w:t"); tt.set(qn("xml:space"), "preserve"); tt.text = t; r.append(tt); return r
        color = "3B3A73" if lvl == 1 else "000000"
        size = 10 if section else (11 if lvl == 1 else 10.5)
        link.append(run(text, bold=(lvl == 1), color="5E8A2E" if section else color, size=size))
        if not section:
            link.append(run("\t" + str(pages.get(i, "00")), bold=(lvl == 1), color=color, size=size))
        p._p.append(link)
        marker._p.addprevious(p._p)
    marker._p.getparent().remove(marker._p)
    doc.save(D + "NivoTime_PRD_Dashboard_Prototype.docx")
    return hs

def render():
    subprocess.run(f"cd {D} && python3 {SOFF} --headless --convert-to pdf NivoTime_PRD_Dashboard_Prototype.docx >/dev/null 2>&1", shell=True)
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(f"pdfinfo {D}NivoTime_PRD_Dashboard_Prototype.pdf", shell=True, capture_output=True, text=True).stdout).group(1))
    texts = [norm(subprocess.run(f"pdftotext -f {k} -l {k} {D}NivoTime_PRD_Dashboard_Prototype.pdf -", shell=True, capture_output=True, text=True).stdout) for k in range(1, n+1)]
    return n, texts

def locate(hs, texts, start):
    pages = {}; cur = start
    for i, (lvl, text, bm) in enumerate(hs):
        key = norm(text)[:40]
        for k in range(cur, len(texts)):
            if key in texts[k]:
                pages[i] = k + 1; cur = k; break
        else:
            print("NOT FOUND:", text)
    return pages

hs = build({})
n, texts = render()
# first content page = first page (after TOC) containing the CEO summary heading
start = next(k for k in range(2, n) if norm("Document Control") in texts[k] and "tableofcontents" not in texts[k])
pages = locate(hs, texts, start)
build(pages)
n2, texts2 = render()
start2 = next(k for k in range(2, n2) if norm("Document Control") in texts2[k] and "tableofcontents" not in texts2[k])
pages2 = locate(hs, texts2, start2)
print("pages:", n2, "stable:", pages == pages2)
if pages != pages2:
    build(pages2); n3, t3 = render(); print("rebuilt", n3)
