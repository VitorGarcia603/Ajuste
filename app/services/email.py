from flask_mail import Message
from app import mail, app

def enviar_pedido(destinatario, pdf_bytes, numero):
    with app.app_context():
        msg = Message(subject=f"Pedido {numero}",
                      recipients=[destinatario],
                      body="Segue PDF do Pedido em anexo.")
        msg.attach(filename=f"pedido_{numero}.pdf",
                   content_type="application/pdf",
                   data=pdf_bytes)
        mail.send(msg)
