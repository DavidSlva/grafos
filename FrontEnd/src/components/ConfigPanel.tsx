import React, { useState } from 'react';

interface CostConfig {
  changeCost: number;
  delayCost: number;
  punctualDelayCost: number;
  bigConstant: number;
}

export default function ConfigPanel() {
  const [costs, setCosts] = useState<CostConfig>({
    changeCost: 1000,
    delayCost: 500,
    punctualDelayCost: 750,
    bigConstant: 9999
  });

  const handleChange = (key: keyof CostConfig) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setCosts(prev => ({ ...prev, [key]: Number(e.target.value) }));
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Configuración de Costos</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Costo de Cambio de Sitio (c1)
            </label>
            <input
              type="number"
              value={costs.changeCost}
              onChange={handleChange('changeCost')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Costo de Retraso (c2)
            </label>
            <input
              type="number"
              value={costs.delayCost}
              onChange={handleChange('delayCost')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Costo de Retraso Puntual (c3)
            </label>
            <input
              type="number"
              value={costs.punctualDelayCost}
              onChange={handleChange('punctualDelayCost')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Constante Grande (B)
            </label>
            <input
              type="number"
              value={costs.bigConstant}
              onChange={handleChange('bigConstant')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Vista Previa de Configuración</h3>
          <pre className="bg-gray-50 p-4 rounded-md overflow-auto">
            {JSON.stringify(costs, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}