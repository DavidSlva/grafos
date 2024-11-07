import React, { useState } from 'react';
import { Table } from './';
import { PlusCircle } from 'lucide-react';

interface ShipData {
  id: string;
  arrival: string;
  plannedArrival: string;
  plannedDeparture: string;
  length: number;
  priority: 'high' | 'medium' | 'low';
}

export default function Ship() {
  const [ships, setShips] = useState<ShipData[]>([]);

  const addShip = () => {
    const newShip: ShipData = {
      id: `SHIP-${ships.length + 1}`,
      arrival: '',
      plannedArrival: '',
      plannedDeparture: '',
      length: 0,
      priority: 'medium'
    };
    setShips([...ships, newShip]);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Gestión de Buques</h2>
        <button
          onClick={addShip}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          <PlusCircle className="w-5 h-5 mr-2" />
          Agregar Buque
        </button>
      </div>

      <div className="bg-white rounded-lg shadow">
        <Table
          columns={[
            { header: 'ID', accessor: 'id' },
            { header: 'Llegada Real', accessor: 'arrival' },
            { header: 'Llegada Planificada', accessor: 'plannedArrival' },
            { header: 'Salida Planificada', accessor: 'plannedDeparture' },
            { header: 'Longitud (m)', accessor: 'length' },
            { header: 'Prioridad', accessor: 'priority' }
          ]}
          data={ships}
          onUpdate={setShips}
        />
      </div>
    </div>
  );
}