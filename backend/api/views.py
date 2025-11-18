from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .data_processor import RealEstateDataProcessor
import os
import re

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

processor = RealEstateDataProcessor()

def get_openai_summary(query, data):
    if not OPENAI_AVAILABLE:
        return generate_mock_summary(query, data)
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return generate_mock_summary(query, data)
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are a real estate market analyst. Based on the following data, provide a concise 3-4 sentence analysis.

Query: {query}

Data Summary: {data}

Provide insights on price trends, demand patterns, and market conditions. Be specific with numbers and percentages."""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional real estate market analyst providing concise, data-driven insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return generate_mock_summary(query, data)

def generate_mock_summary(query, data):
    if 'summary' in data and data['summary']:
        summaries = data['summary'] if isinstance(data['summary'], list) else [data['summary']]
        
        if len(summaries) == 1:
            stats = summaries[0]
            locality = stats.get('locality', 'this area')
            years = stats.get('years_covered', 'N/A')
            price_growth = stats.get('price_growth_percentage', 0)
            latest_rate = stats.get('avg_flat_rate_latest', 0)
            total_sold = stats.get('total_units_sold', 0)
            
            summary = f"Real estate analysis for {locality} ({years}): "
            summary += f"The average flat rate is currently ₹{latest_rate:,.0f} per sqft. "
            summary += f"Price growth over the period is {price_growth:.1f}%. "
            summary += f"Total units sold: {total_sold:,}. "
            
            if price_growth > 10:
                summary += "Strong appreciation observed, indicating high demand and robust market conditions."
            elif price_growth > 5:
                summary += "Moderate growth suggests stable market conditions with steady demand."
            else:
                summary += "Market shows stability with gradual price adjustments."
            
            return summary
        else:
            localities = [s.get('locality', 'Unknown') for s in summaries]
            summary = f"Comparative analysis of {', '.join(localities[:-1])} and {localities[-1]}: "
            
            for stats in summaries:
                locality = stats.get('locality', 'Unknown')
                price_growth = stats.get('price_growth_percentage', 0)
                latest_rate = stats.get('avg_flat_rate_latest', 0)
                total_sold = stats.get('total_units_sold', 0)
                
                summary += f"\n\n{locality}: Average flat rate is ₹{latest_rate:,.0f} per sqft with {price_growth:.1f}% price growth. "
                summary += f"Total units sold: {total_sold:,}. "
                
                if price_growth > 10:
                    summary += "Strong market performance."
                elif price_growth > 5:
                    summary += "Moderate growth trajectory."
                else:
                    summary += "Stable market conditions."
            
            return summary
    
    return "Analysis data not available for the requested location."

def extract_localities_from_query(query):
    import re
    
    query_normalized = re.sub(r'[^\w\s]', ' ', query.lower())
    query_normalized = re.sub(r'\s+', ' ', query_normalized).strip()
    query_words = set(query_normalized.split())
    
    all_localities = processor.get_localities()
    found_localities = []
    
    for locality in all_localities:
        locality_lower = locality.lower()
        locality_normalized = re.sub(r'[^\w\s]', ' ', locality_lower)
        locality_normalized = re.sub(r'\s+', ' ', locality_normalized).strip()
        locality_words = set(locality_normalized.split())
        
        if locality_normalized in query_normalized or locality_words.issubset(query_words):
            found_localities.append(locality)
    
    return found_localities

@api_view(['GET'])
def get_localities(request):
    localities = processor.get_localities()
    return Response({'localities': localities})

@api_view(['POST'])
def analyze_query(request):
    query = request.data.get('query', '').strip()
    
    if not query:
        return Response(
            {'error': 'Query is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    localities = extract_localities_from_query(query)
    
    if not localities:
        available = ', '.join(processor.get_localities()[:5])
        return Response({
            'error': f'No matching locality found in query. Available localities include: {available}, etc.',
            'summary': '',
            'chart_data': {},
            'table_data': []
        })
    
    query_lower = query.lower()
    is_comparison = len(localities) > 1 or 'compare' in query_lower or 'vs' in query_lower
    is_demand = 'demand' in query_lower or 'sold' in query_lower or 'sales' in query_lower
    is_price = 'price' in query_lower or 'rate' in query_lower or 'growth' in query_lower
    
    if is_comparison:
        comparison_data = processor.compare_localities(localities)
        
        chart_data = {}
        if is_demand or (not is_price and not is_demand):
            chart_data = {
                'type': 'demand_comparison',
                'data': comparison_data['demand_trends']
            }
        else:
            chart_data = {
                'type': 'price_comparison',
                'data': comparison_data['price_trends']
            }
        
        summary = get_openai_summary(query, {'summary': comparison_data['summary']})
        
        table_data = []
        for locality in localities:
            locality_table = processor.get_table_data(locality)
            for row in locality_table:
                row['locality'] = locality
                table_data.append(row)
        
        return Response({
            'summary': summary,
            'chart_data': chart_data,
            'table_data': table_data,
            'localities': localities
        })
    
    else:
        locality = localities[0]
        
        price_trend = processor.get_price_trend(locality)
        demand_trend = processor.get_demand_trend(locality)
        summary_stats = processor.get_summary_stats(locality)
        table_data = processor.get_table_data(locality)
        
        if is_demand:
            chart_data = {
                'type': 'demand_trend',
                'data': demand_trend
            }
        else:
            chart_data = {
                'type': 'price_trend',
                'data': price_trend
            }
        
        summary = get_openai_summary(query, {'summary': summary_stats})
        
        return Response({
            'summary': summary,
            'chart_data': chart_data,
            'table_data': table_data,
            'localities': [locality]
        })

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Real Estate Analysis API is running'})
