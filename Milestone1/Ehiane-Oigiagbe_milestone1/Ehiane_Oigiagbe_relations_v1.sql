CREATE TABLE Business (
    business_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    city VARCHAR,
    state VARCHAR
);

CREATE TABLE User (
    user_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    review_count INT
);

CREATE TABLE Review (
    review_id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES User(user_id),
    business_id VARCHAR REFERENCES Business(business_id),
    stars INT,
    date DATE
);

CREATE TABLE Checkin (
    business_id VARCHAR REFERENCES Business(business_id),
    day VARCHAR,
    hour VARCHAR,
    checkins INT,
    PRIMARY KEY (business_id, day, hour)
);
