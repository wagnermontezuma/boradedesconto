import React from 'react';
import { OfferFilters } from '../lib/useOffers';

interface FilterBarProps {
  filters: OfferFilters;
  onFilterChange: (filters: OfferFilters) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ filters, onFilterChange }) => {
  // Handler melhorado para o filtro de loja
  const handleMerchantChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    console.log("Merchant selecionado:", value);
    
    // Atualiza o estado com o novo valor de merchant
    onFilterChange({
      ...filters,
      merchant: value === 'all' ? undefined : value,
    });
  };

  // Handler melhorado para o filtro de desconto
  const handleDiscountChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = parseInt(e.target.value, 10);
    console.log("Desconto mínimo selecionado:", value);
    
    // Atualiza o estado com o novo valor de min_discount
    onFilterChange({
      ...filters,
      min_discount: value,
    });
  };

  // Função para limpar todos os filtros
  const clearAllFilters = () => {
    console.log("Limpando todos os filtros");
    
    // Reseta todos os filtros para os valores padrão
    onFilterChange({
      merchant: undefined,
      min_discount: 0
    });
  };

  // Define se algum filtro está ativo
  const isFilterActive = filters.merchant !== undefined || (filters.min_discount !== undefined && filters.min_discount > 0);

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <div className="flex items-center">
          <h2 className="text-lg font-bold text-gray-800">Filtrar Ofertas</h2>
          {isFilterActive && (
            <button 
              onClick={clearAllFilters}
              className="ml-4 text-sm text-gray-500 hover:text-primary underline"
            >
              Limpar filtros
            </button>
          )}
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Filtro de loja */}
          <div className="min-w-[150px]">
            <label htmlFor="merchant" className="block text-sm font-medium text-gray-700 mb-1">
              Loja
            </label>
            <select
              id="merchant"
              className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50"
              value={filters.merchant || 'all'}
              onChange={handleMerchantChange}
            >
              <option value="all">Todas</option>
              <option value="amazon">Amazon</option>
              <option value="mercadolivre">Mercado Livre</option>
              <option value="aliexpress">AliExpress</option>
            </select>
          </div>

          {/* Filtro de desconto mínimo */}
          <div className="min-w-[150px]">
            <label htmlFor="min-discount" className="block text-sm font-medium text-gray-700 mb-1">
              Desconto Mínimo
            </label>
            <select
              id="min-discount"
              className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50"
              value={filters.min_discount || 0}
              onChange={handleDiscountChange}
            >
              <option value="0">Qualquer</option>
              <option value="10">10% ou mais</option>
              <option value="20">20% ou mais</option>
              <option value="30">30% ou mais</option>
              <option value="40">40% ou mais</option>
              <option value="50">50% ou mais</option>
              <option value="60">60% ou mais</option>
            </select>
          </div>
        </div>
      </div>

      {/* Indicador de filtros ativos */}
      {isFilterActive && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="flex flex-wrap gap-2">
            {filters.merchant && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Loja: {filters.merchant === 'amazon' ? 'Amazon' : 
                       filters.merchant === 'mercadolivre' ? 'Mercado Livre' : 
                       filters.merchant === 'aliexpress' ? 'AliExpress' : filters.merchant}
                <button 
                  onClick={() => onFilterChange({...filters, merchant: undefined})}
                  className="ml-1.5 text-blue-500 hover:text-blue-800"
                >
                  ✕
                </button>
              </span>
            )}
            {filters.min_discount !== undefined && filters.min_discount > 0 && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Desconto: {filters.min_discount}% ou mais
                <button 
                  onClick={() => onFilterChange({...filters, min_discount: 0})}
                  className="ml-1.5 text-green-500 hover:text-green-800"
                >
                  ✕
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterBar; 