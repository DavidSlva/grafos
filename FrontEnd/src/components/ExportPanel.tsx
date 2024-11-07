import React from 'react';
import { Download } from 'lucide-react';
import Button from './Button';

interface ExportPanelProps {
  onExport: () => void;
}

export default function ExportPanel({ onExport }: ExportPanelProps) {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Exportar Datos</h2>
      
      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <div className="prose">
          <p>
            Exporta los datos ingresados en un formato compatible con el modelo de optimización.
            El archivo generado incluirá:
          </p>
          <ul>
            <li>Configuración de buques y sus características</li>
            <li>Sitios de atraque y sus posiciones</li>
            <li>Parámetros de costos y restricciones</li>
            <li>Matriz de tiempos de manipulación</li>
          </ul>
        </div>
        
        <Button
          onClick={onExport}
          icon={<Download className="w-5 h-5" />}
          size="lg"
          className="w-full sm:w-auto"
        >
          Exportar Datos
        </Button>
      </div>
    </div>
  );
}