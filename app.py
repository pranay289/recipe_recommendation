from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import json


app = Flask(__name__)


df = pd.read_csv('recc2.csv')

df["Nutritions"] = df["Nutritions"].apply(lambda x: json.loads(x))
df['recipies'] = df['recipies'].str.lower()
df['Tags'] = df['Tags'].str.lower()

df['bag'] = df['Description'] + ' ' + df['Tags'] + ' ' + df['recipe_name'] + ' ' + df['Ingredients']

tfv = TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                      ngram_range=(1, 3), stop_words='english')

df['bag'] = df['bag'].fillna('')

tfv_matrix = tfv.fit_transform(df['bag'])
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
indices = pd.Series(df.index, index=df['recipies']).drop_duplicates()


@app.route("/alldata")
def all_data():
    data = pd.DataFrame(
        df[['RecipeID', 'recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By', 'RequiredTime',
            'Servings',
            'Ingredients', 'Directions']])
    return_data = data.to_json(orient="records")
    prse = json.loads(return_data)
    response = json.dumps(prse)
    return response


## RECOMENDATION
@app.route("/recomm", methods=['GET', 'POST'])
def recommend_recipe(sig=sig):
    if request.method == 'POST':

        try:

            details = request.form
            title = details['title']
            idx = indices[title]
            sig_scores = list(enumerate(sig[idx]))
            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
            sig_scores = sig_scores[1:200]
            movies_indices = [i[0] for i in sig_scores]
            g = pd.DataFrame(df)
            data = g[['RecipeID', 'recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By', 'RequiredTime',
                      'Servings',
                      'Ingredients', 'Directions']].iloc[movies_indices]
            return_data = data.to_json(orient="records")

            parse = json.loads(return_data)

            return json.dumps(parse)
        except:
            return json.dumps([{"response": "Recipe is not found in list.."}], sort_keys=True,
                              indent=4)


