import React, { useState, useEffect } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { Calculator, Calendar, DollarSign, Clock, BookOpen, Trash2, Plus } from 'lucide-react';
import './App.css';

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [accessToken, setAccessToken] = useState(null);
  const [startDate, setStartDate] = useState('2026-07-01');
  const [endDate, setEndDate] = useState('2026-07-31');
  const [titleFilter, setTitleFilter] = useState('');
  const [onlySage, setOnlySage] = useState(true);

  // Course Rates State
  const [courses, setCourses] = useState([]);
  const [newCourseName, setNewCourseName] = useState('');
  const [newHourlyRate, setNewHourlyRate] = useState('');

  // Calculation Results & UI State
  const [salaryData, setSalaryData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch course rates from DB on load
  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/courses/`);
      setCourses(res.data);
    } catch (err) {
      console.error('Failed to fetch courses:', err);
    }
  };

  const handleAddCourse = async (e) => {
    e.preventDefault();
    setError(''); // پاک کردن خطاهای قبلی

    if (!newCourseName.trim() || !newHourlyRate) {
      setError('Please fill in both Course Code and Rate fields.');
      return;
    }

    try {
      console.log('Sending Add Course request...', {
        course_name: newCourseName.trim(),
        hourly_rate: parseFloat(newHourlyRate)
      });

      const res = await axios.post(`${API_BASE_URL}/courses/`, {
        course_name: newCourseName.trim(),
        hourly_rate: parseFloat(newHourlyRate)
      });

      console.log('Course added successfully:', res.data);

      setNewCourseName('');
      setNewHourlyRate('');
      fetchCourses(); // به‌روزرسانی لیست
    } catch (err) {
      console.error('Error adding course:', err);
      setError(err.response?.data?.detail || 'Failed to add course rate.');
    }
  };

  const handleDeleteCourse = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/courses/${id}`);
      fetchCourses();
    } catch (err) {
      setError('Failed to delete course.');
    }
  };

  // Google OAuth Login Trigger
  const login = useGoogleLogin({
    onSuccess: (tokenResponse) => {
      setAccessToken(tokenResponse.access_token);
      setError('');
    },
    onError: () => setError('Google Login Failed!'),
    scope: 'https://www.googleapis.com/auth/calendar.readonly'
  });

  // Calculate Salary Request
  const calculateSalary = async () => {
    if (!accessToken) {
      setError('Please connect your Google account first.');
      return;
    }

    if (courses.length === 0) {
      setError('Please define at least one course rate before calculating.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/sessions/calculate`, {
        google_token: accessToken,
        start_date: startDate,
        end_date: endDate,
        title_filter: titleFilter || null,
        only_sage: onlySage
      });

      setSalaryData(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Error calculating salary.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <Calculator size={36} color="#4F46E5" />
        <h1>Google Calendar Salary Calculator</h1>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <div className="layout-grid">
        {/* Left Column: Course Rates Management */}
        <div className="card">
          <div className="card-title">
            <BookOpen size={20} />
            <h2>Course Rates DB</h2>
          </div>

          <form onSubmit={handleAddCourse} className="add-course-form">
            <input
              type="text"
              placeholder="Course Code (e.g. PY5)"
              value={newCourseName}
              onChange={(e) => setNewCourseName(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Rate ($/hr)"
              value={newHourlyRate}
              onChange={(e) => setNewHourlyRate(e.target.value)}
              required
            />
            <button type="submit" className="btn-secondary">
              <Plus size={16} /> Add
            </button>
          </form>

          <div className="course-list">
            {courses.length === 0 ? (
              <p className="empty-msg">No course rates defined yet.</p>
            ) : (
              courses.map((c) => (
                <div key={c.id} className="course-item">
                  <span><strong>{c.course_name}</strong>: ${c.hourly_rate}/hr</span>
                  <button onClick={() => handleDeleteCourse(c.id)} className="btn-icon">
                    <Trash2 size={16} color="#EF4444" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column: Calendar & Calculation Controls */}
        <div className="card">
          <div className="card-title">
            <Calendar size={20} />
            <h2>Calculate Salary</h2>
          </div>

          {/* Google Login Status */}
          <div className="auth-box">
            {!accessToken ? (
              <button className="btn-google" onClick={() => login()}>
                Connect Google Calendar 🚀
              </button>
            ) : (
              <div className="status-badge">
                Connected to Google Account
              </div>
            )}
          </div>

          <div className="grid-2">
            <div className="input-group">
              <label>Start Date:</label>
              <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
            </div>
            <div className="input-group">
              <label>End Date:</label>
              <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
            </div>
          </div>

          <div className="input-group" style={{ marginTop: '12px' }}>
            <label>Filter by Title (Optional):</label>
            <input
              type="text"
              placeholder="e.g. [Student-name], PY5"
              value={titleFilter}
              onChange={(e) => setTitleFilter(e.target.value)}
            />
          </div>

          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={onlySage}
                onChange={(e) => setOnlySage(e.target.checked)}
              />
              Calculate <strong>Held</strong> only
            </label>
          </div>

          <button
            className="btn-primary"
            onClick={calculateSalary}
            disabled={loading || !accessToken}
          >
            {loading ? 'Calculating...' : 'Calculate Monthly Salary'}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {salaryData && (
        <div className="card results-card">
          <h2>Salary Calculation Results</h2>

          <div className="stats-grid">
            <div className="stat-card">
              <Clock size={24} color="#4F46E5" />
              <h4>Total Hours</h4>
              <p>{salaryData.summary.total_hours} hrs</p>
            </div>
            <div className="stat-card">
              <Calendar size={24} color="#10B981" />
              <h4>Total Sessions</h4>
              <p>{salaryData.summary.total_sessions} classes</p>
            </div>
            <div className="stat-card highlight">
              <DollarSign size={24} color="#D97706" />
              <h4>Total Salary</h4>
              <p>${salaryData.summary.total_salary.toLocaleString()}</p>
            </div>
          </div>

          <div className="sessions-list">
            <h3>Calculated Sessions Detail:</h3>
            {salaryData.sessions.length === 0 ? (
              <p className="empty-msg">No matching Sage events found in this date range.</p>
            ) : (
              <ul>
                {salaryData.sessions.map((s, idx) => (
                  <li key={idx} className="session-item">
                    <div>
                      <strong>{s.event_title}</strong>
                      <span className="sub-text"> Rate: ${s.hourly_rate}/hr</span>
                    </div>
                    <div>
                      <span>{s.duration_hours} hrs</span>
                      <strong className="amount"> (${s.total_earnings})</strong>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;