from django.shortcuts import render
import datetime

# Create your views here.
THREATS = [
    {'id': 1, 'name': 'Запуск вредоносного ПО', 'short_description': 'Мониторинг запуска вредоносного ПО', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'Наши специалисты детектируют запуск вредоносного программного обеспечения в режиме 24/7, что позволяет защитить рабочие станции пользователей','count':9,'price':10000},
    {'id': 2, 'name': 'Сетевая активность', 'short_description': 'Мониторинг сетевой активности', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'Наши специалисты имеют большой опыт в детектировании атак, основываясь на анализе сетевого трафика','count':16,'price':10000},
    {'id': 3, 'name': 'Эксплуатация уязвимостей', 'short_description': 'Мониторинг эксплуатации уязвимостей на рабочик станциях', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg', 'description':'подробное описание атаки. многобукв. 123456787654548900','count':9,'price':10000},
    {'id': 4, 'name': 'Фишинговые атаки', 'short_description': 'Мониторинг проведения фишинговых атак', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'Наши системы обнаружения фишинга помогут эффективно обнаружить и предотвратить фишинговую атаку','count':12,'price':10000},
    {'id': 5, 'name': 'Атаки DoS/DDoS', 'short_description': 'Мониторинг и противодействие DoS/DDoS атакам', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'подробное описание атаки. многобукв. 123456787654548900','count':73,'price':10000},
    {'id': 6, 'name': 'Эксплуатация уязвимостей web-приложений', 'short_description': 'Мониторинг эксплуатации уязвимостей web-приложений', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'подробное описание атаки. многобукв. 123456787654548900', 'count':1,'price':10000},
]

# TODO
REQUESTS = [{'threat_id':4}]



def get_name_by_id(threats, search_id):
    for threat in threats:
        if threat['id'] == search_id:
            return threat['name']
    return None

def threats_list(request):
    threats = []
    if 'threat_name' in request.GET:
        for threat in THREATS:
            if request.GET['threat_name'].lower() in threat["name"].lower():
                threats.append(threat)
        return render(request, 'index.html', {'threats': threats, 'input_value':request.GET['threat_name'], 'current_count':1})
    return render(request, 'index.html', {'threats': THREATS, 'current_count':1})

def threat_description(request, id):
    for threat in THREATS:
        if threat["id"] == id:
            data = threat
    return render(request, 'description.html', {'threat': data})

def threat_request(request):

    threat_ids = [request['threat_id'] for request in REQUESTS]
    filtered_threats = [threat for threat in THREATS if threat['id'] in threat_ids]
    for threat in filtered_threats:
        threat["status"] = "Draft"
    return render(request, 'request.html', {'current_threats':filtered_threats})