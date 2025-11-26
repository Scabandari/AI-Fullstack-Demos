import { useMutation } from '@tanstack/react-query';
import { predictRisk } from '../services/api';
import {
  usePredictionStore,
  type PredictionStore,
} from '../store/predictionStore';

export const usePrediction = () => {
  const addPrediction = usePredictionStore(
    (state: PredictionStore) => state.addPrediction
  );
  return useMutation({
    mutationFn: predictRisk,
    onSuccess: (data) => {
      console.log('Prediction successful:', data);
      addPrediction({ ...data, timestamp: new Date().toISOString() });
    },
    onError: (error) => {
      console.error('Prediction failed:', error);
    },
  });
};
