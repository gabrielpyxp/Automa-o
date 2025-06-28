import pandas as pd
import sqlite3
import re

def clean_sla(value):
    """Converte valores de SLA para números"""
    try:
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        # Remove % e converte vírgula para ponto
        cleaned = re.sub(r'[^\d.,-]', '', str(value))
        cleaned = cleaned.replace(',', '.')
        return float(cleaned)
    except:
        return None

def main():
    df = pd.read_excel('downloads/resultado.xlsx')
    
    # Selecionar e renomear colunas
    df = df.rename(columns={
        'Cliente': 'NomeCliente',
        'SLA': 'SLA',
        'Abertura': 'Abertura'
    })[['ID', 'NomeCliente', 'SLA', 'Abertura']]
    
    # Converter dados
    df['SLA'] = df['SLA'].apply(clean_sla)
    df['Abertura'] = pd.to_datetime(df['Abertura']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df.dropna()
    
    # Salvar no banco
    conn = sqlite3.connect('relatorios.db')
    df.to_sql('relatorios', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"✅ Dados importados: {len(df)} registros")

if __name__ == '__main__':
    main()