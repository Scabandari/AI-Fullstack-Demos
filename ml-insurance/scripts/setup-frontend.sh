#!/bin/bash

# Setup React + TypeScript frontend with Vite

echo "Setting up React frontend..."

# Initialize Vite project with React + TypeScript
npm create vite@latest client -- --template react-ts

cd client

# Install dependencies
npm install

# Install additional packages
npm install @tanstack/react-query @emotion/react @emotion/styled react-hook-form zod @hookform/resolvers axios zustand

# Install dev dependencies
npm install -D @types/node

# Create directory structure
mkdir -p src/{components,hooks,store,services,types,utils}

# Create component files
touch src/components/{PredictionForm,ResultsDisplay,PredictionHistory}.tsx

# Create other files
touch src/hooks/usePrediction.ts
touch src/store/predictionStore.ts
touch src/services/api.ts
touch src/types/insurance.ts
touch src/utils/sampleData.ts

# Update vite.config.ts with proxy for API
cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react({
    jsxImportSource: '@emotion/react',
  })],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
EOF

# Update tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "jsxImportSource": "@emotion/react",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF

# Create types file
cat > src/types/insurance.ts << 'EOF'
export interface InsuranceFeatures {
  [key: string]: number;
}

export interface PredictionRequest {
  features: InsuranceFeatures;
}

export interface PredictionResponse {
  claim_probability: number;
  risk_level: 'low' | 'medium' | 'high';
}

export interface PredictionResult extends PredictionResponse {
  timestamp: string;
}
EOF

# Create API service
cat > src/services/api.ts << 'EOF'
import axios from 'axios';
import type { PredictionRequest, PredictionResponse } from '../types/insurance';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictRisk = async (data: PredictionRequest): Promise<PredictionResponse> => {
  const response = await api.post<PredictionResponse>('/predict', data);
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};
EOF
import { useState } from 'react';
# Create Zustand store
cat > src/store/predictionStore.ts << 'EOF'
import { create } from 'zustand';
import type { PredictionResult } from '../types/insurance';

interface PredictionStore {
  predictions: PredictionResult[];
  addPrediction: (prediction: PredictionResult) => void;
  clearHistory: () => void;
}

export const usePredictionStore = create<PredictionStore>((set) => ({
  predictions: [],
  addPrediction: (prediction) =>
    set((state) => ({
      predictions: [prediction, ...state.predictions].slice(0, 5),
    })),
  clearHistory: () => set({ predictions: [] }),
}));
EOF

# Create React Query hook
cat > src/hooks/usePrediction.ts << 'EOF'
import { useMutation } from '@tanstack/react-query';
import { predictRisk } from '../services/api';
import { usePredictionStore } from '../store/predictionStore';
import type { PredictionRequest } from '../types/insurance';

export const usePrediction = () => {
  const addPrediction = usePredictionStore((state) => state.addPrediction);

  return useMutation({
    mutationFn: predictRisk,
    onSuccess: (data) => {
      addPrediction({
        ...data,
        timestamp: new Date().toISOString(),
      });
    },
  });
};
EOF

# Update main App.tsx
cat > src/App.tsx << 'EOF'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { css } from '@emotion/react';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';
import PredictionHistory from './components/PredictionHistory';

const queryClient = new QueryClient();

const appStyles = css({
  minHeight: '100vh',
  backgroundColor: '#f5f5f5',
  padding: '2rem',
});

const containerStyles = css({
  maxWidth: '1200px',
  margin: '0 auto',
});

const headerStyles = css({
  textAlign: 'center',
  marginBottom: '2rem',
  h1: {
    fontSize: '2.5rem',
    color: '#1a1a1a',
    marginBottom: '0.5rem',
  },
  p: {
    fontSize: '1.1rem',
    color: '#666',
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div css={appStyles}>
        <div css={containerStyles}>
          <header css={headerStyles}>
            <h1>Insurance Risk Prediction</h1>
            <p>ML-powered driver risk assessment</p>
          </header>
          <PredictionForm />
          <ResultsDisplay />
          <PredictionHistory />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
EOF

# Create placeholder components
cat > src/components/PredictionForm.tsx << 'EOF'
import { css } from '@emotion/react';

const PredictionForm = () => {
  return (
    <div css={css({ padding: '2rem', backgroundColor: 'white', borderRadius: '8px' })}>
      <h2>Prediction Form - TODO</h2>
    </div>
  );
};

export default PredictionForm;
EOF

cat > src/components/ResultsDisplay.tsx << 'EOF'
import { css } from '@emotion/react';

const ResultsDisplay = () => {
  return (
    <div css={css({ marginTop: '2rem' })}>
      <h2>Results - TODO</h2>
    </div>
  );
};

export default ResultsDisplay;
EOF

cat > src/components/PredictionHistory.tsx << 'EOF'
import { css } from '@emotion/react';
import { usePredictionStore } from '../store/predictionStore';

const PredictionHistory = () => {
  const predictions = usePredictionStore((state) => state.predictions);

  return (
    <div css={css({ marginTop: '2rem' })}>
      <h2>History ({predictions.length})</h2>
    </div>
  );
};

export default PredictionHistory;
EOF

# Create sample data util
cat > src/utils/sampleData.ts << 'EOF'
// TODO: Add sample row from train.csv
export const sampleInsuranceData = {
  // Add your 60 features here
};
EOF

echo "✓ Client setup complete!"
echo "To start development:"
echo "  cd client"
echo "  npm run dev"