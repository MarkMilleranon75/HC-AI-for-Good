def test_load():
  return loaded

def compute_probs(neg,pos):
  total = neg+pos
  p0 = neg/total
  p1 = pos/total
  return [p0,p1]

def cond_prob(full_table, the_evidence_column, the_evidence_column_value, the_target_column, the_target_column_value):
  assert the_evidence_column in full_table    
  assert the_target_column in full_table  
  assert the_evidence_column_value in up_get_column(full_table, the_evidence_column)
  assert the_target_column_value in up_get_column(full_table, the_target_column)
  t_subset = up_table_subset(full_table, the_target_column, 'equals', the_target_column_value)
  e_list = up_get_column(t_subset, the_evidence_column)
  p_b_a = sum([1 if v==the_evidence_column_value else 0 for v in e_list])/len(e_list)  
  return p_b_a  

def cond_probs_product(full_table, evidence_row, target_column, target_column_value):
  assert target_column in full_table
  assert target_column_value in up_get_column(full_table, target_column)
  assert isinstance(evidence_row, list)
  assert len(evidence_row) == len(up_list_column_names(full_table)) - 1
  table_columns = up_list_column_names(full_table)
  evidence_columns = table_columns [0:-1]
  evidence_complete = up_zip_lists(evidence_columns, evidence_row)
  cond_prob_list = []
  for col,val in evidence_complete:
    Prob = cond_prob(full_table, col, val, target_column, target_column_value)
    cond_prob_list+=[Prob]
  partial_numerator = up_product(cond_prob_list)
  return partial_numerator

def prior_prob(full_table, the_column, the_column_value):
  assert the_column in full_table
  assert the_column_value in up_get_column(full_table, the_column)
  t_list = up_get_column(full_table, the_column)
  p_a = sum([1 if v==the_column_value else 0 for v in t_list])/len(t_list)
  return p_a

def naive_bayes(full_table, evidence_row, target_column):
  assert target_column in full_table
  assert isinstance(evidence_row, list)
  assert len(evidence_row) == len(up_list_column_names(full_table)) - 1 
  false1=cond_probs_product (full_table, evidence_row, target_column, 0)
  false2=prior_prob(full_table,target_column, 0)
  falsenumerator=false2*false1
  true1=cond_probs_product (full_table, evidence_row, target_column, 1)
  true2=prior_prob(full_table, target_column, 1)
  truenumerator=true2*true1
  neg, pos = compute_probs(falsenumerator, truenumerator)
  return[neg,pos]

def metrics(zipped_list):
  assert isinstance(zipped_list, list)
  assert all([isinstance(v, list) for v in zipped_list])
  assert all([len(v)==2 for v in zipped_list])
  assert all([isinstance(a,(int,float)) and isinstance(b,(int,float)) for a,b in zipped_list]), f'zipped_list contains a non-int or non-float'
  assert all([float(a) in [0.0,1.0] and float(b) in [0.0,1.0] for a,b in zipped_list]), f'zipped_list contains a non-binary value'
  TN = sum([1 if pair==[0,0] else 0 for pair in zipped_list])
  TP = sum([1 if pair==[1,1] else 0 for pair in zipped_list])
  FP = sum([1 if pair==[1,0] else 0 for pair in zipped_list])
  FN = sum([1 if pair==[0,1] else 0 for pair in zipped_list])
  precision= TP/(TP+FP) if (TP+FP) >0 else 0
  recall= TP/(TP+FN) if (TP+FN) >0 else 0
  f1= 2 * (precision * recall) / (precision + recall) if (precision+recall) >0 else 0
  accuracy= sum([1 if a==b else 0 for a,b in zipped_list])/len(zipped_list)
  roundacc=round(accuracy, 2)
  roundF1=round(f1, 2)
  roundpre=round(precision,2)
  roundrec=round(recall, 2)
  return {'Accuracy':roundacc, 'F1':roundF1, 'Precision':roundpre, 'Recall':roundrec}

  def generate_random(n):
    random_weights = [round(uniform(-1, 1), 2) for i in range(n)]
    return random_weights
    
  def node(inputs, weights):
    assert isinstance(inputs,list)
    assert isinstance(weights, list)
    assert len(inputs)==len(weights)
  
    zipped = up_zip_lists(inputs,weights)
    z = sum([x*y for x,y in zipped])
    s = sigmoid(z) 
    return s

  def feed_forward(net_weights, inputs):
    # slide left to right
    for layer in net_weights:
      output = [node(inputs, node_weights) for node_weights in layer]
      inputs = output  #the trick - make input the output of previous layer
    result = output[0]
    return result
    
  def run_random_forest(train, test, target, n):
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=n, max_depth=2, random_state=0)
    X = up_drop_column(train, target)
    y = up_get_column(train,target)
    assert isinstance(y,list)
    assert len(y)==len(X)
    clf.fit(X, y)
    k_feature_table = up_drop_column(test, target)
    k_actuals = up_get_column(test, target)
    probs = clf.predict_proba(k_feature_table)
    assert len(probs)==len(k_actuals)
    assert len(probs[0])==2
    pos_probs = [p for n,p in probs]
    from sklearn.ensemble import RandomForestClassifier
    assert target in train
    assert target in test
    all_mets=[]
    for t in thresholds:
      predictions = [1 if pos>t else 0 for pos in pos_probs]
      pred_act_list = up_zip_lists(predictions, k_actuals)
      mets = metrics(pred_act_list)
      mets['Threshold'] = t
      all_mets = all_mets + [mets]
    metrics_table = up_metrics_table(all_mets)
    return metrics_table

  def try_archs(train_table, test_table, target_column_name, architectures, thresholds):
    for arch in all_architectures:
      probs = up_neural_net(train_table, test_table, arch, target)
      pos_probs = [pos for neg,pos in probs]
    all_mets=[]
    for t in thresholds:
      predictions = [1 if pos>t else 0 for pos in pos_probs]
      pred_act_list = up_zip_lists(predictions, k_actuals)
      mets = metrics(pred_act_list)
      mets['Threshold'] = t
      all_mets = all_mets + [mets]
      print(f'Architecture: {arch}')
      display(up_metrics_table(all_mets))
    return arch_acc_dict
