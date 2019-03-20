import requests

request = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
usd_rub_coefficient = request.json()['rates']['RUB']
usd_thb_coefficient = request.json()['rates']['THB']
thb_rub_coefficient = usd_rub_coefficient/usd_thb_coefficient

def count_for(amount, currency):
    if currency == 'thb':
        rubles = round(amount * thb_rub_coefficient, 2)
        usd = round(amount / usd_thb_coefficient, 2)
        message = """
        {0} бат (THB) это примерно:
        - {1} в рублях (RUB)
        - {2} в долларах США (USD)
        """.format(amount, rubles, usd)
        
    elif currency == 'rub':
        thb = round(amount / thb_rub_coefficient, 2)
        usd = round(amount / usd_rub_coefficient, 2)
        message = """
        {0} рублей (RUB) это примерно:
        - {1} в тайских батах (THB)
        - {2} в долларах США (USD)
        """.format(amount, thb, usd)
        
    elif currency == 'usd':
        rubles = round(amount * usd_rub_coefficient, 2)
        thb = round(amount * usd_thb_coefficient, 2)
        message = """
        {0} долларов США (USD) это примерно:
        - {1} в рублях (RUB)
        - {2} в тайских батах (THB)
        """.format(amount, rubles, thb)

    return message
    

# print('How much?')
# x = input().split()



def check(msg):
    msg = msg.split()
    try:
        amount = float(msg[0])
        if len(msg) == 1:
            result = count_for(amount, 'thb')
            
        elif len(msg) == 2:    
            # amount = float(msg[0])
            currency = msg[1].lower()
            
            if currency in ['rub', 'руб'] or currency[0] in ['r', 'р']:
                result = count_for(amount, 'rub')
            elif currency in ['thb', 'бат'] or currency[0] in ['t', 'т', 'b', 'б']:
                result = count_for(amount, 'thb')
            elif currency in ['usd', 'dollar'] or currency[0] in ['u', 'd', 'д']:
                result = count_for(amount, 'usd') 
        return result        
    except:
        if msg == 'start' or msg == '/start':
            message = '''Привет. Я конвертирую рубли в баты и наоборот.
            Можешь прислать мне как просто цифру - я посчитаю что это баты - так и с указанием валюты - баты, рубли или доллары (ну а вдруг)
            Все эти запросы сработают:
            - 120
            - 10 рублей
            - 500 THB
            - 100 USD
            Для перевода используется средний биржевой курс на текущий момент. Прежде чем совершать какие-либо транзакции, на которых могут отразиться изменения в курсах, необходимо проверить приведённые данные. Курсы предлагаются исключительно в информационных целях и могут быть изменены в любой момент. Этот бот не предлагает совершать каких-либо транзакций с использованием предоставляемых курсов. '''
            return message
        
    