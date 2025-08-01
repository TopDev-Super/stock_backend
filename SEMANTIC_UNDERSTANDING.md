# Semantic Database Understanding System

## Problem Statement

The system needs to understand the meaning of cells in a database table and answer natural language queries correctly. For example:

- **Question**: "What is the trend on symbol 230011 today?"
- **Expected Answer**: "The current trend for Bezeq (symbol 230011) as of 2025-07-27 is uptrend (long position). The stock price is 634.6."

- **Question**: "When was the last time symbol 230011 moved from uptrend to downtrend?"
- **Expected Answer**: "Found 10 trend changes. Recent changes: Bezeq changed from uptrend (long position) to downtrend (short position) on 2025-05-26..."

## Solution Architecture

### 1. Semantic Field Mapping System

The core of the solution is a **Semantic Mapping Service** that understands what each database field means:

```python
# Example field definition
'TheTrendD': FieldDefinition(
    field_name='TheTrendD',
    field_type=FieldType.TREND,
    description='Daily trend indicator',
    possible_values={
        '0': 'sideways (no clear trend)',
        '1': 'uptrend (long position)',
        '2': 'downtrend (short position)'
    },
    table='stock_data'
)
```

### 2. Query Pattern Recognition

The system uses regex patterns to classify different types of questions:

```python
'trend_current': [
    {
        'patterns': [
            r'trend.*symbol\s+(\d+)',
            r'trend.*stock\s+(\d+)',
            r'(\d+).*trend.*today',
            r'current.*trend.*(\d+)',
            r'how.*(\d+).*trending'
        ],
        'sql_template': """
            SELECT s.Nrnum, s.Date, s.TheTrendD, s.Price, s.UpsDowns,
                   n.HebName, n.EngName
            FROM stock_data s
            LEFT JOIN name_index n ON s.Nrnum = n.Nrnum
            WHERE s.Nrnum = {symbol}
            ORDER BY s.Date DESC
            LIMIT 1
        """
    }
]
```

### 3. Enhanced Query Processing

The system combines semantic understanding with LLM-based processing:

1. **Semantic First**: Try to match question patterns and use semantic SQL templates
2. **LLM Fallback**: If no semantic pattern matches, use LLM to generate SQL
3. **Natural Response**: Generate human-readable explanations of results

## Key Components

### 1. SemanticMappingService (`services/semantic_mapping_service.py`)

**Responsibilities:**
- Define semantic meanings of database fields
- Classify question types using regex patterns
- Extract stock symbols from natural language
- Generate contextual SQL queries
- Interpret numeric values into human-readable descriptions

**Key Methods:**
- `classify_question_type()`: Identifies what type of question is being asked
- `extract_symbol_from_question()`: Extracts stock symbols from text
- `generate_contextual_sql()`: Creates SQL based on question type
- `interpret_trend_value()`: Converts 0,1,2 to "sideways", "uptrend", "downtrend"

### 2. EnhancedQueryProcessor (`services/enhanced_query_processor.py`)

**Responsibilities:**
- Orchestrates semantic and LLM-based processing
- Handles query execution and result formatting
- Provides field meaning APIs

**Processing Flow:**
1. Classify question using semantic patterns
2. If semantic pattern matches, use semantic SQL template
3. If no match, fallback to LLM-generated SQL
4. Execute query and generate natural language response

### 3. Updated StockAIService (`services/stock_ai_service.py`)

**Enhancements:**
- Integrates enhanced query processor
- Provides field meaning APIs
- Maintains backward compatibility

## Database Schema Understanding

### Field Meanings

The system understands these key fields:

| Field | Type | Description | Values |
|-------|------|-------------|---------|
| `TheTrendD` | Trend | Daily trend indicator | 0=sideways, 1=uptrend, 2=downtrend |
| `TheTrendW` | Trend | Weekly trend indicator | 0=sideways, 1=uptrend, 2=downtrend |
| `TheTrendM` | Trend | Monthly trend indicator | 0=sideways, 1=uptrend, 2=downtrend |
| `Price` | Price | Stock price | Numeric value |
| `UpsDowns` | Volume | Trading volume/activity | Numeric value |
| `Nrnum` | Symbol | Stock identifier | Numeric symbol |
| `Date` | Date | Trading date | Date value |

### Table Relationships

- `stock_data`: Contains price, volume, trend data
- `name_index`: Contains stock names (Hebrew and English)
- Joined on `Nrnum` field for complete information

## Supported Question Types

### 1. Current Trend Questions
```
"What is the trend on symbol 230011 today?"
"Current trend for 230011"
"How is 230011 trending?"
```

**Response Example:**
```
"The current trend for Bezeq (symbol 230011) as of 2025-07-27 is uptrend (long position). The stock price is 634.6."
```

### 2. Trend Change Questions
```
"When was the last time symbol 230011 moved from uptrend to downtrend?"
"Last time 230011 changed from long to short"
"When did 230011 move from up to down?"
```

