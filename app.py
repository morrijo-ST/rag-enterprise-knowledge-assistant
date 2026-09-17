import re
from collections import Counter
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Enterprise RAG Assistant",layout="wide")
st.title("Enterprise RAG Knowledge Assistant")
st.caption("Synthetic grounded retrieval with citations and unsupported-question controls.")

DOCS=[
{"id":"POL-001","title":"Travel & Expense Policy","department":"Finance","text":"Airfare above $1,200 requires VP approval. Hotel stays should remain below the city cap unless an exception is documented. Expense reports are due within 15 days after travel."},
{"id":"FIN-014","title":"Month-End Close Standard","department":"Finance","text":"Bank reconciliations are completed by business day three. Material reconciling items above $25,000 require controller review. Close commentary is finalized by business day five."},
{"id":"REV-008","title":"Renewal Operations Guide","department":"Revenue","text":"Renewal opportunities should be opened 120 days before contract expiration. At-risk renewals require a documented action plan and weekly status updates."},
{"id":"SEC-003","title":"Data Access Policy","department":"Security","text":"Production financial data is restricted by role. Service accounts must use least privilege and credentials must not be embedded in source code."},
{"id":"OPS-011","title":"Incident Management","department":"Operations","text":"Critical incidents are acknowledged within 15 minutes. An incident owner coordinates response, and a written postmortem is required for severity-one incidents."},
{"id":"HR-004","title":"New Hire Onboarding","department":"People","text":"New hires complete security training during the first week and receive system access only after manager approval."},
]
STOP={"the","a","an","is","are","what","when","how","of","to","and","for","in","on","do","does","i","we"}
def tokens(s): return [w for w in re.findall(r"[a-z0-9]+",s.lower()) if w not in STOP]
def score(q,d):
    qv=Counter(tokens(q)); dv=Counter(tokens(d["title"]+" "+d["text"]))
    return sum(min(qv[k],dv[k]) for k in qv)

departments=st.sidebar.multiselect("Department",sorted({d['department'] for d in DOCS}),default=sorted({d['department'] for d in DOCS}))
q=st.text_input("Ask a question","When are bank reconciliations due and when does controller review apply?")
filtered=[d for d in DOCS if d["department"] in departments]
ranked=sorted([(score(q,d),d) for d in filtered],key=lambda x:x[0],reverse=True)
best=[x for x in ranked if x[0]>0][:3]

if q:
    if not best:
        st.warning("I could not find grounded support for that question in the selected knowledge base.")
    else:
        top=best[0][1]
        st.subheader("Grounded answer")
        st.success(top["text"])
        st.caption(f"Primary source: {top['id']} — {top['title']}")
        st.subheader("Retrieved evidence")
        for s,d in best:
            with st.expander(f"{d['id']} · {d['title']} · relevance {s}"):
                st.write(d["text"])

st.subheader("Knowledge base")
st.dataframe(pd.DataFrame(DOCS)[["id","title","department","text"]],use_container_width=True,hide_index=True)
st.info("Production RAG systems would replace this lightweight lexical retriever with embeddings/vector search, document permissions, evaluation, and an LLM synthesis layer. The public demo emphasizes grounding and citations without requiring API keys.")
