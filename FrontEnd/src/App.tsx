import React, { useState } from 'react';
import { Ship, Berth, Layout, Sidebar, ConfigPanel, ExportPanel } from './components';
import { Ship as ShipIcon, Anchor, Settings, Download } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('ships');

  const handleExport = () => {
    // Implementation for exporting data
    const data = {
      // Collect and format all data here
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'berthing-optimization-data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Layout>
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        items={[
          { id: 'ships', label: 'Buques', icon: <ShipIcon className="w-5 h-5" /> },
          { id: 'berths', label: 'Sitios', icon: <Anchor className="w-5 h-5" /> },
          { id: 'config', label: 'Configuración', icon: <Settings className="w-5 h-5" /> },
          { id: 'export', label: 'Exportar', icon: <Download className="w-5 h-5" /> }
        ]}
      />
      <main className="flex-1 p-8 bg-gray-50">
        {activeTab === 'ships' && <Ship />}
        {activeTab === 'berths' && <Berth />}
        {activeTab === 'config' && <ConfigPanel />}
        {activeTab === 'export' && <ExportPanel onExport={handleExport} />}
      </main>
    </Layout>
  );
}

export default App;