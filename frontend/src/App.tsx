import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { DocumentTextIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

interface QueryResponse {
  answer: string;
  relevant_docs: string[];
}

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await axios.post('http://localhost:8000/query', {
        text: query,
        num_docs: 3
      });
      setResponse(result.data);
    } catch (error) {
      console.error('Error querying the API:', error);
      alert('Error querying the API. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="py-10">
        <header>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold leading-tight text-gray-900">
              PDF Knowledge Base
            </h1>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div className="px-4 py-8 sm:px-0">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="query" className="block text-sm font-medium text-gray-700">
                    Ask a question
                  </label>
                  <div className="mt-1">
                    <textarea
                      rows={4}
                      name="query"
                      id="query"
                      className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                    />
                  </div>
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  {loading ? (
                    <>
                      <ArrowPathIcon className="animate-spin -ml-1 mr-2 h-5 w-5" />
                      Processing...
                    </>
                  ) : (
                    'Ask Question'
                  )}
                </button>
              </form>

              {response && (
                <div className="mt-8 space-y-6">
                  <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <h3 className="text-lg leading-6 font-medium text-gray-900">
                        Answer
                      </h3>
                      <div className="mt-2 prose prose-sm max-w-none">
                        <ReactMarkdown>{response.answer}</ReactMarkdown>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <h3 className="text-lg leading-6 font-medium text-gray-900">
                        Relevant Documents
                      </h3>
                      <div className="mt-2 space-y-4">
                        {response.relevant_docs.map((doc, index) => (
                          <div
                            key={index}
                            className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400"
                          >
                            <div className="flex-shrink-0">
                              <DocumentTextIcon className="h-6 w-6 text-gray-400" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm text-gray-500">{doc}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App; 