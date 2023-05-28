from flask import Flask
# from jinja2 import Markup
import uuid
# from jinja2.utils import markupsafe
# from jinja2 import escape
from flask import Flask, render_template, url_for, request, flash, session, redirect
import pickle
import pandas as pd
from markupsafe import escape
import pickle
# from markupsafe import Markup

# from jinja2.utils import Markupsafe
# markupsafe.Markup()
# Markup('')

import numpy as np
import pandas as pd
# from sklearn.preprocessing import StandardScaler as SS

with open("model.pkl", "rb") as f:
    model = pickle.load(f)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nsdndjngjnnjdasjkwebju5489djkdgjkdjk347hdk'


menu = [{'name': 'New prognois', 'url': 'enter_item'},
        {'name': 'About the project', 'url': 'about'}]


@app.route("/")
@app.route("/index")
def index():
    print(url_for('index'))
    return render_template("index.html", title="Main page", menu=menu)


@app.route("/about")
def about():
    return render_template("about.html", title="About the project", menu=menu)


@app.route("/enter_item", methods=['POST', 'GET'])
def enter_item():
    f1, f2, f3, f4, f5, f6, f7, f8, f9, f10 = False, False, False, False, False, False, False, False, False, False

    if request.method == 'POST':
        pairs = dict(request.form)
        print(pairs)

        if len(pairs['age']) < 1:
            flash('age incorrect!')
        else:
            f1 = True


        if len(pairs['gender']) < 1:
            flash('gender incorrect!')
        else:
            f2 = True

        if len(pairs['refraction']) < 1:
            flash('refraction incorrect!')
        else:
            f3 = True

        if len(pairs['sport_hrs']) < 1:
            flash('sport_hrs incorrect!')
        else:
            f4 = True

        if len(pairs['read_hrs']) < 1:
            flash('read_hrs incorrect!')
        else:
            f5 = True

        if len(pairs['comp_hrs']) < 1:
            flash('comp_hrs incorrect!')
        else:
            f6 = True

        if len(pairs['study_hrs']) < 1:
            flash('comp_hrs incorrect!')
        else:
            f7 = True

        if len(pairs['TV_hrs']) < 1:
            flash('TV_hrs incorrect!')
        else:
            f8 = True


        if len(pairs['mom_myopia']) < 1:
            flash('mom_my incorrect!')
        else:
            f9 = True

        if len(pairs['dad_myopia']) < 1:
            flash('dad_my incorrect!')
        else:
            f10 = True




        if (f1 * f2 * f3 * f4 * f5 * f6 * f7 * f8*f9 * f10 ):

            V = []
            for f in pairs.values():
                V.append(f)

            V = [float(x) for x in V]
            # V = scaler.transform([V])
            # print(V)
            # V = V.reshape(1, -1)

            to_predict = pd.DataFrame(columns=['AGE',
             'GENDER',
             'SPHEQ',
             'SPORTHR',
             'READHR',
             'COMPHR',
             'STUDYHR',
             'TVHR',
             'MOMMY',
             'DADMY'])

            new_r = pd.Series(V, index=to_predict.columns, name='Prognosis')

            to_predict = to_predict.append(new_r)

            to_predict['DIOPTERHR'] = 3 * (to_predict['READHR'] + to_predict['STUDYHR']) + 2 * to_predict[
                'COMPHR'] + 1 * to_predict['TVHR']

            to_predict['FREEHR'] = 105 - to_predict['READHR'] - to_predict['COMPHR'] - to_predict['STUDYHR'] - \
                                   to_predict['TVHR']

            to_predict.loc[(to_predict['MOMMY'] == 1) & (to_predict['DADMY'] == 1), 'BOTH'] = '1'
            to_predict.loc[(to_predict['MOMMY'] == 0) & (to_predict['DADMY'] == 0), 'NONE_PAR'] = '1'
            to_predict = to_predict.fillna(0)
            to_predict.BOTH = to_predict.BOTH.astype(int)
            to_predict.NONE_PAR = to_predict.NONE_PAR.astype(int)

            prediction = model.predict(to_predict)
            print(new_r)
            print(prediction)
            # prediction = model.predict([V])
            # print(V)
            # print(prediction)
            if prediction == 0:


                flash('Congratulations! At this moment myopia risk is low')
            else:
                flash('Your child has high risk of myopia development. Please be aware of myopia prevention measures')


        else:
            print('Check submitted data')


        return render_template("enter_item.html", title = "Try again", menu = menu)
    else:
        return render_template("enter_item.html", title = "Try again", menu = menu)


if __name__ == '__main__':
    app.run(debug=True)
