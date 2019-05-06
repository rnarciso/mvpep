import os
import requests
import pyautogui
import time
import base64
import sys
import subprocess
import webbrowser

class Rsrc:
    logon_buttom = 'entrar.png'
    unit_select_buttom = 'seleciona_empresa.png'
    lateral_tab = 'UTI_NOVO_aba_lateral.png'
    soul_icon = 'soul.png'
    internment = 'internacao.png'
    password_field = 'senha.png'
    username_field = 'usuario.png'
    target_form_tab = 'plano_terapeutico.png'
    date_inter_field = 'data_admissao.png'
    ok = 'ok.png'
    unit = 'morumbi.png'
    copy = 'copiar.png'
    new = 'novo.png'
    calendar = 'calendario.png'
    isolated = 'isolamento.png'
    lateral_rolling_bar = 'rolamento_lateral.png'
    prophylaxies = 'profilaxias.png'
    therapeutic = 'investimento.png'
    predict_LOS = 'tempo_previsto_internacao.png'
    condition = 'gravidade.png'
    save = 'salvar.png'
    sign = 'assinar.png'
    list_of_patients = 'lista.png'
    no_certificate = 'sem_certificado.png'
    delete = 'apagar.png'
    beds = {}
    resources_path = './resources'


    def __init__(self, resource_path=os.path.join(os.sep.join(os.path.abspath(os.getcwd()).split(os.sep)), 'resources')):
        if resource_path is not None:
            self.resources_path = resource_path
        self.update_resources()

    def update_resources(self):
        for resource_name in [a for a in dir(self) if a[0] != '_']:
            if resource_name == 'beds':
                setattr(self, 'beds', dict(((bed, os.path.join(self.resources_path, "{0}_leito_{1}.png".format('UTI', bed))) for bed in range(1, 21))))
            else:
                try:
                    setattr(self, resource_name,
                    os.path.join(self.resources_path, getattr(self, resource_name, '{0}.png'.format(resource_name))))
                except Exception as e:
                    pass


class settings:
    username = '106927'
    #password = 'uMrM3uToyp6cn6Sj'
    password = 'kKmopKunmGZkfGp0'
    beds = {'UTI': range(1, 20 + 1)}


pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
rsrc = Rsrc("C:\\Users\\lfutia\\Documents\\UTI LeForte\\app\\MVPEP\\resources")


def GetUUID():
    try:
        cmd = 'wmic csproduct get uuid'
        uuid = str(subprocess.check_output(cmd))
        pos1 = uuid.find("\\n")+2
        uuid = uuid[pos1:-15]
    except Exception:
        uuid = "non-windows enviroment:"
    return uuid

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=')

def decode(key, string):
    if type(string) is str:
        string = bytes(string.encode('utf-8'))
    string = base64.urlsafe_b64decode(string + b'===')
    string = string.decode('latin')
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def wait_and_click(image, timeout=30, tick=1, offset:tuple=(0, 0), confidence_interval=[0.95, 0.5]):
    confidence = max(confidence_interval)
    steps = timeout / tick
    while pyautogui.locateOnScreen(image, confidence=confidence) is None and timeout > 0:
        time.sleep(tick)
        timeout -= tick
        confidence = max(confidence_interval) - (max(confidence_interval)-min(confidence_interval))*(((steps*tick)-timeout)/(steps*tick))
        #print(confidence)
    if timeout > 0:
        x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence=confidence))
        x += offset[0]
        y += offset[1]
        pyautogui.click((x, y))
        return True
    else:
        return False

'''
def wait_and_click(image, timeout=30, tick=5, offset:tuple=(0, 0), start_confidence=0.75):
    confidence = start_confidence 
    while pyautogui.locateOnScreen(image, confidence=confidence) is None and timeout > 0:
        time.sleep(tick)
        timeout -= tick
        confidence = start_confidence * 0.8
    if timeout > 0:
        x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence=confidence))
        x += offset[0]
        y += offset[1]
        pyautogui.click((x, y))
        return True
    else:
        return False
'''

