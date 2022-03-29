#!/usr/bin/python3
from distutils.log import error
from glob import glob
from pickle import FALSE
from posixpath import split
from simple_term_menu import TerminalMenu
from tabulate import tabulate
import os
import re
import json
"""
Falta possibilidade de chaves alem de .pem
"""
global STOP
global USER
USER = None
STOP = False

    

def ASCIIPEPPER():
    return "\
                                            ........................................ \n\
                                            .............   7?^ .:^~^  ............. \n\
                                            ............  ^7J5PYY55557  ............ \n\
                                            ...........  !PP555P55555P!  ........... \n\
                                            ...........  JP55555555555Y. ........... \n\
                                            ............ .?555555555555. ........... \n\
                                            .............  !5YJY555YYJY:. .......... \n\
                                            ............. :!^~J:75?.?J.:^ .......... \n\
                                            ............. :!:!J^~5J^7?~~^  ......... \n\
                                            .............. .J5Y55555555J  .......... \n\
                                            .............. :555555P5555! ........... \n\
                                            .............  ?5555555555Y. ........... \n\
                                            ...........  .!55555555555^ ............ \n\
                                            .........   ^J5555555555Y^ ............. \n\
                                            .......  .^?YYJYYY5555Y7. .............. \n\
                                            ...... .~?YJJJJJJY55J!:  ............... \n\
                                            ..... :JYYJJYYYYJ?!:   ................. \n\
                                            ..... :777777!~^.    ................... \n\
                                            ........................................"


def ASCII():
    return "              _____ ______ _______      ________ _____    __  __          _   _          _____ ______ _____  \n\
             / ____|  ____|  __ \ \    / /  ____|  __ \  |  \/  |   /\   | \ | |   /\   / ____|  ____|  __ \ \n\
            | (___ | |__  | |__) \ \  / /| |__  | |__) | | \  / |  /  \  |  \| |  /  \ | |  __| |__  | |__) |\n\
             \___ \|  __| |  _  / \ \/ / |  __| |  _  /  | |\/| | / /\ \ | . ` | / /\ \| | |_ |  __| |  _  / \n\
             ____) | |____| | \ \  \  /  | |____| | \ \  | |  | |/ ____ \| |\  |/ ____ \ |__| | |____| | \ \ \n\
            |_____/|______|_|  \_\  \/   |______|_|  \_\ |_|  |_/_/    \_\_| \_/_/    \_\_____|______|_|  \_\n\
                                                                                            BY:Doctorspeppers\n\
                                                                                                            "


def getSshKey(key_name):
    keys = glob.glob(os.getcwd()+"/keys/*")
    if len(keys) > 1:
        for key in keys:
            if key_name == key.split(".")[0]:
                return os.getcwd()+"/keys/"+key

def system(command):
    try:
        os.system(command)
    except OSError:
        print("Algo deu errado com a instancia "+instance['id'])

def sendFile(local_path=None,ssh_path=None,instance=None,all_machines=False,reverse=False):
    if type(instance) == dict and type(all_machines) == list:
        return
    elif instance == None and all_machines==False:
        return
    elif type(instance) == dict and all_machines==False:
        connection = instance["ssh_user"]+"@"+instance["public_ip"]
        command = "scp -i "+getSshKey(instance["ssh_key"])+" "
        if reverse == False:
            if local_path == None and ssh_path == None:
                local_path = input("Digite o caminho absoluto do arquivo/pasta a ser copiado:")
                ssh_path = input("Digite o caminho absoluto da pasta a ser salvo os arquivos:")
            command = command + local_path + " " +connection+":"+ssh_path
            system(command)
        elif reverse == True:
            if local_path == None and ssh_path == None:
                local_path = input("Digite o caminho absoluto do arquivo/pasta a ser salvo do servidor:")
                ssh_path = input("Digite o caminho absoluto da pasta a ser copiado os arquivos:")
            command = command +connection+":"+ssh_path + " "  + local_path 


    elif all_machines==True and instance == None:
        instances = listAllMachines()
        if reverse == False:
            local_path = input("Digite o caminho absoluto do arquivo a ser copiado:")
            ssh_path = input("Digite o caminho absoluto a ser salvo em todos os servidores:")
            for instace in instances:
                sendFile(local_path=local_path,ssh_path=ssh_path,instance=instace)
        elif reverse == True:
            print("AVISO, SERA CRIADO SUB-PASTAS PARA SEPARAR CADA ARQUIVO DE CADA SERVIDOR")
            ssh_path = input("Digite o caminho absoluto do arquivo a ser copiado de servidores:")
            local_path = input("Digite o caminho absoluto da pasta a ser salvo os arquivos:")
            for instace in instances:
                local_path_for_instance = local_path + "/" + instance['id'] + "/"
                system("mkdir "+ local_path)
                sendFile(local_path=local_path_for_instance,ssh_path=ssh_path,instance=instace,reverse=True)


