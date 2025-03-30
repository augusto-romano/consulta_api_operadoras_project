from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from unidecode import unidecode
import numpy as np

app = Flask(__name__)
CORS(app)

# Carregar os dados
df = pd.read_csv('data/Relatorio_cadop.csv', delimiter=';', encoding='UTF-8')


def clean_data(df):
    # Normalizar textos
    text_columns = ['Razao_Social', 'Nome_Fantasia', 'Cidade', 'Logradouro', 'Bairro']
    for col in text_columns:
        df[col] = df[col].apply(lambda x: unidecode(str(x)) if pd.notna(x) else x)
    
    # Tratar valores NaN
    df = df.replace({np.nan: None})
    
    # Converter CNPJ para string
    df['CNPJ'] = df['CNPJ'].astype(str)
    
    return df

df = clean_data(df)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        query_normalized = unidecode(query.lower())
        
        # Busca na Razão Social e no Nome Fantasia
        mask = (
            df['Razao_Social'].str.contains(query_normalized, case=False, na=False) | 
            df['Nome_Fantasia'].str.contains(query_normalized, case=False, na=False)
        )
        
        result = df[mask]
        
        if result.empty:
            return jsonify({
                "success": True,
                "message": "Nenhuma empresa encontrada",
                "results": []
            })
        
        # Ordenar por Razão Social
        result = result.sort_values('Razao_Social')
        
        # Converter para dicionário
        results_data = result.to_dict(orient='records')
        
        return jsonify({
            "success": True,
            "message": f"Encontradas {len(results_data)} empresas",
            "results": results_data
        })
        
    except Exception as e:
        app.logger.error(f"Erro na busca: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Ocorreu um erro ao processar sua solicitação"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)