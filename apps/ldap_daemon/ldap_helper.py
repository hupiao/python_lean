import ldap3
import email

msg = None
with open('./test.eml', 'rb') as fp:
    msg_c = fp.read()
    msg = email.message_from_bytes(msg_c)
print(msg)
print(email.header.decode_header(msg.get('Subject'))[0][0].decode('utf8'))
print(email.header.decode_header(msg["From"])[0][0].decode('utf8'))
print(email.header.decode_header(msg["To"]))
