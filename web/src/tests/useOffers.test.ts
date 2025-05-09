import { renderHook, act } from '@testing-library/react-hooks';
import { useOffers, Offer } from '../lib/useOffers';
import fetchMock from 'jest-fetch-mock';

// Mock do fetch
fetchMock.enableMocks();

describe('useOffers hook', () => {
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  it('deve retornar dados da API quando a requisição for bem-sucedida', async () => {
    // Mock de resposta da API
    const mockApiResponse = {
      data: [
        {
          id: 1,
          merchant: "amazon",
          external_id: "B123456789",
          title: "Produto teste",
          url: "https://amazon.com.br/produto",
          price: 99.99,
          discount_pct: 20,
          ts: "2024-08-01T00:00:00Z"
        }
      ],
      count: 1
    };

    // Configura o mock para retornar dados
    fetchMock.mockResponseOnce(JSON.stringify(mockApiResponse));

    // Renderiza o hook
    const { result, waitForNextUpdate } = renderHook(() => useOffers({
      merchant: 'amazon',
      min_discount: 10
    }));

    // Inicialmente deve estar carregando
    expect(result.current.isLoading).toBe(true);
    expect(result.current.offers).toEqual([]);
    
    // Espera a atualização após a requisição
    await waitForNextUpdate();
    
    // Verifica se os dados foram carregados corretamente
    expect(result.current.isLoading).toBe(false);
    expect(result.current.isError).toBe(false);
    expect(result.current.usedMockData).toBe(false);
    expect(result.current.offers).toEqual(mockApiResponse.data);
    expect(result.current.totalOffersAvailable).toBe(1);

    // Verifica se a chamada foi feita com os parâmetros corretos
    expect(fetchMock).toHaveBeenCalledWith('/api/offers?merchant=amazon&min_discount=10');
  });

  it('deve usar dados mockados quando a API falhar', async () => {
    // Configura o mock para falhar
    fetchMock.mockRejectOnce(new Error('API error'));

    // Renderiza o hook
    const { result, waitForNextUpdate } = renderHook(() => useOffers({
      merchant: 'amazon',
      min_discount: 0
    }));

    // Inicialmente deve estar carregando
    expect(result.current.isLoading).toBe(true);
    
    // Espera a atualização após a requisição
    await waitForNextUpdate();
    
    // Verifica se os dados mockados foram usados
    expect(result.current.isLoading).toBe(false);
    expect(result.current.isError).toBe(false); // Não é erro porque usou fallback
    expect(result.current.usedMockData).toBe(true);
    expect(result.current.offers.length).toBeGreaterThan(0);
    
    // Verifica se todos os resultados são da Amazon
    if (result.current.offers.length > 0) {
      const amazonOffers = result.current.offers.filter(o => o.merchant === 'amazon');
      expect(amazonOffers.length).toBe(result.current.offers.length);
    }
  });

  it('deve retornar array vazio quando não houver ofertas', async () => {
    // Mock de resposta vazia
    const mockEmptyResponse = {
      data: [],
      count: 0
    };

    // Configura o mock para retornar dados vazios
    fetchMock.mockResponseOnce(JSON.stringify(mockEmptyResponse));

    // Renderiza o hook
    const { result, waitForNextUpdate } = renderHook(() => useOffers({
      merchant: 'amazon',
      min_discount: 90 // Desconto alto para não ter resultados
    }));
    
    // Espera a atualização após a requisição
    await waitForNextUpdate();
    
    // Verifica se retornou array vazio
    expect(result.current.isLoading).toBe(false);
    expect(result.current.isError).toBe(false);
    expect(result.current.offers).toEqual([]);
    expect(result.current.totalOffersAvailable).toBe(0);
  });
}); 