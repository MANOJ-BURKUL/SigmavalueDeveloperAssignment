import pandas as pd
import os
from pathlib import Path

class RealEstateDataProcessor:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_path = self.base_dir / 'data' / 'real_estate_data.xlsx'
        self.df = None
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_excel(self.data_path)
            self.df.columns = self.df.columns.str.strip()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()
    
    def get_localities(self):
        if self.df is not None and not self.df.empty:
            return sorted(self.df['final location'].unique().tolist())
        return []
    
    def filter_by_locality(self, locality):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        filtered = self.df[self.df['final location'].str.lower() == locality.lower()]
        return filtered.sort_values('year')
    
    def get_price_trend(self, locality):
        filtered = self.filter_by_locality(locality)
        if filtered.empty:
            return []
        
        trend_data = []
        for _, row in filtered.iterrows():
            trend_data.append({
                'year': int(row['year']),
                'avg_flat_rate': float(row['flat - weighted average rate']) if pd.notna(row['flat - weighted average rate']) else 0,
                'avg_office_rate': float(row['office - weighted average rate']) if pd.notna(row['office - weighted average rate']) else 0,
                'avg_shop_rate': float(row['shop - weighted average rate']) if pd.notna(row['shop - weighted average rate']) else 0
            })
        return trend_data
    
    def get_demand_trend(self, locality):
        filtered = self.filter_by_locality(locality)
        if filtered.empty:
            return []
        
        trend_data = []
        for _, row in filtered.iterrows():
            trend_data.append({
                'year': int(row['year']),
                'total_sold': int(row['total sold - igr']) if pd.notna(row['total sold - igr']) else 0,
                'flat_sold': int(row['flat_sold - igr']) if pd.notna(row['flat_sold - igr']) else 0,
                'office_sold': int(row['office_sold - igr']) if pd.notna(row['office_sold - igr']) else 0,
                'shop_sold': int(row['shop_sold - igr']) if pd.notna(row['shop_sold - igr']) else 0
            })
        return trend_data
    
    def get_summary_stats(self, locality):
        filtered = self.filter_by_locality(locality)
        if filtered.empty:
            return None
        
        latest = filtered.iloc[-1]
        earliest = filtered.iloc[0]
        
        avg_flat_rate_latest = float(latest['flat - weighted average rate']) if pd.notna(latest['flat - weighted average rate']) else 0
        avg_flat_rate_earliest = float(earliest['flat - weighted average rate']) if pd.notna(earliest['flat - weighted average rate']) else 0
        
        price_growth = 0
        if avg_flat_rate_earliest > 0:
            price_growth = ((avg_flat_rate_latest - avg_flat_rate_earliest) / avg_flat_rate_earliest) * 100
        
        total_sales_sum = int(filtered['total sold - igr'].sum()) if 'total sold - igr' in filtered.columns else 0
        
        return {
            'locality': locality,
            'years_covered': f"{int(earliest['year'])}-{int(latest['year'])}",
            'latest_year': int(latest['year']),
            'avg_flat_rate_latest': avg_flat_rate_latest,
            'avg_office_rate_latest': float(latest['office - weighted average rate']) if pd.notna(latest['office - weighted average rate']) else 0,
            'avg_shop_rate_latest': float(latest['shop - weighted average rate']) if pd.notna(latest['shop - weighted average rate']) else 0,
            'price_growth_percentage': round(price_growth, 2),
            'total_units_sold': total_sales_sum,
            'total_units_latest': int(latest['total units']) if pd.notna(latest['total units']) else 0
        }
    
    def get_table_data(self, locality):
        filtered = self.filter_by_locality(locality)
        if filtered.empty:
            return []
        
        table_data = []
        for _, row in filtered.iterrows():
            table_data.append({
                'year': int(row['year']),
                'total_sales': f"₹{int(row['total_sales - igr']):,}" if pd.notna(row['total_sales - igr']) else 'N/A',
                'total_sold': int(row['total sold - igr']) if pd.notna(row['total sold - igr']) else 0,
                'flat_avg_rate': f"₹{int(row['flat - weighted average rate']):,}" if pd.notna(row['flat - weighted average rate']) else 'N/A',
                'office_avg_rate': f"₹{int(row['office - weighted average rate']):,}" if pd.notna(row['office - weighted average rate']) else 'N/A',
                'shop_avg_rate': f"₹{int(row['shop - weighted average rate']):,}" if pd.notna(row['shop - weighted average rate']) else 'N/A',
                'total_units': int(row['total units']) if pd.notna(row['total units']) else 0,
                'carpet_area': f"{int(row['total carpet area supplied (sqft)']):,} sqft" if pd.notna(row['total carpet area supplied (sqft)']) else 'N/A'
            })
        return table_data
    
    def compare_localities(self, localities):
        comparison_data = {
            'price_trends': {},
            'demand_trends': {},
            'summary': []
        }
        
        for locality in localities:
            price_trend = self.get_price_trend(locality)
            demand_trend = self.get_demand_trend(locality)
            summary = self.get_summary_stats(locality)
            
            if price_trend:
                comparison_data['price_trends'][locality] = price_trend
            if demand_trend:
                comparison_data['demand_trends'][locality] = demand_trend
            if summary:
                comparison_data['summary'].append(summary)
        
        return comparison_data
