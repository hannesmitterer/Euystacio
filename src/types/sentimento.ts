/**
 * Canonical SentimentoLiveEvent type for WebSocket broadcasting
 * 
 * This type represents real-time sentimento data broadcast to connected clients
 * through the /api/v2/sentimento/live WebSocket endpoint.
 */
export interface SentimentoLiveEvent {
  /**
   * ISO 8601 timestamp of when this event was generated
   */
  timestamp: string;

  /**
   * Composite sentimento metrics
   */
  composites: {
    /**
     * Hope metric value (0.0 to 1.0)
     */
    hope: number;

    /**
     * Sorrow metric value (0.0 to 1.0)
     */
    sorrow: number;
  };

  /**
   * Seed-003 metrics integration
   */
  seed003?: {
    /**
     * Sample count in current window
     */
    sampleCount: number;

    /**
     * Hope-to-sorrow ratio
     */
    hopeRatio: number;
  };

  /**
   * Event sequence number for this broadcast session
   */
  sequence: number;
}

/**
 * Type for ingestion payload from POST /ingest/sentimento
 */
export interface SentimentoIngestPayload {
  composites: {
    hope: number;
    sorrow: number;
  };
}
