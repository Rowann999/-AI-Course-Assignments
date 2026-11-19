"""Lesson 07: reproducible Bernoulli Naive Bayes analysis.
Run from repository lesson root: python src/naive_bayes.py
The supplied teacher test labels are used ONLY for fixed teaching-test reproduction.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score, confusion_matrix, log_loss, precision_score, recall_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
FEATURES = ["fever_ge_38", "nausea", "lumbar_pain", "urine_pushing", "micturition_pain", "burning_urethra"]
LABEL = "bladder_inflammation"
THRESHOLDS = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95]

def metrics(y, p, threshold=0.5):
    pred = (np.asarray(p) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return dict(n=len(y), TN=int(tn), FP=int(fp), FN=int(fn), TP=int(tp),
                accuracy=float(accuracy_score(y, pred)),
                sensitivity=float(recall_score(y, pred, zero_division=0)),
                specificity=float(tn/(tn+fp)) if tn+fp else None,
                precision=float(precision_score(y, pred, zero_division=0)),
                f1=float(f1_score(y, pred, zero_division=0)),
                log_loss=float(log_loss(y, p, labels=[0, 1])))

def run():
    OUT.mkdir(exist_ok=True)
    train = pd.read_csv(DATA/'train.csv')
    val = pd.read_csv(DATA/'validation.csv')
    test = pd.read_csv(DATA/'locked-test-features.csv')
    labels = pd.read_csv(DATA/'locked-test-labels.csv')
    assert (len(train), len(val), len(test)) == (72, 24, 24)
    assert all(set(d["sample_id"]).isdisjoint(set(e["sample_id"])) for d,e in [(train,val),(train,test),(val,test)])
    assert train[FEATURES+[LABEL]].notna().all().all() and val[FEATURES+[LABEL]].notna().all().all()
    assert all(set(train[c].unique()).issubset({0,1}) for c in FEATURES+[LABEL])
    # Align test labels by sample_id; never assume row-order equality.
    assert labels['sample_id'].is_unique and test['sample_id'].is_unique
    test = test.merge(labels[['sample_id', LABEL]], on='sample_id', validate='one_to_one', how='left', sort=False)
    assert test[LABEL].notna().all()
    model = BernoulliNB(alpha=1.0).fit(train[FEATURES],train[LABEL])
    vp = model.predict_proba(val[FEATURES])[:,1]
    grid=[]
    for t in THRESHOLDS:
        m=metrics(val[LABEL],vp,t)
        grid.append(dict(threshold=t, **m, eligible=m['sensitivity']>=0.90))
    # Max specificity, then nearest 0.5, then smaller threshold.
    eligible=[x for x in grid if x['eligible']]
    assert eligible, 'No threshold meets the pre-specified sensitivity target'
    chosen=sorted(eligible,key=lambda x:(-x['specificity'],abs(x['threshold']-0.5),x['threshold']))[0]['threshold']
    tp=model.predict_proba(test[FEATURES])[:,1]
    prior=np.full(len(val), float(train[LABEL].mean()))
    base=metrics(val[LABEL],prior,0.5)
    dup=[]
    for copies in [0,1,5]:
        cols=FEATURES+[f'lumbar_copy_{i}' for i in range(copies)]
        a=train[FEATURES].copy(); b=val[FEATURES].copy()
        for i in range(copies):
            a[f'lumbar_copy_{i}']=train['lumbar_pain'].to_numpy()
            b[f'lumbar_copy_{i}']=val['lumbar_pain'].to_numpy()
        mm=BernoulliNB(alpha=1.0).fit(a[cols],train[LABEL]); pp=mm.predict_proba(b[cols])[:,1]
        dup.append(dict(extra_lumbar_copies=copies,**metrics(val[LABEL],pp,0.5)))
    query=np.array([[0,0,0,1,1,1]])
    q=float(model.predict_proba(pd.DataFrame(query,columns=FEATURES))[0,1])
    results={'sample_counts':{'train':len(train),'validation':len(val),'test':len(test)},
             'train_positive':int(train[LABEL].sum()),'threshold':chosen,
             'validation':metrics(val[LABEL],vp,chosen),'test':metrics(test[LABEL],tp,chosen),
             'prior_validation':base,'query_000111_probability':q,'duplicate_feature':dup}
    pd.DataFrame(grid).to_csv(OUT/'threshold_grid.csv',index=False)
    pd.DataFrame(dup).to_csv(OUT/'duplicate_feature.csv',index=False)
    pd.DataFrame({'sample_id':val.sample_id,'true_label':val[LABEL],'positive_probability':vp,'predicted_label':(vp>=chosen).astype(int)}).to_csv(OUT/'validation_predictions.csv',index=False)
    pd.DataFrame({'sample_id':test.sample_id,'true_label':test[LABEL],'positive_probability':tp,'predicted_label':(tp>=chosen).astype(int)}).to_csv(OUT/'test_predictions.csv',index=False)
    (OUT/'metrics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    # Single publication-style confusion matrix generated from real validation predictions.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cm=confusion_matrix(val[LABEL],(vp>=chosen).astype(int),labels=[0,1])
    fig,ax=plt.subplots(figsize=(5.4,4.4))
    ax.imshow(cm,cmap='Blues',vmin=0,vmax=max(1,int(cm.max())))
    for i in range(2):
        for j in range(2): ax.text(j,i,str(cm[i,j]),ha='center',va='center',fontsize=17,color='black')
    ax.set_xticks([0,1],['Negative','Positive']);ax.set_yticks([0,1],['Negative','Positive'])
    ax.set_xlabel('Predicted label');ax.set_ylabel('True label');ax.set_title('Validation confusion matrix (n=24)')
    fig.tight_layout();fig.savefig(OUT/'validation_confusion_matrix.png',dpi=180);plt.close(fig)
    return results

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
