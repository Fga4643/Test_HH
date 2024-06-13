from django.http import JsonResponse
import requests

def rates_pars(request):
    val1 = request.GET.get("from")
    val2 = request.GET.get("to")
    cou = request.GET.get("count")
    #Запрос к сайту центробанка
    r= requests.get('https://www.cbr.ru/currency_base/daily/')
    #Начало парсинга, вырезаю таблицу с котировками
    pars=str(r.text).split('<div class="table-wrapper">')[1].split('<div class="request_bottom btns">')[0]
    #Делю по строкам
    pars=pars.split('<tr>')[2:]
    base={}
    for i in pars:
        test=i.split('<td>')[2:]
        base[test[0].split('</td>')[0]]=[float(test[3].split('</td>')[0].replace(",",".")),int(test[1].split('</td>')[0])]
    if val1!="RUB":
        target=base[val1]
    else:
        target=[1,1]
    summa=(target[0]/target[1])*int(cou)
    if val2!="RUB":
        recip=base[val2]
    else:
        recip=[1,1]
    
    prima=recip[0]/recip[1]
    return JsonResponse({'result': summa/prima})

def rates(request):
    val1 = request.GET.get("from")
    val2 = request.GET.get("to")
    cou = request.GET.get("count")
    #Запрос к API цетробанка
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    #Чтение json
    data = response.json()
    if val1!="RUB":
        target=[data['Valute'][val1]['Value'],data['Valute'][val1]['Nominal']]
    else:
        target=[1,1]
    summa=(target[0]/target[1])*int(cou)
    if val2!="RUB":
        recip=[data['Valute'][val2]['Value'],data['Valute'][val2]['Nominal']]
    else:
        recip=[1,1]
    
    prima=recip[0]/recip[1]
    return JsonResponse({'result': summa/prima})