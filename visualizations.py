import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import pandas as pd

def create_gauge_chart(score: float) -> go.Figure:
    """Create a gauge chart for health score visualization
    
    Args:
        score: Health score (0-100)
        
    Returns:
        Plotly gauge chart figure
    """
    # Determine color based on score
    if score >= 80:
        color = "#00CC96"  # Green
    elif score >= 60:
        color = "#FFA15A"  # Orange
    elif score >= 40:
        color = "#FFFF99"  # Yellow
    else:
        color = "#FF6692"  # Red
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Health Score"},
        delta = {'reference': 75, 'position': "top"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(255, 105, 146, 0.3)'},
                {'range': [25, 50], 'color': 'rgba(255, 255, 153, 0.3)'},
                {'range': [50, 75], 'color': 'rgba(255, 161, 90, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(0, 204, 150, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def create_commits_timeline(commit_activity: List[Dict]) -> go.Figure:
    """Create a timeline chart for commit activity
    
    Args:
        commit_activity: List of commit activity data by date
        
    Returns:
        Plotly line chart figure
    """
    if not commit_activity:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No commit data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    # Create DataFrame for easier plotting
    df = pd.DataFrame(commit_activity)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create line chart
    fig = px.line(
        df, 
        x='date', 
        y='commits',
        title='Daily Commit Activity (Last 30 Days)',
        labels={'date': 'Date', 'commits': 'Number of Commits'},
        line_shape='spline'
    )
    
    # Update line style
    fig.update_traces(
        line_color='#636EFA',
        line_width=3,
        marker=dict(size=6)
    )
    
    # Add area fill
    fig.add_scatter(
        x=df['date'], 
        y=df['commits'],
        fill='tonexty',
        mode='none',
        fillcolor='rgba(99, 110, 250, 0.2)',
        showlegend=False
    )
    
    # Update layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            title_font=dict(size=14)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            title_font=dict(size=14)
        ),
        plot_bgcolor='white',
        title_font=dict(size=16, color='darkblue')
    )
    
    return fig

def create_score_breakdown_chart(health_scores: Dict) -> go.Figure:
    """Create a radar chart for health score breakdown
    
    Args:
        health_scores: Dictionary containing component scores
        
    Returns:
        Plotly radar chart figure
    """
    categories = ['Activity', 'Popularity', 'Community', 'Maintenance']
    values = [
        health_scores['activity_score'],
        health_scores['popularity_score'],
        health_scores['community_score'],
        health_scores['maintenance_score']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Health Score',
        line_color='rgba(99, 110, 250, 0.8)',
        fillcolor='rgba(99, 110, 250, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 25]
            )),
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text="Score Breakdown", x=0.5, font=dict(size=16, color='darkblue'))
    )
    
    return fig

def create_metrics_comparison_chart(metrics_data: List[Dict]) -> go.Figure:
    """Create a bar chart comparing repository metrics
    
    Args:
        metrics_data: List of metric dictionaries
        
    Returns:
        Plotly bar chart figure
    """
    metrics = [item['metric'] for item in metrics_data]
    values = [item['value'] for item in metrics_data]
    
    # Create color scale based on values
    colors = px.colors.qualitative.Set3[:len(metrics)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=metrics,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Repository Metrics Overview",
        xaxis_title="Metrics",
        yaxis_title="Count",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white',
        title_font=dict(size=16, color='darkblue')
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside'
    )
    
    return fig
