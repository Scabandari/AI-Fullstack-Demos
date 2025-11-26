import axios from 'axios';
import type {
  PredictionRequest,
  PredictionResponse,
  InsuranceFeatures,
} from '../types/insurance';

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || 'http://localhost:8007'}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictRisk = async (
  data: PredictionRequest
): Promise<PredictionResponse> => {
  const response = await api.post<PredictionResponse>('/predict', data);
  return response.data;
};

export const fetchSampleData = async (): Promise<InsuranceFeatures> => {
  const response = await api.get<{ features: InsuranceFeatures }>('/sample');
  return response.data.features;
};

export const fetchFeatureNames = async (): Promise<string[]> => {
  const response = await api.get<{ features: string[] }>('/features');
  return response.data.features;
};

export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};
