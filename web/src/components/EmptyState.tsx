import React from 'react';

interface EmptyStateProps {
  message?: string;
  suggestion?: string;
}

const EmptyState: React.FC<EmptyStateProps> = ({ 
  message = 'Nenhuma oferta encontrada.',
  suggestion = 'Tente ajustar os filtros ou verifique novamente mais tarde.'
}) => (
  <div className="flex flex-col items-center py-16 px-4 text-gray-500 bg-white rounded-lg shadow-sm">
    <svg xmlns="http://www.w3.org/2000/svg" className="h-20 w-20 mb-6 text-orange-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <p className="text-xl font-medium text-gray-700 mb-2">{message}</p>
    <p className="text-gray-500 mb-6 text-center">{suggestion}</p>
    <button 
      onClick={() => window.location.reload()}
      className="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-600 transition-colors"
    >
      Recarregar página
    </button>
  </div>
);

export default EmptyState; 