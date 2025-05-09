import React from 'react';
import { NextPageContext } from 'next';

interface ErrorProps {
  statusCode?: number;
}

function Error({ statusCode }: ErrorProps) {
  return (
    <div className="flex items-center justify-center h-screen">
      <h1 className="text-2xl font-bold">
        {statusCode
          ? `Erro no servidor: ${statusCode}`
          : 'Erro ao carregar a página'}
      </h1>
    </div>
  );
}

Error.getInitialProps = ({ res, err }: NextPageContext) => {
  const statusCode = res?.statusCode || err?.statusCode || 404;
  return { statusCode };
};

export default Error; 