def login(username: str, password: str):
	headers = {
		    'Origin': 'http://soul',
		    'Upgrade-Insecure-Requests': '1',
		    'Content-Type': 'application/x-www-form-urlencoded',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
		    'X-DevTools-Emulate-Network-Conditions-Client-Id': '6B27F4F0E34F76C08DB3DA3BD44E53C0',
		    'Referer': 'http://soul/mvautenticador-cas/login?service=http%3A%2F%2Fsoulmv-gw-pep%3A80%2Fmvpep%2F2%2Findex_appletless.html',
		}

	params = (
		    ('service', 'http://soulmv-gw-pep:80/mvpep/2/index_appletless.html'),
		)

	data = {
		  'username': username,
		  'not-an-username': '',
		  'password': password,
		  'company': '7',
		  'type': 'AUTHENTICATION_SGU',
		  'timezone': 'GMT-0300',
		  'lt': 'LT-361896-LVlEeoufzdbFToJ3fbDSnvQRVYVe6v-cas.example.org',
		  'execution': 'e2s1',
		  '_eventId': 'submit',
		  'submit': 'LOGIN'
		}

	response = requests.post('http://soul/mvautenticador-cas/login', headers=headers, params=params, data=data)
	

def login():
    try:
        pyautogui.doubleClick(pyautogui.center(pyautogui.locateOnScreen(rsrc.soul_icon, confidence=.75)))
    except Exception as e:
        webbrowser.open_new('http://soul/mvautenticador-cas/login')

    wait_and_click(rsrc.username_field)
    time.sleep(1/2)
    pyautogui.typewrite(settings.username)
    time.sleep(1/2)
    pyautogui.typewrite(['tab'])
    time.sleep(1/2)
    pyautogui.typewrite(decode(GetUUID(), settings.password))
    time.sleep(1/2)
    wait_and_click(rsrc.unit_select_buttom)
    time.sleep(1/2)
    wait_and_click(rsrc.unit)
    #pyautogui.typewrite(['down', 'enter'])
    time.sleep(1/2)
    wait_and_click(rsrc.logon_buttom)
    time.sleep(3)

def new_plans(bedRange=[1, 20]): 
    while not wait_and_click(rsrc.internment, timeout=1):
        login()    
    for bed in range(bedRange[0], bedRange[-1] + 1) if type(bedRange) is not int and len(bedRange) == 2 else bedRange:
        wait_and_click(rsrc.beds[bed])
        wait_and_click(rsrc.lateral_tab)
        wait_and_click(rsrc.target_form_tab)
        if not wait_and_click(rsrc.copy, timeout=10):
            wait_and_click(rsrc.new)
            wait_and_click(rsrc.calendar)
            pyautogui.typewrite(['left', 'enter'])
            wait_and_click(rsrc.isolated)
            wait_and_click(rsrc.lateral_rolling_bar, offset=(16, 287))
            wait_and_click(rsrc.prophylaxies, offset=(108,10))  # TEV
            wait_and_click(rsrc.prophylaxies, offset=(200, 10)) # TGI
            wait_and_click(rsrc.lateral_rolling_bar, offset=(16, 507))
            wait_and_click(rsrc.therapeutic, offset=(664, 10)) # Pleno
            wait_and_click(rsrc.predict_LOS, offset=(310, 11))  # <3 dias
            #wait_and_click(rsrc.predict_LOS, offset=(400, 11))  # 3-7 dias
            #wait_and_click(rsrc.predict_LOS, offset=(559, 11))  # <7 dias
            wait_and_click(rsrc.condition, offset=(227, 17))  # <observation
        else:
            wait_and_click(rsrc.ok)
        #wait_and_click(rsrc.sign)
        wait_and_click(rsrc.list_of_patients)
        wait_and_click(rsrc.no_certificate)


def delete_plans(bedRange=[1, 20]):   
    while not wait_and_click(rsrc.internment, timeout=1):
        login()    
    for bed in range(bedRange[0], bedRange[-1] + 1) if type(bedRange) is not int and len(bedRange) == 2 else bedRange:
        wait_and_click(rsrc.beds[bed])
        wait_and_click(rsrc.lateral_tab)
        wait_and_click(rsrc.target_form_tab)
        wait_and_click(rsrc.delete)
        #wait_and_click(rsrc.sign)
        wait_and_click(rsrc.list_of_patients)
        wait_and_click(rsrc.no_certificate, timeout=1)

if __name__ == "__main__":
    main()


print(2)