@app.route('/time_based', methods=['GET', 'POST'])
def time_based():
    if request.method == "POST":
        details = request.form
        time = details['time']
        # now = datetime.datetime.now()
        # s = int(now.strftime('%H'))
        time = int(time)
        data = pd.DataFrame(
            df[['RecipeID', 'recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By', 'RequiredTime',
                'Servings',
                'Ingredients', 'Directions']])
        if time < 12:
            options = ["breakfast"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
        elif 12 <= time < 15:
            options = ["lunch"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
        elif 15 < time < 20:
            options = ["nasta", "breakfast"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
        elif 20 <= time < 23:
            options = ["lunch", "dinner"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
        elif 23 <= time < 7:
            options = ["drinks", "breakfast"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
        elif time == 0:
            options = ["drinks", "breakfast"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
        else:
            options = ["nasta", "breakfast"]
            result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]
            return_data = result.to_json(orient="records")
            parse = json.loads(return_data)
            return json.dumps(parse)
    return jsonify({"response": False
                    })


# if __name__ == '__main__':
#     # WSGIRequestHandler.protocol_version = "HTTP/1.1"
#     # app.run(debug=False,host="0.0.0.0",port=5000)
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()







## For now it is commented
#
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'pranay'

# mysql = MySQL(app)


# @app.route("/login2", methods=['GET', 'POST'])
# def check_login():
#     if request.method == 'POST':
#         details = request.form
#         email = details['mail']
#         password = details['pass']
#         cur = mysql.connection.cursor()
#         val = cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
#         res = cur.fetchall()
#         iid = ""
#         for i in res:
#             iid = i[0]
#         mysql.connection.commit()
#         cur.close()

#         if val > 0:
#             return json.dumps({'response': True, 'id': iid}, sort_keys=True, indent=4)
#         else:
#             return json.dumps({'response': False}, sort_keys=True, indent=4)

#     return render_template("login.html")


# @app.route("/login")
# def login():
#     return render_template("login.html")


# @app.route("/signup")
# def signup():
#     return render_template("index.html")

# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(THIS_FOLDER, 'reccc.csv')

## Signup Section
# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         details = request.form
#         email = details['email']
#         password = details['password']
#         cur2 = mysql.connection.cursor()
#         val = cur2.execute("SELECT * FROM users WHERE email=%s ", (email,))

#         cur2.close()
#         if val > 0:
#             return json.dumps({'response': False}, sort_keys=True, indent=4)
#         else:
#             cur = mysql.connection.cursor()
#             cur.execute(
#                 "INSERT INTO users(email,password,user_id) VALUES(%s,%s,NULL)",
#                 (email, password))
#             id = cur.lastrowid
#             mysql.connection.commit()
#             cur.close()
#             return json.dumps({'response': True, 'id': id}, sort_keys=True, indent=4)

# @app.route("/signup2", methods=['GET', 'POST'])
# def signup2():
#     if request.method == "POST":
#         details = request.form
#         id = details['id']
#         username = details['username']
#         age = details['age']
#         gender = details['gender']
#         disease = details['disease']
#         vegetarian = details['vegetarian']

#         cur = mysql.connection.cursor()
#         val = cur.execute("UPDATE users SET user_name=%s,age=%s,gender=%s,disease=%s,vegetarian=%s WHERE user_id=%s",
#                           (username, age, gender, disease, vegetarian, id))
#         mysql.connection.commit()
#         cur.close()
#         if val > 0:
#             return json.dumps({'response': True}, sort_keys=True, indent=4)

#         return json.dumps({'response': False}, sort_keys=True, indent=4)


# @app.route("/signup3", methods=['GET', 'POST'])
# def signup3():
#     if request.method == "POST":
#         details = request.form
#         id = details['id']
#         prefernces = details['preference']

#         cur = mysql.connection.cursor()
#         val = cur.execute("UPDATE users SET preferences=%s WHERE user_id=%s",
#                           (prefernces, id))
#         mysql.connection.commit()
#         cur.close()
#         if val > 0:
#             return json.dumps({'response': True}, sort_keys=True, indent=4)
#         return json.dumps({'response': False}, sort_keys=True, indent=4)
## BASED ON PROFILE

# @app.route('/get_reccoom', methods=['GET', 'POST'])
# def get_final_data():
#     if request.method == "POST":
#         details = request.form
#         iid = details['id']
#         cur = mysql.connection.cursor()
#         data = cur.execute("SELECT * FROM users WHERE user_id=%s", iid)
#         val = cur.fetchall()
#         if data > 0:
#             l = []
#             for i in val:
#                 l = i[8]

#             options = ast.literal_eval(l)
#             try:

#                 g = pd.DataFrame(df)
#                 data = g[['RecipeID', 'recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By',
#                           'RequiredTime',
#                           'Servings',
#                           'Ingredients', 'Directions']].iloc[0:300]

#                 result = data[data['Tags'].apply(lambda x: any(item for item in options if item in x))]

#                 return_data = result.to_json(orient="records")
#                 parse = json.loads(return_data)
#                 return json.dumps(parse)
#             except:
#                 return jsonify({"response": False})
#         else:
#             return jsonify({"response": False})
# @app.route("/recomm")
# def recomm_page():
#     return render_template("recipe_rec.html")


# df1 = pd.read_csv('disease.csv')
# dlist = df1["disease"].tolist()
# glist = df1["good"].tolist()
# rlist = df1["restricted"].tolist()


# ## Disease Section
# @app.route("/healthy", methods=['GET', 'POST'])
# def get_healthy():
#     if request.method == 'POST':
#         details = request.form
#         recipe_id = details["recipe_id"]
#         iid = details["id"]
#         cur = mysql.connection.cursor()
#         data = cur.execute("SELECT * FROM users WHERE user_id=%s", iid)
#         val = cur.fetchall()
#         if data > 0:
#             l = []
#             l2 = []
#             for i in val:
#                 l = i[9]
#                 l2 = i[10]

#             glist = ast.literal_eval(l)
#             rlist = ast.literal_eval(l2)
#             d = df[df.RecipeID == int(recipe_id)]

#             isGood = d[d['Ingredients'].apply(lambda x: any(item for item in glist if item in x))]
#             isBad = d[d['Ingredients'].apply(lambda x: any(item for item in rlist if item in x))]

#             return jsonify({"isGood": isGood.empty == False, "isBad": isBad.empty == False})


# @app.route("/disease", methods=['GET', 'POST'])
# def get_diseas():
#     if request.method == 'POST':
#         # try:
#         details = request.form
#         iid = details["id"]
#         disease = details["disease"]
#         v1 = []
#         v2 = []

#         if disease in dlist:
#             idx = dlist.index(disease)
#             v1 = glist[idx]
#             v2 = rlist[idx]
#         # if len(v2) == 0:
#         #         v2 = "none"
#         # if len(v1)==0:
#         #         v1="none"
#         cur = mysql.connection.cursor()
#         val = cur.execute("UPDATE users SET good=%s,rescrited=%s WHERE user_id=%s", (v1, v2, iid))
#         mysql.connection.commit()
#         cur.close()
#         if val > 0:
#             return json.dumps({'response': True}, sort_keys=True, indent=4)

#         return json.dumps({'response': False}, sort_keys=True, indent=4)

#         # except:
#         #     return json.dumps({"response": "error"}, sort_keys=True,
#         #                       indent=4)
# user_history

# @app.route("/history", methods=['GET', 'POST'])
# def post_user_history():
#     if request.method == "POST":
#         details = request.form
#         iid = details['id']
#         user_id = details['user_id']

#         cur2 = mysql.connection.cursor()
#         val = cur2.execute(
#             "SELECT * FROM user_history WHERE id=%s",
#             (iid,))
#         cur2.close()
#         if val > 0:
#             return json.dumps({'response': False}, sort_keys=True, indent=4)
#         else:
#             cur = mysql.connection.cursor()
#             cur.execute(
#                 "INSERT INTO user_history(id,user_id) VALUES (%s,%s)",
#                 (iid, user_id))
#             mysql.connection.commit()
#             cur.close()
#             return json.dumps({'response': True}, sort_keys=True, indent=4)


# # show user history
# @app.route('/show_history', methods=['GET', 'POST'])
# def show_user_history():
#     if request.method == "POST":
#         details = request.form
#         try:
#             iid = details['id']
#             cur = mysql.connection.cursor()
#             data = cur.execute("SELECT * FROM user_history WHERE user_id=%s", (iid))
#             val = cur.fetchall()
#             l = []

#             if data != 0:
#                 for i in val:
#                     l.append(i[0])
#                 data = df.loc[df['RecipeID'].isin(l)]
#                 d = data.to_json(orient="records")
#                 parse = json.loads(d)

#                 return json.dumps(parse)
#             else:
#                 return jsonify({"response": False})
#         except:
#             return jsonify({"response": False})


# # auto Scrolllll

# @app.route('/pref', methods=['GET', 'POST'])
# def get_pref():
#     if request.method == "POST":
#         details = request.form
#         id = details['id']
#         cur = mysql.connection.cursor()
#         data = cur.execute("SELECT * FROM users WHERE user_id=%s", id)
#         val = cur.fetchall()
#         if data > 0:
#             l = []
#             for i in val:
#                 l = i[8]
#                 options = ast.literal_eval(l)
#                 # return_data = options.to_json(orient="records")
#                 # parse = json.loads(return_data)
#                 return jsonify(options)
#         else:
#             return jsonify({"response": False})


# @app.route('/auto_scroll', methods=['GET', 'POST'])
# def get_auto():
#     if request.method == "POST":
#         details = request.form
#         iid = details['id']
#         cur = mysql.connection.cursor()
#         data = cur.execute("SELECT * FROM users WHERE user_id=%s", iid)
#         val = cur.fetchall()
#         if data > 0:
#             l = []
#             for i in val:
#                 l = i[8]
#                 options = ast.literal_eval(l)
#                 try:

#                     g = pd.DataFrame(df)
#                     data = g[['recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By', 'RequiredTime',
#                               'Servings',
#                               'Ingredients', 'Directions', 'ExtraTags']].iloc[0:4]

#                     result = data[data['ExtraTags'].apply(lambda x: any(item for item in options if item in x))]

#                     return_data = result.to_json(orient="records")
#                     parse = json.loads(return_data)
#                     return json.dumps(parse)
#                 except:
#                     return jsonify({"response": False})
#         else:
#             return jsonify({"response": False})
#     else:
#         jsonify({"response": False})


# @app.route('/ing_list', methods=['GET', 'POST'])
# def ing_list():
#     if request.method == "POST":
#         details = request.form
#         iid = details['id']
#         list = details['ing_list']
#         cur = mysql.connection.cursor()
#         data = cur.execute("SELECT * FROM users WHERE user_id=%s", iid)
#         val = cur.fetchall()

#         if data > 0:
#             l = []
#             for i in val:
#                 l = i[8]
#             data = pd.DataFrame(
#                 df[['RecipeID', 'recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By', 'RequiredTime',
#                     'Servings',
#                     'Ingredients', 'Directions', 'ExtraTags']])

#             user_opt = ast.literal_eval(l)

#             user_res = data[data['ExtraTags'].apply(lambda x: any(item for item in user_opt if item in x))]

#             options = ast.literal_eval(list)

#             result = user_res[user_res['Ingredients'].apply(lambda x: any(item for item in options if item in x))]

#             variable = result[
#                 ['RecipeID', 'recipies', 'ImageLink', 'Description', 'Tags', 'Nutritions', 'By', 'RequiredTime',
#                  'Servings',
#                  'Ingredients', 'Directions', 'ExtraTags']]
#             variable["length"] = variable["Ingredients"].str.len()

#             sorted_val = variable.sort_values(by=["length"], ascending=True)

#             return_data = sorted_val.to_json(orient="records")
#             parse = json.loads(return_data)
#             return json.dumps(parse)