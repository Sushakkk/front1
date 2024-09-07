from django.shortcuts import render
import datetime

# Create your views here.
THREATS = [
    {'id': 1, 'name': 'Запуск вредоносного ПО', 'short_description': 'Описание атаки 1', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'подробное описание атаки. многобукв. 123456787654548900'},
    {'id': 2, 'name': 'Подозрительная сетевая активность', 'short_description': 'Описание атаки 2', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'подробное описание атаки. многобукв. 123456787654548900'},
    {'id': 3, 'name': 'Исполнение скриптов PowerShell', 'short_description': 'Описание атаки 3', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'подробное описание атаки. многобукв. 123456787654548900'},
    {'id': 4, 'name': 'Эксплуатация известных уязвимостей', 'short_description': 'Описание атаки 4', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'подробное описание атаки. многобукв. 123456787654548900'},
    {'id': 5, 'name': 'Фишинговые атаки', 'short_description': 'Описание атаки 5', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'подробное описание атаки. многобукв. 123456787654548900'},
    {'id': 6, 'name': 'Атаки DoS/DDoS', 'short_description': 'Описание атаки 6', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'подробное описание атаки. многобукв. 123456787654548900'},
    {'id': 7, 'name': 'Эксплуатация уязвимостей web-приложений', 'short_description': 'Описание атаки 7', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'подробное описание атаки. многобукв. 123456787654548900'},
]

# TODO
REQUESTS = []



def get_name_by_id(threats, search_id):
    for threat in threats:
        if threat['id'] == search_id:
            return threat['name']
    return None

def threats_list(request):
    total_requests = 2 # TODO
    
    threats = []
    if 'threat_name' in request.GET:
        for threat in THREATS:
            if request.GET['threat_name'].lower() in threat["name"].lower():
                threats.append(threat)
        return render(request, 'index.html', {'threats': threats, 'input_value':request.GET['threat_name'], 'total_requests':total_requests})
    return render(request, 'index.html', {'threats': THREATS, 'total_requests':total_requests})

def threat_description(request, id):
    for threat in THREATS:
        if threat["id"] == id:
            data = threat
    return render(request, 'description.html', {'threat': data})

def threat_request(request):
    current_threats = []
    return render(request, 'request.html', {'current_threats':current_threats})