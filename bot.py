from telethon import TelegramClient, events, sync
import time
import re
import telethon
import os
import pickle
api_id = '24583348'
api_hash = '2e1f41b8438bedde28a66d38758042bb'
# inicializa o cliente
client = telethon.TelegramClient("session_name", api_id, api_hash)

# conecta com o servidor
client.start()

#verifica o save
if os.path.exists("saved_data.pickle"):
    # Load 
    with open("saved_data.pickle", "rb") as f:
        saved_data = pickle.load(f)
    channel_id = saved_data["channel_id"]
    groups = saved_data["groups"]

    # se deseja colocar links dnv
    overwrite = input("Quer recolocar os links?(s/n): ")
    if overwrite.lower() == "s":
        canal = input("Coloque o link do ouvinte: ")
        grupo = []
        numg = int(input("Quantos grupos serão adicionados?: "))
        for i in range(numg):
            grupo.append(input(f"Link {i+1}:"))
        groups = [client.get_entity(link) for link in grupo]
        channel_id = client.get_entity(canal)

        # Save
        saved_data = {"channel_id": channel_id, "groups": groups}
        with open("saved_data.pickle", "wb") as f:
            pickle.dump(saved_data, f)
else:
    # se não existir, criar
    canal = input("Coloque o link do ouvinte: ")
    grupo = []
    numg = int(input("Quantos grupos serão adicionados?: "))
    for i in range(numg):
        grupo.append(input(f"Link {i+1}:"))
    groups = [client.get_entity(link) for link in grupo]# id's
    channel_id = client.get_entity(canal)  # Replace this with the channel ID

    # salva a data
    saved_data = {"channel_id": channel_id, "groups": groups}
    with open("saved_data.pickle", "wb") as f:
        pickle.dump(saved_data, f)
os.system('cls')
os.system('mode con:cols=100 lines=2')
# set id da ultima mensagem
last_message_id = 0
print("Encaminhando...")
# começa o loop
while True:
    # Usa iter_messages() para pegar as mensagens
    for message in client.iter_messages(channel_id):
        # Checa se houve nova mensagem
        if message.id > last_message_id:
            # atualiza mensagem
            last_message_id = message.id
                # enviar mensagem
            message_text = re.sub(r"@\S+\s", "", message.message)
            if message.document is not None:
                    # Send the document
                for group in groups:
                    client.send_message(group, message_text, file=message.document)
            elif message.photo is not None:
                # Send the photo
                for group in groups:
                    client.send_message(group, message_text, file=message.photo)
            elif message.media is not None:
                # Send the video
                for group in groups:
                    client.send_message(group, message_text, file=message.media)
            else:
                for group in groups:
                    client.send_message(group, message_text)
        time.sleep(0.1)