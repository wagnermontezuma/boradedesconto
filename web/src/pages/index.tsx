import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import OfferCard from '../components/OfferCard';
import FilterBar from '../components/FilterBar';
import { Offer, OfferFilters, useOffers } from '../lib/useOffers';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';

export default function Home() {
  // Estado para controlar os filtros
  const [filters, setFilters] = useState<OfferFilters>({
    merchant: undefined,
    min_discount: 0
  });

  // Usar o hook que sempre retornará dados mockados como fallback
  const { offers, isLoading, isError } = useOffers(filters);

  // Estado para controlar se já carregou a primeira vez
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  // Após o primeiro carregamento, marca como carregado
  useEffect(() => {
    if (!isLoading && isInitialLoad) {
      setIsInitialLoad(false);
    }
  }, [isLoading, isInitialLoad]);

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
        <header className="bg-orange-500 py-6 shadow-md relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold text-white">BoraDeDesconto</h1>
                <p className="text-white opacity-90">Ofertas em tempo quase-real dos principais e-commerces</p>
              </div>
              <div className="flex items-center space-x-4">
                <div className="hidden md:block bg-white text-orange-600 font-bold text-xl px-4 py-2 rounded-lg transform rotate-3 shadow-lg">
                  Até 60% OFF
                </div>
                <a 
                  href="/stats" 
                  className="bg-orange-600 text-white hover:bg-orange-700 transition-colors px-4 py-2 rounded-lg shadow text-sm md:text-base"
                >
                  Estatísticas
                </a>
              </div>
            </div>
          </div>
          {/* Elementos decorativos */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-orange-400 rounded-full transform translate-x-1/2 -translate-y-1/2 opacity-50"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-orange-400 rounded-full transform -translate-x-1/3 translate-y-1/3 opacity-30"></div>
        </header>

        {/* Conteúdo principal */}
        <div className="container mx-auto px-4 py-8">
          {/* Filtros */}
          <FilterBar 
            filters={filters} 
            onFilterChange={setFilters} 
          />

          {/* Estado de carregamento inicial */}
          {isInitialLoad && isLoading && (
            <div className="py-20">
              <LoadingSpinner />
            </div>
          )}

          {/* Estado de erro */}
          {isError && (
            <div className="text-center py-8 mb-8">
              <div className="inline-block bg-red-50 text-red-500 px-6 py-4 rounded-lg border border-red-200">
                <p className="text-lg">Erro ao carregar ofertas. Mostrando dados de exemplo.</p>
              </div>
            </div>
          )}

          {/* Grid de ofertas */}
          {(!isLoading || !isInitialLoad) && offers.length > 0 ? (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {offers.map((offer: Offer) => (
                  <OfferCard key={`${offer.merchant}-${offer.external_id}-${offer.id}`} offer={offer} />
                ))}
              </div>
              <div className="mt-10 text-center">
                <p className="text-gray-500 text-sm">Mostrando {offers.length} produtos em oferta</p>
              </div>
            </>
          ) : (!isLoading || !isInitialLoad) && offers.length === 0 ? (
            <EmptyState 
              message="Nenhuma oferta encontrada com os filtros selecionados." 
              suggestion="Tente remover alguns filtros para ver mais ofertas."
            />
          ) : null}
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