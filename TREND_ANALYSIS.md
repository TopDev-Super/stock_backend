# Trend Analysis System

This document explains how the trend analysis system works and how to use it to answer questions about stock trends.

## Overview

The trend analysis system allows users to ask natural language questions about stock trends and get intelligent answers. It specifically handles:

- **Current trend analysis** for any stock symbol
- **Trend change detection** (when stocks moved from uptrend to downtrend or vice versa)
- **Trend history** over specified time periods
- **Pattern analysis** and statistics

## How It Works

### 1. Trend Values
The system uses numeric trend values:
- `1` = **Uptrend** (Long position)
- `2` = **Downtrend** (Short position)  
- `0` = **Sideways** (No clear trend)

### 2. Database Field
The system reads from the `TheTrendD` field in your stock data table, which contains the daily trend values.

### 3. Query Processing
When a user asks a question, the system:
1. **Analyzes the question** to determine if it's trend-related
2. **Extracts the stock symbol** (e.g., "230011")
3. **Classifies the query type** (current trend, trend change, history, etc.)
4. **Executes the appropriate analysis**
5. **Returns a natural language answer**

## Supported Question Types

### Current Trend Questions
```
"What is the trend on symbol 230011 today?"
"Trend of 230011"
"How is 230011 trending?"
"Current trend for 230011"
```

### Trend Change Questions
```
"When was the last time symbol 230011 moved from uptrend to downtrend?"
"Last time 230011 changed from long to short"
"When did 230011 move from down to up?"
"Trend change for 230011"
```

### Trend History Questions
```
"Trend history for symbol 230011"
"How has 230011 been trending?"
"Trend pattern for 230011"
```

## API Endpoints

### 1. Natural Language Query
```
POST /query
{
    "question": "What is the trend on symbol 230011 today?"
}
```

### 2. Direct Trend Analysis
```
POST /trend/current/{symbol}
POST /trend/changes/{symbol}?from_trend=1&to_trend=2
POST /trend/history/{symbol}?days=30
POST /trend/analysis/{symbol}
```

## Example Responses

### Current Trend Response
```json
{
    "status": "success",
    "symbol": "230011",
    "current_trend": 1,
    "trend_description": "uptrend",
    "date": "2024-01-15",
    "price": 150.25,
    "volume": 1000000
}
```

### Trend Change Response
```json
{
    "status": "success",
    "symbol": "230011",
    "trend_changes": [
        {
            "date": "2024-01-10",
            "from_trend": 1,
            "from_trend_desc": "uptrend",
            "to_trend": 2,
            "to_trend_desc": "downtrend",
            "price": 145.50,
            "volume": 1200000
        }
    ],
    "total_changes": 1
}
```

## Implementation Details

### Files Created/Modified

1. **`services/trend_analysis_service.py`**
   - Core trend analysis functionality
   - Database queries for trend data
   - Trend interpretation and statistics

2. **`services/query_processor.py`**
   - Natural language query processing
   - Pattern matching for trend questions
   - Query classification and routing

3. **`services/stock_ai_service.py`** (Modified)
   - Integrated trend analysis with existing LLM service
   - Fallback to general LLM for non-trend queries

4. **`api/main.py`** (Modified)
   - Added new trend-specific API endpoints
   - Enhanced error handling

### Database Requirements

Your stock data table should have:
- `symbol` field (stock identifier)
- `TheTrendD` field (trend values: 0, 1, 2)
- `date` field (date of the data)
- `price` field (stock price)
- `volume` field (trading volume)

## Testing

Run the test script to verify functionality:

```bash
cd backend
python test_trend_analysis.py
```

This will test:
- Current trend analysis
- Trend change detection
- Trend history retrieval
- Natural language query processing

## Extending the System

### Adding New Question Types

1. **Add patterns** to `query_processor.py`:
```python
'trend_patterns': {
    'new_type': [
        r'your regex pattern here',
        r'another pattern'
    ]
}
```

2. **Add processing logic** in `process_trend_query()` method

3. **Add corresponding analysis** in `trend_analysis_service.py`

### Adding New Analysis Types

1. **Create new method** in `TrendAnalysisService`
2. **Add API endpoint** in `main.py`
3. **Update query processor** to handle new patterns

## Error Handling

The system handles various error scenarios:
- **Symbol not found**: Returns appropriate error message
- **No data available**: Handles empty result sets
- **Database errors**: Logs and returns user-friendly messages
- **Invalid queries**: Falls back to general LLM processing

## Performance Considerations

- **Caching**: Consider caching frequently requested trend data
- **Indexing**: Ensure database indexes on `symbol`, `date`, and `TheTrendD` fields
- **Query optimization**: Use appropriate LIMIT clauses and date ranges
- **Connection pooling**: Already implemented in database connection

## Future Enhancements

1. **Real-time updates**: WebSocket connections for live trend updates
2. **Trend prediction**: ML models for trend forecasting
3. **Multi-timeframe**: Support for different time periods (hourly, weekly, etc.)
4. **Alert system**: Notifications when trends change
5. **Visualization**: Charts and graphs for trend data 