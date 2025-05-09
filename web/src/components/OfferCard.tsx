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
    external_id
  } = offer;

  // Trunca o título se for muito longo
  const truncatedTitle = title.length > 70
    ? `${title.substring(0, 70)}...`
    : title;

  // Determina a classe de badge baseada no desconto
  let discountBadgeClass = 'bg-discount-low';
  if (discount_pct >= 30) discountBadgeClass = 'bg-discount-medium';
  if (discount_pct >= 50) discountBadgeClass = 'bg-discount-high';

  // Logo do merchant
  const merchantLogos: Record<string, string> = {
    amazon: '/merchants/amazon.svg',
    mercadolivre: '/merchants/ml.svg',
    aliexpress: '/merchants/aliexpress.svg',
    default: '/merchants/default.svg',
  };

  const logoSrc = merchantLogos[merchant] || merchantLogos.default;

  // Gera uma URL para a imagem do produto com base no título ou ID
  const getProductImage = () => {
    if (merchant === 'amazon' && external_id) {
      // Usa a API de imagens da Amazon
      return `https://images-na.ssl-images-amazon.com/images/P/${external_id}.jpg`;
    }
    
    // Caso não tenha ASIN válido, usa imagens baseadas no título do produto
    const lowerTitle = title.toLowerCase();
    
    if (lowerTitle.includes('smartphone') || lowerTitle.includes('galaxy') || lowerTitle.includes('iphone')) {
      return "https://m.media-amazon.com/images/I/61L1ItFgFHL.jpg";
    } 
    else if (lowerTitle.includes('notebook') || lowerTitle.includes('laptop')) {
      return "https://m.media-amazon.com/images/I/61onAgKP5gL.jpg";
    }
    else if (lowerTitle.includes('smart tv') || lowerTitle.includes('television')) {
      return "https://m.media-amazon.com/images/I/71LJJrKbezL.jpg";
    }
    else if (lowerTitle.includes('echo') || lowerTitle.includes('alexa')) {
      return "https://m.media-amazon.com/images/I/51MzOv8LuOL.jpg";
    }
    else if (lowerTitle.includes('kindle')) {
      return "https://m.media-amazon.com/images/I/71cWMiouRQL.jpg";
    }
    else if (lowerTitle.includes('headset') || lowerTitle.includes('fone')) {
      return "https://m.media-amazon.com/images/I/61CGHv6kmWL.jpg";
    }
    else if (lowerTitle.includes('playstation') || lowerTitle.includes('console')) {
      return "https://m.media-amazon.com/images/I/51051FiD9UL.jpg";
    }
    else if (lowerTitle.includes('airpods') || lowerTitle.includes('apple')) {
      return "https://m.media-amazon.com/images/I/61SUj2aKoEL.jpg";
    }
    else if (lowerTitle.includes('smartwatch') || lowerTitle.includes('watch')) {
      return "https://m.media-amazon.com/images/I/61Nhi2nJGWL.jpg";
    }
    else if (lowerTitle.includes('tablet')) {
      return "https://m.media-amazon.com/images/I/815a+XjrgRL.jpg";
    }
    else if (lowerTitle.includes('rtx') || lowerTitle.includes('placa de vídeo')) {
      return "https://m.media-amazon.com/images/I/51N6iZZOZmL.jpg";
    }
    else if (lowerTitle.includes('aspirador') || lowerTitle.includes('robot vacuum')) {
      return "https://m.media-amazon.com/images/I/71VbHaAqbML.jpg";
    }
    
    // Fallback para outros produtos
    return "https://via.placeholder.com/300x200?text=Produto";
  };

  const productImage = getProductImage();

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {/* Badge de desconto */}
      <div className={`absolute top-2 right-2 ${discountBadgeClass} text-white text-xs font-bold rounded-full px-2 py-1 z-10`}>
        {discount_pct}% OFF
      </div>

      {/* Imagem do produto */}
      <div className="h-48 bg-gray-200 relative">
        <img
          src={productImage}
          alt={truncatedTitle}
          className="w-full h-full object-contain p-2"
          onError={(e) => {
            // Fallback para imagem padrão em caso de erro
            (e.target as HTMLImageElement).src = "https://via.placeholder.com/300x200?text=Produto";
          }}
        />

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
            onClick={() => {
              console.log(`Clique em oferta: ${id} - ${title.substring(0, 30)}...`);
            }}
          >
            Ver Oferta
          </a>
        </div>
      </div>
    </div>
  );
};

export default OfferCard; 