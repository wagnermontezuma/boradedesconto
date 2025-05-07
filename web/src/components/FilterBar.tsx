import React from 'react';
import { OfferFilters } from '../lib/useOffers';

interface FilterBarProps {
  filters: OfferFilters;
  onFilterChange: (filters: OfferFilters) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ filters, onFilterChange }) => {
  const handleMerchantChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      merchant: value === 'all' ? undefined : value,
    });
  };

  const handleDiscountChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = parseInt(e.target.value, 10);
    onFilterChange({
      ...filters,
      min_discount: value,
    });
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <h2 className="text-lg font-bold text-gray-800">Filtrar Ofertas</h2>
        
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
              <option value="50">50% ou mais</option>
              <option value="70">70% ou mais</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterBar; 