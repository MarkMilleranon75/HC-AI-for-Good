def test_load():
  return 'loaded'

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

