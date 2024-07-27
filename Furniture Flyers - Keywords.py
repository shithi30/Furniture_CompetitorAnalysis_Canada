#!/usr/bin/env python
# coding: utf-8

# import
import pandas as pd
import duckdb
import re

# pref.
pd.set_option('display.max_rows', 3000)

# read
read_df = pd.read_csv("C:/Users/shith/Downloads/Competitive Landscape - Tepperman's - Furniture - Flyers.csv")

# platform cloud
def word_freq(platform):

    # filter
    flyer_df = duckdb.query("select * from read_df where platform='"+ platform +"'" ).df()
    if platform == "all": flyer_df = duckdb.query("select * from read_df where platform!='Walmart' ").df()
    
    # paragraph
    sku = flyer_df["sku"].tolist()
    sku_ref = ""
    for s in sku:
        p = re.sub('[^a-zA-Z\s]+', '', s.lower())
        sku_ref = sku_ref + " " + p
    
    # split into words
    sku_ref_split = sku_ref.split()
    
    # word df
    cloud_df = pd.DataFrame()
    cloud_df['word'] = sku_ref_split
    
    # cloud df
    qry = '''
    select word, count(*) times
    from cloud_df
    group by 1
    order by 2 desc
    '''
    cloud_df = duckdb.query(qry).df()

    # return
    return cloud_df

# call
brick_df = word_freq("The Brick")
teppermans_df = word_freq("Tepperman''s")
leons_df = word_freq("Leon''s")
total_df = word_freq("all")

# common - in all
qry = '''
select *, tbl1.times+tbl2.times+tbl3.times total_times
from 
    leons_df tbl1
    inner join
    teppermans_df tbl2 using(word)
    inner join
    brick_df tbl3 using(word)
order by total_times desc
'''
res_df = duckdb.query(qry).df()
display(res_df)

# common - with total
qry = '''
select word, tbl0.times, tbl1.times leons_times, tbl2.times tepper_times, tbl3.times brick_times
from 
    total_df tbl0
    left join 
    leons_df tbl1 using(word)
    left join
    teppermans_df tbl2 using(word)
    left join
    brick_df tbl3 using(word)
where tbl0.times >= 2
order by tbl0.times desc
'''
res_df = duckdb.query(qry).df()
display(res_df)

# # experiment basis
# import enchant
# d = enchant.Dict("en_US")
# d.check("lrelf")
# d.suggest("lrelf")



