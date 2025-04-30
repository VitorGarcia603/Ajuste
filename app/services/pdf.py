import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

def gerar_pdf_pedido(pedido, empresa):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    if getattr(empresa, "logo_path", None):
        c.drawImage(empresa.logo_path, 20*mm, h-40*mm,
                    height=20*mm, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(70*mm, h-25*mm, empresa.nome)
    c.setFont("Helvetica", 9)
    c.drawString(70*mm, h-30*mm, empresa.endereco)
    c.drawString(70*mm, h-35*mm, f"Tel.: {empresa.telefone}")

    topo = h-50*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, topo, f"PEDIDO #{pedido.numero}")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, topo-6*mm, f"Data: {pedido.data.strftime('%d/%m/%Y')}")

    y = topo-20*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y, "Qtd")
    c.drawString(40*mm, y, "Descrição")
    c.drawString(140*mm, y, "Unit.")
    c.drawString(170*mm, y, "Subtotal")
    c.line(20*mm, y-2*mm, 190*mm, y-2*mm)

    c.setFont("Helvetica", 10)
    for item in pedido.itens:
        y -= 6*mm
        c.drawString(22*mm, y, str(item.qtd))
        c.drawString(40*mm, y, item.produto.nome[:60])
        c.drawRightString(160*mm, y, f"R$ {item.preco_unit:.2f}")
        c.drawRightString(190*mm, y, f"R$ {item.subtotal:.2f}")

    y -= 10*mm
    c.line(120*mm, y, 190*mm, y)
    y -= 6*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(180*mm, y, f"TOTAL: R$ {pedido.total:.2f}")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()
