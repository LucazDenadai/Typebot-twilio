import requests
from config import Config

class UserSession:
    user_sessions = {}

    @staticmethod
    def get_or_create_session(sender, typebot_id):
        if sender in UserSession.user_sessions:
            return UserSession.user_sessions[sender]
        
        session_id = UserSession.create_new_session(sender, typebot_id)
        UserSession.user_sessions[sender] = session_id
        return session_id
    
    @staticmethod
    def create_new_session(sender, typebot_id):
        # Lógica para criar uma nova sessão
        session_url = f"{Config.TYPEBOT_BASE_URL}/typebots/{typebot_id}/startChat"
        response = requests.post(session_url, json={"visitorId": sender})
        
        if response.status_code == 200 and "sessionId" in response.json():
            return response.json()["sessionId"]
        return None