import base64
from cryptography.fernet import Fernet
from Cryptodome.PublicKey import DSA
from Cryptodome.Hash import SHA3_256
from xml.dom import minidom
from pathlib import Path



def initialize_certificates_database():
    #Added
    [f.unlink() for f in Path("../private_keys").glob("*") if f.is_file()]

    certs_doc = minidom.Document()
    certs_root = certs_doc.createElement("Certificates")
    certs_doc.appendChild(certs_root)

    with open("../bin/certificates.xml", "w") as file:
        file.write(certs_doc.toxml())


def add_certificate(certs_doc, login, identity, public_key):
    xml_certs = certs_doc.getElementsByTagName("Certificates")[0]

    xml_new_cert = certs_doc.createElement("Certificate")
    xml_certs.appendChild(xml_new_cert)

    xml_login = certs_doc.createElement("Login")
    xml_new_cert.appendChild(xml_login)
    xml_login_text = certs_doc.createTextNode(login)
    xml_login.appendChild(xml_login_text)

    xml_identity = certs_doc.createElement("Identity")
    xml_new_cert.appendChild(xml_identity)
    xml_identity_text = certs_doc.createTextNode(identity)
    xml_identity.appendChild(xml_identity_text)

    xml_public_key = certs_doc.createElement("PublicKey")
    xml_new_cert.appendChild(xml_public_key)
    xml_public_key_text = certs_doc.createTextNode(public_key.decode())
    xml_public_key.appendChild(xml_public_key_text)


def create_user(certs_doc, login, identity, password):
    keys = DSA.generate(bits=2048)
    add_certificate(certs_doc, login, identity, keys.public_key().exportKey())

    # user's private key is encoded (using symmetric cryptography) and stored on the disk
    private_key_encrypting_key = SHA3_256.new(password.encode()).digest()
    private_key_encrypter = Fernet(base64.b64encode(private_key_encrypting_key))
    encrypted_private_key = private_key_encrypter.encrypt(keys.exportKey())

    with open(f"../private_keys/{login}_PrivateKey", "wb") as private_key_file:
        private_key_file.write(encrypted_private_key)


def create_users(login, identity, password):

    certs_doc = minidom.parse("../bin/certificates.xml")
    create_user(certs_doc, login, identity, password)

    with open("../bin/certificates.xml", "w") as certs_file:
        certs_file.write(certs_doc.toprettyxml())

initialize_certificates_database()
create_users("user1", "first user", "passw00rd")
create_users("user2", "second user", "password")

while True:
    print("Enter login:")
    login = input()
    print("Enter identity:")
    identity = input()
    print("Enter password:")
    password = input()
    create_users(login, identity, password)
    print("Added successfully \n\n")
