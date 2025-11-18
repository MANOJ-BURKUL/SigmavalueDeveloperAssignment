import React, { useState } from 'react';
import axios from 'axios';
import ChartComponent from './ChartComponent';

const ChatInterface = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = { type: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${backendUrl}/api/analyze/`, {
        query: query
      });

      const botMessage = {
        type: 'bot',
        content: response.data
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: error.response?.data?.error || 'An error occurred while processing your query.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  const sampleQueries = [
    'Give me analysis of Wakad',
    'Compare Ambegaon Budruk and Aundh demand trends',
    'Show price growth for Akurdi over the last 3 years'
  ];

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-lg-10 mx-auto">
          <div className="card shadow-sm">
            <div className="card-header bg-primary text-white">
              <h4 className="mb-0">Real Estate Analysis Chatbot</h4>
              <small>Ask questions about real estate trends in Pune localities</small>
            </div>
            <div className="card-body" style={{ minHeight: '500px', maxHeight: '500px', overflowY: 'auto' }}>
              {messages.length === 0 ? (
                <div className="text-center text-muted mt-5">
                  <h5>Welcome! Try asking about real estate in Pune</h5>
                  <p className="mt-3">Sample queries:</p>
                  {sampleQueries.map((sq, idx) => (
                    <button
                      key={idx}
                      className="btn btn-outline-primary btn-sm m-1"
                      onClick={() => setQuery(sq)}
                    >
                      {sq}
                    </button>
                  ))}
                </div>
              ) : (
                messages.map((msg, idx) => (
                  <div key={idx} className="mb-3">
                    {msg.type === 'user' ? (
                      <div className="text-end">
                        <div className="badge bg-primary text-wrap" style={{ maxWidth: '80%', fontSize: '0.95rem', padding: '10px' }}>
                          {msg.content}
                        </div>
                      </div>
                    ) : msg.type === 'error' ? (
                      <div className="alert alert-danger">{msg.content}</div>
                    ) : (
                      <div>
                        {msg.content.summary && (
                          <div className="alert alert-info">
                            <strong>Summary:</strong> {msg.content.summary}
                          </div>
                        )}
                        
                        {msg.content.chart_data && Object.keys(msg.content.chart_data).length > 0 && (
                          <div className="my-3">
                            <ChartComponent chartData={msg.content.chart_data} />
                          </div>
                        )}
                        
                        {msg.content.table_data && msg.content.table_data.length > 0 && (
                          <div className="table-responsive mt-3">
                            <h6>Detailed Data:</h6>
                            <table className="table table-striped table-sm table-hover">
                              <thead className="table-dark">
                                <tr>
                                  {msg.content.table_data[0].locality && <th>Locality</th>}
                                  <th>Year</th>
                                  <th>Total Sales</th>
                                  <th>Units Sold</th>
                                  <th>Flat Avg Rate</th>
                                  <th>Office Avg Rate</th>
                                  <th>Shop Avg Rate</th>
                                  <th>Total Units</th>
                                  <th>Carpet Area</th>
                                </tr>
                              </thead>
                              <tbody>
                                {msg.content.table_data.map((row, i) => (
                                  <tr key={i}>
                                    {row.locality && <td>{row.locality}</td>}
                                    <td>{row.year}</td>
                                    <td>{row.total_sales}</td>
                                    <td>{row.total_sold}</td>
                                    <td>{row.flat_avg_rate}</td>
                                    <td>{row.office_avg_rate}</td>
                                    <td>{row.shop_avg_rate}</td>
                                    <td>{row.total_units}</td>
                                    <td>{row.carpet_area}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))
              )}
              
              {loading && (
                <div className="text-center">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
              )}
            </div>
            <div className="card-footer">
              <form onSubmit={handleSubmit}>
                <div className="input-group">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Ask about real estate trends (e.g., 'Analyze Wakad')"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={loading}
                  />
                  <button 
                    className="btn btn-primary" 
                    type="submit"
                    disabled={loading || !query.trim()}
                  >
                    {loading ? 'Analyzing...' : 'Send'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
