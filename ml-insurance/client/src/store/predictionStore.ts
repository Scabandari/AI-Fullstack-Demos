import { create } from 'zustand';
import type { PredictionResult, InsuranceFeatures } from '../types/insurance';

export interface PredictionStore {
  predictions: PredictionResult[];
  sampleData: InsuranceFeatures | null;
  isLoadingSample: boolean;
  addPrediction: (prediction: PredictionResult) => void;
  clearHistory: () => void;
}

export const usePredictionStore = create<PredictionStore>((set) => ({
  predictions: [],
  sampleData: null,
  isLoadingSample: false,
  addPrediction: (prediction) =>
    set((state) => ({
      predictions: [prediction, ...state.predictions].slice(0, 5),
    })),
  clearHistory: () => set({ predictions: [] }),
}));
