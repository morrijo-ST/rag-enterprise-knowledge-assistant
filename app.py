
import html
import pandas as pd
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] {{opacity:1!important;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-tag] {{background:{ACCENT}25!important;color:{INK}!important;border:1px solid {ACCENT}50;}}
    [data-tag] span,[data-tag] button {{color:{INK}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import re
st.set_page_config(page_title='Enterprise Knowledge / Morris',layout='wide')
shell('KNOWLEDGE WORKSPACE','Answers begin with evidence.','Search the policy collection, read the source, and see exactly what supports a response.','editorial')
DOCS=[
{"id":"POL-001","title":"Travel & Expense Policy","department":"Finance","text":"Airfare above $1,200 requires VP approval. Hotel stays should remain below the city cap unless an exception is documented. Expense reports are due within 15 days after travel."},
{"id":"FIN-014","title":"Month-End Close Standard","department":"Finance","text":"Bank reconciliations are completed by business day three. Material reconciling items above $25,000 require controller review. Close commentary is finalized by business day five."},
{"id":"REV-008","title":"Renewal Operations Guide","department":"Revenue","text":"Renewal opportunities should be opened 120 days before contract expiration. At-risk renewals require a documented action plan and weekly status updates."},
{"id":"SEC-003","title":"Data Access Policy","department":"Security","text":"Production financial data is restricted by role. Service accounts must use least privilege and credentials must not be embedded in source code."},
{"id":"OPS-011","title":"Incident Management","department":"Operations","text":"Critical incidents are acknowledged within 15 minutes. An incident owner coordinates response, and a written postmortem is required for severity-one incidents."},
{"id":"HR-004","title":"New Hire Onboarding","department":"People","text":"New hires complete security training during the first week and receive system access only after manager approval."},
]

STOP={'the','a','an','is','are','what','when','how','of','to','and','for','in','on','do','does','i','we','can','my','our','please','tell','me','about'}
def tokens(text):return set(re.findall(r'[a-z0-9]+',text.lower()))-STOP

departments=st.sidebar.multiselect('Department',sorted({d['department'] for d in DOCS}),default=sorted({d['department'] for d in DOCS}))
a,b=st.columns([1.4,1])
with a:
    st.subheader('Find the source before the answer.')
    q=st.text_input('Search policy documents','When are bank reconciliations due and when does controller review apply?')
    filtered=[d for d in DOCS if d['department'] in departments]
    query=tokens(q)
    ranked=sorted([(len(query & tokens(d['title']+' '+d['text'])),d) for d in filtered],key=lambda x:x[0],reverse=True)
    hits=[(score,d) for score,d in ranked if score>=2][:3]
    if not q.strip():st.info('Enter a policy question to inspect matching sources.')
    elif not hits:st.warning('Insufficient keyword evidence in the selected documents. Try a more specific question or expand the department filter.')
    else:
        st.caption('RETRIEVED PASSAGES · KEYWORD SEARCH')
        for score,d in hits:
            with st.container(border=True):
                st.subheader(d['title'])
                st.write(d['text'])
                st.caption(f"{d['id']} · {d['department']} · {score} matching query terms")
        st.info('These are source excerpts, not a generated answer. A keyword match does not establish that the passage answers every part of your question.')
with b:
    st.subheader('Source reader')
    if filtered:
        chosen=st.selectbox('Document',[d['id'] for d in filtered])
        d=next(d for d in filtered if d['id']==chosen)
        st.write(f"**{d['title']}**")
        st.write(d['text'])
        st.caption(f"Document {d['id']} / {d['department']}")
    else:st.info('Choose at least one department to view sources.')
with st.expander('Knowledge inventory'):
    table(pd.DataFrame(filtered,columns=['id','title','department','text']),'knowledge_inventory')
brief('Retrieval prototype using six fictional documents. No embeddings, vector database, permissions service, or language-model generation is connected. The interface demonstrates source inspection and evidence limits.')
