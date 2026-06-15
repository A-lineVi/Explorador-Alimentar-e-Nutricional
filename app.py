import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from leitura import leitura_dados_taco

#configuração da pagina
st.set_page_config(page_title= "Explorador de Nutrição Global", layout="wide")

# Função de filtragem
def renderizar_filtros(df):
    st.sidebar.header("Filtros Avançados")

    #Filtro por categoria 
    termo_busca = st.sidebar.text_input("Buscar Alimento (ex: pão, arroz, feijão):", "")
    categoria = st.sidebar.multiselect("Categorias", options=df['Categoria'].unique(), default=df['Categoria'].unique())

    #filtro de restrição Alimentar
    st.sidebar.subheader("Restrições Alimentares")
    sem_gluten = st.sidebar.checkbox("Sem Glúten")
    sem_lactose = st.sidebar.checkbox("Sem Lactose")
    
    #filtro personalizado de restrição
    st.sidebar.write('---')
    st.sidebar.subheader("Excluir Ingredientes/Alergênio")
    excluir_termo = st.sidebar.text_input("Excluir derivados de (ex: suíno, amendoim, castanhas):", "")
    
    #Aplicando filtro de logica de filtragem
    df_filtrado = df[df['Categoria'].isin(categoria)]
    
    #Aplicando Termo de Busca
    if termo_busca:
        termo_final = termo_busca.lower().strip()
        df_filtrado = df_filtrado[df_filtrado['Produto'].str.contains(termo_final, case=False, na=False)]
        
    #aplicando filtro de restrição
    if sem_gluten:
        df_filtrado = df_filtrado[df_filtrado['Gluten']== False]
    if sem_lactose:
        df_filtrado = df_filtrado[df_filtrado['Lactose']== False]
    #aplicando filtro personalizado
    if excluir_termo:
        termo_excluir_final = excluir_termo.lower().strip()
        df_filtrado = df_filtrado[~df_filtrado['Produto'].str.contains(termo_excluir_final, case=False, na=False)]
    
    return df_filtrado, excluir_termo

#função de visualização
def grafico_macronutrientes(df_filtrado):
    st.subheader("Comparativo de Macronutrientes (por 100g)")

    if df_filtrado.empty:
        st.warning("Nenhum dado dispinível com os filtros selecionados")
        return
    
    cor_texto = '#e0e0e0'
    cor_borda = '#424242'

    fig, ax = plt.subplots(figsize=(10,6))
    
    #Transparencia do fundo do grafico
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    #Gerar grafico de barras
    df_plot = df_filtrado.head(10).set_index ('Produto')[['Carboidratos (g)', 'Proteinas (g)', 'Gorduras (g)']]
    df_plot.plot(kind='bar', ax=ax, color=['#ffd166', '#06d6a0', '#ef476f'])

    ax.set_xlabel('Produto', color=cor_texto, fontsize=11)
    ax.set_ylabel('Gramas (g)', color=cor_texto, fontsize=11)

    ax.tick_params(axis='x', colors=cor_texto, labelsize=10)
    ax.tick_params(axis='y', colors=cor_texto, labelsize=10)

    plt.xticks(rotation=35, ha='right')

    #costomização de linhas e borda do gráfico:
    for spine in ax.spines.values():
        spine.set_color(cor_borda)
    
    #costomização da legenda
    legenda = ax.legend(facecolor='none', edgecolor=cor_borda)
    for text in legenda.get_texts():
        text.set_color(cor_texto)

    plt.tight_layout()

    st.pyplot(fig, clear_figure=True)

#Função do Simulador (calcula um conjunto de alimentos)
def simulador_nutricional(df):
    st.write("---")
    st.header("Simulador de Refeições Diárias")
    st.write("Adicione alimentos ao seu dia a dia para recalcular o impacto nutricional total.")

    if 'diario_alimentar' not in st.session_state:
        st.session_state.diario_alimentar =[]
    
    col_add, col_resumo = st.columns([1, 1])

    with col_add:
        st.subheader("Adicionar Alimento")
        alimentos_disponiveis = df['Produto'].unique()
        alimentos_selecionados = st.selectbox("Selecione o Alimento:", options=alimentos_disponiveis)
        quantidade = st.number_input("Quantidade consumida (em gramas):", min_value=1, value=100, step=10)

        if st.button("Adicionar Refeição"):
            dados_alimento = df[df['Produto'] == alimentos_selecionados].iloc[0]
            fator = quantidade / 100.0

            item_refeicao ={
                'Produto': alimentos_selecionados,
                'Quantidade': quantidade,
                'Calorias': float(dados_alimento['Calorias (kcal)']) * fator,
                'Carboidratos': float(dados_alimento['Carboidratos (g)']) * fator,
                'Proteinas': float(dados_alimento['Proteinas (g)']) * fator,
                'Gorduras': float(dados_alimento['Gorduras (g)']) * fator
            }

            st.session_state.diario_alimentar.append(item_refeicao)
            st.success(f"{quantidade}g, de {alimentos_selecionados}, adicionados com sucesso!")
        
        if st.session_state.diario_alimentar:
            if st.button("Limpar Tudo"):
                st.session_state.diario_alimentar = []
                st.rerun()
    with col_resumo:
        st.subheader("Resumo do Dia")

        if not st.session_state.diario_alimentar:
            st.info("O seu prato esta vazio. Adicione alimentos para começar!")
        else:
            df_diario = pd.DataFrame(st.session_state.diario_alimentar)
            st.dataframe(df_diario[['Produto', 'Quantidade', 'Calorias']], width='stretch')

            total_cal = df_diario['Calorias'].sum()
            total_carbo = df_diario['Carboidratos'].sum()
            total_protein = df_diario['Proteinas'].sum()
            total_gord = df_diario['Gorduras'].sum()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric('Calorias', f"{total_cal:.1f} kcal")
            m2.metric('Carboidratos', f"{total_carbo:.1f}g")
            m3.metric("Proteínas", f"{total_protein:.1f}g")
            m4.metric("Gordura", f"{total_gord:.1f}g")

#Monitor Principal (execução)
def main():
    st.title("Exploração Alimentar e Nutricional")
    st.write("Explore dados nutricionais, filtre por alérgenos e simule o impacto das suas refeições diárias.")

    #carrega base de dados
    df_original = leitura_dados_taco()

    #aplica filtros via sidebar
    df_filtrado, excluir_termo = renderizar_filtros(df_original)

    #Layout em colunas
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("Alimentos Selecionados")

        #Mostra o filtro de exclusão personalizado, se houver
        if excluir_termo:
            st.info(f"Alimentos contendo {excluir_termo}, foram ocultados da lista.")

        st.dataframe(df_filtrado[['Produto', 'Categoria']], width='stretch')

    with col2:
        st.subheader("Resumo da Seleção")
        st.metric("Total de itens", len(df_filtrado))
    
    st.write("---")

    grafico_macronutrientes(df_filtrado)
    
    simulador_nutricional(df_original)

if __name__ == "__main__":
    main()