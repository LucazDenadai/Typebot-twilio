import requests
from app.models.user_session import UserSession
from config import Config

class TypebotService:
    @staticmethod
    def get_or_create_session(sender, typebot_id):
        """
        Obtém ou cria uma sessionId para o usuário no Typebot.
        """
        if sender in UserSession.user_sessions:
            return UserSession.user_sessions[sender], None  # Retorna sessionId já existente

        # Criar nova sessão no Typebot
        session_url = f"{Config.TYPEBOT_BASE_URL}/typebots/{typebot_id}/startChat"
        response = requests.post(session_url, json={"visitorId": sender})
        
        if response.status_code == 200 and "sessionId" in response.json():
            session_id = response.json()["sessionId"]
            UserSession.user_sessions[sender] = session_id  # Salva sessionId para futuras mensagens

            # Enviar mensagem inicial para iniciar o fluxo
            initial_message_payload = {
                "message": {
                    "text": "ola",
                    "type": "text"
                }
            }
            message_url = f"{Config.TYPEBOT_BASE_URL}/sessions/{session_id}/continueChat"
            initial_response = requests.post(message_url, json=initial_message_payload)

            return session_id, initial_response.json()
        else:
            print("❌ Erro ao criar sessionId:", response.text)
            return None, None

    @staticmethod
    def extract_text_from_response(response_json):
        messages = response_json.get("messages", [])
        extracted_texts = []

        for message in messages:
            if message.get("type") == "text" and "content" in message:
                rich_text = message["content"].get("richText", [])
                for item in rich_text:
                    if item.get("type") == "p":
                        for child in item.get("children", []):
                            if "text" in child:
                                extracted_texts.append(child["text"])
                            elif child.get("type") == "inline-variable":
                                for inline_child in child.get("children", []):
                                    if "text" in inline_child:
                                        extracted_texts.append(inline_child["text"])

        return " ".join(extracted_texts)

    @staticmethod
    def process_message(data):
        # Verifica se a chave 'From' está presente nos dados
        if 'From' not in data:
            raise KeyError("Missing 'From' in request data")
        
        sender = data['From']
        typebot_id = Config.TYPEBOT_ID
        session_id, initial_response = TypebotService.get_or_create_session(sender, typebot_id)
        
        if not session_id:
            return {"error": "Erro ao conectar com o chatbot."}

        # Enviar mensagem de boas-vindas para o Typebot se for uma nova sessão
        if initial_response:
            return TypebotService.extract_text_from_response(initial_response)

        # Enviar mensagem para o Typebot
        message_url = f"{Config.TYPEBOT_BASE_URL}/sessions/{session_id}/continueChat"
        message_payload = {
            "message": {
                "text": data['message'],
                "type": "text"
            }
        }

        response = requests.post(message_url, json=message_payload)

        # Processar resposta do Typebot
        if response.status_code == 200:
            return TypebotService.extract_text_from_response(response.json())
        else:
            return "Desculpe, ocorreu um erro ao processar sua mensagem."