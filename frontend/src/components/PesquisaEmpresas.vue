<template>
    <div class="container">
      <h1 class="title">Procurar Operadoras</h1>
      
      <div class="search-box">
        <input 
          type="text" 
          v-model="query" 
          placeholder="Digite o nome da operadora" 
          class="search-input"
          @keyup.enter="fetchCompanies"
        />
        <button @click="fetchCompanies" class="search-button">
          <span v-if="!loading">Buscar</span>
          <span v-else class="spinner"></span>
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>
      
      <div v-if="companies.length > 0" class="results-container">
        <div class="results-header">
          <h2>Resultados ({{ companies.length }})</h2>
          <div class="results-filter">
            <input 
              type="text" 
              v-model="tableFilter" 
              placeholder="Filtrar resultados..." 
              class="filter-input"
            />
          </div>
        </div>
        
        <div class="table-responsive">
          <table class="results-table">
            <thead>
              <tr>
                <th @click="sortBy('Razao_Social')">Razão Social</th>
                <th @click="sortBy('Nome_Fantasia')">Nome Fantasia</th>
                <th @click="sortBy('Registro_ANS')">Registro ANS</th>
                <th @click="sortBy('CNPJ')">CNPJ</th>
                <th>Detalhes</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="company in filteredCompanies" :key="company.Registro_ANS">
                <td>{{ company.Razao_Social }}</td>
                <td>{{ company.Nome_Fantasia || '-' }}</td>
                <td>{{ company.Registro_ANS }}</td>
                <td>{{ formatCNPJ(company.CNPJ) }}</td>
                <td>
                  <button @click="showDetails(company)" class="details-button">
                    Ver detalhes
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div v-else-if="query && !loading" class="no-results">
        <p>Nenhuma operadora encontrada para "{{ query }}"</p>
      </div>
      
      <!-- Modal de detalhes -->
      <div v-if="selectedCompany" class="modal-overlay" @click.self="selectedCompany = null">
        <div class="modal-content">
          <button class="modal-close" @click="selectedCompany = null">&times;</button>
          <h2>{{ selectedCompany.Razao_Social }}</h2>
          
          <div class="company-details">
            <div class="detail-row">
              <span class="detail-label">Nome Fantasia:</span>
              <span>{{ selectedCompany.Nome_Fantasia || '-' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Registro ANS:</span>
              <span>{{ selectedCompany.Registro_ANS }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">CNPJ:</span>
              <span>{{ formatCNPJ(selectedCompany.CNPJ) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Modalidade:</span>
              <span>{{ selectedCompany.Modalidade }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Endereço:</span>
              <span>
                {{ selectedCompany.Logradouro }}, {{ selectedCompany.Numero }}<br>
                {{ selectedCompany.Bairro }}<br>
                {{ selectedCompany.Cidade }}/{{ selectedCompany.UF }}<br>
                CEP: {{ formatCEP(selectedCompany.CEP) }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Contato:</span>
              <span>
                Telefone: {{ formatPhone(selectedCompany.Telefone) }}<br>
                Fax: {{ formatPhone(selectedCompany.Fax) }}<br>
                Email: {{ selectedCompany.Endereco_eletronico || '-' }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Representante:</span>
              <span>
                {{ selectedCompany.Representante }}<br>
                Cargo: {{ selectedCompany.Cargo_Representante }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Data de Registro:</span>
              <span>{{ selectedCompany.Data_Registro_ANS }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        query: '',
        companies: [],
        loading: false,
        error: null,
        tableFilter: '',
        selectedCompany: null,
        sortField: 'Razao_Social',
        sortDirection: 'asc'
      };
    },
    computed: {
      filteredCompanies() {
        let filtered = this.companies;
        
        if (this.tableFilter) {
          const filter = this.tableFilter.toLowerCase();
          filtered = filtered.filter(company => 
            company.Razao_Social.toLowerCase().includes(filter) ||
            (company.Nome_Fantasia && company.Nome_Fantasia.toLowerCase().includes(filter)) ||
            company.CNPJ.includes(filter)
          );
        }
        
        return filtered.sort((a, b) => {
          const fieldA = a[this.sortField] || '';
          const fieldB = b[this.sortField] || '';
          
          if (this.sortDirection === 'asc') {
            return fieldA.localeCompare(fieldB);
          } else {
            return fieldB.localeCompare(fieldA);
          }
        });
      }
    },
    methods: {
      async fetchCompanies() {
        if (!this.query.trim()) {
          this.error = "Por favor, digite um termo para busca";
          return;
        }
        
        this.loading = true;
        this.error = null;
        this.companies = [];
        
        try {
          const response = await axios.get('http://localhost:5000/search', {
            params: { query: this.query.trim() }
          });
          
          if (response.data.success) {
            this.companies = response.data.results;
            if (this.companies.length === 0) {
              this.error = "Nenhuma operadora encontrada com esse nome";
            }
          } else {
            this.error = response.data.message || 'Erro na busca';
          }
        } catch (err) {
          console.error('Erro ao buscar empresas:', err);
          this.error = err.response?.data?.error || 'Erro ao conectar com o servidor';
        } finally {
          this.loading = false;
        }
      },
      formatCNPJ(cnpj) {
        if (!cnpj) return '-';
        // Remove caracteres não numéricos
        const cleaned = cnpj.toString().replace(/\D/g, '');
        
        // Formatação do CNPJ: 00.000.000/0000-00
        return cleaned.replace(
          /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
          '$1.$2.$3/$4-$5'
        );
      },
      formatCEP(cep) {
        if (!cep) return '-';
        const cleaned = cep.toString().replace(/\D/g, '');
        return cleaned.replace(/^(\d{5})(\d{3})$/, '$1-$2');
      },
      formatPhone(phone) {
        if (!phone) return '-';
        const cleaned = phone.toString().replace(/\D/g, '');
        
        if (cleaned.length === 10) {
          return cleaned.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
        } else if (cleaned.length === 11) {
          return cleaned.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
        }
        
        return cleaned;
      },
      showDetails(company) {
        this.selectedCompany = company;
      },
      sortBy(field) {
        if (this.sortField === field) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortField = field;
          this.sortDirection = 'asc';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .title {
    text-align: center;
    color: #ffffff;
    margin-bottom: 30px;
  }
  
  .search-box {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
  
  .search-input {
    padding: 12px 15px;
    font-size: 16px;
    border: 1px solid #ffffff;
    border-radius: 4px;
    width: 400px;
    margin-right: 10px;
  }
  
  .search-button {
    padding: 12px 25px;
    background-color: #ff0000;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 100px;
  }
  
  .search-button:hover {
    background-color: #2980b9;
  }
  
  .spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .results-container {
    margin-top: 30px;
    background: rgb(0, 0, 0);
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 20px;
  }
  
  .results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .filter-input {
    padding: 8px 12px;
    border: 1px solid #554c4c;
    border-radius: 4px;
    width: 250px;
  }
  
  .table-responsive {
    overflow-x: auto;
  }
  
  .results-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .results-table th, .results-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ffffff;
  }
  
  .results-table th {
    background-color: #ff0000;
    font-weight: 600;
    cursor: pointer;
    position: relative;
  }
  
  .results-table th:hover {
    background-color: #e9ecef;
  }
  
  .results-table tr:hover {
    background-color: #353f3d;
  }
  
  .details-button {
    padding: 6px 12px;
    background-color: #3700ff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .details-button:hover {
    background-color: #000000;
  }
  
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: rgb(0, 0, 0);
    padding: 30px;
    border-radius: 8px;
    max-width: 800px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
  }
  
  .modal-close {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 24px;
    background: none;
    border: none;
    cursor: pointer;
    color: #7f8c8d;
  }
  
  .company-details {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 20px;
  }
  
  .detail-row {
    margin-bottom: 15px;
  }
  
  .detail-label {
    font-weight: 600;
    color: #ff0000;
    display: block;
    margin-bottom: 5px;
  }
  
  /* Responsividade */
  @media (max-width: 768px) {
    .search-box {
      flex-direction: column;
    }
    
    .search-input {
      width: 100%;
      margin-right: 0;
      margin-bottom: 10px;
    }
    
    .company-details {
      grid-template-columns: 1fr;
    }
    
    .results-header {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .filter-input {
      width: 100%;
      margin-top: 10px;
    }
  }
  
  .error-message {
    color: #e74c3c;
    background-color: #fadbd8;
    padding: 10px 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .no-results {
    text-align: center;
    padding: 20px;
    color: #7f8c8d;
    background-color: #f8f9fa;
    border-radius: 4px;
  }
  </style>