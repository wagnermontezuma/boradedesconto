import React from 'react';
import { render, screen } from '@testing-library/react';
import OfferCard from './OfferCard';
import type { Offer } from '../lib/useOffers';

const mockOffer: Offer = {
  id: 1,
  merchant: "amazon",
  external_id: "B08X7JX9MB",
  title: "Smartphone Samsung Galaxy A54 5G 128GB 8GB RAM Preto",
  url: "https://www.amazon.com.br/dp/B08X7JX9MB?tag=wagnermontezu-20",
  price: 1899.99,
  discount_pct: 25,
  ts: "2023-06-01T10:00:00Z"
};

const mockOfferNoDiscount: Offer = {
    id: 2,
    merchant: "mercadolivre",
    external_id: "MLB123",
    title: "Produto Sem Desconto Teste",
    url: "http://mercadolivre.com/mlb123",
    price: 100.00,
    discount_pct: 0,
    ts: "2023-06-02T10:00:00Z"
};


describe('OfferCard Component', () => {
  it('renders offer title correctly', () => {
    render(<OfferCard offer={mockOffer} />);
    expect(screen.getByText((content: string, element: HTMLElement | null) => {
        const hasText = (node: Element | null): boolean => node?.textContent === mockOffer.title;
        const nodeHasText = hasText(element);
        const childrenDontHaveText = Array.from(element?.children || []).every(child => !hasText(child as Element));
        return nodeHasText && childrenDontHaveText;
      })).toBeInTheDocument();
  });

  it('renders offer price correctly formatted', () => {
    render(<OfferCard offer={mockOffer} />);
    expect(screen.getByText((content: string, element: HTMLElement | null) => content.includes('1.899,99'))).toBeInTheDocument();
  });

  it('displays discount percentage when discount_pct > 0', () => {
    render(<OfferCard offer={mockOffer} />);
    expect(screen.getByText(/25%/)).toBeInTheDocument();
  });

  it('does not display discount percentage when discount_pct is 0', () => {
    render(<OfferCard offer={mockOfferNoDiscount} />);
    const discountBadge = screen.queryByText(/% OFF/i);
    if (discountBadge) {
        expect(screen.queryByText(/0% OFF/i)).not.toBeInTheDocument(); 
        expect(screen.queryByText(/\d+% OFF/i)).not.toBeInTheDocument();
    } else {
        expect(discountBadge).not.toBeInTheDocument();
    }
  });


  it('renders the merchant logo or name', () => {
    render(<OfferCard offer={mockOffer} />);
    const merchantImage = screen.queryByAltText(`${mockOffer.merchant} logo`);
    if (merchantImage) {
      expect(merchantImage).toBeInTheDocument();
    } else {
      expect(screen.getByText(new RegExp(mockOffer.merchant, "i"))).toBeInTheDocument();
    }
  });

  it('contains a link to the offer URL', () => {
    render(<OfferCard offer={mockOffer} />);
    const expectedLink = `/go/${mockOffer.id}`;
    
    const linkElement = screen.getAllByRole('link').find(
        (link): link is HTMLAnchorElement => (link as HTMLAnchorElement).href.endsWith(expectedLink)
    );
    expect(linkElement).toBeInTheDocument();
    expect(linkElement).toHaveAttribute('href', expectedLink);
  });
}); 