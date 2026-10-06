import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def executar_pipeline():
    df_transacoes = pd.read_csv('transacoes.csv', encoding='latin1')

    df_transacoes['valor'] = df_transacoes.groupby('estado_cliente')['valor'].transform(
        lambda x: x.fillna(x.median())
    )

    df_transacoes['plataforma'] = 'Mobile'

    df_transacoes['data_transacao'] = pd.to_datetime(df_transacoes['data_transacao'])
    df_transacoes['data_transacao'] = df_transacoes['data_transacao'].dt.tz_localize('America/Sao_Paulo')

    df_transacoes['dia_semana'] = df_transacoes['data_transacao'].dt.day_name()
    df_transacoes['mes'] = df_transacoes['data_transacao'].dt.month

    df_transacoes = df_transacoes.drop_duplicates(keep='first').reset_index(drop=True)

    filtro_setembro_sp_rj = (
        (df_transacoes['mes'] == 9) &
        ((df_transacoes['estado_cliente'] == 'SP') | (df_transacoes['estado_cliente'] == 'RJ')) &
        (df_transacoes['valor'] > 5000.00)
    )
    df_filtrado = df_transacoes[filtro_setembro_sp_rj].copy()
    
    print("--- Transações Filtradas (Setembro, SP/RJ, Valor > R$ 5.000,00) ---")
    print(df_filtrado.head(), "\n")

    risco_dict = {
        'C100': 'Baixo',
        'C101': 'Alto',
        'C102': 'Médio',
        'C103': 'Baixo',
        'C104': 'Alto'
    }

    df_transacoes['nivel_risco'] = df_transacoes['id_cliente'].map(risco_dict)

    tabela_dinamica = pd.pivot_table(
        df_transacoes,
        values='valor',
        index='mes',
        columns='nivel_risco',
        aggfunc='sum',
        margins=True,
        margins_name='Total'
    )
    
    print("--- Tabela Dinâmica (Soma do Valor por Mês e Risco) ---")
    print(tabela_dinamica, "\n")


    def calcular_zscore_por_estado(df):
        media_estado = df.groupby('estado_cliente')['valor'].transform('mean')
        std_estado = df.groupby('estado_cliente')['valor'].transform('std')
        return (df['valor'] - media_estado) / std_estado

    df_transacoes['z_score'] = calcular_zscore_por_estado(df_transacoes)

    df_anomalias = df_transacoes[df_transacoes['z_score'] > 2.5].copy()
    
    print(f"--- Detecção de Anomalias (Z-Score > 2.5): {len(df_anomalias)} encontradas ---")
    print(df_anomalias[['id_cliente', 'estado_cliente', 'valor', 'z_score']].head(), "\n")

    df_diario = df_transacoes.set_index('data_transacao').resample('D')['valor'].sum().reset_index()
    df_diario['media_móvel_7d'] = df_diario['valor'].rolling(window=7).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df_diario['data_transacao'], df_diario['valor'], label='Valor Total Diário', color='#1f77b4', linewidth=1.5)
    ax.plot(df_diario['data_transacao'], df_diario['media_móvel_7d'], label='Média Móvel (7 Dias)', color='#ff7f0e', linewidth=2.5, linestyle='--')

    ax.set_ylim(bottom=0)
    ax.set_title('Desempenho Diário de Transações e Média Móvel (7 Dias)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Data', fontsize=11)
    ax.set_ylabel('Valor Total (R$)', fontsize=11)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('relatorio_transacoes.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    executar_pipeline()