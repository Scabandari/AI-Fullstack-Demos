// Represents the 60 insurance features (all numeric)
export interface InsuranceFeatures {
  [key: string]: number; // Dynamic keys like "ps_car_13": 0.5, "ps_ind_01": 2
}

// What we send TO the API
export interface PredictionRequest {
  features: InsuranceFeatures; // Wraps features in an object
}

// What we get BACK from the API
export interface PredictionResponse {
  claim_probability: number; // 0.1234 (12.34% chance of claim)
  risk_level: 'low' | 'medium' | 'high'; // Risk category
}

// Extended version with timestamp for history (stored in Zustand)
export interface PredictionResult extends PredictionResponse {
  timestamp: string; // ISO string like "2024-11-20T10:30:00Z"
}
