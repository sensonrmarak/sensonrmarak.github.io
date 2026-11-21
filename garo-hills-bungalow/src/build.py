"""Assemble the report HTML and print it to a single A4 PDF."""
import os, subprocess, sys
import content1 as c1, content2 as c2, content3 as c3, content4 as c4, content5 as c5

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
* { box-sizing: border-box; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 9.6pt; line-height: 1.45; color: #262626; margin: 0; }
p { margin: 0 0 7pt; text-align: justify; }
h1 { font-size: 34pt; margin: 6pt 0 4pt; font-weight: 700; letter-spacing: -0.5pt; color: #2b2b2b; }
h2 { font-size: 12.5pt; margin: 16pt 0 8pt; padding: 6pt 10pt; border-left: 5px solid #9aa58a; border-radius: 2px; color: #2b2b2b; break-after: avoid; }
h3 { font-size: 10.2pt; margin: 10pt 0 4pt; color: #4a3f2a; break-after: avoid; }
.b1 { background: #e7f0e1; } .b2 { background: #f5ead9; } .b3 { background: #e3ebf3; } .b4 { background: #f6e4e8; }
.b5 { background: #ece9dc; } .b6 { background: #e2edee; } .b7 { background: #efe6f3; } .b8 { background: #f8efd6; }
.b9 { background: #e6f1ea; } .b10 { background: #f3e7df; } .b11 { background: #e5e9f4; }
.hl { background: #fff1a8; padding: 0 2pt; border-radius: 2px; font-weight: 600; white-space: nowrap; }
.cover { height: 255mm; display: flex; flex-direction: column; justify-content: center; break-after: page; }
.cover .kicker { text-transform: uppercase; letter-spacing: 2pt; font-size: 9pt; color: #6b7a55; }
.cover .sub { font-size: 12pt; color: #555; margin-bottom: 18pt; font-style: italic; }
.keyfacts { border-collapse: collapse; width: 100%; font-size: 10pt; }
.keyfacts td { border-bottom: 1px solid #e3dccb; padding: 6pt 6pt; vertical-align: top; }
.keyfacts td:first-child { width: 34%; color: #555; }
.note { font-size: 8.4pt; color: #555; }
table.t { border-collapse: collapse; width: 100%; margin: 4pt 0 10pt; }
table.t th { background: #f1ede3; text-align: left; font-weight: 600; padding: 4pt 5pt; border-bottom: 1.5px solid #c9bfa6; }
table.t td { padding: 3.5pt 5pt; border-bottom: 1px solid #ebe5d7; vertical-align: top; }
table.t tr { break-inside: avoid; }
table.small { font-size: 8.6pt; } table.tiny { font-size: 7.5pt; }
table.t .n { text-align: right; white-space: nowrap; }
tr.grp td { background: #faf7f0; font-weight: 700; color: #6b5a33; }
tr.tot td { font-weight: 700; border-top: 1.5px solid #c9bfa6; }
tr.why td { font-size: 7.8pt; color: #6b5a33; font-style: italic; padding-top: 0; }
table.totals { font-size: 9.4pt; }
figure { margin: 6pt 0 10pt; }
figure.dwgfig { break-inside: avoid; border: 1px solid #e3dccb; padding: 0; }
figure.dwgfig svg { width: 100%; height: auto; display: block; }
.refs { display: flex; gap: 8pt; }
.refs figure { flex: 1; margin: 0; } .refs img { width: 100%; height: 150pt; object-fit: cover; border-radius: 3px; }
.refs figcaption { font-size: 7.6pt; color: #666; margin-top: 2pt; }
ul { margin: 0 0 8pt; padding-left: 14pt; } li { margin-bottom: 4pt; }
.pb { break-before: page; }
.sign { margin-top: 16pt; font-size: 8.4pt; color: #555; border-top: 1px solid #ddd; padding-top: 6pt; }
"""


def html():
    parts = [
        c1.cover(), c1.statement(), c1.climate(), c1.references(),
        '<div class="pb"></div>', c2.area_statement(),
        '<div class="pb"></div>', c2.plan_pages(), c2.room_schedule(),
        c2.walls_table(), c2.walkthrough(),
        '<div class="pb"></div>', c3.elevation_section(), c3.structure(),
        '<div class="pb"></div>', c3.dw_schedule(), c3.finishes(),
        '<div class="pb"></div>', c4.firehouse(), c4.garage(),
        '<div class="pb"></div>', c4.landscape(),
        '<div class="pb"></div>', c4.roof_and_gate(),
        '<div class="pb"></div>', c5.cost(), c5.checks(),
    ]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Courtyard Bungalow, Garo Hills</title><style>{CSS}</style></head>
<body>{''.join(parts)}</body></html>"""


PRINT_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.argv[2], { waitUntil: 'load' });
  await p.pdf({ path: process.argv[3], format: 'A4', printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:7pt;color:#777;width:100%;padding:0 15mm;display:flex;justify-content:space-between;font-family:Helvetica,Arial"><span>Courtyard Bungalow, Garo Hills, Meghalaya | Design report</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
  await b.close();
})();
"""

if __name__ == "__main__":
    h = os.path.join(OUT, "Courtyard_Bungalow_Garo_Hills_Design_Report.html")
    pdf = os.path.join(OUT, "Courtyard_Bungalow_Garo_Hills_Design_Report.pdf")
    open(h, "w", encoding="utf-8").write(html())
    js = os.path.join(HERE, "print.js")
    open(js, "w").write(PRINT_JS)
    subprocess.run(["node", js, h, pdf], check=True)
    print(pdf)
