import React, { useState } from 'react';
import { Table } from './';
import { PlusCircle } from 'lucide-react';

interface BerthData {
  id: string;
  position: number;
  maxLength: number;
  status: 'available' | 'occupied';
}

export default function Berth() {
  const [berths, setBerths] = useState<BerthData[]>([]);

  const addBerth = () => {
    const newBerth: BerthData = {
      id: `BERTH-${berths.length + 1}`,
      position: 0,
      maxLength: 0,
      status: 'available'
    };
    setBerths([...berths, newBerth]);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Sitios de Atraque</h2>
        <button
          onClick={addBerth}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          <PlusCircle className="w-5 h-5 mr-2" />
          Agregar Sitio
        </button>
      </div>

      <div className="bg-white rounded-lg shadow">
        <Table
          columns={[
            { header: 'ID', accessor: 'id' },
            { header: 'Posición (m)', accessor: 'position' },
            { header: 'Longitud Máxima', accessor: 'maxLength' },
            { header: 'Estado', accessor: 'status' }
          ]}
          data={berths}
          onUpdate={setBerths}
        />
      </div>
    </div>
  );
}