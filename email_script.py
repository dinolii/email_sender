import smtplib
import getpass
from email.mime.text import MIMEText
# There are default settings
# Please do not change them
SMTP_SSL_HOST = 'smtp.gmail.com'  # smtp.mail.yahoo.com
SMTP_SSL_PORT= 465


def prompt():
    username = input("Type the your email and press enter:\n")
    password = getpass.getpass("Type the password of the email and press enter:\n")
    subject = input("Enter the subject of the email:\n")
    src_file = input("Enter the name of the csv file:\n")
    template = input("Enter the name of the template file:\n")
    return username, password, subject, src_file, template


def extract_info(src, options):
    name_to_info = {}
    option_to_index = {}
    with open(src) as csv_reader:
        first_line = csv_reader.readline()
        first_line = first_line.rstrip()
        components = first_line.split(",")
        for option in options:
            if option not in option_to_index:
                option_to_index[option] = components.index(option)
        keys = list(option_to_index.keys())
        index = [option_to_index[key] for key in keys]
        name_index = keys.index("Name")
        name_ele = index[name_index]
        keys.remove("Name")
        index.remove(name_ele)
        keys = ["Name"] + keys
        for line in csv_reader:
            line = line.strip()
            info = line.split(",")
            full_name = info[option_to_index[keys[0]]]
            if full_name not in name_to_info:
                name_to_info[full_name] = []
                for i in range(1, len(keys)):
                    temp = info[option_to_index[keys[i]]]
                    name_to_info[full_name].append({keys[i]: temp})
    return option_to_index, name_to_info


def generate_template(src):
    with open(src) as file_handle:
        lines = file_handle.readlines()
        template = "".join(lines)
        return template


def replace_template(template, name, info):
    email = ""
    template = template.replace("Name", name)
    for dict in info:
        for key in dict:
            if key == "Email":
                email = dict[key]
            else:
                template = template.replace(key, dict[key])
    return template, email


def send_email(server, sender, receiver, subject, msg):
    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    target = [receiver]
    server.sendmail(sender, target, msg.as_string())


def extract_option(src):
    with open(src) as file_handle:
        return file_handle.readline().strip().split(",")


if __name__ == "__main__":
    username, password, subject, src_file, template_file = prompt()
    template = generate_template(template_file)
    options = extract_option(src_file)
    option_to_index, user_info = extract_info(src_file, options)
    sender = username
    server = smtplib.SMTP_SSL(SMTP_SSL_HOST, SMTP_SSL_PORT)
    server.login(username, password)
    for user in user_info:
        new_template, receiver = replace_template(template, user, user_info[user])
        send_email(server, sender, receiver, subject, new_template)
    server.quit()
