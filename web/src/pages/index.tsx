import React, { useState } from 'react';
import Head from 'next/head';
import OfferCard from '../components/OfferCard';
import FilterBar from '../components/FilterBar';
import { Offer, OfferFilters, useOffers } from '../lib/useOffers';

// Dados da API substituirão isso, mantendo para fallback
const MOCK_OFFERS: Offer[] = [
  {
    id: 1,
    merchant: 'amazon',
    external_id: 'B08X7JX9MB',
    title: 'Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto',
    url: 'https://www.amazon.com.br/dp/B08X7JX9MB',
    price: 1899.99,
    discount_pct: 25,
    ts: '2023-06-01T10:00:00Z'
  },
  {
    id: 2,
    merchant: 'amazon',
    external_id: 'B09V3YW11L',
    title: 'Aspirador de Pó Robô Xiaomi Robot Vacuum-Mop 2',
    url: 'https://www.amazon.com.br/dp/B09V3YW11L',
    price: 1499.99,
    discount_pct: 35,
    ts: '2023-06-01T09:45:00Z'
  },
  {
    id: 3,
    merchant: 'mercadolivre',
    external_id: 'MLB2163772914',
    title: 'Smart TV Samsung 50" Crystal UHD 4K BU8000 2022',
    url: 'https://www.mercadolivre.com.br/p/MLB2163772914',
    price: 2399.99,
    discount_pct: 40,
    ts: '2023-06-01T09:30:00Z'
  },
  {
    id: 4,
    merchant: 'mercadolivre',
    external_id: 'MLB2789425378',
    title: 'Notebook Dell Inspiron 15 3000 Intel Core i5 8GB RAM 256GB SSD',
    url: 'https://www.mercadolivre.com.br/p/MLB2789425378',
    price: 3299.99,
    discount_pct: 15,
    ts: '2023-06-01T09:15:00Z'
  },
  {
    id: 5,
    merchant: 'aliexpress',
    external_id: '1005004563781452',
    title: 'Fones de ouvido sem fio TWS Bluetooth 5.3',
    url: 'https://www.aliexpress.com/item/1005004563781452.html',
    price: 89.99,
    discount_pct: 60,
    ts: '2023-06-01T09:00:00Z'
  },
  {
    id: 6,
    merchant: 'amazon',
    external_id: 'B08JCRL4T5',
    title: 'Echo Dot 4ª Geração Smart Speaker com Alexa',
    url: 'https://www.amazon.com.br/dp/B08JCRL4T5',
    price: 299.99,
    discount_pct: 45,
    ts: '2023-06-01T08:45:00Z'
  }
];

export default function Home() {
  const [filters, setFilters] = useState<OfferFilters>({
    merchant: undefined,
    min_discount: 0
  });

  // Usar a API real em vez de dados mockados
  const { offers, isLoading, isError } = useOffers(filters);
  
  // Fallback para dados mockados em caso de erro ou ambiente de desenvolvimento sem API
  const displayOffers = isError || offers.length === 0 ? MOCK_OFFERS : offers;
  
  // Aplica os filtros apenas se estivermos usando dados mockados
  const filteredOffers = isError || offers.length === 0 
    ? MOCK_OFFERS.filter(offer => {
        // Filtro de merchant
        if (filters.merchant && offer.merchant !== filters.merchant) {
          return false;
        }
        
        // Filtro de desconto mínimo
        if (filters.min_discount && offer.discount_pct < filters.min_discount) {
          return false;
        }
        
        return true;
      })
    : offers; // Se estiver usando API, ela já retorna filtrado

  return (
    <>
      <Head>
        <title>BoraDeDesconto - Ofertas em tempo quase-real</title>
        <meta name="description" content="Agregador de ofertas dos principais e-commerces em tempo quase-real" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gray-100">
        {/* Cabeçalho */}
        <header className="bg-primary py-6">
          <div className="container mx-auto px-4">
            <h1 className="text-3xl font-bold text-white">BoraDeDesconto</h1>
            <p className="text-white opacity-90">Ofertas em tempo quase-real dos principais e-commerces</p>
          </div>
        </header>

        {/* Conteúdo principal */}
        <div className="container mx-auto px-4 py-8">
          {/* Filtros */}
          <FilterBar 
            filters={filters} 
            onFilterChange={setFilters} 
          />

          {/* Estado de carregamento */}
          {isLoading && (
            <div className="text-center py-10">
              <p className="text-gray-500 text-lg">Carregando ofertas...</p>
            </div>
          )}

          {/* Estado de erro */}
          {isError && (
            <div className="text-center py-10">
              <p className="text-red-500 text-lg">Erro ao carregar ofertas. Mostrando dados de exemplo.</p>
            </div>
          )}

          {/* Grid de ofertas */}
          {!isLoading && filteredOffers.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {filteredOffers.map(offer => (
                <OfferCard key={`${offer.merchant}-${offer.external_id}`} offer={offer} />
              ))}
            </div>
          ) : !isLoading && (
            <div className="text-center py-10">
              <p className="text-gray-500 text-lg">Nenhuma oferta encontrada com os filtros selecionados.</p>
            </div>
          )}
        </div>

        {/* Rodapé */}
        <footer className="bg-gray-800 text-white py-6">
          <div className="container mx-auto px-4 text-center">
            <p>© 2024 BoraDeDesconto - Versão MVP</p>
            <p className="text-sm opacity-70 mt-2">
              BoraDeDesconto não é afiliado a nenhuma das lojas mencionadas.
              Preços e disponibilidade podem mudar sem aviso prévio.
            </p>
          </div>
        </footer>
      </main>
    </>
  );
} 