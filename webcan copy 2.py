import requests
import cv2
from roboflow import Roboflow

# Carrega o modelo da API do Roboflow
rf = Roboflow(api_key="H4uvuCVjiUboOLYWORyl")
project = rf.workspace("ufsc-o5foa").project("tcc-visual")
dataset = project.version(2).download("tensorflow")
model = project.version(2).model

# Inicializa a câmera
cap = cv2.VideoCapture(0)

while True:
    # Captura o frame da câmera
    ret, frame = cap.read()

    # Salva o frame como uma imagem temporária
    cv2.imwrite("temp_frame.jpg", frame)

    # Inferência no frame capturado
    result = model.predict("temp_frame.jpg", confidence=40, overlap=30).json()
    print(result)
    
    up_memory(result['predictions'])
    
    # Supondo que 'result' contém as coordenadas do objeto detectado
    for obj in result['predictions']:
        x, y, w, h = int(obj['x']), int(obj['y']), int(obj['width']), int(obj['height'])
        cv2.rectangle(frame, (x, y), (w, h), (0, 0, 0), 2)

    # Mostra o frame na janela
    cv2.imshow('Camera Frame', frame)

    # Pressione 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()

def up_memory(prediction):
    # URL do endpoint onde você deseja fazer o POST
    url = 'http://localhost:8000/seu_endpoint/'

    # Dados que você deseja enviar no corpo do POST (substitua pelos seus dados)
    data = {
        "_class": prediction['class'],
        "_x": prediction['x'],
        "_y": prediction['y']
    }

    # Realiza o pedido POST
    response = requests.post(url, data=data)

    # Verifica a resposta do servidor
    if response.status_code == 200:
        print("Pedido POST bem-sucedido!")
        print("Resposta do servidor:")
        print(response.text)
    else:
        print("Erro ao fazer o pedido POST. Código de status:", response.status_code)
