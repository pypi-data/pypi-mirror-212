from skimage.filters import threshold_otsu
import openai
import numpy as np
import pandas as pd
import scanpy as sc
import time

def extra_genes_inquiry(adata, genes, cluster_ids, log_counts_layer, use_raw):
    
    def get_gene_counts(j, data):
        try:
            return data[:,j].X.A
        except AttributeError:
            return data[:,j].X

    def process_genes(data):
        extra_strs = ''
        for j in genes:
            if j in data.var_names:
                gene_count = get_gene_counts(j, data)
                _threshold = threshold_otsu(gene_count)
                proportion = sum(gene_count[cluster_ids]>= _threshold) / sum(cluster_ids)
                if proportion >= 0.2:
                    extra_strs += j + " is upregulated in the cluster. "
                else:
                    extra_strs += j + " is downregulated in the cluster. "
        return extra_strs

    if log_counts_layer == None and not use_raw:
        return process_genes(adata)
    elif log_counts_layer == None:
        return process_genes(adata.raw)
    else:
        adata[:, j].layer[log_counts_layer] = get_gene_counts(j, adata)
        return process_genes(adata)

def DE_to_df(_adata, rank_key, _padj_thresh=0.05, _logfc_thresh=1):
    def process_genes(i, direction):
        _log2foldmask = (_adata.uns[rank_key]['logfoldchanges'][i].astype('double') >= _logfc_thresh) if direction == "up" else (_adata.uns[rank_key]['logfoldchanges'][i].astype('double') <= -_logfc_thresh)
        _pvalmask = _adata.uns[rank_key]['pvals_adj'][i].astype('double') <= _padj_thresh
        _additional = pd.DataFrame({
            i: _adata.uns[rank_key]['names'][i].astype('str')[_log2foldmask & _pvalmask],
            'logfoldchanges_'+i: np.abs(_adata.uns[rank_key]['logfoldchanges'][i].astype('double')[_log2foldmask & _pvalmask])
        })
        _ribo_gene_mask = [gene.startswith('RPL') or gene.startswith('RPS') for gene in _additional[i]]
        _mt_gene_mask = [gene.startswith('MT-') for gene in _additional[i]]
        _drop_id = np.array(np.array(_ribo_gene_mask) | np.array(_mt_gene_mask))

        _additional = _additional.sort_values(by='logfoldchanges_'+i, ascending=False)
        _additional = _additional.iloc[_drop_id==False, :].reset_index(drop=True)

        return _additional

    _pass_genes_up = pd.DataFrame()
    _pass_genes_down = pd.DataFrame()

    for i in set(_adata.uns[rank_key]['pvals_adj'].dtype.names):
        _pass_genes_up = pd.concat([_pass_genes_up, process_genes(i, "up")[i]], ignore_index=False, axis=1)
        _pass_genes_down = pd.concat([_pass_genes_down, process_genes(i, "down")[i]], ignore_index=False, axis=1)

    return _pass_genes_up, _pass_genes_down

def generate_response(system_msg, user_msg, model, temperature, top_p, frequency_penalty, presence_penalty):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            return response
        except:
            time.sleep(5)


def extract_command(response, var_name):
    original_string = response["choices"][0]["message"]["content"]
    try:
        _, command = original_string.split(f"{var_name} = ", 1)
        final_command = f"{var_name} = {command.split('`', 1)[0]}"
    except ValueError:
        final_command = ""

    return final_command


def use_chat_GPT(system_msg, user_msg, display_conversation, model, temperature, top_p, frequency_penalty, presence_penalty, var_name):
    print('==================Response Generating======================')

    response = generate_response(system_msg, user_msg, model, temperature, top_p, frequency_penalty, presence_penalty)
    
    if display_conversation:
        print(response["choices"][0]["message"]["content"])

    final_command = extract_command(response, var_name)

    return final_command

def create_system_msg1(adata, organism, tissue, cluster_name, pass_genes_up, pass_genes_down, ini_id, ini_extra_genes, log_counts_layer, use_raw, ngenes, model_name, prior_knowledge):
    system_msg1 = f'I have a single-cell RNA-seq expression profile of cells in {organism}\'s {tissue}. Differential gene analysis shows '
    DE_str = f'a group of cells upregulate {list(pass_genes_up[cluster_name][0:ngenes*2].dropna().values)} and downregulate {list(pass_genes_down[cluster_name][0:ngenes*2].dropna().values)}. {prior_knowledge}'
    system_msg1 += DE_str 
    
    cluster_ids = adata.obs['cluster_blind'] == cluster_name
    extra_strs = extra_genes_inquiry(adata, ini_extra_genes, cluster_ids, log_counts_layer, use_raw)
    system_msg1 += extra_strs
    system_msg1 += f" The initial guess made by {model_name} was {ini_id}. "
    
    return system_msg1

def create_user_msg1():
    return "Is the guess reasonable? Based on the given information, identify the most specific cell type possible. In particular, I'm interested in understanding the specific subtype of the cell type this cluster may represent. Write a single-line Python command defining a list variable called 'inference' whose content is the cell type subset inferred."

