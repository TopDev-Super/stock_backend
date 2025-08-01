import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import re

logger = logging.getLogger(__name__)

class FieldType(Enum):
    """Types of database fields for semantic understanding"""
    TREND = "trend"
    PRICE = "price"
    VOLUME = "volume"
    SYMBOL = "symbol"
    DATE = "date"
    INDICATOR = "indicator"
    GRADE = "grade"
    NAME = "name"

@dataclass
class FieldDefinition:
    """Definition of a database field with its semantic meaning"""
    field_name: str
    field_type: FieldType
    description: str
    possible_values: Optional[Dict[str, str]] = None
    unit: Optional[str] = None
    table: Optional[str] = None
    
    def get_value_description(self, value: Any) -> str:
        """Get human-readable description of a field value"""
        if self.possible_values and str(value) in self.possible_values:
            return self.possible_values[str(value)]
        return str(value)

class SemanticMappingService:
    """Service for understanding the semantic meaning of database fields"""
    
    def __init__(self):
        self.field_definitions = self._initialize_field_definitions()
        self.query_patterns = self._initialize_query_patterns()
    
    def _initialize_field_definitions(self) -> Dict[str, FieldDefinition]:
        """Initialize field definitions with semantic meanings"""
        return {
            # Trend fields
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
            ),
            'TheTrendW': FieldDefinition(
                field_name='TheTrendW',
                field_type=FieldType.TREND,
                description='Weekly trend indicator',
                possible_values={
                    '0': 'sideways (no clear trend)',
                    '1': 'uptrend (long position)',
                    '2': 'downtrend (short position)'
                },
                table='stock_data'
            ),
            'TheTrendM': FieldDefinition(
                field_name='TheTrendM',
                field_type=FieldType.TREND,
                description='Monthly trend indicator',
                possible_values={
                    '0': 'sideways (no clear trend)',
                    '1': 'uptrend (long position)',
                    '2': 'downtrend (short position)'
                },
                table='stock_data'
            ),
            
            # Price and volume fields
            'Price': FieldDefinition(
                field_name='Price',
                field_type=FieldType.PRICE,
                description='Stock price',
                unit='currency',
                table='stock_data'
            ),
            'UpsDowns': FieldDefinition(
                field_name='UpsDowns',
                field_type=FieldType.VOLUME,
                description='Trading volume/activity',
                unit='shares',
                table='stock_data'
            ),
            'UpsDownsD': FieldDefinition(
                field_name='UpsDownsD',
                field_type=FieldType.VOLUME,
                description='Daily trading volume',
                unit='shares',
                table='stock_data'
            ),
            
            # Symbol and name fields
            'Nrnum': FieldDefinition(
                field_name='Nrnum',
                field_type=FieldType.SYMBOL,
                description='Stock identifier/symbol',
                table='stock_data'
            ),
            'HebName': FieldDefinition(
                field_name='HebName',
                field_type=FieldType.NAME,
                description='Stock name in Hebrew',
                table='name_index'
            ),
            'EngName': FieldDefinition(
                field_name='EngName',
                field_type=FieldType.NAME,
                description='Stock name in English',
                table='name_index'
            ),
            
            # Date field
            'Date': FieldDefinition(
                field_name='Date',
                field_type=FieldType.DATE,
                description='Trading date',
                table='stock_data'
            ),
            
            # Indicator fields
            'MainSug': FieldDefinition(
                field_name='MainSug',
                field_type=FieldType.INDICATOR,
                description='Main suggestion/indicator',
                table='stock_data'
            ),
            'SubSug': FieldDefinition(
                field_name='SubSug',
                field_type=FieldType.INDICATOR,
                description='Sub suggestion/indicator',
                table='stock_data'
            ),
            'Index': FieldDefinition(
                field_name='Index',
                field_type=FieldType.INDICATOR,
                description='Market index value',
                table='stock_data'
            ),
            
            # Grade fields
            'FinalGradeD': FieldDefinition(
                field_name='FinalGradeD',
                field_type=FieldType.GRADE,
                description='Final daily grade/rating',
                table='stock_data'
            ),
            'FinalGradeW': FieldDefinition(
                field_name='FinalGradeW',
                field_type=FieldType.GRADE,
                description='Final weekly grade/rating',
                table='stock_data'
            ),
            'FinalGradeM': FieldDefinition(
                field_name='FinalGradeM',
                field_type=FieldType.GRADE,
                description='Final monthly grade/rating',
                table='stock_data'
            ),
        }
    
    def _initialize_query_patterns(self) -> Dict[str, List[Dict]]:
        """Initialize patterns for recognizing different types of queries"""
        return {
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
            ],
            'trend_change': [
                {
                    'patterns': [
                        r'last.*time.*(\d+).*moved.*uptrend.*downtrend',
                        r'last.*time.*(\d+).*changed.*long.*short',
                        r'when.*(\d+).*moved.*up.*down',
                        r'trend.*change.*(\d+)'
                    ],
                    'sql_template': """
                        SELECT s1.Nrnum, s1.Date, s1.TheTrendD as from_trend, 
                               s2.TheTrendD as to_trend, s1.Price, s1.UpsDowns,
                               n.HebName, n.EngName
                        FROM stock_data s1
                        JOIN stock_data s2 ON s1.Nrnum = s2.Nrnum 
                            AND s1.Date < s2.Date
                        LEFT JOIN name_index n ON s1.Nrnum = n.Nrnum
                        WHERE s1.Nrnum = {symbol}
                            AND s1.TheTrendD = 1 AND s2.TheTrendD = 2
                        ORDER BY s1.Date DESC
                        LIMIT 10
                    """
                }
            ],
            'trend_history': [
                {
                    'patterns': [
                        r'trend.*history.*(\d+)',
                        r'(\d+).*trend.*last.*(\d+).*days',
                        r'how.*(\d+).*trending.*last'
                    ],
                    'sql_template': """
                        SELECT s.Nrnum, s.Date, s.TheTrendD, s.Price, s.UpsDowns,
                               n.HebName, n.EngName
                        FROM stock_data s
                        LEFT JOIN name_index n ON s.Nrnum = n.Nrnum
                        WHERE s.Nrnum = {symbol}
                        ORDER BY s.Date DESC
                        LIMIT {days}
                    """
                }
            ]
        }
    
    def get_field_definition(self, field_name: str) -> Optional[FieldDefinition]:
        """Get the semantic definition of a field"""
        return self.field_definitions.get(field_name)
    
    def get_field_by_type(self, field_type: FieldType) -> List[FieldDefinition]:
        """Get all fields of a specific type"""
        return [fd for fd in self.field_definitions.values() if fd.field_type == field_type]
    
    def extract_symbol_from_question(self, question: str) -> Optional[str]:
        """Extract stock symbol from a natural language question"""
        # Look for patterns like "symbol 230011", "stock 230011", "230011"
        patterns = [
            r'symbol\s+(\d+)',
            r'stock\s+(\d+)',
            r'(\d{6,})',  # 6+ digit numbers
        ]
        
        for pattern in patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def classify_question_type(self, question: str) -> Tuple[str, Dict]:
        """Classify the type of question being asked"""
        question_lower = question.lower()
        
        for query_type, patterns_list in self.query_patterns.items():
            for pattern_info in patterns_list:
                for pattern in pattern_info['patterns']:
                    match = re.search(pattern, question_lower)
                    if match:
                        return query_type, {
                            'pattern': pattern,
                            'sql_template': pattern_info['sql_template'],
                            'matches': match.groups()
                        }
        
        return 'general', {}
    
    def generate_contextual_sql(self, question: str, question_type: str, context: Dict) -> str:
        """Generate SQL query based on question type and context"""
        if question_type == 'trend_current':
            symbol = self.extract_symbol_from_question(question)
            if symbol:
                return context['sql_template'].format(symbol=symbol)
        
        elif question_type == 'trend_change':
            symbol = self.extract_symbol_from_question(question)
            if symbol:
                return context['sql_template'].format(symbol=symbol)
        
        elif question_type == 'trend_history':
            symbol = self.extract_symbol_from_question(question)
            days = 7  # Default to 7 days
            # Extract number of days if mentioned
            days_match = re.search(r'(\d+).*days?', question.lower())
            if days_match:
                days = int(days_match.group(1))
            
            if symbol:
                return context['sql_template'].format(symbol=symbol, days=days)
        
        # Fallback to general query
        return None
    
    def interpret_trend_value(self, value: Any) -> str:
        """Convert numeric trend value to human-readable description"""
        trend_def = self.field_definitions.get('TheTrendD')
        if trend_def and trend_def.possible_values:
            return trend_def.possible_values.get(str(value), f"Unknown trend value: {value}")
        return str(value)
    
    def generate_natural_response(self, question: str, results: List[Dict], question_type: str) -> str:
        """Generate natural language response based on results and question type"""
        if not results:
            return "No data found for your query."
        
        if question_type == 'trend_current':
            result = results[0]
            symbol = result.get('Nrnum', 'Unknown')
            trend_value = result.get('TheTrendD')
            trend_desc = self.interpret_trend_value(trend_value)
            stock_name = result.get('EngName') or result.get('HebName') or f"Stock {symbol}"
            date = result.get('Date')
            price = result.get('Price')
            
            return f"The current trend for {stock_name} (symbol {symbol}) as of {date} is {trend_desc}. The stock price is {price}."
        
        elif question_type == 'trend_change':
            if len(results) == 0:
                return "No trend changes found for the specified criteria."
            
            changes = []
            for result in results[:5]:  # Limit to 5 most recent changes
                symbol = result.get('Nrnum', 'Unknown')
                stock_name = result.get('EngName') or result.get('HebName') or f"Stock {symbol}"
                date = result.get('Date')
                from_trend = self.interpret_trend_value(result.get('from_trend'))
                to_trend = self.interpret_trend_value(result.get('to_trend'))
                
                changes.append(f"{stock_name} changed from {from_trend} to {to_trend} on {date}")
            
            return f"Found {len(results)} trend changes. Recent changes: {'; '.join(changes)}."
        
        elif question_type == 'trend_history':
            symbol = results[0].get('Nrnum', 'Unknown')
            stock_name = results[0].get('EngName') or results[0].get('HebName') or f"Stock {symbol}"
            
            trend_summary = {}
            for result in results:
                trend = self.interpret_trend_value(result.get('TheTrendD'))
                trend_summary[trend] = trend_summary.get(trend, 0) + 1
            
            summary_parts = [f"{count} days of {trend}" for trend, count in trend_summary.items()]
            
            return f"Trend history for {stock_name} (symbol {symbol}): {', '.join(summary_parts)}."
        
        # Default response
        return f"Found {len(results)} results for your query."

# Global instance
semantic_mapping_service = SemanticMappingService() 