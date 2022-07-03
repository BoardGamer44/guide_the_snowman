from flask import Flask, render_template, redirect, url_for, session
from forms import ArrowForm, GameCreationForm, CustomGameForm
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)

# app.secret_key = 'session_secret_key'

@app.route('/game_<variable>', methods=['GET', 'POST'])
def game(variable): # функция представления игрового поля
    message = session['message'] # в браузерной сессии храняться некоторые переменные
    fieldlist = session.get('fieldlist', None)
    form = ArrowForm()

    if form.validate_on_submit() and 'win in' not in message:
        direction = form.direction.data
        session['fieldlist'] = move_snowman(session['fieldlist'], direction) # вызов функции перемещения снеговика
        message = session['message']
        fieldlist = session.get('fieldlist', None)
        return render_template('game.html',
                               form=form,
                               fieldlist=fieldlist,
                               message=message)
    elif form.validate_on_submit() and 'win in' in message: # после победы отправка формы вызывает редирект на выбор игры
        return redirect(url_for('gamestart'))
    return render_template('game.html',
                           form=form,
                           fieldlist=fieldlist,
                           message=message)


@app.route('/customgame', methods=['GET', 'POST'])
def customgamestart():  # тут генерируеться игровое поле с заданными параметрами
    form = CustomGameForm()
    if form.validate_on_submit():
        name = form.name.data
        size = form.size.data
        rate = form.rate.data # вероятность в процентах с которой очередная клетка будет проходимой
        terrain = form.terrain.data # выбор картинки вместо камней
        fieldlist_origin9 = [['snow' if random.randint(1, 100) < rate else terrain for x in range(size)]
                             for x in range(size)]
        fieldlist_origin9[1][1], fieldlist_origin9[size - 2][size - 2] = 'snowman', 'finish' # старт и финишь фиксированны
        session['fieldlist'] = fieldlist_origin9 # тут храниться поле
        session['count'] = 0 # тут храниться счетчик сделанных движений
        session['name'] = name # тут храниться имя игрока
        session['message'] = f'The custom game of {name} is start. Guide the snowman to the end.' # сообщение над полем
        return redirect(url_for('game', variable=f'custom_level_{size}x{size}')) # динамическая ссылка
    return render_template('customgame.html',
                           form=form)


@app.route('/', methods=['GET', 'POST'])
def gamestart(): # тут выбираеться фиксированное игровое поле и имя игрока
    form = GameCreationForm()
    if form.validate_on_submit():
        name = form.name.data
        level = form.level.data
        fieldlist_origin3 = [
            ['s', '0', 'f'],
            ['1', '0', '1'],
            ['1', '1', '1']
        ]
        fieldlist_origin5 = [
            ['1', '1', '1', '1', 'f'],
            ['0', '1', '0', '0', '0'],
            ['0', '1', '1', '1', '1'],
            ['0', '0', '0', '1', '0'],
            ['s', '1', '1', '1', '1'],
        ]
        fieldlist_origin7 = [
            ['0', '1', '1', '1', '0', '0', '0'],
            ['1', '1', '0', '1', '0', 'f', '1'],
            ['1', '0', '0', '1', '1', '0', '1'],
            ['1', '1', '0', '0', 's', '0', '1'],
            ['0', '1', '0', '0', '0', '1', '1'],
            ['0', '1', '0', '1', '1', '1', '0'],
            ['0', '1', '1', '1', '0', '0', '0'],
        ]

        if level == 3:
            fieldlist = fieldlist_origin3
        elif level == 5:
            fieldlist = fieldlist_origin5
        elif level == 7:
            fieldlist = fieldlist_origin7
            
        # заполнение поля картинками, код заменяеться на имя файла, который поздее будет превращен в url
        filldict = {'1': 'snow', '0': 'rock', 's': 'snowman', 'f': 'finish'}
        for i, string in enumerate(fieldlist):
            for j, cell in enumerate(string):
                fieldlist[i][j] = filldict[cell]

        session['fieldlist'] = fieldlist
        session['count'] = 0
        session['name'] = name
        session['message'] = f'The game of {name} is start. Guide the snowman to the end.'

        return redirect(url_for('game', variable=f'level_{level}x{level}'))

    return render_template('index.html',
                           form=form)


def move_snowman(fieldlist, direction):
    for i, string in enumerate(fieldlist): # тут определяеться текущее положение снеговика
        for j, cell in enumerate(string):
            if cell == 'snowman':
                hor = i
                ver = j
# далее исходя из выбранного направления проверяться следующая клетка
# если это снег, то две клетки меняются местами(на тот случай если проходимая местность поменяться со снега на траву например)
# в сообщении выводиться число совершенных перемещений
# если это конец, то предыдущая клетка становиться снегом, а вместо финиша появляеться снеговик в очках
# если это препятствие или край поля - выводиться предупреждение
    if direction == '3' and ver + 1 < len(fieldlist) and fieldlist[hor][ver + 1] in ['snow', 'finish']:
        if fieldlist[hor][ver + 1] == 'finish':
            fieldlist[hor][ver], fieldlist[hor][ver + 1] = 'snow', 'winner'
            session['message'] = f'{session["name"]} win in {session["count"] + 1} turns'
        else:
            fieldlist[hor][ver], fieldlist[hor][ver + 1] = fieldlist[hor][ver + 1], fieldlist[hor][ver]
            session['count'] += 1
            session['message'] = f'{session["name"]} made {session["count"]} moves'

    elif direction == '0' and ver - 1 < len(fieldlist) and fieldlist[hor][ver - 1] in ['snow', 'finish']:
        if fieldlist[hor][ver - 1] == 'finish':
            fieldlist[hor][ver], fieldlist[hor][ver - 1] = 'snow', 'winner'
            session['message'] = f'{session["name"]} win in {session["count"] + 1} turns'
        else:
            fieldlist[hor][ver], fieldlist[hor][ver - 1] = fieldlist[hor][ver - 1], fieldlist[hor][ver]
            session['count'] += 1
            session['message'] = f'{session["name"]} made {session["count"]} moves'

    elif direction == '1' and hor - 1 < len(fieldlist) and fieldlist[hor - 1][ver] in ['snow', 'finish']:
        if fieldlist[hor - 1][ver] == 'finish':
            fieldlist[hor][ver], fieldlist[hor - 1][ver] = 'snow', 'winner'
            session['message'] = f'{session["name"]} win in {session["count"] + 1} turns'
        else:
            fieldlist[hor][ver], fieldlist[hor - 1][ver] = fieldlist[hor - 1][ver], fieldlist[hor][ver]
            session['count'] += 1
            session['message'] = f'{session["name"]} made {session["count"]} moves'

    elif direction == '2' and hor + 1 < len(fieldlist) and fieldlist[hor + 1][ver] in ['snow', 'finish']:
        if fieldlist[hor + 1][ver] == 'finish':
            fieldlist[hor][ver], fieldlist[hor + 1][ver] = 'snow', 'winner'
            session['message'] = f'{session["name"]} win in {session["count"] + 1} turns'
        else:
            fieldlist[hor][ver], fieldlist[hor + 1][ver] = fieldlist[hor + 1][ver], fieldlist[hor][ver]
            session['count'] += 1
            session['message'] = f'{session["name"]} made {session["count"]} moves'
    else:
        session['message'] = 'Nope. Snowman can only move on snow!'

    return fieldlist # отредактированное поле возвращаеться на отрисовку


if __name__ == "__main__":
    app.run()

# app.run(debug=True)
