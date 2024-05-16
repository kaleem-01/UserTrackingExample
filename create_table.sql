CREATE TABLE PageView (
  id INT PRIMARY KEY,
  page TEXT,
  time_spent INT, 
  start_time DATETIME
);
CREATE TABLE Button (
  id INT PRIMARY KEY,
  button INT 
);