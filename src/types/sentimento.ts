/**
 * Canonical SentimentoLiveEvent payload shape
 * Broadcast to WebSocket clients via /api/v2/sentimento/live
 */
export interface SentimentoLiveEvent {
  timestamp: string; // ISO 8601 timestamp
  composites: {
    hope: number;
    sorrow: number;
  };
  source?: string; // Optional source identifier
  sequence?: number; // Optional sequence number for ordering
}

/**
 * Ingest payload for POST /ingest/sentimento
 */
export interface SentimentoIngestPayload {
  composites: {
    hope: number;
    sorrow: number;
  };
  source?: string;
  metadata?: Record<string, any>;
}
