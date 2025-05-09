import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface ClickStats {
  click_count: number;
  offer_id: number;
  merchant: string;
  title: string;
}

export default function Stats() {
  const [stats, setStats] = useState<ClickStats[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [days, setDays] = useState(30);
  const router = useRouter();

  // Carregar estatísticas quando a página for carregada
  useEffect(() => {
    const fetchStats = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`/api/stats/clicks?days=${days}`);
        
        if (!response.ok) {
          throw new Error('Erro ao buscar estatísticas de cliques');
        }
        
        const data = await response.json();
        setStats(data.data || []);
        setIsError(false);
      } catch (error) {
        console.error('Erro ao buscar estatísticas:', error);
        setIsError(true);
        setStats([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, [days]);

  const handleDaysChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setDays(Number(e.target.value));
  };

  const handleBackClick = () => {
    router.push('/');
  };

  return (
    <>
      <Head>
        <title>Estatísticas de Cliques | BoraDeDesconto</title>
        <meta name="description" content="Estatísticas de cliques nas ofertas do BoraDeDesconto" />
      </Head>

      <main className="min-h-screen bg-gray-100">
        {/* Cabeçalho */}
        <header className="bg-orange-500 py-6 shadow-md relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold text-white">Estatísticas</h1>
                <p className="text-white opacity-90">Análise de cliques nas ofertas</p>
              </div>
              <button
                onClick={handleBackClick}
                className="bg-white text-orange-600 px-4 py-2 rounded-lg shadow hover:bg-orange-50 transition-colors"
              >
                Voltar para Ofertas
              </button>
            </div>
          </div>
          {/* Elementos decorativos */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-orange-400 rounded-full transform translate-x-1/2 -translate-y-1/2 opacity-50"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-orange-400 rounded-full transform -translate-x-1/3 translate-y-1/3 opacity-30"></div>
        </header>

        {/* Conteúdo principal */}
        <div className="container mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Cliques por Oferta</h2>
              <div className="flex items-center space-x-2">
                <label htmlFor="days" className="text-gray-600">Período:</label>
                <select
                  id="days"
                  value={days}
                  onChange={handleDaysChange}
                  className="border border-gray-300 rounded-md px-3 py-2 bg-white"
                >
                  <option value={7}>Últimos 7 dias</option>
                  <option value={30}>Últimos 30 dias</option>
                  <option value={90}>Últimos 90 dias</option>
                  <option value={180}>Últimos 180 dias</option>
                </select>
              </div>
            </div>

            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-500"></div>
              </div>
            ) : isError ? (
              <div className="text-center py-8">
                <p className="text-red-500">Erro ao carregar estatísticas. Tente novamente mais tarde.</p>
              </div>
            ) : stats.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">Nenhum clique registrado no período selecionado.</p>
                <p className="text-gray-400 mt-2">As estatísticas são registradas quando usuários clicam em ofertas.</p>
              </div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="min-w-full bg-white">
                    <thead>
                      <tr className="bg-gray-100 text-gray-600 uppercase text-sm leading-normal">
                        <th className="py-3 px-6 text-left">Título</th>
                        <th className="py-3 px-6 text-center">Loja</th>
                        <th className="py-3 px-6 text-center">Cliques</th>
                      </tr>
                    </thead>
                    <tbody className="text-gray-600 text-sm">
                      {stats.map((stat) => (
                        <tr key={stat.offer_id} className="border-b border-gray-200 hover:bg-gray-50">
                          <td className="py-3 px-6 text-left">
                            <div className="line-clamp-2">{stat.title}</div>
                          </td>
                          <td className="py-3 px-6 text-center">
                            <span className={`px-3 py-1 rounded-full text-xs ${
                              stat.merchant === 'amazon' 
                                ? 'bg-blue-100 text-blue-800' 
                                : stat.merchant === 'mercadolivre' 
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-gray-100 text-gray-800'
                            }`}>
                              {stat.merchant === 'amazon' 
                                ? 'Amazon' 
                                : stat.merchant === 'mercadolivre' 
                                ? 'Mercado Livre'
                                : stat.merchant}
                            </span>
                          </td>
                          <td className="py-3 px-6 text-center">
                            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs">
                              {stat.click_count}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="mt-6 text-right text-sm text-gray-500">
                  Total de cliques: {stats.reduce((total, stat) => total + stat.click_count, 0)}
                </div>
              </>
            )}
          </div>
        </div>

        {/* Rodapé */}
        <footer className="bg-gray-800 text-white py-6">
          <div className="container mx-auto px-4 text-center">
            <p>© 2024 BoraDeDesconto - Versão MVP</p>
            <p className="text-sm opacity-70 mt-2">
              Analytics de cliques para análise de desempenho de ofertas
            </p>
          </div>
        </footer>
      </main>
    </>
  );
} 