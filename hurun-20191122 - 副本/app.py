
from flask import Flask, render_template, request
from jinja2 import Markup, Environment, FileSystemLoader
import pandas as pd
import cufflinks as cf
import plotly as py
import plotly.graph_objs as go
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
from pyecharts.charts import Geo,Pie,Bar,Grid,Line,Scatter,Timeline
from pyecharts.globals import ChartType, SymbolType,ThemeType


CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

app = Flask(__name__)

# 准备工作
df = pd.read_csv('hurun.csv', encoding='utf-8', delimiter="\t")
df1 = pd.read_csv('brandcount.csv')
df2 = pd.read_csv('channel.csv')
df3 = pd.read_csv('rank.csv')
regions_available = list(df1.行业类别.dropna().unique())
cf.set_config_file(offline=True, theme="ggplot")
py.offline.init_notebook_mode()

industry = list(df1['行业类别'])
data = list(df1['6-11月'])


def pie_scroll_legend() -> Pie:
    a = (
        Pie(init_opts=opts.InitOpts(width="690px",height="410px"))
        .add("",[list(z) for z in zip(industry,data)],radius=["40%", "75%"])
        .set_global_opts(
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="83%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return a

def geo_卫视品牌赞助数量() -> Geo:
    b = (
        Geo(init_opts=opts.InitOpts(width="600px",height="400px"))
        .add_schema(maptype="china")
        .add("各卫视品牌赞助数量统计",list(zip(list(df2['省份']),list(df2['品牌数量']))),type_=ChartType.HEATMAP,)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=31),
        )
    )
    return b

def bar6() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(width="600px",height="400px"))
        .add_xaxis(list(df1['行业类别']))
        .add_yaxis("投放时长（分）", list(df1['6月']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(#title_opts=opts.TitleOpts("2019年6月份各行业赞助情况一览"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0,formatter="{value} /分")))
                         #grid_opts=opts.GridOpts(width="90%",height="90%"))
    )
    
    return c

def timeline_bar() -> Timeline:
    """
    color_function = (
        function(params){
            if (params.value >= 0 && params.value <= 1367) {
                return 'red';
            } else if (params.value > 1367 && params.value <= 6417) {
                return 'blue';
            }
            return 'green';
        }
    )
    """
    x = list(df1['行业类别'])
    tl = Timeline(init_opts=opts.InitOpts(width="650px",height="500px"))
    """
    bar = (
        Bar()
        .add_xaxis(x)#,interval=0,rotate=30)
        .add_yaxis("投放时长（分）", list(df1['6-11月']))#,itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)))
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('6-11')),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=60,interval=0))) 
    )
    tl.add(bar, "{}月份".format('6-11'))
    """ 
    bar1 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("投放时长（分）", list(df1['6月']))#,itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('6')),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0,formatter="{value} /分")))
    )
    tl.add(bar1, "{}月份".format('6'))
    
    bar2 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("投放时长（分）", list(df1['7月']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('7')))
    )
    tl.add(bar2, "{}月份".format('7'))
    
    bar3 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("投放时长（分）", list(df1['8月']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('8')))
    )
    tl.add(bar3, "{}月份".format('8'))
    
    bar4 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("投放时长（分）", list(df1['9月']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))    
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('9')))
    )
    tl.add(bar4, "{}月份".format('9')) 
    
    bar5 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("投放时长（分）", list(df1['10月']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))    
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('10')))
    )
    tl.add(bar5, "{}月份".format('10'))
    
    bar6 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("投放时长（分）", list(df1['11月']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))    
        .set_global_opts(title_opts=opts.TitleOpts("{}月份各行业赞助情况一览".format('11')))
    )
    tl.add(bar6, "{}月份".format('11'))
    return tl



@app.route('/',methods=['GET'])
def brand_2019():
    drink = df3[:10][['序号','品牌名称','厂商名称','费用（万元）','时长（分钟）','频次（次）','费用占比']]
    drug = df3[10:20]
    food = df3[20:30]
    alcohol = df3[30:40]
    data_str = drink.to_html()
    a = pie_scroll_legend()
    brand = a.render_embed()
    b = geo_卫视品牌赞助数量()
    brandcount = b.render_embed()
    c = bar6()
    monthsix = c.render_embed()
    tl = timeline_bar()
    sixmonth = tl.render_embed()
    return render_template('results2.html',
                           the_res = data_str,
                           the_select_region=regions_available,
                           the_brand=brand,
                           the_brand_count=brandcount,
                           the_month_six=sixmonth)

@app.route('/',methods=['POST'])
def brand_select() -> 'html':
    the_region = request.form["the_region_selected"]
    print(the_region) # 检查用户输入
    dfs = df.query("region=='{}'".format(the_region))
    df_summary = dfs.groupby("行业").agg({"企业名称":"count","估值（亿人民币）":"sum","成立年份":"mean"}).sort_values(by = "企业名称",ascending = False )
    #print(df_summary.head(5)) # 在后台检查描述性统计
    ## user select
    # print(dfs)
    # 交互式可视化画图
    fig = dfs.iplot(kind="bar", x="行业大类", y="赞助投放时长（分）", asFigure=True)
    py.offline.plot(fig, filename="example.html",auto_open=False)
    with open("example.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    # plotly.offline.plot(data, filename='file.html')
    data_str = dfs.to_html()
    a = pie_scroll_legend()
    brand = a.render_embed()
    b = geo_卫视品牌赞助数量()
    brandcount = b.render_embed()
    return render_template('results2.html',
                            the_plot_all = plot_all,
                            the_res = data_str,
                            the_select_region=regions_available,
                            the_brand=brand,
                            the_brand_count=brandcount
                           )
    
@app.route('/rank',methods=['GET'])
def brand_rank():
    drink = df3[:10]
    drug = df3[10:20]
    food = df3[20:30]
    alcohol = df3[30:40]
    drinkdata = drink.to_html()
    drugdata = drug.to_html()
    fooddata = food.to_html()
    alcoholdata = alcohol.to_html()
    return render_template('rank.html',
                           the_rank = drinkdata,
                           the_drug = drugdata,
                           the_food = fooddata,
                           the_alcohol = alcoholdata,
                           )

if __name__ == '__main__':
    app.run(debug=True,port=8000)