def shellOneMachine(instance = None,entry_index=False,index=False,command=False,script=None):
    if instance == None:
        listAllMachines()
    elif instance != None and entry_index == False:
        if entry_index == False:
        
            options = ["[1] Abrir novo terminal",
                "[2] Usar este terminal",
                "[3] Executar script", 
                "[q] Exit"]

            terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_black","bold","bg_green"),shortcut_key_highlight_style=("fg_gray",),title="Server manager \n"+ASCIIPEPPER()+"\n\n"+ASCII())
            menu_entry_index = terminal_menu.show()
            if menu_entry_index == 0:
                command = "gnome-terminal -- ssh -i " + getSshKey(instance['ssh_key']) +" "+instance["ssh_user"]+"@"+instance["public_ip"]
                system(command)
            elif menu_entry_index == 1:
                print("digite 'q' para sair")
                while command != "q":
                    prefix = "ssh -i " + getSshKey(instance['ssh_key']) +" "+instance["ssh_user"]+"@"+instance["public_ip"]
                    command = input(instance["ssh_user"]+"@"+instance["public_ip"]+"~:$")
                    system(prefix+" '"+command+"'")
            elif menu_entry_index == 2:
                script = input("Digite o caminho absoluto do script a ser executado:")
                prefix = "ssh -i " + getSshKey(instance['ssh_key']) +" "+instance["ssh_user"]+"@"+instance["public_ip"]
                system(prefix+"bash -s < "+script)

        elif instance != None and entry_index != None and index != False:
            if index == 0:
                command = "gnome-terminal -- ssh -i " + getSshKey(instance['ssh_key']) +" "+instance["ssh_user"]+"@"+instance["public_ip"]
                system(command)
            elif index == 1 and command != None:
                if 'name_tag' in instance:
                    print(instance['name_tag']+" "+instance["ssh_user"]+"@"+instance["public_ip"])
                else:
                    print(instance["ssh_user"]+"@"+instance["public_ip"])
                prefix = "ssh -i " + getSshKey(instance['ssh_key']) +" "+instance["ssh_user"]+"@"+instance["public_ip"]
                system(prefix+" '"+command+"'")
            elif index == 2 and script != None:
                prefix = "ssh -i " + getSshKey(instance['ssh_key']) +" "+instance["ssh_user"]+"@"+instance["public_ip"]
                system(prefix+"bash -s < "+script)

def shellAllMachines():
    instances = listAllMachines(terminal=False)
    options = ["[1] Abrir novo terminal",
        "[2] Usar este terminal",
        "[3] Executar script", 
        "[q] Exit"]

    terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_black","bold","bg_green"),shortcut_key_highlight_style=("fg_gray",),title="Server manager \n"+ASCIIPEPPER()+"\n\n"+ASCII())
    menu_entry_index = terminal_menu.show()
    for instance in instances:
        if menu_entry_index == 0:
            shellOneMachine(instance = instance,entry_index=True,index=0)
        elif menu_entry_index == 1:
            print("digite 'q' para sair")
            while command != "q":
                command = input("all instances ~:$")
                shellOneMachine(instance = instance,entry_index=True,index=1,command=command)
        elif menu_entry_index == 2:
            script = input("Digite o caminho absoluto do script a ser executado:")
            shellOneMachine(instance = instance,entry_index=True,index=2,command=False,script=script)

def updateListMachines():
    if USER == None:
        chooseAwsProfile()
    all_regions_result = []
    all_regions = {
        "us":["us-east-2","us-east-1","us-west-1","us-west-2"],
        "af":["af-south-1"],
        "ap":["ap-east-1","ap-southeast-3","ap-south-1","ap-northeast-3","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-northeast-1"],
        "ca":["ca-central-1"],
        "eu":["eu-central-1","eu-west-1","eu-west-2","eu-south-1","eu-west-3","eu-north-1"],
        "me":["me-south-1"],
        "sa":["sa-east-1","us-gov-east-1","us-gov-west-1"],
    }
    for region in all_regions[CONTINENT]:
        instances = 0
        req = os.popen("aws ec2 describe-instances --profile "+USER+" --region "+region).read()
        result = json.loads(req)
        if len(result['Reservations']) != 0:
            for x in range(0,len(result['Reservations'])):
                all_regions_result += result['Reservations'][x]["Instances"]
                instances += len(result['Reservations'][x]["Instances"])
            print(str(instances)+" instances in "+region+" regions")
        else:
            print("0 instances in "+region+" regions")

    with open("instances.json","w") as fp:
        json.dump(all_regions_result,fp,indent=4)