def start_conversation(adata, organism, tissue, cluster_name, pass_genes_up, pass_genes_down, ini_id, ini_extra_genes, display_conversation, prior_knowledge, log_counts_layer, use_raw, ngenes, model_name, temperature, top_p, frequency_penalty, presence_penalty, sleep_time, prompt_only):
    if prompt_only:
        system_msg1 = f'I have a single-cell RNA-seq expression profile of cells in {organism}\'s {tissue}. Differential gene analysis shows '
        DE_str = f'a group of cells upregulate {list(pass_genes_up[cluster_name][0:ngenes*2].dropna().values)} and downregulate {list(pass_genes_down[cluster_name][0:ngenes*2].dropna().values)}. {prior_knowledge}'
        system_msg1 += DE_str 
        user_msg1 = "Based on the given information, identify the most specific cell type possible. In particular, I'm interested in understanding the specific subtype of the cell type this cluster may represent. Write a single-line Python command defining a list variable called 'inference' whose content is the cell type subset inferred."
        print(system_msg1)
        print(user_msg1)
    else:
        globals_dict = globals()
        locals_dict = locals()
        
        system_msg1 = create_system_msg1(adata, organism, tissue, cluster_name, pass_genes_up, pass_genes_down, ini_id, ini_extra_genes, log_counts_layer, use_raw, ngenes, model_name, prior_knowledge)
        user_msg1 = create_user_msg1()
    
        if display_conversation:
            print(system_msg1)
            print(user_msg1)
    
        final_command_1 = use_chat_GPT(system_msg1, user_msg1, display_conversation, model_name, temperature = temperature, top_p = top_p, frequency_penalty = frequency_penalty, presence_penalty = presence_penalty, var_name = 'inference')
        exec(final_command_1, globals_dict, locals_dict)
        inference = locals_dict['inference']
    
        print('==================GPT Cooling======================')
        time.sleep(sleep_time)
    
        return inference

def chat_workflow(adata, openaikey, cluster_key, organism = 'unknown',tissue = 'unknown', DE_dfs = None, rank_key = None, display_conversation = True,
                  double_verification  = True, prior_knowledge = '', log_counts_layer = None, use_raw = False, ngenes = 20,
                  model_name = 'gpt-3.5-turbo', temperature = 0, top_p = 1, 
                  frequency_penalty = 0, presence_penalty = 0, sleep_time = 5, prompt_only = False):
    openai.api_key = openaikey
    adata.obs['cluster_blind'] = adata.obs.groupby(cluster_key).ngroup().astype('str')
    if DE_dfs == None and rank_key == None:
        if use_raw == True and log_counts_layer == None:
            sc.tl.rank_genes_groups(adata, groupby='cluster_blind', key_added='rank',method = 'wilcoxon',use_raw  = True)
        elif log_counts_layer == None:
            sc.tl.rank_genes_groups(adata, groupby='cluster_blind', key_added='rank',method = 'wilcoxon')
        else:
            sc.tl.rank_genes_groups(adata, groupby='cluster_blind', key_added='rank',method = 'wilcoxon',layer = log_counts_layer)
        pass_genes_up, pass_genes_down = DE_to_df(adata,rank_key = 'rank')
    elif DE_dfs == None:
        pass_genes_up, pass_genes_down = DE_to_df(adata,rank_key)
    else:
        pass_genes_up = DE_dfs[0]
        pass_genes_down = DE_dfs[1]

    if prompt_only:
        for i in set(adata.obs['cluster_blind']):
            print('=================for re-indexed cluster '+ i +'====================')
            spec_inference = start_conversation(adata,organism,tissue, i, pass_genes_up,
                                   pass_genes_down, None, None, display_conversation, prior_knowledge, 
                                   log_counts_layer, use_raw, ngenes, model_name, temperature, top_p, frequency_penalty, presence_penalty, sleep_time, prompt_only)
    else:
        system_msg0 = 'I have a single-cell RNA-seq expression profile of cells in ' + organism +"'s "+ tissue +'. Differential gene analysis shows '
        for i in set(adata.obs['cluster_blind']):
            DE_str = 'Cluster '+i+ ' upregulates ' + str(list(pass_genes_up[i][0:ngenes].dropna().values))+ 'and downregulates ' + str(list(pass_genes_down[i][0:ngenes].dropna().values)) +'.'
        system_msg0 += DE_str
        user_msg0 =     "Identify the cell type and cell type subset of each cluster using the information I provided.\
                        Write a single python command that defines a list variable called ini_infer, where its first entry is a dict whose keys are the strings of cluster indices and values are the cell type you identified,\
                        and the second entry is a list of 30 genes that can better characterize these cell types you identified."
        if display_conversation:
            print(system_msg0)
            print(user_msg0)
        
        final_command_0 = use_chat_GPT(system_msg0,user_msg0,display_conversation = True,
                                       model = 'gpt-3.5-turbo',temperature = temperature, top_p = top_p, frequency_penalty = frequency_penalty,
                                       presence_penalty = presence_penalty, var_name = 'ini_infer')
        locals_dict = locals()
        exec(final_command_0,locals_dict)
        ini_infer = locals_dict['ini_infer']
        
        adata.obs['GPT_celltype'] = ''
        for i in set(adata.obs['cluster_blind']):
            if double_verification  == True:
                spec_inference = start_conversation(adata,organism,tissue, i, pass_genes_up,
                                   pass_genes_down, ini_infer[0][i], ini_infer[1], display_conversation, prior_knowledge, 
                                   log_counts_layer, use_raw, ngenes, model_name, temperature, top_p, frequency_penalty, presence_penalty, sleep_time)
                adata.obs['GPT_celltype'][adata.obs['cluster_blind'] == i] = str(spec_inference)
            else:
                adata.obs['GPT_celltype'][adata.obs['cluster_blind'] == i] = ini_infer[0][i]
    adata.uns['pass_genes_up'] = pass_genes_up
    adata.uns['pass_genes_down'] = pass_genes_down