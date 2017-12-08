from flask import Flask, request, render_template
import json

json_list = []#список всех введеных голосовавшими данных
words_dict = {1: {}, 2: {}, 3 :{}, 4: {}, 5: {}, 6: {}, 7: {}} #список синонимов (1,2,3 .. - номер заданного в форме сллова по порядку)
ages = []#список возрастов
male_fem = []# пол
spheres = [] #сфер деятельности
work_student = [] #подсчет работающих и учащихся одновременно

words_dict_ = {'солидный': 1 ,'тотальный' :2 ,  'истошный': 3,  'безукоризненный': 4,\
               'безотлагательный':5 , 'вопиющий' : 6,'исчерпывающий': 7} #расшифровка списка синонимов

f = open('res.txt', 'w')#создаем чистый файл для запси введенных данных 
f.close()

#--------------------------------------------------------------------------------------------------------------------
def write_to(dict_): #записывает в файл и в список, введенные пользователем данные
    f = open('res.txt' , 'a') #дозапись в файл
    js = json.dumps(dict_)
    json_list.append(js)
    f.write(js + '\n')
    f.close()

def count_words(dict_, key_): #подсчет сколько кажджый из уникальных синонимов  был вписан
    try:
        dict_[key_] = dict_[key_] + 1
    except: 
        dict_[key_] =  1
    return dict_

def words_uniq(words_dict,word1, word2, word3, word4, word5, word6, word7): #списки уникальных значений синонимов, для каждого слова
    words_dict[1] = count_words(words_dict[1], word1)
    words_dict[2] = count_words(words_dict[2], word2)
    words_dict[3] = count_words(words_dict[3], word3)
    words_dict[4] = count_words(words_dict[4], word4)
    words_dict[5] = count_words(words_dict[5], word5)
    words_dict[6] = count_words(words_dict[6], word6)
    words_dict[7] = count_words(words_dict[7], word7)
    return words_dict

def ages_min_max(age):#минимальный и максимальных возраст участников опроса и колвичество участников всего
    ages.append(int(age))
    return str(min(ages)), str(max(ages)), str(len(ages))

def male_fem_count(sex):#процентное соотношение мужчин и женщин, прошедших опрос
    male_fem.append(sex)
    male = [i for i in male_fem if i == 'male']
    female = [i for i in male_fem if i == 'female']
    n = len(male_fem)
    return str(round(len(male)*100/n)), str(round(len(female)*100/n))

def sphere_count(sph):#процентное соотношение работников/учащихся в сферах деятельности (мат. произв, итнеллектуальная, услуги) 
    spheres.append(sph)
    matpr = [i for i in spheres if i == 'matpr']
    inte = [i for i in spheres if i == 'int']
    ser = [i for i in spheres if i == 'ser']
    n = len(spheres)
    return str(round(len(matpr)*100/n)), str(round(len(inte)*100/n)), str(round(len(ser)*100/n))

def wrk_stdnt_count(all_):#процентное соотношение работников/учащихся в сферах деятельности (мат. произв, итнеллектуальная, услуги) 
    try: #узнаем есть ли флажок на вариантах работа и учеба
        a = all_['job_w'] 
        b = all_['job_s'] 
        work_student.append(0)#к списку добавится элемент 0, если отмечены оба варианта
    except:
        pass #если нет одного из флагов, список не пополняется 
    return str(round(len(work_student)*100/len(ages))) #на выход идет длина списка work_student
#-----------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)

from flask import url_for

@app.route('/')
def index(): 
    return render_template('index1.html')

@app.route('/stats')#после отправки ответов, идет перенаправление на страницу со статистикой
def stats():   
    try:
        searchword = request.args       

        wrd = words_uniq(words_dict, searchword['sol'],searchword['tot'], \
                   searchword['ist'],searchword['uko'],searchword['otl'],searchword['vop'],searchword['isc'])

        ages = ages_min_max(searchword['age'])
        mf_count = male_fem_count(searchword['sex'])
        sph = sphere_count(searchword['sph'])
        write_to(searchword)
        return render_template('stats.html', words1 = words_dict[1], words2 = words_dict[2],words3 = words_dict[3], \
                              words4 = words_dict[4], words5 = words_dict[5],words6 = words_dict[6],\
                              words7 = words_dict[7], \
                            mina = ages[0], maxa = ages[1], fem = mf_count[1], mal = mf_count[0], \
                              pro = sph[0], inte = sph[1], serv = sph[2], \
                              work_student = wrk_stdnt_count(searchword), all_p = ages[2] )
    except: 
        return 'Некорректный ввод данных!'

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results():
    searchword = request.args
    wrd = searchword['word']
    key_ = words_dict_ [wrd]
    wrds = {}
    try:
        b = searchword['all']
        cat = 'самый популярный(ые)'
        m = max(words_dict[key_].values())
        for i in words_dict[key_]:
            if words_dict[key_][i] == m:
                wrds[i] =  words_dict[key_][i]                
    except: 
        cat = 'все синонимы'
        wrds = words_dict[key_]
    return render_template('results.html', word_ = wrd, cat = cat, words = wrds)

@app.route('/json')
def json_():
    return render_template('json.html', js = json_list)


if __name__ == '__main__':
    app.run()