def machineOptions(instance):
    options = ["[1] Abrir shell", 
            "[2] Enviar arquivo", 
            "[3] Receber arquivo"
            "[q] Exit",
            "[X] Adicionar tag (Em desenvolvimento)", 
            "[X] Opções avançadas de estado da instancia (Em desenvolvimento)",
            "[X] Opções avançadas de volume (Em desenvolvimento)",
            "[X] Opções avançadas de rede (Em desenvolvimento)", 
            "[X] Opções avançadas de imagem (Em desenvolvimento)"] 
    functions = [shellOneMachine,
                sendFile,
                sendFile,
                exit]
    terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_black","bold","bg_green"),shortcut_key_highlight_style=("fg_gray",),title="Server manager \n"+ASCIIPEPPER()+"\n\n"+ASCII())
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 3:
        functions[menu_entry_index](instance,reverse=True)
    else:
        functions[menu_entry_index](instance)

def listAllMachines(terminal=True):
    if (os.path.isfile("instances.json") == False):
        updateListMachines()
    with open("instances.json") as fp:
        instances = json.load(fp)
    instances_info = []
    for instance in instances:
        instance_reduced = {}
        for tag in instance["Tags"]:
            if tag["Key"] == "user":
                instance_reduced["ssh_user"] = tag["Value"]
            elif tag['Key'] == "Name":
                instance_reduced["name_tag"] = tag['Value']
        instance_reduced['id'] = instance['InstanceId']
        instance_reduced['public_ip'] = instance['PublicIpAddress']
        instance_reduced["plataform"] = instance["PlatformDetails"]
        instance_reduced["state"] = instance["State"]['Name']
        instance_reduced['ssh_key'] = instance['KeyName']
        instances_info.append(instance_reduced)
    if terminal == True:
        header = instances_info[0].keys()
        rows =  [x.values() for x in instances_info]

        print(tabulate(rows, header, tablefmt='fancy_grid',showindex=True))
        value = input("Choose a machine by index or quit(q):")
        if value == "q":
            return
        else:
            machineOptions(instances_info[int(value)])
    else:
        return instances_info



def chooseContinent():
    global CONTINENT
    options = ["[1] US",
            "[2] Africa",
            "[3] Asia Pacific",
            "[4] Canada",
            "[5] Europe",
            "[6] Middle East",
            "[7] South America",
            "[8] AWS GovCloud",
            "[q] Exit"]
    prefix = ["us",
                "af",
                "ap",
                "ca",
                "eu",
                "me",
                "sa",
                "Gov",
                exit]
    terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_black","bold","bg_green"),shortcut_key_highlight_style=("fg_gray",),title="Server manager \n"+ASCIIPEPPER()+"\n\n"+ASCII())
    menu_entry_index = terminal_menu.show()
    CONTINENT = prefix[menu_entry_index]



def chooseAwsProfile():
    global USER
    users_options = []
    users_list = []
    with open(os.path.expanduser('~')+"/.aws/credentials","r") as credentials:
        credentials_text = str(''.join(credentials.readlines()))
        users = re.findall("\[.+\]", credentials_text)
        for x,user in zip(range(0,len(users)),users):
            users_options.append("["+str(x)+"]" + str(''.join(user[1:-1])))
            users_list.append(str(''.join(user[1:-1])))
    terminal_menu = TerminalMenu(users_options,menu_highlight_style=("fg_black","bold","bg_green"),shortcut_key_highlight_style=("fg_gray",),title="Server manager \n"+ASCIIPEPPER()+"\n\n"+ASCII())
    menu_entry_index = terminal_menu.show()
    USER = users_list[menu_entry_index]
    chooseContinent()

def exit():
    global STOP
    STOP = True


def main():
    while STOP != True:

        options = ["[1] Comando para uma maquina especifica", #shellOneMachine
                    "[2] Comando para todas as maquinas", #shellAllMachines
                    "[3] Atualizar lista de maquinas", #updateListMachines
                    "[4] Listar todas as maquinas", #listAllMachines
                    "[5] Escolha perfil AWS", #chooseAwsProfile
                    "[q] Exit",
                    "[X] Opções avançadas de instancias (Em desenvolvimento)"] #exit
        functions = [shellOneMachine,
                    shellAllMachines,
                    updateListMachines,
                    listAllMachines,
                    chooseAwsProfile,
                    exit]
        terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_black","bold","bg_green"),shortcut_key_highlight_style=("fg_gray",),title="Server manager \n"+ASCIIPEPPER()+"\n\n"+ASCII())
        menu_entry_index = terminal_menu.show()
        functions[menu_entry_index]()
        

if __name__ == "__main__":
    main()