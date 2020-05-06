import subprocess # te ajuta sa executi comenzi de shell sau bash pentru diferite sisteme de operare
import optparse
import re

def get_current_mac(interface):
    # pentru a citi ce afiseaza comanda pe care o dam in linux se foloseste subprocess.check_output()
    # aici este pus fix ce intoarce comanda adica tot carnatul
    # pentru a lua fix bucata ce ne trebuie se foloseste regex
    # se poate folosi pythex sa vezi pattern
    ifconfig_check = subprocess.check_output(["ifconfig", interface])

    mac_return = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_check.decode()) # se cauta dupa check
    if mac_return:
        return mac_return.group(0)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interfata de schimbare a adresei MAC") # specificam prima optiune pe care o folosim
    parser.add_option("-m", "--mac", dest="mac_address", help="Noua adresa mac") # specificam prima optiune pe care o folosim
    (option, arguments) = parser.parse_args()
    if not option.interface:
        parser.error("Specifica te rog o interfata!. Foloseste --help pentru mai multe informatii")
    elif not option.mac_address:
        parser.error("Specifica te rog o adresa de mac valida. Foloseste --help pentru mai multe informatii")
    else:
        return option

def change_mac(interface, mac_address):
    subprocess.call(["ifconfig",  interface, "down"]) #asa se foloseste cel mai bine
    print('Dezactivare Retea...')
    subprocess.call(["ifconfig", interface, "hw" ,"ether", mac_address])
    print('Setare adresa noua...{}'.format(mac_address))
    subprocess.call(["ifconfig", interface, "up"])
    print('Activare retea')


option = get_arguments()
current_mac =  get_current_mac(option.interface)

if current_mac is None:
    print("Adresa de MAC sau interfata nu este valida!")
else:
    print("Adresa actuala de MAC = {}".format(str(current_mac))) 

    change_mac(option.interface, option.mac_address)
    current_mac =  get_current_mac(option.interface)
    if current_mac == option.mac_address:
        print("Adresa a fost schimbata cu succes!")
    else:
        print("Adresa nu a putut fi schimbata!")
