/**
 * Configuration loaded from environment variables
 */
export interface Config {
  port: number;
  sentimentoBroadcastHz: number;
  sentimentoBufferMaxKb: number;
  councilToken: string;
}

/**
 * Load configuration from environment variables with defaults
 */
export function loadConfig(): Config {
  return {
    port: parseInt(process.env.PORT || '3000', 10),
    sentimentoBroadcastHz: parseInt(process.env.SENTIMENTO_BROADCAST_HZ || '10', 10),
    sentimentoBufferMaxKb: parseInt(process.env.SENTIMENTO_BUFFER_MAX_KB || '512', 10),
    councilToken: process.env.COUNCIL_TOKEN || '',
  };
}
