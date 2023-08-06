
import win32com.client as win32
import re

# def merge_html(html1, signature):
#     html1_soup = BeautifulSoup(html1, 'html.parser')
#     html2_soup = BeautifulSoup(f'<body><p>{signature}<p></body>', 'html.parser')

#     for element in html2_soup.body:
#         html1_soup.body.append(element)
    
#     return str(html1_soup)

def validate_domains(email_list, valid_domains=["@bronxcare.org", "@bronxleb.org"]):
    all_matched = True
    for email in email_list:
        matched = False
        for domain in valid_domains:
            if re.search(f"{domain}$", email):
                matched = True
        
        if not matched:
            print("{email} does not have a valid domain")
            all_matched = False
    
    return all_matched

def send_email(receiver_email_list, subject, body, cc_email_list=[], bcc_email_list=[], attachments=[]):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.GetInspector #Necessary to get signature body
    
    all_emails_valid = validate_domains(receiver_email_list + cc_email_list + bcc_email_list)

    if not all_emails_valid:
        raise NameError("All emails do not have a valid domain!")

    receiver_email_string = ";".join(receiver_email_list)
    cc_email_string = ";".join(cc_email_list)
    bcc_email_string = ";".join(bcc_email_list)

    mail.To = receiver_email_string
    mail.Subject = subject

    index = mail.HTMLBody.find('>', mail.HTMLBody.find('<body'))
    mail.HTMLBody = mail.HTMLBody[:index + 1] + body + mail.HTMLBody[index + 1:]

    mail.CC = cc_email_string
    mail.BCC = bcc_email_string

    counter = 0 
    for attachment in attachments:
        counter+= 1
        mail.Attachments.Add(str(attachment), Position = counter)
    
    mail.Send()




# def send_email(sender_email, receiver_email_list, subject, body, 
#     cc_email_list=[], bcc_email_list=[], attachments=[], mailserver="localhost", port=1025):
    
#     receiver_email_string = ", ".join(receiver_email_list)
#     cc_email_string = ", ".join(cc_email_list)
#     bcc_email_string = ", ".join(bcc_email_list)

#     # port = 1125  # For SSL
#     context = ssl.create_default_context()
    
#     # Create a multipart message and set headers
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email_string
#     message["Cc"] = cc_email_string
#     message["Bcc"] = bcc_email_string
#     message["Subject"] = subject

#     message.attach(MIMEText(body, "html"))

#     for attachment_file in attachments:

#         with open(attachment_file, 'rb') as attachment:
#             part = MIMEBase("application", "octet-stream")
#             part.set_payload(attachment.read())

#         # Encode file in ASCII characters to send by email    
#         encoders.encode_base64(part)

#         # Add header as key/value pair to attachment part
#         part.add_header(
#             "Content-Disposition",
#             f"attachment; filename= {attachment_file}",
#         )

#         # Add attachment to message and convert message to string
#         message.attach(part)

#     text = message.as_string()

#     with smtplib.SMTP(mailserver, port) as server:
#         server.sendmail(sender_email, receiver_email_list, text)

#     # with smtplib.SMTP(mailserver, port, context=context) as server:
#     #     server.login(sender_email, password)
#     #     server.sendmail(sender_email, receiver_email_list, text) 

# def send_email_from_instructions(target_report, sender_email, attachments=[], mailserver="localhost", port=1025):
#     instructions = lookup_email_instructions(target_report)
    
#     receiver_email_list = instructions["to"]
#     subject = instructions["subject"]
#     body = instructions["body"]
#     cc_email_list = instructions["cc"]
#     bcc_email_list = instructions["bcc"]


#     send_email(sender_email, receiver_email_list, subject, body,
#         cc_email_list=cc_email_list, bcc_email_list=bcc_email_list, attachments=attachments,
#         mailserver=mailserver, port=port)

# def lookup_email_instructions(target_report):
#     try:
#         report_instructions = instructions_json[target_report]
#         subject = report_instructions["subject"]
#         to = report_instructions["to"]
#         cc = report_instructions["cc"]
#         bcc = report_instructions["bcc"]
#         body = ""

#         if type(report_instructions["body"]) == dict:
#             template_file = report_instructions["body"]["template"]
#             with open(template_file, "r") as f:
#                 contents = f.read()
#                 body = contents
#         else:
#             body = report_instructions["body"]
        
#         return {
#             "subject": subject,
#             "body": body,
#             "to": to,
#             "cc": cc,
#             "bcc": bcc
#         }
#     except KeyError:
#         raise KeyError(f"The report '{target_report}' was not found in the instructions file.")


