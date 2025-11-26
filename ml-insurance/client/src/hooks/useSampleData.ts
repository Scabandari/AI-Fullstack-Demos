import { useQuery } from '@tanstack/react-query';
import { fetchSampleData } from '../services/api';

export const useSampleData = () => {
  return useQuery({
    queryKey: ['sampleData'],
    queryFn: fetchSampleData,
    staleTime: Infinity, // Sample data never changes
    enabled: false, // Only fetch when manually triggered
  });
};
