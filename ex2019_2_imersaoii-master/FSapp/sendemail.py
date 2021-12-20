import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



def send(email, matricula):
    try:
        fromaddr = "testeemail@fabrica.unipe.br"
        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = email
        msg['Subject'] = "Imersao"

        body = "Este é o seu qrcode que será usado na imersão da fábrica de software"

        msg.attach(MIMEText(body, 'plain'))

        filename = str(matricula) + '.png'

        attachment = open('media/qrcode/'+str(matricula)+'.png', 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        attachment.close()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "imersao2.0")
        text = msg.as_string()

        server.sendmail(fromaddr, email, text)
        server.quit()
        print('\nEmail enviado com sucesso!')


    except Exception as e:
        print(e)
        print("\nErro ao enviar email")









def sendlink(lista):
    sender = "testeemail@fabrica.unipe.br"
    print(lista)
    msg = MIMEMultipart()
    msg['From'] = sender

    msg['To']  = ", ".join(lista)
    msg['Subject'] = "Inscrição Área de Interesse - Fábrica de Software"

    body = "Esse e-mail é um teste."
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtpObj = smtplib.SMTP("smtp.gmail.com",587)
        smtpObj.ehlo()
        smtpObj.starttls()

        smtpObj.login("testeemail@fabrica.unipe.br", "imersao2.0")
        smtpObj.sendmail(sender, lista, msg.as_string())
        print("Email enviado!")
    except Exception as e:
        print(e)