import os
import pandas as pd


def make_dataframe(path, labels):
    df = pd.DataFrame()
    df['result'] = labels
    df['quantity'] = 1
    data = df.groupby(['result'], as_index=False).sum()
    data.to_csv(path.info + '/predictions.csv')
    return data


def filter_dataframe(dataframe):
    labels = [
        'saudavel',
        'ardido&mofado',
        'bandinha',
        'caruncho',
        'contaminantes',
        'genetico',
        'manchado',
        'mordido']
    results = {}
    for label in labels:
        value = dataframe.loc[dataframe['result'] == label]['quantity'].values
        if len(value) > 0:
            results[label] = value[0]
        else:
            results[label] = 0
    return results


def from_database(analysis):
    problems_df = pd.DataFrame() 
    geometric_df = pd.DataFrame()
    problem, problem_labels, geometric, geometric_labels = [], [], [], []
    if analysis.saudavel != 0:
        problem_labels.append('Saudavel')
        problem.append(analysis.saudavel)
    if analysis.ardido != 0:
        problem_labels.append('Ardido-Mofado')
        problem.append(analysis.ardido)
    if analysis.bandinha != 0:
        problem_labels.append('Bandinha')
        problem.append(analysis.bandinha)
    if analysis.caruncho != 0:
        problem_labels.append('Caruncho')
        problem.append(analysis.caruncho)
    if analysis.contaminantes != 0:
        problem_labels.append('Contaminantes')
        problem.append(analysis.contaminantes)
    if analysis.imaturo != 0:
        problem_labels.append('Imaturo')
        problem.append(analysis.imaturo)
        geometric_labels.append('imaturo')
        geometric.append(analysis.imaturo)
    if analysis.genetico != 0:
        problem_labels.append('Genetico')
        problem.append(analysis.genetico)
    if analysis.manchado != 0:
        problem_labels.append('Manchado')
        problem.append(analysis.manchado)
    if analysis.mordido != 0:
        problem_labels.append('Mordido')
        problem.append(analysis.mordido)
    if analysis.size_12 != 0:
        geometric_labels.append('Peneira-12')
        geometric.append(analysis.size_12)
    if analysis.size_11 != 0:
        geometric_labels.append('Peneira-11')
        geometric.append(analysis.size_11)
    if analysis.size_10 != 0:
        geometric_labels.append('Peneira-10')
        geometric.append(analysis.size_10)
    if analysis.size_9 != 0:
        geometric_labels.append('Peneira-9')
        geometric.append(analysis.size_9)
    geometric_df['type'] = geometric_labels
    geometric_df['quantity'] = geometric 
    problems_df['type'] = problem_labels
    problems_df['quantity'] = problem
    
    return problems_df, geometric_df

