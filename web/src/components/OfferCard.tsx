import React from 'react';
import Image from 'next/image';
import { Offer } from '../lib/useOffers';
import ImageWithFallback from './ImageWithFallback';

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

  const logoSrc = merchantLogos[merchant.toLowerCase()] || merchantLogos.default;

  // Gera uma URL para a imagem do produto com base no título ou ID
  const getProductImage = () => {
    if (merchant === 'amazon' && external_id) {
      // Amazon usa vários formatos de imagem, alguns têm mudado com o tempo
      // Tentamos o formato mais recente primeiro
      return `https://m.media-amazon.com/images/I/${external_id}.jpg`;
    }
    
    // Caso não tenha ASIN válido ou tenha dado erro, usa imagens baseadas no título do produto
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
  const fallbackImage = "https://via.placeholder.com/300x200?text=Produto";

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {/* Badge de desconto */}
      <div className={`absolute top-2 right-2 ${discountBadgeClass} text-white text-xs font-bold rounded-full px-2 py-1 z-10`}>
        {discount_pct}% OFF
      </div>

      {/* Imagem do produto */}
      <div className="h-48 bg-gray-200 relative">
        <div className="w-full h-full relative">
          <ImageWithFallback
            src={productImage}
            fallbackSrc={fallbackImage}
            alt={truncatedTitle}
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            className="object-contain p-2"
          />
        </div>

        {/* Logo do merchant */}
        <div className="absolute bottom-2 left-2 bg-white rounded-full p-1 h-8 w-8 flex items-center justify-center">
          <Image
            src={logoSrc}
            alt={merchant}
            width={24}
            height={24}
            className="h-6 w-6"
          />
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