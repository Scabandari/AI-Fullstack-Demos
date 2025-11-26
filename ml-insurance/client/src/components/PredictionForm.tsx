import { useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { css } from '@emotion/react';
import { Divider } from '@mui/material';

import { usePrediction } from '../hooks/usePrediction';
import { useFeatureNames } from '../hooks/useFeatureNames';
import { useSampleData } from '../hooks/useSampleData';
import { usePredictionStore } from '../store/predictionStore';

const formStyles = css({
  backgroundColor: 'white',
  padding: '1rem',
  paddingBottom: '3rem',
  borderRadius: '8px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  width: '100%',
  h2: {
    textAlign: 'left',
  },
});

const gridStyles = css({
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
  gap: '1rem',
  marginBottom: '1.5rem',
});

const fieldStyles = css({
  display: 'flex',
  flexDirection: 'column',
  label: {
    fontSize: '0.85rem',
    fontWeight: 500,
    marginBottom: '0.25rem',
    color: '#333',
  },
  input: {
    padding: '0.5rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '0.9rem',
    '&:focus': {
      outline: 'none',
      borderColor: '#4CAF50',
    },
  },
});

const buttonGroupStyles = css({
  display: 'flex',
  gap: '1rem',
  justifyContent: 'center',
});

const buttonStyles = css({
  padding: '0.75rem 2rem',
  fontSize: '1rem',
  fontWeight: 600,
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  transition: 'all 0.2s',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  },
  '&:disabled': {
    opacity: 0.5,
    cursor: 'not-allowed',
    transform: 'none',
  },
});

const primaryButtonStyles = css(buttonStyles, {
  backgroundColor: '#4CAF50',
  color: 'white',
  '&:hover:not(:disabled)': {
    backgroundColor: '#45a049',
  },
});

const secondaryButtonStyles = css(buttonStyles, {
  backgroundColor: '#f0f0f0',
  color: '#333',
  '&:hover:not(:disabled)': {
    backgroundColor: '#e0e0e0',
  },
});

const resultsStyles = css({
  boxSizing: 'border-box',
  color: 'black',
  border: '1px solid blue',
  display: 'grid',
  width: '100%',
  minHeight: '200px',
  // gridTemplateRows: '50px 30px 30px 30px', // 4 rows
  gridTemplateRows: '55px 1fr', // 4 rows
  gridTemplateColumns: '1fr 50px 1fr', // 3 columns: content | gap | content
  gridTemplateAreas: `
    "latestHeader . historyHeader"
    "latestContent . historyList"
  `,
  gap: '0',
  'h3:first-of-type': {
    backgroundColor: 'green',
    gridArea: 'latestHeader',
    textAlign: 'left',
  },
  // 'h3:last-of-type': {
  '#historyHeader': {
    gridArea: 'historyHeader',
    backgroundColor: 'yellow',
    textAlign: 'left',
  },
  '#latestContent': {
    gridArea: 'latestContent',
    backgroundColor: 'blue',

    display: 'grid',
    gridTemplateColumns: '1fr 1fr 1fr',
    alignItems: 'center',
    justifyItems: 'center',
  },
  '#historyList': {
    gridArea: 'historyList',
    backgroundColor: 'red',
  },
});

