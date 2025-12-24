import React, { useState } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './chat.module.css';

function ChatPage() {
  const { siteConfig } = useDocusaurusContext();
  const { retrievalApiUrl } = siteConfig.customFields as { retrievalApiUrl: string };

  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = {
      sender: 'user',
      text: query,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${retrievalApiUrl}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_message: query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const botMessage = {
        sender: 'bot',
        data: data, // { answer: "...", citations: [...] }
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      setError(error.message);
      const errorMessage = {
        sender: 'bot',
        error: `Failed to get a response: ${error.message}`,
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  return (
    <Layout title="Chat" description="Chat with the RAG system">
      <div className={styles.chatContainer}>
        <div className={styles.messageContainer}>
          {messages.map((message, index) => (
            <div key={index} className={`${styles.message} ${styles[message.sender]}`}>
              {message.sender === 'bot' && message.data ? (
                <div>
                  <p>{message.data.answer}</p>
                  {message.data.citations && message.data.citations.length > 0 && (
                    <div className={styles.citations}>
                      <h4>Sources:</h4>
                      <ul>
                        {message.data.citations.map((citation, i) => (
                          <li key={i}>
                            {citation.source_path} 
                            {citation.chapter && ` - ${citation.chapter}`}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : message.error ? (
                <div className={styles.error}>{message.error}</div>
              ) : (
                message.text
              )}
            </div>
          ))}
          {loading && (
            <div className={`${styles.message} ${styles.bot}`}>
              <div className={styles.loading}>Thinking...</div>
            </div>
          )}
        </div>
        <form onSubmit={handleSubmit} className={styles.inputForm}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className={styles.input}
            placeholder="Ask a question..."
            disabled={loading}
          />
          <button type="submit" className={styles.button} disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </Layout>
  );
}

export default ChatPage;
