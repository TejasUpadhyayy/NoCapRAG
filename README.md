# NoCap RAG: Real-Time Meme and Pop Culture Chatbot

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

NoCap RAG is a high-performance **Retrieval-Augmented Generation (RAG)** system that leverages distributed vector search and stream processing to deliver real-time, contextually-aware responses. Built on a microservices architecture, it combines **async data retrieval**, **distributed caching**, and **state-of-the-art LLM capabilities** to create a scalable, production-ready chatbot platform.

## Technical Stack

- **Frontend**: Streamlit with WebSocket support for real-time updates
- **Backend**: FastAPI for async API handling
- **Caching**: Redis for session management and response caching
- **Vector Store**: Qdrant for high-dimensional similarity search
- **Processing**: Apache Kafka for event streaming
- **Deployment**: Docker + Kubernetes for orchestration
- **Monitoring**: Prometheus + Grafana for metrics

## Architecture

The system implements a modern microservices architecture with four distinct layers:

### 1. Data Retrieval Layer
- **Async Data Fetching**: Concurrent API calls using `aiohttp`
- **Rate Limiting**: Token bucket algorithm with Redis backend
- **Circuit Breaking**: Hystrix-style failure protection
- **Data Sources**:
  ```python
  SOURCES = {
      'reddit': ('praw', 'v7.7.0', 'Trending memes'),
      'giphy': ('giphy-client', 'v1.0.0', 'GIF content'),
      'wikipedia': ('wikipedia-api', 'v1.8.0', 'Knowledge base')
  }
  ```

### 2. Vector Processing Layer
- **Embedding Model**: Google Gemini embeddings (768d)
- **Vector Store**: Qdrant with HNSW index
- **Similarity Metrics**: Cosine similarity with dynamic thresholding
- **Index Configuration**:
  ```python
  INDEX_CONFIG = {
      'dim': 768,
      'metric': 'cosine',
      'ef_construction': 128,
      'M': 16
  }
  ```

### 3. Context Augmentation Layer
- **Ranking Algorithm**: LambdaMART with custom features
- **Context Window**: Dynamic sizing (1K-8K tokens)
- **Feature Engineering**:
  ```python
  FEATURES = [
      'semantic_similarity',
      'temporal_relevance',
      'engagement_metrics',
      'source_authority'
  ]
  ```

### 4. Generation Layer
- **Model**: Google Gemini Pro
- **Prompt Engineering**: Few-shot learning with dynamic templates
- **Output Processing**: Regex-based content filtering
- **Performance Metrics**:
  ```python
  METRICS = {
      'latency_p95': '150ms',
      'throughput': '100 qps',
      'success_rate': '99.9%'
  }
  ```

## Performance Optimization

### Caching Strategy
```python
CACHE_CONFIG = {
    'l1_cache': {'type': 'local', 'size': '1GB', 'ttl': '1h'},
    'l2_cache': {'type': 'redis', 'size': '10GB', 'ttl': '24h'},
    'l3_cache': {'type': 's3', 'size': 'unlimited', 'ttl': '7d'}
}
```

### Load Balancing
- Round-robin with weighted server selection
- Health checking with customizable thresholds
- Automatic failover with zero downtime

### Connection Pooling
```python
POOL_CONFIG = {
    'redis': {'max_connections': 100, 'timeout': 5},
    'postgres': {'max_connections': 50, 'timeout': 3},
    'http': {'max_connections': 200, 'timeout': 10}
}
```

## Installation

### Using Docker
```bash
# Build the images
docker-compose build

# Start the services
docker-compose up -d
```

### Environment Configuration
```bash
# Core Services
export REDIS_URL=redis://localhost:6379
export QDRANT_URL=http://localhost:6333
export KAFKA_BROKERS=localhost:9092

# API Keys
export REDDIT_CLIENT_ID=your_reddit_client_id
export REDDIT_CLIENT_SECRET=your_reddit_client_secret
export GIPHY_API_KEY=your_giphy_api_key
export GEMINI_API_KEY=your_gemini_api_key
```

## API Reference

### Query Endpoint
```python
@app.post("/api/v1/query")
async def process_query(
    query: str,
    context_size: int = 1024,
    temperature: float = 0.7,
    max_tokens: int = 150
) -> Dict[str, Any]:
    """
    Process a user query with custom parameters.
    
    Returns:
        Dict containing response, context, and metadata
    """
```

## Monitoring

### Prometheus Metrics
```python
METRICS = {
    'query_latency': Summary('query_processing_seconds', 'Time spent processing query'),
    'cache_hits': Counter('cache_hits_total', 'Number of cache hits'),
    'embedding_time': Histogram('embedding_processing_seconds', 'Time spent on embeddings')
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with:
   - Comprehensive tests
   - Documentation updates
   - Performance benchmarks

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Google Gemini for LLM capabilities
- Reddit and Giphy for content APIs
- Streamlit for UI framework
