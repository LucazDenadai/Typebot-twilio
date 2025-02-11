from flask import Blueprint, request, jsonify,Response
from app.services.typebot_service import TypebotService
import xmltodict
import logging
import xml.etree.ElementTree as ET

typebot_bp = Blueprint('typebot', __name__)

@typebot_bp.route('/whatsapp', methods=['POST'])
def webhook():
    if request.content_type == 'application/xml':
        data = xmltodict.parse(request.data)
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        data = request.json
    
    # Adiciona log para depuração
    logging.info(f"Received data: {data}")
    print(data)
    
    # Mapeia a propriedade 'From' para 'sender'
    if 'From' in data:
        data['sender'] = data['From']
    
    # Verifica se a chave 'sender' está presente nos dados
    if 'sender' not in data or data["sender"] == "":
        return jsonify({"error": "Missing 'sender' in request data"}), 400
    
    # Adiciona a mensagem ao dicionário de dados
    data['message'] = data.get('Body', '')

    response = TypebotService.process_message(data)
    print(response)
    
    # Constrói a resposta XML
    root = ET.Element("Response")
    message = ET.SubElement(root, "Message")
    message.text = response

    xml_response = ET.tostring(root, encoding='utf-8', method='xml').decode()

    return Response(xml_response, mimetype='application/xml')

@typebot_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is running"})