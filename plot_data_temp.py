import pandas as pd
import matplotlib.pyplot as plt
import collections

df = pd.read_csv("t20_practice.csv")

sngl_scores = ['0', '3', '19', '7', '16', '8', '11', '14', '9', '12', '5', '20', '1', '18', '4', '13', '6', '10', '15', '2', '17', '25', '50']
dbl_scores = [f'D{i}' for i in sngl_scores if i != "0" and '25' not in i and 'Bull' not in i]
tbl_scores = [f'T{i}' for i in sngl_scores if i != "0" and '25' not in i and 'Bull' not in i]
       
score_sets = [sngl_scores, dbl_scores, tbl_scores]

# get thrown darts
all_darts = [i.strip(" ") for i in list(df['Dart1']) + list(df['Dart2']) + list(df['Dart3'])]
all_sngl = [i for i in all_darts if 'T' not in i and 'D' not in i]
all_dbl = [i for i in all_darts if 'D' in i and i not in ("0", "25", "50")]
all_tbl = [i for i in all_darts if 'T' in i and i not in ("0", "25", "50")]

fig, ax = plt.subplots()

colours = ['blue', 'red', 'green']
names = ['Singles', 'Doubles', 'Trebles']
for i, scores in enumerate([all_sngl, all_dbl, all_tbl]):
    freq = dict(collections.Counter(scores))

    for score in score_sets[i]:
        if score not in scores:
            freq[score] = 0

    index_map = {score: i for i, score in enumerate(score_sets[i])}
    freq = sorted(freq.items(), key=lambda pair: index_map[pair[0]])
    freq = [i[1] for i in freq]

    if i > 0:
        freq += [0, 0] # add 0 25s and 0 50s for plotting doubles and trebles

    # plot with same x axis
    ax.bar(score_sets[0], freq, color=colours[i], label=names[i], edgecolor="black", zorder=2)

ax.grid(linewidth="0.5", linestyle="--", zorder=1)
ax.legend()
ax.set_ylabel("Number of hits")
ax.set_xlabel("Score")
plt.show()

