import React from 'react';
import { Offer } from '../lib/useOffers';

interface OfferCardProps {
  offer: Offer;
}

const formatPrice = (price: number): string => {
  return price.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  });
};

const OfferCard: React.FC<OfferCardProps> = ({ offer }) => {
  const {
    id,
    title,
    merchant,
    price,
    discount_pct,
    url,
  } = offer;

  // Trunca o título se for muito longo
  const truncatedTitle = title.length > 70
    ? `${title.substring(0, 70)}...`
    : title;

  // Determina a classe de badge baseada no desconto
  let discountBadgeClass = 'bg-green-500';
  if (discount_pct >= 30) discountBadgeClass = 'bg-orange-500';
  if (discount_pct >= 50) discountBadgeClass = 'bg-red-500';

  // Logo do merchant
  const merchantLogos: Record<string, string> = {
    amazon: '/merchants/amazon.svg',
    mercadolivre: '/merchants/ml.svg',
    aliexpress: '/merchants/aliexpress.svg',
    default: '/merchants/default.svg',
  };

  const logoSrc = merchantLogos[merchant] || merchantLogos.default;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {/* Badge de desconto */}
      <div className={`absolute top-2 right-2 ${discountBadgeClass} text-white text-xs font-bold rounded-full px-2 py-1`}>
        {discount_pct}% OFF
      </div>

      {/* Imagem do produto (mock por enquanto) */}
      <div className="h-48 bg-gray-200 relative">
        {/* TODO: Substituir pelo componente de imagem real quando disponível */}
        <div className="w-full h-full flex items-center justify-center text-gray-400">
          Imagem do Produto
        </div>

        {/* Logo do merchant */}
        <div className="absolute bottom-2 left-2 bg-white rounded-full p-1 h-8 w-8 flex items-center justify-center">
          <img src={logoSrc} alt={merchant} className="h-6 w-6" />
        </div>
      </div>

      {/* Conteúdo do card */}
      <div className="p-4">
        <h3 className="text-sm font-medium text-gray-700 h-12 line-clamp-2" title={title}>
          {truncatedTitle}
        </h3>

        <div className="mt-2 flex justify-between items-end">
          <div>
            <span className="text-lg font-bold text-primary">{formatPrice(price)}</span>
          </div>
          
          <a
            href={`/api/go/${id}`}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-primary hover:bg-primary-dark text-white px-3 py-1 rounded text-sm transition-colors"
          >
            Ver Oferta
          </a>
        </div>
      </div>
    </div>
  );
};

export default OfferCard; 