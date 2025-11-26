import { useQuery } from '@tanstack/react-query';
import { fetchFeatureNames } from '../services/api';

export const useFeatureNames = () => {
  return useQuery({
    queryKey: ['featureNames'],
    queryFn: fetchFeatureNames,
    staleTime: Infinity, // Never changes
  });
};
