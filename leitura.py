import pandas as pd
import os

def leitura_dados_taco():
    if not os.path.exists("taco-db-nutrientes.csv"):
        return pd.DataFrame()
    
    df_principais = pd.read_csv("taco-db-nutrientes.csv", on_bad_lines='skip', skipinitialspace=True)

    #Carrega o arquivo dos Minerais
    if os.path.exists("taco-db-nutrientes-2.csv"):
        df_extras = pd.read_csv("taco-db-nutrientes-2.csv", on_bad_lines='skip', skipinitialspace=True)
        #junta as duas tabelas
        df_bruto = pd.merge(df_principais, df_extras, on='id')
    else:
        df_bruto = df_principais

    #limpeza de espaços em branco nas colunas
    df_bruto.columns = df_bruto.columns.str.strip()

    #dicionario das colunas
    mapeamento_colunas ={
        'Nome': 'Produto',
        'Energia (kcal)': 'Calorias (kcal)',
        'Carboidrato (g)': 'Carboidratos (g)',
        'Proteína (g)': 'Proteinas (g)',
        'Lipídeos (g)': 'Gorduras (g)' 
    }

    colunas = ['Nome', 'Energia (kcal)', 'Carboidrato (g)', 'Proteína (g)', 'Lipídeos (g)']
    df_configurado = df_bruto[colunas].rename(columns=mapeamento_colunas)

    #Segurança contra textos (Tr,*), nas colunas nutricionais
    colunas_numericas = ['Calorias (kcal)', 'Carboidratos (g)', 'Proteinas (g)', 'Gorduras (g)']
    for col in colunas_numericas:
        df_configurado[col] = pd.to_numeric(df_configurado[col], errors='coerce').fillna(0.0)

    df_configurado['Produto'] = df_configurado['Produto'].str.strip().str.capitalize()
    df_configurado['Categoria'] = 'Alimentos'

    #engenharia dos alergenos
    df_configurado['Gluten'] = df_configurado['Produto'].str.contains('pão|trigo|farinha de trigo|macarrão|massa|biscoito|aveia|centeio|cevada', case=False, na=False)
    df_configurado['Lactose'] = df_configurado['Produto'].str.contains('queijo|leite|iogurte|creme de leite|manteiga|requeijão|soro|coalhada', case=False, na=False)

    #ordem alfabetica
    df_configurado = df_configurado.sort_values(by='Produto', ascending=True)

    return df_configurado