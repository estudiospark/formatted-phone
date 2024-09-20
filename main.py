from flask import Flask, request, Response
import re

app = Flask(__name__)


# Função para formatar o número de telefone
def format_phone_number(international_format):
    phone_pattern = r"(\+55)\s(\d{2})\s(\d{5})-(\d{4})"
    match = re.match(phone_pattern, international_format)

    if not match:
        return None

    country_code, ddd, first_part, second_part = match.groups()

    if int(ddd) > 27 and first_part.startswith('9'):
        first_part = first_part[1:]  # Remove o dígito '9'

    formatted_phone_number = f"{country_code} {ddd} {first_part}-{second_part}"

    return formatted_phone_number


# Rota para formatar o número de telefone
@app.route('/format_phone', methods=['POST'])
def format_phone():
    content = request.json  # Recebe dados JSON
    international_format = content.get('phone')  # Extrai o número de telefone

    if international_format:
        result = format_phone_number(international_format)
        if result:
            return Response(
                result, mimetype='text/plain'
            )  # Retorna apenas o número formatado como texto puro
        return Response("Invalid phone number format", status=400)

    return Response("No phone number provided", status=400)


# Inicia o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
