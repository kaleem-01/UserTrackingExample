CREATE TABLE PageView (
  session_id INT,
  page TEXT,
  time_spent INT, 
  start_time DATETIME
);
CREATE TABLE Button (
  session_id INT,
  button INT 
);