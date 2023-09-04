# AÇÔES DISPONÍVEIS #
# Cada função/método corresponde a uma ação (por momento apenas simulada)
import datetime
import requests
import json
import requests
import cv2
from roboflow import Roboflow

class Action:    
    def get_element(self, ctx):
        # Carrega o modelo da API do Roboflow
        rf = Roboflow(api_key="H4uvuCVjiUboOLYWORyl")
        project = rf.workspace().project("tcc-visual-yinmq")
        model = project.version(1).model

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
            
            self.up_memory(result)
            
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
        
    def up_memory(self, prediction):
        url = ''
        data = {}
        # URL do endpoint onde você deseja fazer o POST
        for result in prediction['predictions']:
            if result['class'] == 'obstaculo':
                url = 'http://localhost:8000/obstacle/'

                # Dados que você deseja enviar no corpo do POST (substitua pelos seus dados)
                data = {
                    "_class": result['class'],
                    "_x": result['x'],
                    "_y": result['y']
                }
            elif result['class'] == 'robo':
                url = 'http://localhost:8000/robot/'

                # Dados que você deseja enviar no corpo do POST (substitua pelos seus dados)
                data = {
                    "_class": result['class'],
                    "_x": result['x'],
                    "_y": result['y']
                }
            elif result['class'] == 'objetivo':
                url = 'http://localhost:8000/goal/'

                # Dados que você deseja enviar no corpo do POST (substitua pelos seus dados)
                data = {
                    "_class": result['class'],
                    "_x": result['x'],
                    "_y": result['y']
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
