/**
 * Seed-003: KPI tracking system for hope/sorrow metrics
 * Tracks samples and calculates hope ratio
 */

interface Sample {
  sorrow: number;
  hope: number;
  timestamp: number;
}

class Seed003Metrics {
  private samples: Sample[] = [];
  private readonly maxSamples = 1000; // Keep last 1000 samples

  /**
   * Push a new sample of sorrow and hope values
   * Called by SentimentoWSHub for each broadcast event
   */
  pushSample(sorrow: number, hope: number): void {
    this.samples.push({
      sorrow,
      hope,
      timestamp: Date.now(),
    });

    // Trim to max samples
    if (this.samples.length > this.maxSamples) {
      this.samples = this.samples.slice(-this.maxSamples);
    }
  }

  /**
   * Calculate the hope ratio from recent samples
   * @returns The ratio of hope to total sentiment (hope + sorrow)
   */
  getHopeRatio(): number {
    if (this.samples.length === 0) {
      return 0;
    }

    let totalHope = 0;
    let totalSorrow = 0;

    for (const sample of this.samples) {
      totalHope += sample.hope;
      totalSorrow += sample.sorrow;
    }

    const total = totalHope + totalSorrow;
    if (total === 0) {
      return 0;
    }

    return totalHope / total;
  }

  /**
   * Get statistics about current samples
   */
  getStats() {
    if (this.samples.length === 0) {
      return {
        sampleCount: 0,
        hopeRatio: 0,
        avgHope: 0,
        avgSorrow: 0,
      };
    }

    let totalHope = 0;
    let totalSorrow = 0;

    for (const sample of this.samples) {
      totalHope += sample.hope;
      totalSorrow += sample.sorrow;
    }

    const sampleCount = this.samples.length;
    const total = totalHope + totalSorrow;

    return {
      sampleCount,
      hopeRatio: total === 0 ? 0 : totalHope / total,
      avgHope: totalHope / sampleCount,
      avgSorrow: totalSorrow / sampleCount,
    };
  }
}

// Singleton instance
export const seed003Metrics = new Seed003Metrics();
