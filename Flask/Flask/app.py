import base64
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io


app = Flask(__name__, template_folder="templates")

final_df = pd.read_csv('datasets/final_df.csv', index_col=0)
country_list = list(final_df.index)
cat_list = ['Culinaric', 'Safety', 'Culture', 'Landscape', 'Weather']


def wr(rating):
    wr = {}
    for k in rating.keys():
        wr[k] = rating[k] / sum(rating.values())
    return wr


def get_scores(rating):

    weigthed_rating = wr(rating)
    scores = {}
    for cou in country_list:
        score = 0
        for cat in cat_list:
            score += (final_df.loc[cou, cat] * weigthed_rating[cat])
        scores[cou] = score
    return scores


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommendations", methods=["POST"])
def recommendations():
    rating = {}
    for key in request.form:
        full_key = key[:-1] if key.endswith('_') else key
        rating[full_key] = int(request.form[key])

    my_dict = get_scores(rating)
    sorted_dict = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)
    data = sorted_dict[:3]
    labels = [item[0] for item in data]
    values = [item[1] for item in data]

    plt.figure(figsize=(6, 6))
    plt.bar(labels, values, color='skyblue')
    plt.ylabel('Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image buffer to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template("recommendations.html", image_base64=image_base64)


if __name__ == "__main__":
    app.run(debug=True)