**Response Example:**
```
"Found 10 trend changes. Recent changes: Bezeq changed from uptrend (long position) to downtrend (short position) on 2025-05-26..."
```

### 3. Trend History Questions
```
"Trend history for symbol 230011"
"230011 trend last 7 days"
"How has 230011 been trending?"
```

**Response Example:**
```
"Trend history for Bezeq (symbol 230011): 5 days of uptrend (long position), 2 days of sideways (no clear trend)."
```

## API Endpoints

### Core Query Endpoint
```
POST /query
{
    "question": "What is the trend on symbol 230011 today?",
    "limit": 100
}
```

### Field Meaning Endpoints
```
GET /fields/meanings                    # All field meanings
GET /fields/TheTrendD/meaning          # Specific field meaning
GET /semantic/trend-values             # Trend value meanings
```

### Example Response
```json
{
    "status": "success",
    "question": "What is the trend on symbol 230011 today?",
    "sql_query": "SELECT s.Nrnum, s.Date, s.TheTrendD, s.Price, s.UpsDowns, n.HebName, n.EngName FROM stock_data s LEFT JOIN name_index n ON s.Nrnum = n.Nrnum WHERE s.Nrnum = 230011 ORDER BY s.Date DESC LIMIT 1",
    "results": [...],
    "explanation": "The current trend for Bezeq (symbol 230011) as of 2025-07-27 is uptrend (long position). The stock price is 634.6.",
    "row_count": 1,
    "query_type": "semantic_trend_current"
}
```

## Configuration and Extensibility

### Adding New Field Meanings

To add semantic understanding for a new field:

```python
# In semantic_mapping_service.py
'NewField': FieldDefinition(
    field_name='NewField',
    field_type=FieldType.INDICATOR,
    description='New indicator field',
    possible_values={
        '0': 'low',
        '1': 'medium', 
        '2': 'high'
    },
    table='stock_data'
)
```

### Adding New Question Patterns

To support new question types:

```python
# In semantic_mapping_service.py
'new_question_type': [
    {
        'patterns': [
            r'your regex pattern here',
            r'another pattern'
        ],
        'sql_template': """
            SELECT your SQL template here
            WHERE condition = {parameter}
        """
    }
]
```

## Testing

Run the comprehensive test suite:

```bash
cd backend
python test_semantic_understanding.py
```

This tests:
- ✅ Semantic field definitions
- ✅ Query classification  
- ✅ Symbol extraction
- ✅ Trend value interpretation
- ✅ Natural language response generation
- ✅ Database field meaning API

## Benefits of This Approach

### 1. **Not Hardcoded**
- Field definitions are configurable
- Question patterns are extensible
- SQL templates can be modified
- New question types can be added

### 2. **Semantic Understanding**
- System understands what fields mean
- Converts numeric values to human-readable descriptions
- Provides context-aware responses

### 3. **Hybrid Approach**
- Semantic patterns for known question types (fast, accurate)
- LLM fallback for complex queries (flexible, powerful)
- Best of both worlds

### 4. **Natural Language Responses**
- Converts technical data to human-readable answers
- Includes stock names, trend descriptions, dates
- Contextual explanations

### 5. **Extensible Architecture**
- Easy to add new fields and meanings
- Simple to extend question patterns
- Modular design for maintenance

## Example Usage

### Question: "What is the trend on symbol 230011 today?"

**Processing Steps:**
1. **Classification**: Identified as `trend_current` question
2. **Symbol Extraction**: Extracted "230011" from question
3. **SQL Generation**: Used semantic template with symbol substitution
4. **Query Execution**: Retrieved latest trend data with stock name
5. **Response Generation**: "The current trend for Bezeq (symbol 230011) as of 2025-07-27 is uptrend (long position). The stock price is 634.6."

### Question: "When was the last time symbol 230011 moved from uptrend to downtrend?"

**Processing Steps:**
1. **Classification**: Identified as `trend_change` question
2. **Symbol Extraction**: Extracted "230011" from question
3. **SQL Generation**: Used trend change template (JOIN to find transitions)
4. **Query Execution**: Found trend change records
5. **Response Generation**: "Found 10 trend changes. Recent changes: Bezeq changed from uptrend (long position) to downtrend (short position) on 2025-05-26..."

## Conclusion

This semantic understanding system successfully solves the problem of making the system understand database cell meanings and answer natural language queries correctly. It provides:

- **Accurate understanding** of what database fields mean
- **Natural language processing** of stock-related questions
- **Intelligent responses** that convert technical data to human-readable answers
- **Extensible architecture** that can be easily modified and extended
- **Hybrid approach** combining semantic patterns with LLM capabilities

The system can now correctly answer questions like "What is the trend on symbol 230011 today?" with proper understanding that `TheTrendD` field values of 1 mean "uptrend (long position)" and 2 mean "downtrend (short position)". 