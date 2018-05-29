
import os
import matplotlib.pyplot as plt
import pandas as pd
import model.dbScript as db
import utilities.IOProperties as prop


def plot_graph():
    article_name = "All_Article_Year"
    filepath = os.path.join(prop.date_count,  article_name+'.tsv')
    # date_count = db.get_article_count(article_name)

    single_article = 'article_all'

    year_count = db.get_article_year_count(single_article)

    write_into_file(year_count, filepath)

    plt.bar(range(len(year_count)), year_count.values(), align='center')
    plt.xticks(range(len(year_count)), list(year_count.keys()))
    #
    plt.ylabel('No. of articles')
    plt.title(article_name)
    #
    plt.xticks(rotation=90)
    plt.savefig(prop.graph+article_name + ".png")
    plt.show()


def plot_mulitiple_line_month_graph():
    article_names = ["Expressen", "Aftonbladet", "SVD","DN"] #,"svd","dn" , "aftonbladet"
    line_colors = ["#1DACD6", "red", "orange", "purple"]

    df_article_names = ["df_expressen", "df_aftonbladet", "df_svd", "df_dn"]

    df_all = []

    # article_count = {}
    i = 0
    tick_spacing = 1

    fig = plt.figure()
    ax = fig.add_subplot(111)


    for single_article in article_names:
        date_count = db.get_article_count(single_article)
        # print(len(date_count))
        single_article_name = single_article

        single_article = pd.DataFrame(list(sorted(date_count.items())), columns=['Year', single_article_name])
        single_article['Year'] = pd.to_datetime(single_article['Year'])
        # print(single_article['Year'])
        # df_all.append(df_article_names[i])

    # for single_df in df_all:
    # print(df_all[1])
    # df = df_all[0].merge(df_all[1], how='outer', left_index=True, right_index=True)
    # df = df_all[0].join(df_all[1], how = 'outer')
    # df = pd.concat([df_all[0], df_all[1]], verify_integrity=True, ignore_index=True)
    # print(df)

    #
    #
        ax.plot('Year', single_article_name, data=single_article, marker='', color=line_colors[i], linewidth=1)
        # plt.tick_params(axis='both', top='off', right='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        # ax.set_xlabel("X-Label",fontsize=10,color='red')
        # plt.setp(ax.get_xticklabels(),visible=False)
        i += 1
    #

    # my_xticks = [x for x in range(1992, 2019, 1)]


    my_xticks = ['-'.join(str(x).split("-")[0:2]) for x in single_article['Year']]
    # # my_xticks = single_article['Year'].apply(lambda x:x.strftime('%Y-%m'))
    # print(my_xticks)
    #
    plt.xticks(my_xticks, my_xticks)
    plt.ylabel('Antal artiklar', fontsize=16)
    plt.legend(loc=1, prop={'size': 16})
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #
    # #
    plt.xticks(rotation= 90, fontsize=12)
    plt.show()
    # plt.savefig(prop.graph + "Year.png")

def plot_multiple_line_year_graph():
    article_names = ["Expressen", "Aftonbladet", "SVD","DN"] #,"svd","dn" , "aftonbladet"
    line_colors = ["skyblue", "red", "orange", "purple"]

    # article_count = {}
    i = 0
    tick_spacing = 1
    fig, ax = plt.subplots()

    for single_article in article_names:
        date_count = db.get_article_year_count(single_article)
        single_article_name = single_article
    #
    # key, value = max(article_count.items(), key=lambda x:x[1])
    #     print(date_count)
    #     print(list(sorted(date_count.items())))

        single_article = pd.DataFrame(list(sorted(date_count.items())), columns=['Year', single_article_name])
        # print(single_article)
        single_article['Year'] = pd.to_datetime(single_article['Year'])
        # print(single_article['Year'])

        my_xticks = [str(x).split("-")[0] for x in single_article['Year']]
        # print(my_xticks)
        # lab_xticks = [x for x in range(1992, 2019, 1)]


        ax.plot('Year', single_article_name, data=single_article, marker='', color=line_colors[i], linewidth=1)
        i += 1

    plt.xticks(my_xticks)
    plt.ylabel('Antal artiklar', fontsize=14)
    # plt.title('Number of articles published each year')
    plt.legend(loc=2, prop={'size': 14})
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #
    # #
    plt.xticks(rotation= 90, fontsize= 14)
    plt.margins(0.1)
    plt.show()

def write_into_file(date_count, filepath):
    header = ['Year', 'Frequency']

    with open(filepath, "a") as f:
        f.write('\t'.join(header) + "\n")
        for key, value in date_count.items():
            f.write("{}\t{}\n".format(key, value))

if __name__ == "__main__":
    plot_graph()
    # plot_mulitiple_line_month_graph()
    # plot_multiple_line_year_graph()