const PredictionForm = () => {
  const { mutate, isPending } = usePrediction();
  const { predictions } = usePredictionStore();
  const { data: featureNames = [], isLoading: loadingFeatures } =
    useFeatureNames();
  const { refetch: fetchSample, isFetching: isLoadingSample } = useSampleData();

  // Build schema only when features are available
  const predictionSchema = useMemo(() => {
    if (!featureNames || featureNames.length === 0) return z.object({});

    return z.object(
      featureNames.reduce((acc, name) => {
        acc[name] = z.coerce.number();
        return acc;
      }, {} as Record<string, z.ZodNumber>)
    );
  }, [featureNames]);

  type PredictionFormData = z.infer<typeof predictionSchema>;

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PredictionFormData>({
    resolver: zodResolver(predictionSchema),
  });

  const onSubmit = (data: PredictionFormData) => {
    mutate({ features: data });
  };

  const loadSampleData = async () => {
    const result = await fetchSample(); // Fetches from API on click
    if (result.data) {
      reset(result.data as PredictionFormData); // Populates form with fetched data
    }
  };

  if (loadingFeatures) {
    return <div>Loading form...</div>;
  }

  return (
    <form css={formStyles} onSubmit={handleSubmit(onSubmit)}>
      <h2 css={css({ marginBottom: '1.5rem', color: '#333' })}>
        Driver Information
      </h2>

      <div css={gridStyles}>
        {featureNames.map((name) => (
          <div key={name} css={fieldStyles}>
            <label htmlFor={name}>{name}</label>
            <input id={name} type='number' step='any' {...register(name)} />
            {errors[name] && (
              <span css={css({ color: 'red', fontSize: '0.75rem' })}>
                {errors[name]?.message}
              </span>
            )}
          </div>
        ))}
      </div>

      <div css={buttonGroupStyles}>
        <button
          type='button'
          css={secondaryButtonStyles}
          onClick={loadSampleData}
          disabled={isPending}
        >
          Load Sample Data
        </button>
        <button type='submit' css={primaryButtonStyles} disabled={isPending}>
          {isPending ? 'Predicting...' : 'Predict Risk'}
        </button>
      </div>
      <Divider css={css({ margin: '1.5rem 0' })} />
      <div css={resultsStyles}>
        <h3 id='latestHeader'>Predicted Risk</h3>
        <h3 id='historyHeader'>History</h3>
        <div id='latestContent'>
          {/* <div>Risk Level</div>
          <div>Claim Probability</div>
          <div>Timestamp</div>
          {predictions[0] ? (
            <>
              <div>{predictions[0].risk_level.toUpperCase()}</div>
              <div>{(predictions[0].claim_probability * 100).toFixed(2)}%</div>
              <div>{new Date(predictions[0].timestamp).toLocaleString()}</div>
            </>
          ) : (
            <>
              <div>N/A</div>
              <div>N/A</div>
              <div>N/A</div>
            </>
          )} */}
          <table>
            <thead>
              <tr>
                <th>Risk Level</th>
                <th>Claim Probability</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  {predictions[0]
                    ? predictions[0].risk_level.toUpperCase()
                    : 'N/A'}
                </td>
                <td>
                  {predictions[0]
                    ? (predictions[0].claim_probability * 100).toFixed(2) + '%'
                    : 'N/A'}
                </td>
                <td>
                  {predictions[0]
                    ? new Date(predictions[0].timestamp).toLocaleString()
                    : 'N/A'}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div id='historyList'></div>
      </div>
      {/* {predictions.length > 0 && (
        <div css={resultsStyles}>
          <h3 css={css({ textAlign: 'left', color: '#333' })}>
            Risk Prediction
          </h3>
          <div
            id='latestContent'
            css={css({ display: 'flex', flexDirection: 'row' })}
          >
            {`Risk Level: ${predictions[0].risk_level.toUpperCase()}, Claim Probability: ${(
              predictions[0].claim_probability * 100
            ).toFixed(2)}%`}
            <strong>
              {new Date(predictions[0].timestamp).toLocaleString()}:
            </strong>{' '}
          </div>
          <h3>History</h3>
          <ul css={css({ listStyle: 'none', padding: 0 })}>
            {predictions.map((pred, index) => (
              <li
                key={index}
                css={css({
                  color: 'black',
                  padding: '0.75rem',
                  borderRadius: '4px',
                  marginBottom: '0.5rem',
                })}
              >
                <strong>{new Date(pred.timestamp).toLocaleString()}:</strong>{' '}
                {`Risk Level: ${pred.risk_level.toUpperCase()}, Claim Probability: ${(
                  pred.claim_probability * 100
                ).toFixed(2)}%`}
              </li>
            ))}
          </ul>
        </div>
      )} */}
    </form>
  );
};

export default PredictionForm;
