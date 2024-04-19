from flask import Flask, request, jsonify
import uuid
import qrcode
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)


def generate_unique_url():

    """Генерация уникального URL-адреса для сертификата."""

    unique_id = uuid.uuid4()
    return f"https://example.com/certificate/{unique_id}"


def create_qr_code(url, filename):

    """Создание QR-кода с указанным URL-адресом и сохранение его в файле."""

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


def generate_certificate_with_qr(template_name):

    """Создание сертификата с QR-кодом на основе указанного шаблона."""

    # Определяем размеры и другие параметры шаблона
    if template_name == "template1":
        width, height = 800, 600  # Примерные размеры шаблона 1
        title_text = "Certificate Template 1"
        # Здесь могут быть другие параметры для шаблона 1
    elif template_name == "template2":
        width, height = 600, 400  # Примерные размеры шаблона 2
        title_text = "Certificate Template 2"
        # Здесь могут быть другие параметры для шаблона 2
    else:
        raise ValueError("Неподдерживаемый шаблон")

    # Создаем пустое изображение сертификата
    certificate_img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(certificate_img)

    # Добавляем текст заголовка
    title_font = ImageFont.truetype("arial.ttf", 24)
    draw.text((10, 10), title_text, font=title_font, fill='black')

    # Генерируем уникальный URL
    url = generate_unique_url()

    # Создаем уникальное имя файла для QR-кода
    qr_code_filename = f"qr_code_{uuid.uuid4()}.png"

    # Создаем QR-код с сгенерированным URL
    create_qr_code(url, qr_code_filename)

    # Определяем расположение QR-кода на сертификате
    x_offset, y_offset = 50, 50  # Примерные координаты для размещения QR-кода
    qr_code_img = Image.open(qr_code_filename)

    # Вставляем QR-код на сертификат с указанными смещениями
    certificate_img.paste(qr_code_img, (x_offset, y_offset))

    # Сохраняем измененное изображение сертификата с QR-кодом
    certificate_with_qr_filename = f"certificate_with_qr_{template_name}.png"
    certificate_img.save(certificate_with_qr_filename)

    # Возвращаем имя файла с сертификатом и QR-кодом
    return certificate_with_qr_filename


@app.route('/generate_certificate', methods=['GET'])
def generate_certificate():

    """Генерация сертификата с QR-кодом на основе указанного шаблона."""

    template_name = request.args.get('template_name')
    if not template_name:
        return jsonify({'error': 'Не указано имя шаблона'}), 400

    try:
        certificate_filename = generate_certificate_with_qr(template_name)
        return jsonify({'certificate_filename': certificate_filename})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/')
def index():

    """Главная страница сервиса."""

    return 'Добро пожаловать в сервис генерации сертификатов с QR-кодом!'


if __name__ == '__main__':
    app.run(debug=True)
