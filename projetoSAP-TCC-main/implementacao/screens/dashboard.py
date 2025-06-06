import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

def dashboard():
    
    col1, col2 = st.columns([1, 4])
    with col1:
        logo_path = Path(__file__).parent.parent / "assets" / "SAPlogoDashboard.png"
        st.image(str(logo_path), width=100) 
    with col2:
        st.title("Dashboard - Visão Geral")

    st.sidebar.header("Filtros")
    data_inicio = st.sidebar.date_input("Data Início", value=pd.to_datetime("2025-01-01"))
    data_fim = st.sidebar.date_input("Data Fim", value=pd.to_datetime("2025-04-10"))

    # Dados simulados
    np.random.seed(42)
    dados = pd.DataFrame({
        "data": pd.date_range("2025-01-01", periods=100),
        "vendas": np.random.randint(20, 100, 100),
        "clientes": np.random.randint(5, 20, 100),
        "lucro": np.random.uniform(1000, 5000, 100)
    })

    dados_filtrados = dados[(dados["data"] >= pd.to_datetime(data_inicio)) & (dados["data"] <= pd.to_datetime(data_fim))].copy()

    st.subheader("Indicadores Principais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas Totais", int(dados_filtrados["vendas"].sum()))
    col2.metric("Clientes Atendidos", int(dados_filtrados["clientes"].sum()))
    col3.metric("Lucro Médio", f"R$ {dados_filtrados['lucro'].mean():.2f}")

    st.markdown("---")

    st.subheader("Visualização dos Dados")
    escolha_grafico = st.selectbox("Escolha o tipo de gráfico", ["Linha", "Barra", "Pizza"])

    if escolha_grafico == "Linha":
        fig_vendas = px.line(dados_filtrados, x="data", y="vendas", title="Vendas diárias", markers=True)
        st.plotly_chart(fig_vendas, use_container_width=True)

        fig_clientes = px.line(dados_filtrados, x="data", y="clientes", title="Clientes por dia", markers=True)
        st.plotly_chart(fig_clientes, use_container_width=True)

        fig_lucro = px.line(dados_filtrados, x="data", y="lucro", title="Lucro diário", markers=True)
        st.plotly_chart(fig_lucro, use_container_width=True)

    elif escolha_grafico == "Barra":
        fig_vendas = px.bar(dados_filtrados, x="data", y="vendas", title="Vendas diárias")
        st.plotly_chart(fig_vendas, use_container_width=True)

        fig_clientes = px.bar(dados_filtrados, x="data", y="clientes", title="Clientes por dia")
        st.plotly_chart(fig_clientes, use_container_width=True)

        fig_lucro = px.bar(dados_filtrados, x="data", y="lucro", title="Lucro diário")
        st.plotly_chart(fig_lucro, use_container_width=True)

    else:   
        df_pizza = dados_filtrados.copy()
        df_pizza['mes'] = df_pizza['data'].dt.to_period('M').astype(str)

        fig_vendas = px.pie(df_pizza.groupby('mes')['vendas'].sum().reset_index(),
                            names='mes', values='vendas', title="Vendas por mês")
        st.plotly_chart(fig_vendas, use_container_width=True)

        fig_clientes = px.pie(df_pizza.groupby('mes')['clientes'].sum().reset_index(),
                             names='mes', values='clientes', title="Clientes por mês")
        st.plotly_chart(fig_clientes, use_container_width=True)

        fig_lucro = px.pie(df_pizza.groupby('mes')['lucro'].sum().reset_index(),
                          names='mes', values='lucro', title="Lucro por mês")
        st.plotly_chart(fig_lucro, use_container_width=True)

    st.markdown("---")

    if st.button("Logout"):
        for key in ['logado', 'usuario', 'tipo_usuario', 'tela']:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

if __name__ == "__main__":
    dashboard()
