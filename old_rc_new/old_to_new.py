#!/usr/local/python
'''
Main script for creating report card data
'''

### 
# settings
###
monthly_stats = ""
page_views = ""
comscore_directory = ""

output_folder = './output'


import old_charts
import new_charts
import comscore
import targets


# HACK dict for consistent colormapping
from collections import defaultdict
seen_labels = {}
count_labels = defaultdict(int)
color_index = 0
colors = ["rgb(165,0,38)","rgb(215,48,39)","rgb(244,109,67)","rgb(253,174,97)","rgb(254,224,144)","rgb(255,255,191)","rgb(224,243,248)","rgb(171,217,233)","rgb(116,173,209)","rgb(69,117,180)","rgb(49,54,149)"] # colorbrewer spectral

# wan can limit the number of fixed colors to labels that appear more than once
multi_lables = ['Latin-America', 'All projects', 'Europe', 'Middle-East/Africa', 'French', 'China', 'Russian', 'World', 'Target', 'Commons', 'English', 'Italian', 'Chinese', 'German', 'North-America', 'India', 'Japanese', 'Asia Pacific', 'Spanish', 'Total']
for i,l in enumerate(multi_lables):
    seen_labels[l] = colors[i%len(colors)]

def get_color(l):
    global color_index,seen_labels
    if l not in seen_labels:
        return None
        seen_labels[l] = colors[color_index%len(colors)]
        color_index+=1   

    count_labels[l] += 1
    return seen_labels[l]


def dataset_ui_json(ds_id,n=None,color=True):
    '''HACK warning. Temp function to generate dataset-ui friendly graph description json file. If you read this you can likely (and hopefully) delete this function :)
    '''
    import json

    headers = [s.strip() for s in open('./output/%s.csv'%ds_id,'r').readline()[:-1].split(',')]

    print "------------------------------------"
    print ds_id
    print

    for i,h in enumerate(headers):
        if i==0:
            # don't want the date
            continue 
        if n and i > n:
            # return only n elements
            return

        metric = {
                "index": 0,
                "source_id": ds_id,
                "source_col": i,
                "label": h,                        
                "color": get_color(h),            
                "type": "int",
                "timespan": {
                    "start": None,
                    "end": None,
                    "step": None
                },
                "disabled": False,
                "visible": True,
                "format_value": None,
                "format_axis": None,
                "transforms": [],
                "scale": 1}

        if not color or metric['color'] is None:
            del metric['color']


        print json.dumps(metric)
        print ','
        


def create_all():
    # recreate ErikZ charts
    old_charts.create_all()
    comscore.create_all()

    # new charts
    new_charts.create_all()

    # target charts 
    # TODO: start/end date for projection are hard-coded in target.py
    # Note that it used previously deployed data to /data/datasources/rc to create datafiles.
    targets.create_all()


    #HACK! #HACK! #HACK!
    dataset_ui_json('rc_binary_files')
    dataset_ui_json('rc_article_count',n=8)
    dataset_ui_json('rc_new_article_count',n=5)
    dataset_ui_json('rc_edits_count',n=5)
    dataset_ui_json('rc_new_editors_count',n=10)
    dataset_ui_json('rc_active_editors_count',n=10)
    dataset_ui_json('rc_very_active_editors_count',n=10)
    dataset_ui_json('rc_page_requests',n=7)

    dataset_ui_json('rc_page_requests_mobile')


    dataset_ui_json('rc_comscore_region_uv',color=False)
    dataset_ui_json('rc_comscore_region_reach',color=False)
    dataset_ui_json('rc_comscore_properties',color=False)

    dataset_ui_json('rc_active_editors_target')
    dataset_ui_json('rc_page_requests_mobile_target')


    # print seen_labels
    # print count_labels
    # print
    # print [k for k,v in count_labels.iteritems() if v>1 ]


if __name__ == '__main__':
    create_all()


    



