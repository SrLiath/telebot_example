import os
import pickle
import re
import time
import telethon
import PySimpleGUI as sg

api_id = '24583348'
api_hash = '2e1f41b8438bedde28a66d38758042bb'

# inicializa o cliente
client = telethon.TelegramClient("session_name", api_id, api_hash)

# cria a janela
sg.theme("DarkBlue")
layout = [
    [sg.Text("Link do canal de origem:"), sg.Input(key="-CANAL-")],
    [sg.Text("Links dos grupos de destino:")],
    [sg.Multiline(key="-GRUPOS-", size=(50, 5))],
    [sg.Button("Salvar"), sg.Button("Iniciar"), sg.Button("Sair")]
]
window = sg.Window("Encaminhador de Mensagens", layout)

# loop principal da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        break
    elif event == "Salvar":
        # Salva as informações na pickle
        canal = values["-CANAL-"]
        grupos = values["-GRUPOS-"].strip().split("\n")
        grupos = [await client.get_entity(link.strip()) for link in grupos]
        channel_id = await client.get_entity(canal)

        saved_data = {"channel_id": channel_id, "groups": grupos}
        with open("saved_data.pickle", "wb") as f:
            pickle.dump(saved_data, f)
        sg.popup("Informações salvas com sucesso!")
    elif event == "Iniciar":
        # Verifica se as informações já foram salvas antes
        if os.path.exists("saved_data.pickle"):
            with open("saved_data.pickle", "rb") as f:
                saved_data = pickle.load(f)
            channel_id = saved_data["channel_id"]
            grupos = saved_data["groups"]
        else:
            sg.popup("As informações de canal e grupos ainda não foram salvas. Por favor, salve-as primeiro.")
            continue
        
        # Começa o loop de encaminhamento
        last_message_id = 0
        while True:
            for message in client.iter_messages(channel_id):
                if message.id > last_message_id:
                    last_message_id = message.id
                    message_text = re.sub(r"@\S+\s", "", message.message)
                    if message.document is not None:
                        for grupo in grupos:
                            client.send_message(grupo, message_text, file=message.document)
                    elif message.photo is not None:
                        for grupo in grupos:
                            client.send_message(grupo, message_text, file=message.photo)
                    elif message.media is not None:
                        for grupo in grupos:
                            client.send_message(grupo, message_text, file=message.media)
                    else:
                        for grupo in grupos:
                            client.send_message(grupo, message_text)
                    time.sleep(0.1)

# fecha a janela
window.close()
