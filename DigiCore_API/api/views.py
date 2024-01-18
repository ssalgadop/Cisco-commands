from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.views import View
from .models import settingsLog
from .models import Device
import json
import re
import telnetlib
import time

# Create your views here.
class viewHandler(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        settings = list(settingsLog.objects.values())
        if len(settings)>0:
            datos = {'message':"Success",'settings':settings}
        else:
            datos = {'message':"Not Found"}
        return JsonResponse(datos)
    def post(self,request):
        #print(request.body)
        jd=json.loads(request.body)
        pattern = r"Denegar\s+el\s+acceso\s+de\s+(PC1|A|PC2|B|PC3|C|PC4|D)\s+a\s+internet" # Dependiendo de la cantidad de hosts que se tengan se debe agregar o quitar elementos en el (PC1|A|PC2|B).
        pattern2 = r"Crear\s+vlan\s+(\w+)\s+en\s+el\s+piso\s+(uno|dos)"
        ipt = jd['input']
        res = re.search(pattern,ipt)
        res2 = re.search(pattern2,ipt)
        # Dirección IP y puerto telnet del dispositivo en GNS3
        HOST = "192.168.234.130"  # dirección IP de tu dispositivo en GNS3
        user123 = "baki"
        password123 = "12345"
        if res: # Se encontro el patron
            # TELNET AL HOST x.x.x.x
            tn123 = telnetlib.Telnet(HOST, timeout=10)
            # TELNET CREDENCIALES
            tn123.read_until(b"Username:", timeout=1)
            tn123.write(user123.encode("ascii") + b"\n")
            tn123.read_until(b"Password:", timeout=5)
            tn123.write(password123.encode("ascii") + b"\n")
            if ("PC1" in ipt) or ("A" in ipt): #Nodo A o PC1 estan en el piso 1.
                # Se verifica si existe alguna lista de acceso.
                Devices = list(Device.objects.values())
                pc = [device for device in Devices if device['name'] == 'PC1']
                digirouters = [device for device in Devices if device['name'] == 'DigiRouter']
                flag = False
                for router in digirouters:
                    if(router['firewall'] == 101):
                        flag = True
                        if(pc[0]['firewall'] == 101): # Ya estaba creada la regla
                            datos = {'message':"Success"}
                            return JsonResponse(datos)
                if (flag):
                    commands = [
                        b"configure terminal\n",
                        b"no access-list 101 permit ip any any\n",
                        b"access-list 101 deny ip host 192.168.1.3 host 192.168.234.130\n",
                        b"access-list 101 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 101 permit ip any any\n",
                        b"interface FastEthernet0/0\n",  # Interfaz hacia la LAN1
                        b"ip access-group 101 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    otp = "$configure terminal $ access-list 101 deny ip host 192.168.1.3 host 192.168.234.130 $ access-list 101 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $access-list 101 permit ip any any $interface FastEthernet0/0 $ip access-group 101 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
                else:
                    commands = [
                        b"configure terminal\n",
                        b"access-list 101 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 101 permit ip any any\n",
                        b"interface FastEthernet0/0\n",  # Interfaz hacia la LAN1
                        b"ip access-group 101 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    digirouters = [device for device in Devices if device['ip_address'] == '192.168.1.1']
                    d =Device.objects.get(id=digirouters[0]['id'])
                    d.firewall = 101
                    d.save()
                    d=Device.objects.get(ip_address=pc[0]['ip_address'])
                    d.firewall = 101
                    d.save()
                    otp = "$configure terminal $ access-list 101 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $ access-list 101 permit ip any any $ interface FastEthernet0/0 $ ip access-group 101 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
            elif("PC2" in ipt) or ("B" in ipt): #Nodo B o PC2
                # Se verifica si existe alguna lista de acceso.
                Devices = list(Device.objects.values())
                pc = [device for device in Devices if device['name'] == 'PC2']
                digirouters = [device for device in Devices if device['name'] == 'DigiRouter']
                flag = False
                for router in digirouters:
                    if(router['firewall'] == 101):
                        flag = True
                        if(pc[0]['firewall'] == 101): # Ya estaba creada la regla
                            datos = {'message':"Success"}
                            return JsonResponse(datos)
                if (flag):
                    commands = [
                        b"configure terminal\n",
                        b"no access-list 101 permit ip any any\n",
                        b"access-list 101 deny ip host 192.168.1.2 host 192.168.234.130\n",
                        b"access-list 101 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 101 permit ip any any\n",
                        b"interface FastEthernet0/0\n",  # Interfaz hacia la LAN1
                        b"ip access-group 101 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    otp = "$ configure terminal $ access-list 101 deny ip host 192.168.1.2 host 192.168.234.130 $ access-list 101 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $access-list 101 permit ip any any $interface FastEthernet0/0 $ip access-group 101 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
                else:
                    print(pc[0]['ip_address'])
                    commands = [
                        b"configure terminal\n",
                        b"access-list 101 deny ip host " +pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 101 permit ip any any\n",
                        b"interface FastEthernet0/0\n",  # Interfaz hacia la LAN1
                        b"ip access-group 101 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    digirouters = [device for device in Devices if device['ip_address'] == '192.168.1.1']
                    d =Device.objects.get(id=digirouters[0]['id'])
                    d.firewall = 101
                    d.save()
                    d=Device.objects.get(ip_address=pc[0]['ip_address'])
                    d.firewall = 101
                    d.save()
                    otp = "$configure terminal $ access-list 101 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $ access-list 101 permit ip any any $ interface FastEthernet0/0 $ ip access-group 101 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
            elif("PC3" in ipt) or ("C" in ipt): #Nodo C o PC3
                # Se verifica si existe alguna lista de acceso.
                Devices = list(Device.objects.values())
                pc = [device for device in Devices if device['name'] == 'PC3']
                digirouters = [device for device in Devices if device['name'] == 'DigiRouter']
                flag = False
                for router in digirouters:
                    if(router['firewall'] == 102):
                        flag = True
                        if(pc[0]['firewall'] == 102): # Ya estaba creada la regla
                            datos = {'message':"Success"}
                            return JsonResponse(datos)
                if (flag):
                    commands = [
                        b"configure terminal\n",
                        b"no access-list 102 permit ip any any\n",
                        b"access-list 102 deny ip host 192.168.2.3 host 192.168.234.130\n",
                        b"access-list 102 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 102 permit ip any any\n",
                        b"interface FastEthernet0/1\n",  # Interfaz hacia la LAN1
                        b"ip access-group 102 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    otp = "$ configure terminal $ access-list 102 deny ip host 192.168.2.3 host 192.168.234.130 $ access-list 102 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $access-list 102 permit ip any any $interface FastEthernet0/1 $ip access-group 102 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
                else:
                    commands = [
                        b"configure terminal\n",
                        b"access-list 102 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 102 permit ip any any\n",
                        b"interface FastEthernet0/1\n",  # Interfaz hacia la LAN1
                        b"ip access-group 102 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    digirouters = [device for device in Devices if device['ip_address'] == '192.168.2.1']
                    d =Device.objects.get(id=digirouters[0]['id'])
                    d.firewall = 102
                    d.save()
                    d=Device.objects.get(ip_address=pc[0]['ip_address'])
                    d.firewall = 102
                    d.save()
                    otp = "$configure terminal $ access-list 102 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $ access-list 102 permit ip any any $ interface FastEthernet0/1 $ ip access-group 102 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
            else: #Nodo D o PC4
                # Se verifica si existe alguna lista de acceso.
                print("aca")
                Devices = list(Device.objects.values())
                pc = [device for device in Devices if device['name'] == 'PC4']
                digirouters = [device for device in Devices if device['name'] == 'DigiRouter']
                flag = False
                for router in digirouters:
                    if(router['firewall'] == 102):
                        flag = True
                        if(pc[0]['firewall'] == 102): # Ya estaba creada la regla
                            datos = {'message':"Success"}
                            return JsonResponse(datos)
                if (flag):
                    commands = [
                        b"configure terminal\n",
                        b"no access-list 102 permit ip any any\n",
                        b"access-list 102 deny ip host 192.168.2.2 host 192.168.234.130\n",
                        b"access-list 102 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 102 permit ip any any\n",
                        b"interface FastEthernet0/1\n",  # Interfaz hacia la LAN1
                        b"ip access-group 102 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    otp = "$ configure terminal $ access-list 102 deny ip host 192.168.2.2 host 192.168.234.130 $ access-list 102 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $access-list 102 permit ip any any $interface FastEthernet0/1 $ip access-group 102 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
                else:
                    commands = [
                        b"configure terminal\n",
                        b"access-list 102 deny ip host "+ pc[0]['ip_address'].encode('utf-8') + b" host 192.168.234.130\n",
                        b"access-list 102 permit ip any any\n",
                        b"interface FastEthernet0/1\n",  # Interfaz hacia la LAN1
                        b"ip access-group 102 in\n",
                        b"exit\n"
                    ]
                    # Ejecutar comandos de configuración
                    for command in commands:
                        tn123.write(command)
                        time.sleep(1)  # Espera breve entre comandos
                    tn123.write(b"exit\n")
                    tn123.close()
                    digirouters = [device for device in Devices if device['ip_address'] == '192.168.2.1']
                    d =Device.objects.get(id=digirouters[0]['id'])
                    d.firewall = 102
                    d.save()
                    d=Device.objects.get(ip_address=pc[0]['ip_address'])
                    d.firewall = 102
                    d.save()
                    otp = "$configure terminal $ access-list 102 deny ip host "+str(pc[0]['ip_address'])+" host 192.168.234.130 $ access-list 102 permit ip any any $ interface FastEthernet0/1 $ ip access-group 102 in $ exit"
                    settingsLog.objects.create(input=jd['input'],output=otp)
                    datos = {'message':"Success"}
                    return JsonResponse(datos)
        elif res2: # Comandos de vlan
            # TELNET AL HOST x.x.x.x
            tn123 = telnetlib.Telnet(HOST, timeout=10)
            # TELNET CREDENCIALES
            tn123.read_until(b"Username:", timeout=1)
            tn123.write(user123.encode("ascii") + b"\n")
            tn123.read_until(b"Password:", timeout=5)
            tn123.write(password123.encode("ascii") + b"\n")
            Devices = list(Device.objects.values())
            vlan = [device for device in Devices if device['vlan'] == int(res2.group(1))]
            print(vlan)
            if vlan: # Existe el nombre
                print("entro")
                datos = {'message':"Error"}
                return JsonResponse(datos)
            elif("uno" in ipt): # Piso 1
                print(res2.group(1).encode('utf-8'))
                commands = [
                    b"configure terminal\n",
                    b"interface FastEthernet0/0.10\n",
                    b"encapsulation dot1Q 10\n",
                    b"ip address 192.168.3.1 255.255.255.0\n",
                    b"description VLAN "+res2.group(1).encode('utf-8')+b"\n",
                    b"exit\n",
                    b"exit\n",
                ]
                # Ejecutar comandos de configuración
                for command in commands:
                    tn123.write(command)
                    time.sleep(1)  # Espera breve entre comando
                tn123.write(b"exit\n")
                tn123.close()
                d=Device.objects.get(interface='FastEthernet0/0')
                d.vlan = res2.group(1)
                d.save()
                otp = "$configure terminal $interface FastEthernet0/0.10 $ encapsulation dot1Q 10 $ ip address 192.168.3.1 255.255.255.0 $ description VLAN "+res2.group(1)+" $ exit $ exit"
                settingsLog.objects.create(input=jd['input'],output=otp)
                datos = {'message':"Success"}
                return JsonResponse(datos)
            else: # Piso 2
                commands = [
                    b"configure terminal\n",
                    b"interface FastEthernet0/1.20\n",
                    b"encapsulation dot1Q 20\n",
                    b"ip address 192.168.4.1 255.255.255.0\n",
                    b"description VLAN "+res2.group(1).encode('utf-8')+b"\n",
                    b"exit\n",
                    b"exit\n",
                ]
                # Ejecutar comandos de configuración
                for command in commands:
                    tn123.write(command)
                    time.sleep(1)  # Espera breve entre comando
                tn123.write(b"exit\n")
                tn123.close()
                d=Device.objects.get(interface='FastEthernet0/1')
                d.vlan = res2.group(1)
                d.save()
                otp = "$configure terminal $interface FastEthernet0/0.20 $ encapsulation dot1Q 20 $ ip address 192.168.4.1 255.255.255.0 $ description VLAN "+res2.group(1)+" $ exit $ exit"
                settingsLog.objects.create(input=jd['input'],output=otp)
                datos = {'message':"Success"}
                return JsonResponse(datos)
        else: # Caso contrario error de sintaxis
            datos = {'message':'Command not found'}
            return JsonResponse(datos)
    def put(self,request): # No lo vamos a usar en teoria
        pass
    def delete(self,request): # No lo vamos a usar en teoria
        pass
