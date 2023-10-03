import base64

import cryptography
from Cryptodome.PublicKey import DSA
from Cryptodome.Hash import SHA3_256
from Cryptodome.Signature import DSS
from cryptography.fernet import Fernet
from xml.dom import minidom
import os


def validate_file(file_path):
    return True if os.path.isfile(file_path) else False


def validate_folder(folder_path):
    return True if os.path.isdir(folder_path) else False


def validate_credentials(key):
    if key['login'] == '' or key['password'] == '':
        return ""
    if not os.path.isfile(f"../private_keys/{key['login']}_PrivateKey"):
        return ""

    with open(f"../private_keys/{key['login']}_PrivateKey", "rb") as private_key_file:
        encrypted_private_key = private_key_file.read()

    private_key_decrypting_key = SHA3_256.new(key["password"].encode()).digest()
    private_key_decrypter = Fernet(base64.b64encode(private_key_decrypting_key))
    try:
        private_key = private_key_decrypter.decrypt(encrypted_private_key)
        return private_key
    except cryptography.fernet.InvalidToken:
        return ""


def sign_file(credentials, file_path, signed_file_folder_path, private_key):
    file = open(file_path, "rb")
    file_content = file.read()
    file_hash = SHA3_256.new(file_content)
    file.close()

    private_key_object = DSA.import_key(private_key)
    signer = DSS.new(private_key_object, "fips-186-3")
    signature = signer.sign(file_hash)

    signed_file_content = create_signed_file_content(file_content, signature, credentials["login"])
    signed_file_name = os.path.basename(file_path) + ".xml"
    signed_file = open(signed_file_folder_path + "/" + signed_file_name, "w")
    signed_file.write(signed_file_content)
    signed_file.close()

    return True


def create_signed_file_content(file_content, signature, login):
    """
    :param bytes file_content: the content of the file to be signed
    :param bytes signature: the signature of the file to be signed
    :param str login: the login of the signer

    Creates a string with the content of an XML file with the content of the file to be signed, the signature the
    signer's login.

    :return: the signed file content as string with an XML document content
    """
    doc = minidom.Document()

    xml_root_element = doc.createElement('SignedDocument')
    doc.appendChild(xml_root_element)

    xml_file_content_element = doc.createElement('FileContent')
    xml_root_element.appendChild(xml_file_content_element)
    # file_content is encoded to base64 and then decoded to string:
    xml_file_content = doc.createTextNode(base64.b64encode(file_content).decode())
    xml_file_content_element.appendChild(xml_file_content)

    xml_signature_element = doc.createElement('Signature')
    xml_root_element.appendChild(xml_signature_element)
    # signature is encoded to base64 and then decoded to string:
    xml_signature = doc.createTextNode(base64.b64encode(signature).decode())
    xml_signature_element.appendChild(xml_signature)

    xml_login_element = doc.createElement('SignerLogin')
    xml_root_element.appendChild(xml_login_element)
    xml_login = doc.createTextNode(login)
    xml_login_element.appendChild(xml_login)

    return doc.toprettyxml()


def get_identity(file_path):
    xml_content = minidom.parse(file_path)
    file_content = xml_content.getElementsByTagName('FileContent')[0].childNodes[0].data
    signature = xml_content.getElementsByTagName('Signature')[0].childNodes[0].data
    login = xml_content.getElementsByTagName('SignerLogin')[0].childNodes[0].data
    public_key, identity = find_key(login)

    if not public_key:
        return ""

    decoded_content = base64.b64decode(file_content)
    decoded_hash = SHA3_256.new(decoded_content)

    new_key = DSA.importKey(public_key)
    verifier = DSS.new(new_key, "fips-186-3")
    signature = base64.b64decode(signature)
    try:
        verifier.verify(decoded_hash, signature)
        valid = True
    except ValueError:
        valid = False

    if valid:
        return identity
    else:
        return ""


def find_key(login):
    certs_doc = minidom.parse("certificates.xml")
    # todo: zakodować dodanie entera na końcu pliku przy generowaniu, bo inaczej się nie sparsuje
    xml_cert_list = certs_doc.getElementsByTagName("Certificate")

    key = False
    identity = False

    for xml_cert in xml_cert_list:
        xml_login = xml_cert.getElementsByTagName('Login')[0].firstChild.nodeValue

        if login == xml_login:
            key = xml_cert.getElementsByTagName('PublicKey')[0].firstChild.nodeValue
            identity = xml_cert.getElementsByTagName('Identity')[0].firstChild.nodeValue

    return key, identity


def save_decrypted_content(file_path, target_dir):
    xml_content = minidom.parse(file_path)
    file_content = xml_content.getElementsByTagName('FileContent')[0].childNodes[0].data
    file_content = base64.b64decode(file_content)
    name = os.path.basename(file_path)
    name = name[:len(name) - 4]
    f = open(target_dir + "/" + name, "wb")
    f.write(file_content)
    f.close()
