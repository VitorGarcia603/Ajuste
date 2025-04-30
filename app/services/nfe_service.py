import base64, os, hashlib, datetime, tempfile
from pathlib import Path
from lxml import etree
from qrcode import make as make_qr
from reportlab.pdfgen import canvas
import xmlsec
from pynfe.nfe import NFe

MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", "media/nfe"))
XML_DIR  = MEDIA_ROOT / "xml"
PDF_DIR  = MEDIA_ROOT / "pdf"
XML_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(parents=True, exist_ok=True)

PFX_B64  = os.getenv("NFE_PFX_BASE64", "")
PFX_PWD  = os.getenv("NFE_PFX_PWD", "")

def _hash(pedido_id:int) -> str:
    return hashlib.sha1(f"{pedido_id}".encode()).hexdigest()[:10]

def gerar_xml(pedido) -> Path:
    xml_path = XML_DIR / f"NFe-{_hash(pedido.id)}.xml"
    if xml_path.exists():
        return xml_path

    nfe = NFe(versao='4.00')

    nfe.emitente(
        cnpj=pedido.empresa.cnpj,
        razao_social=pedido.empresa.razao_social,
        ie=pedido.empresa.ie or "ISENTO",
        uf=pedido.empresa.uf,
        municipio=pedido.empresa.cidade
    )
    nfe.destinatario(
        cpfcnpj=pedido.cliente.cnpj,
        razao_social=pedido.cliente.razao_social,
        uf=pedido.cliente.uf,
        municipio=pedido.cliente.cidade
    )
    for item in pedido.itens:
        nfe.adicionar_item(
            codigo=item.produto.codigo,
            descricao=item.produto.descricao,
            ncm=item.produto.ncm,
            cfop=item.produto.cfop,
            unidade=item.produto.unidade,
            quantidade=item.qtd,
            valor_unit=item.preco,
            icms_situacao="102",
            icms_origem="0"
        )
    nfe.calcular_totais()
    nfe.ide(serie=1, numero=pedido.id, dh_emissao=datetime.datetime.now())
    nfe.add_duplicata(numero=1, valor=nfe.total['vNF'], vencimento=datetime.date.today())
    xml_path.write_text(nfe.xml(), encoding="utf-8")
    return xml_path

def assinar_xml(xml_path: Path) -> Path:
    if not PFX_B64:
        return xml_path
    key_data = base64.b64decode(PFX_B64)
    doc = etree.parse(str(xml_path))
    xmlsec.tree.add_ids(doc, ["infNFe"])
    ctx = xmlsec.SignatureContext()
    key = xmlsec.Key.from_memory(key_data, xmlsec.KeyFormat.PKCS12, PFX_PWD)
    ctx.key = key
    signature_node = xmlsec.template.create(
        doc,
        xmlsec.Transform.EXCL_C14N,
        xmlsec.Transform.RSA_SHA1,
        ns="ds"
    )
    doc.getroot().insert(0, signature_node)
    ref = xmlsec.template.add_reference(signature_node, xmlsec.Transform.SHA1)
    xmlsec.template.add_transform(ref, xmlsec.Transform.ENVELOPED)
    xmlsec.template.add_transform(ref, xmlsec.Transform.EXCL_C14N)
    xmlsec.template.ensure_key_info(signature_node)
    ctx.sign(signature_node)
    xml_path.write_bytes(etree.tostring(doc, xml_declaration=True, encoding="utf-8"))
    return xml_path

def validar_xml(xml_path: Path) -> list:
    # Placeholder validation stub
    return []

def gerar_danfe(xml_path: Path) -> Path:
    pdf_path = PDF_DIR / xml_path.name.replace("NFe", "DANFE").replace(".xml", ".pdf")
    if pdf_path.exists():
        return pdf_path
    c = canvas.Canvas(str(pdf_path), pagesize=(595, 842))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 800, "DANFE – Documento Auxiliar da NF-e (MODELO 55) – HOMOLOGAÇÃO")
    c.setFont("Helvetica", 10)
    c.drawString(40, 780, f"Arquivo XML: {xml_path.name}")
    qr_data = f"https://hom.sefaz/scdanfe/{xml_path.stem}"
    qr_img = make_qr(qr_data).resize((140,140))
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        qr_img.save(tmp.name)
        c.drawImage(tmp.name, 40, 620)
    c.showPage()
    c.save()
    return pdf_path
