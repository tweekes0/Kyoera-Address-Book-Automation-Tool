import os
import constants

from datetime import date
from xml.dom import minidom
from xml.etree.ElementTree import Comment, Element, ElementTree, tostring

def beautify_xml(xml_string):
    rough_string = tostring(xml_string, 'utf-8')

    return minidom.parseString(rough_string).toprettyxml()

def generate_xml(user_data, filename):
    xml_string = Element('DeviceAddressBook_v5_2')
    xml_string.append(Comment('Main Address Book'))

    address_book = []
    email_otk = []
    smb_otk = []

    for i in range(len(user_data)): 
        display_name = str(user_data[i][1]).title()
        email_address = str(user_data[i][3]).title()
        smb_path = str(user_data[i][4])

        address_book.append(
            Element('Item', Type="Contact", Id=str(i+1), DisplayName= display_name, SendKeisyou="0", DisplayNameKana= display_name,\
                MailAddress=email_address, SendCorpName="", SendPostName="", SmbHostName=constants.SMB_HOSTNAME, SmbPath=smb_path,\
                SmbLoginPasswd=constants.SMB_LOGIN_PASSWD, SmbLoginName=constants.SMB_LOGIN_NAME, SmbPort=constants.SMB_PORT, FtpPath="", FtpHostName="", FtpLoginName="", FtpLoginPasswd="",\
                FtpPort="21", FaxNumber="", FaxSubaddress="", FaxPassword="", FaxCommSpeed="BPS_33600", FaxECM="On", FaxEncryptKeyNumber="0", FaxEncryption="Off",\
                FaxEncryptBoxEnabled="Off", FaxEncryptBoxID="0000", InetFAXAddr="", InetFAXMode="Simple", InetFAXResolution="3", InetFAXFileType="TIFF_MH",\
                IFaxSendModeType="IFAX", InetFAXDataSize="1", InetFAXPaperSize="1", InetFAXResolutionEnum="Default", InetFAXPaperSizeEnum="Default")
        )

        email_otk.append(
            Element('Item', Type="OneTouchKey", Id=str(i+1), DisplayName= display_name, AddressId=str(i+1), AddressType="EMAIL")
        )

        smb_otk.append(
            Element("Item", Type="OneTouchKey", Id=str(i + 1 + len(user_data)), DisplayName= display_name, AddressId=str(i+1), AddressType="SMB")
        )   

    xml_string.extend(address_book)

    xml_string.append(Comment('Email OneTouch Keys'))
    xml_string.extend(email_otk)

    xml_string.append(Comment('SMB OneTouch Keys'))
    xml_string.extend(smb_otk)
    
    if not os.path.exists(constants.ADDRESS_BOOK_DIR): 
        os.mkdir(constants.ADDRESS_BOOK_DIR)

    filename = f"{filename} {date.today()}.xml"
    with open(os.path.join(constants.ADDRESS_BOOK_DIR, filename), 'w') as file:
        file.write(beautify_xml(xml_string))
        file.close()

def banner():
    print("="*40)
    print("Kyocera Address Book Creation Tool")
    print("Enter 'help' for a list of commands")
    print("Enter 'help' 'COMMAND NAME' for more.")
    print("="*40)
    print()
